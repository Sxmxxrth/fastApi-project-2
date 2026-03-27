from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.salary import Salary
from app.schema.salary import SalaryCreate, SalaryUpdate, SalaryOut

router = APIRouter(prefix="/salary", tags=["Salary"])

@router.get("/", response_model=list[SalaryOut])
def list_salaries(db: Session = Depends(get_db)):
    try:
        return db.query(Salary).filter(Salary.is_deleted == False).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching salaries: {ex}")

@router.get("/{salary_id}", response_model=SalaryOut)
def get_salary(salary_id: int, db: Session = Depends(get_db)):
    try:
        salary = db.query(Salary).filter(Salary.salary_id == salary_id, Salary.is_deleted == False).first()
        if not salary:
            raise HTTPException(status_code=404, detail="Salary not found")
        return salary
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching salary: {ex}")

@router.post("/", response_model=SalaryOut)
def create_salary(salary: SalaryCreate, db: Session = Depends(get_db)):
    try:
        new_salary = Salary(**salary.dict())
        db.add(new_salary)
        db.commit()
        db.refresh(new_salary)
        return new_salary
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating salary: {ex}")

@router.put("/{salary_id}", response_model=SalaryOut)
def update_salary(salary_id: int, salary_update: SalaryUpdate, db: Session = Depends(get_db)):
    try:
        salary = db.query(Salary).filter(Salary.salary_id == salary_id).first()
        if not salary:
            raise HTTPException(status_code=404, detail="Salary not found")
        for key, value in salary_update.dict(exclude_unset=True).items():
            setattr(salary, key, value)
        db.commit()
        db.refresh(salary)
        return salary
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating salary: {ex}")

@router.delete("/{salary_id}")
def delete_salary(salary_id: int, db: Session = Depends(get_db)):
    try:
        salary = db.query(Salary).filter(Salary.salary_id == salary_id).first()
        if not salary:
            raise HTTPException(status_code=404, detail="Salary not found")
        salary.is_deleted = True
        db.commit()
        return {"message": "Salary soft deleted"}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting salary: {ex}")

@router.patch("/{salary_id}/restore", response_model=SalaryOut)
def restore_salary(salary_id: int, db: Session = Depends(get_db)):
    try:
        salary = db.query(Salary).filter(Salary.salary_id == salary_id).first()
        if not salary:
            raise HTTPException(status_code=404, detail="Salary not found")
        salary.is_deleted = False
        db.commit()
        db.refresh(salary)
        return salary
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error restoring salary: {ex}")
