from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class OrderCreate(BaseModel):
    user_id: int
    order_date: Optional[date] = None
    status: Optional[str] = "PENDING"
    total_items: Optional[int] = 0
    is_deleted: Optional[bool] = False

class OrderUpdate(BaseModel):
    status: Optional[str]
    total_items: Optional[int]

class OrderOut(OrderCreate):
    order_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        validate_by_name = True
