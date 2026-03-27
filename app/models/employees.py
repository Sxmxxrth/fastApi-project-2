from sqlalchemy import  Integer, String, Date, Numeric, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
import enum
from decimal import Decimal
from typing import Optional




class EmployeeStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Employee(Base):
    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    manager_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("employees.employee_id"), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100))
    joining_date: Mapped[Optional[Date]] = mapped_column(Date)
    salary: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    status: Mapped[EmployeeStatus] = mapped_column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    user = relationship("User", backref="employee")
    manager = relationship("Employee", remote_side=[employee_id], backref="subordinates")
    salaries = relationship("Salary", back_populates="employee")

