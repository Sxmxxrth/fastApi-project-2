from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base): 
    __tablename__ = "products" 
    
    product_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(100), nullable=False) 
    price = Column(Float, nullable=False) 
    stock = Column(Integer, nullable=False) 
    category_id = Column(Integer, ForeignKey("categories.category_id")) 
    image_url = Column(String(255)) 
    brand = Column(String(100)) 
    size = Column(String(10)) 
    color = Column(String(50)) 
    material = Column(String(100)) 
    is_deleted = Column(Boolean, default=False)
    description  = Column(String(1000), nullable=True)
    
# app/models/product.py


# here we have a relationship between Product and Category
    category = relationship("Category", back_populates="products")

    # Relationships
    category = relationship("Category", back_populates="products")
    carts = relationship("Cart", back_populates="product", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product")
    favorites = relationship("Favorite", back_populates="product", cascade="all, delete-orphan")
    views = relationship("ProductView", back_populates="product")

class ProductView(Base):
    __tablename__ = "product_views"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    user = relationship("User", back_populates="product_views")

    user = relationship("User", back_populates="product_views")
    product = relationship("Product", back_populates="views")