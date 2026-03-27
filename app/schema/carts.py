from pydantic import BaseModel
from datetime import datetime


class CartBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class CartCreate(CartBase):
    pass

class CartResponse(CartBase):
    cart_id: int

    class Config:
        from_attributes = True
        validate_by_name = True


