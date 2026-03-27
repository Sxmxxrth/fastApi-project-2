from sqlalchemy import String, ForeignKey, TIMESTAMP, text, Boolean, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime
from .carts import Cart
from .favorites import Favorite
from .task import Task
from .review import Review
from .post import Post
from .order import Order
from .comment import Comment
from .roles import Role
from .salary import Salary

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    carts: Mapped[list["Cart"]] = relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    salaries: Mapped[list["Salary"]] = relationship("Salary", back_populates="user")
    views: Mapped[list["ProductView"]] = relationship("ProductView", back_populates="user")
    audit_trails: Mapped[list["AuditTrail"]] = relationship("AuditTrail", back_populates="user")
    product_views: Mapped[list["ProductView"]] = relationship("ProductView", back_populates="user")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="user")