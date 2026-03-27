from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class RoleType(str, Enum):
    USER = "USER"
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    MODERATOR = "MODERATOR"

class RoleBase(BaseModel):
    role_name: str
    role_type: RoleType

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    role_name: Optional[str] = None
    role_type: Optional[RoleType] = None
    is_deleted: Optional[bool] = None

class RoleOut(RoleBase):
    role_id: int
    is_deleted: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class RoleOut(RoleBase):
    role_id: int
    is_deleted: bool
    created_at: Optional[datetime]   # keep datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        populate_by_name = True
        validate_by_name = True