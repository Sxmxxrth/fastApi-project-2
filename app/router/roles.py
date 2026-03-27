from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.roles import Role
from app.schema.roles import RoleCreate, RoleUpdate, RoleOut

router = APIRouter(prefix="/roles", tags=["Roles"])

# List all roles
@router.get("/", response_model=list[RoleOut])
def list_roles(db: Session = Depends(get_db)):
    try:
        roles = db.query(Role).filter(Role.is_deleted == False).all()
        return roles
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching roles: {ex}")

# Get role by ID
@router.get("/{role_id}", response_model=RoleOut)
def get_role(role_id: int, db: Session = Depends(get_db)):
    try:
        role = db.query(Role).filter(Role.role_id == role_id, Role.is_deleted == False).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching role: {ex}")

# Create role
@router.post("/", response_model=RoleOut)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    try:
        new_role = Role(**role.dict())
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating role: {ex}")

# Update role
@router.put("/{role_id}", response_model=RoleOut)
def update_role(role_id: int, role_update: RoleUpdate, db: Session = Depends(get_db)):
    try:
        role = db.query(Role).filter(Role.role_id == role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        for key, value in role_update.dict(exclude_unset=True).items():
            setattr(role, key, value)
        db.commit()
        db.refresh(role)
        return role
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating role: {ex}")

# Soft delete role
@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    try:
        role = db.query(Role).filter(Role.role_id == role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        role.is_deleted = True
        db.commit()
        return {"message": "Role soft deleted"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting role: {ex}")

# Restore role
@router.patch("/{role_id}/restore", response_model=RoleOut)
def restore_role(role_id: int, db: Session = Depends(get_db)):
    try:
        role = db.query(Role).filter(Role.role_id == role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        role.is_deleted = False
        db.commit()
        db.refresh(role)
        return role
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error restoring role: {ex}")
