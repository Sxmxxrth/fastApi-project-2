from sqlalchemy import Column, Integer, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
class FraudCheck(Base):
    __tablename__ = "fraud_checks"
    fraud_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum("FLAGGED", "CLEARED", name="fraud_status"),
    default="FLAGGED")
    created_at = Column(TIMESTAMP, server_default=func.now())
class BlockedUser(Base):
    __tablename__ = "blocked_users"
    block_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    reason = Column(Text, nullable=False)
    blocked_at = Column(TIMESTAMP, server_default=func.now())