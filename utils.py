import asyncio
from pymongo.errors import (ConnectionFailure,
                            OperationFailure,
                            PyMongoError)

async def run_with_retry(fn, max_retries=5):
    delay = 0.2

    for attempt in range(max_retries):
        try:
            return await fn()
        except PyMongoError as e:
            msg = str(e)

            if ("TransientTransactionError" in msg or
                "UnknownTransactionCommitResult" in msg):

                await asyncio.sleep(delay)
                delay *= 2
                continue

            raise e
    raise Exception("Transaction failed after retries")
