from pydantic import BaseModel, Field

class PaymentRequest(BaseModel):
    wallet_id: str = Field(...)
    amount: float = Field(..., gt=0)

class PaymentResponse(BaseModel):
    status: str
    new_balance: float
    transaction_id: str
