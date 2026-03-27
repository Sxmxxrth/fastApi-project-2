from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    parent_category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=True)
    is_deleted = Column(Integer, default=0, nullable=False)

    children = relationship("Category", backref="parent", remote_side=[category_id])
    products = relationship("Product", back_populates="category")
