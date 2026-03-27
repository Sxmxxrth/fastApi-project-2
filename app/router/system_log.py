from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.system_log import SystemLog
from app.schema.system_log import SystemLogCreate, SystemLogRead
from app.core.database import get_db

router = APIRouter(prefix="/system_logs", tags=["System Logs"])

@router.post("/", response_model=SystemLogRead)
def create_log(log: SystemLogCreate, db: Session = Depends(get_db)):
    try:
        db_log = SystemLog(log_type=log.log_type, message=log.message)
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error creating log: {ex}")


@router.get("/{log_id}", response_model=SystemLogRead)
def get_log(log_id: int, db: Session = Depends(get_db)):
    try:
        db_log = db.query(SystemLog).filter(SystemLog.log_id == log_id).first()
        if not db_log:
            raise HTTPException(status_code=404, detail="Log not found")
        return db_log
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error retrieving log: {ex}")


@router.get("/", response_model=list[SystemLogRead])
def list_logs(db: Session = Depends(get_db)):
    try:
        logs = db.query(SystemLog).order_by(SystemLog.created_at.desc()).all()
        return logs
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error listing logs: {ex}")
