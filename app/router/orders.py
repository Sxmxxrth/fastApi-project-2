from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Order
from app.schema.orders import OrderCreate, OrderUpdate, OrderOut
from app.models.user import User
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:

        user = db.query(User).filter(User.user_id == order.user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_order = Order(
            user_id=order.user_id,
            order_date=order.order_date,
            status=order.status,
            total_items=order.total_items,
            is_deleted=order.is_deleted,
            user_name=user.username   
        )


        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    except HTTPException as http_exc:
        raise http_exc
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating order: {ex}")


@router.get("/", response_model=list[OrderOut])
def get_orders(db: Session = Depends(get_db)):
    try:
        return db.query(Order).filter(Order.is_deleted == 0).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {ex}")

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.order_id == order_id, Order.is_deleted == 0).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching order: {ex}")

@router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, update_data: OrderUpdate, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.order_id == order_id, Order.is_deleted == 0).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(order, key, value)
        db.commit()
        db.refresh(order)
        return order
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating order: {ex}")

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.is_deleted = 1
        db.commit()
        return {"message": "Order deleted successfully"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting order: {ex}")

# dashboard orders
@router.get("/dashboard/orders", response_model=list[OrderOut])
def dashboard_orders(db: Session = Depends(get_db)):
    try:
        return db.query(Order).filter(Order.is_deleted == 0).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard orders: {ex}")







# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from app.models import Order
# from app.schema.orders import OrderCreate, OrderUpdate, OrderOut


# router = APIRouter(prefix="/orders", tags=["Orders"])

# @router.post("/", response_model=OrderOut)
# def create_order(order: OrderCreate, db: Session = Depends(get_db)):
#     new_order = Order(**order.dict())
#     db.add(new_order)
#     db.commit()
#     db.refresh(new_order)
#     return new_order

# @router.get("/", response_model=list[OrderOut])
# def get_orders(db: Session = Depends(get_db)):
#     return db.query(Order).filter(Order.is_deleted == 0).all()

# @router.get("/{order_id}", response_model=OrderOut)
# def get_order(order_id: int, db: Session = Depends(get_db)):
#     order = db.query(Order).filter(Order.order_id == order_id, Order.is_deleted == 0).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order

# @router.put("/{order_id}", response_model=OrderOut)
# def update_order(order_id: int, update_data: OrderUpdate, db: Session = Depends(get_db)):
#     order = db.query(Order).filter(Order.order_id == order_id, Order.is_deleted == 0).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     for key, value in update_data.dict(exclude_unset=True).items():
#         setattr(order, key, value)
#     db.commit()
#     db.refresh(order)
#     return order

# @router.delete("/{order_id}")
# def delete_order(order_id: int, db: Session = Depends(get_db)):
#     order = db.query(Order).filter(Order.order_id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     order.is_deleted = 1
#     db.commit()
#     return {"message": "Order deleted successfully"}

# # dashboard orders
# @router.get("/dashboard/orders", response_model=list[OrderOut])
# def dashboard_orders(db: Session = Depends(get_db)):    
#     return db.query(Order).filter(Order.is_deleted == 0).all()
