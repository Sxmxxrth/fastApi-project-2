from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Permission, RolePermission, Role

router = APIRouter(prefix="/security", tags=["Security & Access Control"])

@router.get("/permissions")
def list_permissions(db: Session = Depends(get_db)):
    try:
        return db.query(Permission).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching permissions: {ex}")

@router.post("/permissions")
def create_permission(permission: dict, db: Session = Depends(get_db)):
    try:
        db_perm = Permission(**permission)
        db.add(db_perm)
        db.commit()
        db.refresh(db_perm)
        return db_perm
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating permission: {ex}")

@router.post("/role-permissions")
def assign_permission(payload: dict, db: Session = Depends(get_db)):
    try:
        rp = RolePermission(**payload)
        db.add(rp)
        db.commit()
        return {"message": "Permission assigned to role"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error assigning permission: {ex}")

@router.delete("/role-permissions/{role_id}/{permission_id}")
def remove_permission(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    try:
        rp = db.query(RolePermission).filter_by(role_id=role_id, permission_id=permission_id).first()
        if not rp:
            raise HTTPException(status_code=404, detail="RolePermission not found")
        db.delete(rp)
        db.commit()
        return {"message": "Permission removed from role"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error removing permission: {ex}")
