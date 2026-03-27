from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, TIMESTAMP, func, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime
class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.order_id"), index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.product_id"), index=True)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    shipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("shipments.shipment_id"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    # # relationships
    # order = relationship("Order", back_populates="order_items")
    # shipment = relationship("Shipment", back_populates="order_items")
    # product = relationship("Product", back_populates="order_items")


    order = relationship("Order", back_populates="order_items")
    shipment = relationship("Shipment", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


