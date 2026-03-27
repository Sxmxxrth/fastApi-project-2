from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base

class ShippingProvider(Base):
    __tablename__ = "shipping_providers"

    provider_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    contact_email: Mapped[str] = mapped_column(String(100), nullable=True)
    contact_info : Mapped[str] = mapped_column(String(255), nullable=True)
    shipments = relationship("Shipment", back_populates="provider")



class Shipment(Base):
    __tablename__ = "shipments"

    shipment_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.order_id"))
    provider_id: Mapped[int] = mapped_column(Integer, ForeignKey("shipping_providers.provider_id"))
    tracking_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("PENDING", "SHIPPED", "DELIVERED", "CANCELLED", name="shipment_status"),
        default="PENDING"
    )
    shipped_date: Mapped[Date] = mapped_column(Date, nullable=True)
    delivered_date: Mapped[Date] = mapped_column(Date, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # ✅ added

    order = relationship("Order", back_populates="shipments")
    provider = relationship("ShippingProvider", back_populates="shipments")
    order_items = relationship("OrderItem", back_populates="shipment")

# class Shipment(Base):
#     __tablename__ = "shipments"

#     shipment_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.order_id"))
#     provider_id: Mapped[int] = mapped_column(Integer, ForeignKey("shipping_providers.provider_id"))
#     tracking_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
#     status: Mapped[str] = mapped_column(
#         Enum("PENDING", "SHIPPED", "DELIVERED", "CANCELLED", name="shipment_status"),
#         default="PENDING"
#     )
#     shipped_date: Mapped[Date] = mapped_column(Date, nullable=True)
#     delivered_date: Mapped[Date] = mapped_column(Date, nullable=True)

    order = relationship("Order", back_populates="shipments")
    provider = relationship("ShippingProvider", back_populates="shipments")
    order_items = relationship("OrderItem", back_populates="shipment")  # ✅ now works
