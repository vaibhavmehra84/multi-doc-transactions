import logging
from fastapi import FastAPI, HTTPException, Request
from bson import ObjectId
from datetime import datetime
from pymongo import UpdateOne, InsertOne, UpdateMany

from db import client, wallets, ledger
from models import PaymentRequest, PaymentResponse
from utils import run_with_retry

app = FastAPI()
logger = logging.getLogger(__name__)


@app.post("/payment", response_model=PaymentResponse)
async def process_payment(req: PaymentRequest, request: Request):

    # --------- Precompute everything OUTSIDE the transaction ----------
    # (Critical for high throughput)
    amt = req.amount
    src = req.wallet_id
    dst = req.to_wallet_id
    now = datetime.utcnow()

    debit_id = str(ObjectId())
    credit_id = str(ObjectId())

    debit_entry = {
        "_id": debit_id,
        "wallet_id": src,
        "amount": -amt,
        "type": "DEBIT",
        "timestamp": now,
    }

    credit_entry = {
        "_id": credit_id,
        "wallet_id": dst,
        "amount": amt,
        "type": "CREDIT",
        "timestamp": now,
    }

    # Pre-build debit pipeline (heavy logic computed once)
    debit_pipeline = [
        {
            "$set": {
                "balance": {
                    "$cond": {
                        "if": {"$gte": ["$balance", amt]},
                        "then": {"$subtract": ["$balance", amt]},
                        "else": "$balance"
                    }
                }
            }
        }
        
    ]

    # Pre-build bulk ops (created once)
    bulk_ops = [
        UpdateOne({"_id": src}, debit_pipeline),
        UpdateOne({"_id": dst}, {"$inc": {"balance": amt}}),
        #InsertOne(debit_entry),
        #InsertOne(credit_entry),
    ]
    # Pre-build update many with a tweaked data model
    bulk_ops2=[
        UpdateMany({"$or":[{"_id":dst},{"_id":src}]}, debit_pipeline)
    ]

    # ----------------- TRANSACTION FUNCTION -----------------
    async def txn():
        async with await client.start_session() as session:
            async with session.start_transaction():

                # One network round trip
                result = await wallets.bulk_write(
                    bulk_ops2,
                    session=session,
                    ordered=False  # allows server-side reordering/parallelism
                )

                #result = await wallets.update_many(
                #    {"$or":[{"_id":dst},{"_id":src}]}, debit_pipeline,
                #    session=session
                #)

                # --------------- Ultra-fast validation ---------------

                # Debit must match exactly one document
                if result.matched_count < 1:
                    raise HTTPException(400, "Source wallet not found")

                # Debit must modify 1 doc → balance must be >= amount
                if result.modified_count < 1:
                    raise HTTPException(400, "Insufficient balance")

                # Credit must match target wallet
                #if result.matched_count < 2:
                #    raise HTTPException(404, "Target wallet not found")

                # Ledger entries must both be inserted
                #if result.inserted_count != 1:
                #    raise HTTPException(500, "Ledger insert failed")

                return PaymentResponse(
                    status="success",
                    debit_entry_id=debit_id,
                    credit_entry_id=credit_id,
                )

    # Run with retry logic (abort-retry for transient errors)
    return await run_with_retry(txn)
