from pydantic import BaseModel

class TransactionData(BaseModel):
    id: str
    date: str
    amount_paid: float
    currency: str
    supplier_id: str
    discount: float
    amount_due: float
    transaction_type: str
    transaction_status: str
    payment_type: str