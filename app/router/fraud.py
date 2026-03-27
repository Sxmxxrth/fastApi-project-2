from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.fraud import FraudCheck, BlockedUser
from app.schema.fraud import FraudCheckCreate, FraudCheckResponse,BlockedUserCreate, BlockedUserResponse

router = APIRouter(prefix="/fraud", tags=["Fraud & Risk"])
@router.post("/checks", response_model=FraudCheckResponse)
def create_fraud_check(fraud: FraudCheckCreate, db: Session = Depends(get_db)):
    try:
        new_check = FraudCheck(**fraud.dict())
        db.add(new_check)
        db.commit()
        db.refresh(new_check)
        return new_check
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating fraud check: {ex}")


@router.get("/checks/{fraud_id}", response_model=FraudCheckResponse)
def get_fraud_check(fraud_id: int, db: Session = Depends(get_db)):
    try:
        check = db.query(FraudCheck).filter(FraudCheck.fraud_id == fraud_id).first()
        if not check:
            raise HTTPException(status_code=404, detail="Fraud check not found")
        return check
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error retrieving fraud check: {ex}")

@router.patch("/checks/{fraud_id}", response_model=FraudCheckResponse)
def update_fraud_status(fraud_id: int, status: str, db: Session = Depends(get_db)):
    try:
        check = db.query(FraudCheck).filter(FraudCheck.fraud_id == fraud_id).first()
        if not check:
            raise HTTPException(status_code=404, detail="Fraud check not found")
        check.status = status
        db.commit()
        db.refresh(check)
        return check
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating fraud status: {ex}")

@router.post("/blocked", response_model=BlockedUserResponse)
def block_user(user: BlockedUserCreate, db: Session = Depends(get_db)):
    try:
        blocked = BlockedUser(**user.dict())
        db.add(blocked)
        db.commit()
        db.refresh(blocked)
        return blocked
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error blocking user: {ex}")
    
@router.get("/blocked/{user_id}", response_model=BlockedUserResponse)
def get_blocked_user(user_id: int, db: Session = Depends(get_db)):
    try:
        blocked = db.query(BlockedUser).filter(BlockedUser.user_id == user_id).first()
        if not blocked:
            raise HTTPException(status_code=404, detail="User not blocked")
        return blocked
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error retrieving blocked user: {ex}")

@router.delete("/blocked/{user_id}")
def unblock_user(user_id: int, db: Session = Depends(get_db)):
    try:
        blocked = db.query(BlockedUser).filter(BlockedUser.user_id == user_id).first()
        if not blocked:
            raise HTTPException(status_code=404, detail="User not blocked")
        db.delete(blocked)
        db.commit()
        return {"detail": "User unblocked"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error unblocking user: {ex}")