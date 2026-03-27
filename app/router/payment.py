from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.payment import Payment
from app.schema.payment import PaymentCreate, PaymentUpdate, PaymentOut
from decimal import Decimal

router = APIRouter(prefix="/payments", tags=["Payments"])

# List all payments
@router.get("/", response_model=list[PaymentOut])
def list_payments(db: Session = Depends(get_db)):
    try:
        return db.query(Payment).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching payments: {ex}")

# Get payment by ID
@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching payment: {ex}")

# Create payment

@router.post("/", response_model=PaymentOut)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    # Guard clause
    amount: Decimal = payment.payment_amount
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Payment amount must be greater than zero")

    try:
        # Use model_dump instead of dict
        new_payment = Payment(**payment.model_dump())
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return new_payment
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating payment: {ex}")

# Update payment
@router.put("/{payment_id}", response_model=PaymentOut)
def update_payment(payment_id: int, payment_update: PaymentUpdate, db: Session = Depends(get_db)):
    try:
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        for key, value in payment_update.model_dump(exclude_unset=True).items():
            setattr(payment, key, value)
        db.commit()
        db.refresh(payment)
        return payment
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating payment: {ex}")

# Delete payment (hard delete)
@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        db.delete(payment)
        db.commit()
        return {"message": "Payment deleted successfully"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting payment: {ex}")

# dashboard route for payments summary
@router.get("/dashboard/summary")
def payment_summary(db: Session = Depends(get_db)):
    try:    
        return db.query(Payment).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching payment summary: {ex}")    
