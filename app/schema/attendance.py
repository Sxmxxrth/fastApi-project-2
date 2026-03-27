# 
from pydantic import BaseModel
from datetime import date, datetime, time
from typing import Optional, Literal


class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    total_hours: Optional[float] = None
    leave_type: Optional[Literal["NONE", "SICK", "CASUAL", "PAID"]] = "NONE"
    status: Optional[Literal["PRESENT", "ABSENT", "LEAVE"]] = "PRESENT"

    class Config:
        from_attributes = True


class AttendanceCreate(AttendanceBase):
    status: Optional[str] = "PRESENT"


class AttendanceUpdate(BaseModel):
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    total_hours: Optional[float] = None
    leave_type: Optional[Literal["NONE", "SICK", "CASUAL", "PAID"]] = None
    status: Optional[Literal["PRESENT", "ABSENT", "LEAVE"]] = None


class AttendanceOut(AttendanceBase):
    attendance_id: int
    created_at: datetime
    is_deleted: bool


    class OutConfig:
        from_attributes = True
        validate_by_name = True
        populate_by_name = True