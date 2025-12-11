from pydantic import BaseModel, Field
from typing import Optional

class PaymentRequest(BaseModel):
    wallet_id: str
    to_wallet_id: str
    amount: float = Field(..., gt=0)

class PaymentResponse(BaseModel):
    status: str
    debit_entry_id: str
    credit_entry_id: str
    #idempotency_key: str
