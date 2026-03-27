from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class InvoiceItemCreate(BaseModel):
    description: str
    qty: int
    unit_price: float
    tax: float = 0.0

class InvoiceItemOut(BaseModel):
    id: int
    invoice_id: int
    description: str
    qty: int
    unit_price: float
    tax: float
    total: float

    class Config:
        from_attributes = True

class InvoiceCreate(BaseModel):
    user_name: str
    status: str = "pending"
    items: List[InvoiceItemCreate]

class InvoiceOut(BaseModel):
    invoice_id: int
    user_name: Optional[str]
    status: str
    total_amount: float
    amount_paid: float
    created_at: datetime
    items: List[InvoiceItemOut]

    class Config:
        from_attributes = True

class InvoiceUpdate(BaseModel):
    status: str
    amount_paid: float
