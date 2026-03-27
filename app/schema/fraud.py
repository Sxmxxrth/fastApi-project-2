from pydantic import BaseModel
from typing import Optional

class FraudCheckBase(BaseModel):
    order_id: int
    reason: str
    status: Optional[str] = "FLAGGED"

class FraudCheckCreate(FraudCheckBase):
    pass

class FraudCheckResponse(FraudCheckBase):
    fraud_id: int
    created_at: str

    class Config:
        from_attributes = True
        validate_by_name = True

class BlockedUserBase(BaseModel):
    user_id: int
    reason: str

class BlockedUserCreate(BlockedUserBase):
    pass

class BlockedUserResponse(BlockedUserBase):
    block_id: int
    blocked_at: str

    class Config:
        from_attributes = True
        validate_by_name = True