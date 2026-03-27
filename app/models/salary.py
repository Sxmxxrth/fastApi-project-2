from sqlalchemy import Column, Integer, String, DECIMAL, Date, Enum, TIMESTAMP, ForeignKey, Boolean, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Salary(Base):
    __tablename__ = "salary"

    salary_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    month = Column(String(20), nullable=False)
    base_salary = Column(DECIMAL(10,2), nullable=False)
    bonus = Column(DECIMAL(10,2), default=0)
    deductions = Column(DECIMAL(10,2), default=0)
    net_salary = Column(DECIMAL(10,2), nullable=False)
    status = Column(Enum("PAID", "PENDING", name="salary_status"), default="PENDING")
    paid_date = Column(Date, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    employee = relationship("Employee", back_populates="salaries")
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) 
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    #  Relationship back to User 
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id")) 
    user = relationship("User", back_populates="salaries")