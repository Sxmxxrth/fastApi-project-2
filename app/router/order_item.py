from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.order_item import OrderItem
from app.schema.order_item import OrderItemCreate, OrderItemUpdate, OrderItemOut

router = APIRouter(prefix="/order-items", tags=["Order Items"])

# List all order items
@router.get("/", response_model=list[OrderItemOut])
def list_order_items(db: Session = Depends(get_db)):
    try:
        return db.query(OrderItem).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching order items: {ex}")

# Get order item by ID
@router.get("/{order_item_id}", response_model=OrderItemOut)
def get_order_item(order_item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(OrderItem).filter(OrderItem.order_item_id == order_item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Order item not found")
        return item
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching order item: {ex}")

# Create order item
@router.post("/", response_model=OrderItemOut)
def create_order_item(order_item: OrderItemCreate, db: Session = Depends(get_db)):
    try:
        new_item = OrderItem(**order_item.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating order item: {ex}")

# Update order item
@router.put("/{order_item_id}", response_model=OrderItemOut)
def update_order_item(order_item_id: int, order_item_update: OrderItemUpdate, db: Session = Depends(get_db)):
    try:
        item = db.query(OrderItem).filter(OrderItem.order_item_id == order_item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Order item not found")
        for key, value in order_item_update.dict(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating order item: {ex}")

# Delete order item
@router.delete("/{order_item_id}")
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(OrderItem).filter(OrderItem.order_item_id == order_item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Order item not found")
        db.delete(item)
        db.commit()
        return {"message": "Order item deleted successfully"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting order item: {ex}")
