from pydantic import BaseModel, Field
from typing import Optional, List


class CategorySchema(BaseModel):
    category_id: int
    category_name: str

    class Config:
        from_attributes = True
        populate_by_name = True

class CategoryBase(BaseModel):
    category_name: str
    parent_category_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    category_name: Optional[str]
    parent_category_id: Optional[int]

class CategoryOut(CategoryBase):
    category_id: int
    is_deleted: bool
    children: List["CategoryOut"] = Field(default_factory=list)

    class Config:
        from_attributes = True
        validate_by_name = True
        
CategoryOut.model_rebuild()

