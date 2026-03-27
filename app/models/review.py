from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, TIMESTAMP, text, Boolean, DateTime, CheckConstraint, Enum, Text
from app.core.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Review(Base): 
    __tablename__ = "reviews" 
    review_id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False) 
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False) 
    rating = Column(Integer, nullable=False) 
    description = Column(Text) 
    fit_feedback = Column(Enum("small", "true", "large", name="fit_feedback_enum"), nullable=True) 
    created_at = Column(TIMESTAMP, server_default=func.now()) 
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 
    is_deleted = Column(Boolean, default=False) 
    # comment = Column(Text, nullable=True)

    __table_args__ = ( 
        CheckConstraint("rating BETWEEN 1 AND 5", name="valid_rating"), 
        )
    
    # Relationships 
    product = relationship("Product", back_populates="reviews") 
    user = relationship("User", back_populates="reviews")