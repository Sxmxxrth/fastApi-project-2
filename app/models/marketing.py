from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date, DECIMAL, Text, TIMESTAMP, Boolean
from datetime import date, datetime
from app.core.database import Base

class Coupon(Base):
    __tablename__ = "coupons"

    coupon_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    discount: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=True)
    valid_from: Mapped[date] = mapped_column(Date, nullable=True)
    valid_to: Mapped[date] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Campaign(Base):
    __tablename__ = "campaigns"

    campaign_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")  # ENUM in DB


class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"

    subscriber_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    subscribed_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
