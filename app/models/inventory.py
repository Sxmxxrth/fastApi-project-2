from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouse_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=True)

    movements = relationship("InventoryMovement", back_populates="warehouse")


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    warehouse_id: Mapped[int] = mapped_column(Integer, ForeignKey("warehouses.id"))
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    movement_type: Mapped[str] = mapped_column(String(10), nullable=False)  # "IN" or "OUT"
    timestamp: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    # Relationship back to warehouse
    warehouse_id: Mapped[int] = mapped_column(Integer, ForeignKey("warehouses.warehouse_id"))
    warehouse = relationship("Warehouse", back_populates="movements")
