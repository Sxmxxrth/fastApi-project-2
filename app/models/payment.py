# from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, DECIMAL
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
# from app.core.database import Base


# class Payment(Base):
#     __tablename__ = "payments"

#     payment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
#     payment_method = Column(String(50), nullable=False)
#     payment_status = Column(String(50), nullable=False)
#     created_at = Column(TIMESTAMP, server_default=func.now())
#     payment_amount = Column(DECIMAL(10,2), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
#     amount = Column(DECIMAL(10,2), nullable=False)
    

#     order = relationship("Order", back_populates="payments")
#     user = relationship("User", back_populates="payments")
from sqlalchemy import String, TIMESTAMP, ForeignKey, Numeric, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())

    payment_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    # If you don't need both, remove `amount`
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="payments")
    user: Mapped["user"] = relationship("User", back_populates="payments")
