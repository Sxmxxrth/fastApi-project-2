from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from enum import Enum

class SalaryStatus(str, Enum):
    PAID = "PAID"
    PENDING = "PENDING"

class SalaryBase(BaseModel):
    employee_id: int
    month: str
    base_salary: float
    bonus: Optional[float] = 0
    deductions: Optional[float] = 0
    net_salary: float
    status: SalaryStatus = SalaryStatus.PENDING
    paid_date: Optional[date] = None

class SalaryCreate(SalaryBase):
    pass

class SalaryUpdate(BaseModel):
    month: Optional[str] = None
    base_salary: Optional[float] = None
    bonus: Optional[float] = None
    deductions: Optional[float] = None
    net_salary: Optional[float] = None
    status: Optional[SalaryStatus] = None
    paid_date: Optional[date] = None
    is_deleted: Optional[bool] = None

class SalaryOut(SalaryBase):
    salary_id: int
    is_deleted: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
