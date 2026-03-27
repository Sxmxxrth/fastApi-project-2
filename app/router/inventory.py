from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.inventory import Warehouse, InventoryMovement
from app.schema.inventory import (
    WarehouseCreate, WarehouseUpdate, WarehouseOut,
    InventoryMovementCreate, InventoryMovementOut,
    InventorySummary
)

router = APIRouter(prefix="/inventory", tags=["Inventory & Warehouse"])

# ---------------- Warehouses ---------------- #

@router.get("/warehouses", response_model=list[WarehouseOut])
def list_warehouses(db: Session = Depends(get_db)):
    try:
        return db.query(Warehouse).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching warehouses: {ex}")

@router.post("/warehouses", response_model=WarehouseOut)
def create_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    try:
        db_wh = Warehouse(**warehouse.dict())
        db.add(db_wh)
        db.commit()
        db.refresh(db_wh)
        return db_wh
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating warehouse: {ex}")

@router.put("/warehouses/{id}", response_model=WarehouseOut)
def update_warehouse(id: int, warehouse: WarehouseUpdate, db: Session = Depends(get_db)):
    try:
        db_wh = db.query(Warehouse).filter(Warehouse.warehouse_id == id).first()
        if not db_wh:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        update_data = warehouse.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_wh, key, value)
        db.commit()
        db.refresh(db_wh)
        return db_wh
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating warehouse: {ex}")

@router.delete("/warehouses/{id}")
def delete_warehouse(id: int, db: Session = Depends(get_db)):
    try:
        db_wh = db.query(Warehouse).filter(Warehouse.warehouse_id == id).first()
        if not db_wh:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        db.delete(db_wh)
        db.commit()
        return {"message": "Warehouse deleted"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting warehouse: {ex}")


# ---------------- Inventory Movements ---------------- #

@router.get("/movements", response_model=list[InventoryMovementOut])
def list_movements(db: Session = Depends(get_db)):
    try:
        return db.query(InventoryMovement).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching movements: {ex}")

@router.post("/movements", response_model=InventoryMovementOut)
def record_movement(movement: InventoryMovementCreate, db: Session = Depends(get_db)):
    try:
        db_mv = InventoryMovement(**movement.dict())
        db.add(db_mv)
        db.commit()
        db.refresh(db_mv)
        return db_mv
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error recording movement: {ex}")


# ---------------- Inventory Summary ---------------- #

@router.get("/summary", response_model=list[InventorySummary])
def inventory_summary(db: Session = Depends(get_db)):
    try:
        results = (
            db.query(
                Warehouse.warehouse_id.label("warehouse_id"),
                Warehouse.name.label("warehouse_name"),
                db.func.sum(InventoryMovement.quantity).label("total_stock")
            )
            .join(InventoryMovement, Warehouse.warehouse_id == InventoryMovement.warehouse_id)
            .group_by(Warehouse.warehouse_id, Warehouse.name)
            .all()
        )
        return results
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching summary: {ex}")
