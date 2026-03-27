from pydantic import BaseModel
from datetime import datetime
from typing import  Any


class ReportCacheOut(BaseModel):
    report_id: int
    report_type: str
    data: Any
    generated_at: datetime

    class Config:
        from_attributes = True   # replaces orm_mode in Pydantic v2


class ProductViewOut(BaseModel):
    product_id: int
    views: int
