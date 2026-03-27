from sqlalchemy import Integer, String, ForeignKey, Date, TIMESTAMP, Numeric, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.core.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(100)) 
    status: Mapped[str] = mapped_column(String(20), default="pending")  
    amount_paid: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.order_id"), nullable=True)

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    tax_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    due_date: Mapped[datetime] = mapped_column(Date)

    # relationships
    items = relationship("InvoiceItem", back_populates="invoice")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(Integer, ForeignKey("invoices.invoice_id")) 
    description: Mapped[str] = mapped_column(String(255))
    qty: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2))
    tax: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    total: Mapped[float] = mapped_column(Numeric(10, 2))

    # relationships
    invoice = relationship("Invoice", back_populates="items")
    # items = relationship("OrderItem", back_populates="invoice_item")
