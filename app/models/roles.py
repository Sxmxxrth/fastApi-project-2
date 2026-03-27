from sqlalchemy import String, Enum, TIMESTAMP, Boolean, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import enum

# Enum for role types
class RoleType(str, enum.Enum):
    USER = "USER"
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    MODERATOR = "MODERATOR"

# Role model
class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role_name: Mapped[str] = mapped_column(String(50), nullable=False)
    role_type: Mapped[RoleType] = mapped_column(Enum(RoleType), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # relationships
    permissions = relationship("RolePermission", back_populates="role")
    users = relationship("User", back_populates="role")
