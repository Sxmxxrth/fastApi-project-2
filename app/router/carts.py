from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.carts import Cart
from app.schema.carts import CartCreate, CartResponse

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=list[CartResponse])
def get_all_carts(db: Session = Depends(get_db)):
    return db.query(Cart).all()

@router.post("/", response_model=CartResponse)
def create_cart(cart: CartCreate, db: Session = Depends(get_db)):
    new_cart = Cart(**cart.dict())
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

@router.delete("/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart entry not found")
    db.delete(cart)
    db.commit()
    return {"message": f"Cart entry {cart_id} deleted successfully"}
