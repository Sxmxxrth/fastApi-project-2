from typing import Optional, Dict 
from datetime import datetime, timedelta, timezone 
from jose import jwt, JWTError 
from passlib.context import CryptContext 
import os 
import bcrypt
# from dotenv import load_dotenv

# load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def get_password_hash(password: str) -> str: 
    try: 
        return pwd_context.hash(password) 
    except Exception as ex: 
        raise Exception(f"Password hashing failed: {str(ex)}")

def verify_password(plain_password: str, hashed_password: str) -> bool: 
    try: 
        return pwd_context.verify(plain_password, hashed_password) 
    except Exception as ex: 
        raise Exception(f"Password verification failed: {str(ex)}")

def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str: 
    try: 
        to_encode = data.copy() 
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) 
        to_encode.update({"exp": int(expire.timestamp())}) 
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 
    except Exception as ex: 
        raise Exception(f"Token creation failed: {str(ex)}")

def verify_token(token: str) -> dict[str, str]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as ex:
        raise Exception(f"Invalid credentials : {ex}")
    except Exception as ex:
        raise Exception(f"Token verification failed: {str(ex)}")