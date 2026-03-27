from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    title: str 
    content: str 
    author_id: int


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_deleted: Optional[bool] = None

class PostOut(PostBase):
    post_id: int
    author_id: int
    is_deleted: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class PostResponse(BaseModel): 
    post_id: int 
    title: str 
    content: str 
    author_id: int 
    is_deleted: bool 
    created_at: datetime 
    updated_at: datetime 
class Config: 
    from_attributes = True