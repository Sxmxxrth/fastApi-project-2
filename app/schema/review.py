from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    rating: conint(ge=1, le=5)
    description: Optional[str] = None
    fit_feedback: Optional[str] = None

class ReviewCreate(ReviewBase):
    product_id: int

class ReviewUpdate(ReviewBase):
    pass

class ReviewOut(ReviewBase):
    review_id: int
    user_id: int
    product_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True
