from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.audit_trail import AuditTrail
from app.schema.audit_trail import AuditTrailCreate, AuditTrailOut

router = APIRouter(prefix="/audit", tags=["Audit Trail"])

@router.post("/", response_model=AuditTrailOut)
def create_audit(audit: AuditTrailCreate, db: Session = Depends(get_db)):
    try:
        new_audit = AuditTrail(**audit.dict())
        db.add(new_audit)
        db.commit()
        db.refresh(new_audit)
        return new_audit
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating audit trail: {ex}")

@router.get("/", response_model=list[AuditTrailOut])
def list_audits(db: Session = Depends(get_db)):
    try:
        return db.query(AuditTrail).order_by(AuditTrail.created_at.desc()).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching audit trails: {ex}")

@router.get("/{audit_id}", response_model=AuditTrailOut)
def get_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = db.query(AuditTrail).filter(AuditTrail.audit_id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit trail not found")
    return audit

@router.delete("/{audit_id}")
def delete_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = db.query(AuditTrail).filter(AuditTrail.audit_id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit trail not found")
    try:
        db.delete(audit)
        db.commit()
        return {"message": "Audit trail deleted successfully"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting audit trail: {ex}")
