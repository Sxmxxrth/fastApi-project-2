from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------------- Warehouse ---------------- #

class WarehouseBase(BaseModel):
    name: str
    location: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(WarehouseBase):
    name: Optional[str] = None
    location: Optional[str] = None


class WarehouseOut(WarehouseBase):
    id: int

    class Config:
        from_attributes = True


# ---------------- Inventory Movement ---------------- #

class InventoryMovementBase(BaseModel):
    warehouse_id: int
    product_name: str
    quantity: int
    movement_type: str  # "IN" or "OUT"

class InventoryMovementCreate(InventoryMovementBase):
    pass

class InventoryMovementOut(InventoryMovementBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# ---------------- Summary ---------------- #

class InventorySummary(BaseModel):
    warehouse_id: int
    warehouse_name: str
    total_stock: int
