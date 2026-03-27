from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, Literal

# Coupons
class CouponBase(BaseModel):
    code: str
    discount: Optional[float] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True

class CouponCreate(CouponBase):
    pass

class CouponUpdate(BaseModel):
    discount: Optional[float] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    is_active: Optional[bool] = None

class CouponOut(CouponBase):
    coupon_id: int


# Campaigns
class CampaignBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[Literal["ACTIVE", "INACTIVE"]] = "ACTIVE"

    class Config:
        from_attributes = True

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[Literal["ACTIVE", "INACTIVE"]] = None

class CampaignOut(CampaignBase):
    campaign_id: int


# Newsletter Subscribers
class SubscriberBase(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True

class SubscriberCreate(SubscriberBase):
    pass

class SubscriberOut(SubscriberBase):
    subscriber_id: int
    subscribed_at: datetime
