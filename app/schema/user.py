from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


# User Schema
class UserCreate(BaseModel):
    full_name: str 
    username: str 
    phone: Optional[str] = None 
    email: EmailStr 
    password: str 
    role_id: int
    
    @field_validator("password", mode="before")
    def validate_password_length(cls, v: str) -> str:
        encoded = v.encode("utf-8")
        if len(encoded) > 72:
            truncated = encoded[:72].decode("utf-8", errors="replace")
            return truncated
        return v
    @field_validator("username")
    def username_not_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Username cannot be empty")
        return v




class UserLogin(BaseModel):
    email: EmailStr
    password: str    


class UserBase(BaseModel):
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True
        validate_by_name = True
        populate_by_name = True


class UserRegister(BaseModel):
    full_name: str
    username: str
    phone: Optional[str] = None
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
        validate_by_name = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str