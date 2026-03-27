from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional

from app.models.user import User
from app.schema import UserLogin, UserCreate, UserResponse, Token
from app.core.database import get_db
from app.utils.security import hash_password, verify_password, create_access_token, decode_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Login endpoint
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user or not verify_password(user.password, db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        token = create_access_token({"sub": db_user.email})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(ex)}")

# Register endpoint
@router.post("/register", response_model=UserResponse, operation_id="register_user")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = User(
            full_name=user.full_name,
            username=user.username,
            phone=user.phone,
            email=user.email,
            password_hash=hash_password(user.password),
            role_id=user.role_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(ex)}")
