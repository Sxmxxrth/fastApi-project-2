366
from typing import Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal

# Define a proper type alias
PositiveAmount = Annotated[Decimal, Field(gt=0, decimal_places=2)]

class PaymentBase(BaseModel):
    order_id: int
    payment_method: str
    payment_status: str
    payment_amount: PositiveAmount  # ✅ now valid for both Pydantic and Pylance

class PaymentCreate(PaymentBase):
    """Schema for creating a payment (all fields required)."""
    pass

class PaymentUpdate(BaseModel):
    """Schema for updating a payment (partial updates allowed)."""
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    payment_amount: Optional[PositiveAmount] = None

class PaymentOut(PaymentBase):
    """Schema for returning payment data."""
    payment_id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
        validate_by_name = True
