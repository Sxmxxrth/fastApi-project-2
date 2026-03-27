from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.Attendance import Attendance
from app.schema.attendance import AttendanceCreate, AttendanceUpdate, AttendanceOut
from datetime import datetime, time, date

router = APIRouter(prefix="/attendance", tags=["Attendance"])

# GET /attendance → List attendance records (filters: date, employee, status)
@router.get("/", response_model=list[AttendanceOut])
def list_attendance(
    filter_date: date | None = Query(None),
    employee_id: int | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Attendance).filter(Attendance.is_deleted == False)
        if filter_date:
            query = query.filter(Attendance.date == filter_date)  # ✅ match DB column
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        if status:
            query = query.filter(Attendance.status == status)
        return query.all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching attendance records: {ex}")

# POST /attendance → Add attendance record

def to_time(dt: datetime | None) -> time | None:
    return dt.time() if dt else None

@router.post("/", response_model=AttendanceOut)
def add_attendance(record: AttendanceCreate, db: Session = Depends(get_db)):
    try:
        new_record = Attendance(
            employee_id=record.employee_id,
            date=record.date,
            status=record.status,
            leave_type=record.leave_type,
            check_in_time=to_time(record.check_in_time),   # ✅ convert
            check_out_time=to_time(record.check_out_time), # ✅ convert
            total_hours=record.total_hours,
            is_deleted=False,
            created_at=datetime.now()
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding attendance record: {ex}")

# PUT /attendance/{id} → Update attendance

@router.put("/{attendance_id}", response_model=AttendanceOut)
def update_attendance(attendance_id: int, update_data: AttendanceUpdate, db: Session = Depends(get_db)):
    try:
        record = db.query(Attendance).filter(
            Attendance.attendance_id == attendance_id,
            Attendance.is_deleted == False
        ).first()

        if not record:
            raise HTTPException(status_code=404, detail="Attendance record not found")

        update_dict = update_data.model_dump(exclude_unset=True)

        if "check_in_time" in update_dict:
            update_dict["check_in_time"] = to_time(update_dict["check_in_time"])
        if "check_out_time" in update_dict:
            update_dict["check_out_time"] = to_time(update_dict["check_out_time"])

        for key, value in update_dict.items():
            setattr(record, key, value)

        db.commit()
        db.refresh(record)
        return record

    except HTTPException:
        raise
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating attendance record: {ex}")

# DELETE /attendance/{id} → Soft delete attendance
@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    try:
        record = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()  # ✅ fixed
        if not record:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        record.is_deleted = True
        db.commit()
        return {"message": "Attendance record soft deleted successfully"}
    except HTTPException:
        raise
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting attendance record: {ex}")

# GET /attendance/dashboard → Dashboard view of attendance
@router.get("/dashboard")
def dashboard_attendance(db: Session = Depends(get_db)):
    try:
        return db.query(Attendance).filter(Attendance.is_deleted == False).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard attendance: {ex}")
