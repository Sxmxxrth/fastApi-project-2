from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Employee
from app.schema import EmployeeCreate, EmployeeUpdate, EmployeeOut
from sqlalchemy import func
from typing import Any

router = APIRouter(prefix="/employees", tags=["Employees"])

# GET /employees → List employees
@router.get("/", response_model=list[EmployeeOut])
def list_employees(db: Session = Depends(get_db)):
    try:
        return db.query(Employee).filter(Employee.is_deleted == False).all()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error listing employees: {ex}")

# GET /employees/dashboard → Dashboard view of employees
@router.get("/dashboard")
def employee_dashboard(db: Session = Depends(get_db)) -> dict[str, Any]:
    try:
        employees = db.query(Employee).filter(Employee.is_deleted == False).all()

        total_employees = len(employees)
        active_employees = sum(1 for e in employees if e.status == "ACTIVE")
        inactive_employees = sum(1 for e in employees if e.status == "INACTIVE")
        deleted_employees = db.query(Employee).filter(Employee.is_deleted == True).count()

        department_counts = (
            db.query(Employee.department, func.count(Employee.employee_id))
            .filter(Employee.is_deleted == False)
            .group_by(Employee.department)
            .all()
        )
        department_summary = {dept: count for dept, count in department_counts}

        return {
            "summary": {
                "total_employees": total_employees,
                "active_employees": active_employees,
                "inactive_employees": inactive_employees,
                "deleted_employees": deleted_employees,
                "by_department": department_summary,
            },
            "employees": [
                {
                    "employee_id": e.employee_id,
                    "user_id": e.user_id,
                    "manager_id": e.manager_id,
                    "department": e.department,
                    "joining_date": e.joining_date,
                    "salary": float(e.salary) if e.salary is not None else None,
                    "status": e.status,
                }
                for e in employees
            ],
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching employee dashboard: {ex}")

# GET /employees/{id} → Employee details
@router.get("/{employee_id:int}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        employee = db.query(Employee).filter(Employee.employee_id == employee_id, Employee.is_deleted == False).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error fetching employee: {ex}")

# POST /employees → Create employee
@router.post("/", response_model=EmployeeOut)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        new_employee = Employee(**employee.model_dump())
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        return new_employee
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error creating employee: {ex}")

# PUT /employees/{id} → Update employee info
@router.put("/{employee_id:int}", response_model=EmployeeOut)
def update_employee(employee_id: int, update_data: EmployeeUpdate, db: Session = Depends(get_db)):
    try:
        employee = db.query(Employee).filter(Employee.employee_id == employee_id, Employee.is_deleted == False).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(employee, key, value)
        db.commit()
        db.refresh(employee)
        return employee
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error updating employee: {ex}")

# DELETE /employees/{id} → Soft delete employee
@router.delete("/{employee_id:int}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        employee.is_deleted = True
        db.commit()
        return {"message": "Employee soft deleted successfully"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error deleting employee: {ex}")
