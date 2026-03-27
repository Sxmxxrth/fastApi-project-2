from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ProductSchema(BaseModel): 
    id: int = Field(..., alias="product_id") 
    name: str 
    price: float 
    stock: int 
    category_id: int | None = None 
    image_url: str | None = None 
    brand: str | None = None 
    size: str | None = None 
    color: str | None = None 
    material: str | None = None 
    is_deleted: bool 
    descriptionn: Optional[str] = None
    
    class Config: 
        from_attributes = True
        populate_by_name = True

class ProductBase(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int
    category_id: Optional[int] = None
    image_url: Optional[str] = None

class ProductCreate(BaseModel):
    name: str 
    description: Optional[str] = None 
    price: float 
    stock: int 
    category_id: Optional[int] = None
    image_url: Optional[str] = None 
    brand: Optional[str] = None 
    size: Optional[str] = None 
    color: Optional[str] = None 
    material: Optional[str] = None
    description : str = Field(alias="description")

    class config:
        from_attributes = True
        populate_by_name = True

    @field_validator("stock") 
    def validate_stock(cls, v): 
        if v < 0: 
            raise ValueError("Stock cannot be negative") 
        return v


class ProductUpdate(ProductBase):
    name: str 
    descriptionn: Optional[str] = None 
    price: float 
    stock: int 
    category_id: Optional[int] = None
    image_url: Optional[str] = None 
    brand: Optional[str] = None 
    size: Optional[str] = None 
    color: Optional[str] = None 
    material: Optional[str] = None



class ProductOut(ProductBase):
    id: int = Field(..., alias="product_id") 
    name: str 
    price: float 
    stock: int 
    category_id: int | None = None 
    image_url: str | None = None 
    brand: str | None = None 
    size: str | None = None 
    color: str | None = None 
    material: str | None = None 
    is_deleted: bool

    class Config:
        from_attributes = True
        populate_by_name = True


class ProductResponse(BaseModel):
    pass

    class Config:
        from_attributes = True
        populate_by_name = True