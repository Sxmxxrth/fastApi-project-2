from pydantic import BaseModel
from typing import Optional
from datetime import datetime


#Shipping Provider

class ShippingProviderBase(BaseModel):
    name: str
    contact_info: Optional[str] = None

class ShippingProviderCreate(ShippingProviderBase):
    pass

class ShippingProviderUpdate(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None

class ShippingProviderOut(ShippingProviderBase):
    provider_id: int
    class Config:
        from_attributes = True


#Shipment 

class ShipmentBase(BaseModel):
    order_id: int
    provider_id: int
    tracking_number: Optional[str] = None

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdateStatus(BaseModel):
    status: str

class ShipmentOut(ShipmentBase):
    shipment_id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True


class ShipmentTracking(BaseModel):
    shipment_id: int
    tracking_number: Optional[str]
    status: str
