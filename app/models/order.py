from sqlalchemy import Integer, String, ForeignKey, Date, TIMESTAMP, func, Boolean, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.core.database import Base

class Order(Base): 
    __tablename__ = "orders" 

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id")) 
    order_date: Mapped[datetime] = mapped_column(Date) 
    status: Mapped[str] = mapped_column(String(50)) 
    total_items: Mapped[int] = mapped_column(Integer) 
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now()) 
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    user_name = Column(String, nullable=False) 

    # relationships
    user = relationship("User")
    payments = relationship("Payment", back_populates="order")
    order_items = relationship("OrderItem", back_populates="order")
    shipments = relationship("Shipment", back_populates="order")
    items = relationship("OrderItem", back_populates="order")
