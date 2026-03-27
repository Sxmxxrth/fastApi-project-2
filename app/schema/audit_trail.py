from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditTrailBase(BaseModel):
    user_id: int
    action: str
    table_name: str
    record_id: Optional[int] = None
    message: Optional[str] = None

class AuditTrailCreate(AuditTrailBase):
    pass

class AuditTrailOut(AuditTrailBase):
    audit_id: int
    created_at: datetime

    class Config:
        from_attributes = True
