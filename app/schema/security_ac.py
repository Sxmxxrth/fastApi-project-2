from pydantic import BaseModel
from datetime import datetime

class PermissionBase(BaseModel):
    name: str
    description: str | None = None

class PermissionCreate(PermissionBase):
    pass

class PermissionRead(PermissionBase):
    id: int
    class Config:
        from_attributes = True

class RolePermissionAssign(BaseModel):
    role_id: int
    permission_id: int

class AuditTrailRead(BaseModel):
    id: int
    user_id: int
    table_name: str
    action: str
    timestamp: datetime
    details: str | None = None
    class Config:
        from_attributes = True
        
