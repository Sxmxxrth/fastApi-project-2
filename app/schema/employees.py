from pydantic import BaseModel
from datetime import date
from typing import Optional



class EmployeeBase(BaseModel):
    user_id: int
    manager_id: Optional[int] = None
    department: Optional[str] = None
    joining_date: Optional[date] = None
    salary: Optional[float] = None
    status: Optional[str] = "ACTIVE"


# improve karna hai 
class EmployeeCreate(EmployeeBase):
    user_id: int
    manager_id: Optional[int] = None
    department: Optional[str] = None
    joining_date: Optional[date] = None
    salary: Optional[float] = None
    status: Optional[str] = "ACTIVE"

class EmployeeUpdate(BaseModel):
    manager_id: Optional[int]
    department: Optional[str]
    salary: Optional[float]
    status: Optional[str]

class EmployeeOut(EmployeeBase):
    employee_id: int
    is_deleted: bool

    class Config:
        from_attributes = True
        validate_by_name = True


