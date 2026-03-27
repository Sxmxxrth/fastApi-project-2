from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

class OrderItemOut(OrderItemBase):
    order_item_id: int

    class Config:
        from_attributes = True
        validate_by_name = True