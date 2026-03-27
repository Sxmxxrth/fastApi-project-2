from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FavoriteBase(BaseModel):
    user_id: int
    product_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteUpdate(BaseModel):
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    is_deleted: Optional[bool] = None

class FavoriteOut(FavoriteBase):
    favorite_id: int
    is_deleted: bool
    created_at: Optional[datetime]

class FavoriteResponse(BaseModel):
    favorite_id: int
    user_id: int
    product_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        validate_by_name = True