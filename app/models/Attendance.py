from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Boolean, Date, DateTime, DECIMAL, Enum, Time
from datetime import datetime, timezone
from typing import Optional
from app.core.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(Enum("PRESENT", "ABSENT", "LEAVE"), nullable=True)
    leave_type: Mapped[Optional[str]] = mapped_column(Enum("NONE", "SICK", "CASUAL", "PAID"), nullable=True)
    check_in_time: Mapped[Optional[Time]] = mapped_column(DateTime, nullable=True)
    check_out_time: Mapped[Optional[Time]] = mapped_column(DateTime, nullable=True)
    total_hours: Mapped[Optional[float]] = mapped_column(DECIMAL(5, 2), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    