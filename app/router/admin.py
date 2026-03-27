from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models import User, Employee, Product, Order, Attendance, Salary, Payment  
from app.models.order_item import OrderItem  
from app.models.Attendance import Attendance

router = APIRouter(prefix="/admin", tags=["Admin Utilities"])

# GET /dashboard/summary → High-level stats

@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    try:
        users_count = db.query(func.count(User.user_id)).scalar()
        employees_count = db.query(func.count(Employee.employee_id)).scalar()
        products_count = db.query(func.count(Product.product_id)).scalar()
        orders_count = db.query(func.count(Order.order_id)).scalar()
        revenue = db.query(func.sum(OrderItem.price * OrderItem.quantity)).scalar()  # use actual column

        return {
            "users": users_count,
            "employees": employees_count,
            "products": products_count,
            "orders": orders_count,
            "revenue": revenue or 0
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Fetching summary failed: {str(ex)}")


# GET /reports/sales → Sales report (monthly, yearly)
@router.get("/reports/sales")
def sales_report(period: str = "monthly", db: Session = Depends(get_db)):
    try:
        if period == "monthly":
            result = (
                db.query(
                    func.date_format(Order.order_date, "%Y-%m").label("month"),
                    func.sum(OrderItem.price * OrderItem.quantity).label("revenue")
                )
                .join(Order, Order.order_id == OrderItem.order_id)  # ✅ join with Order
                .group_by("month")
                .order_by("month")
                .all()
            )
        else:  # yearly
            result = (
                db.query(
                    func.year(Order.order_date).label("year"),
                    func.sum(OrderItem.price * OrderItem.quantity).label("revenue")
                )
                .join(Order, Order.order_id == OrderItem.order_id)  # ✅ join with Order
                .group_by("year")
                .order_by("year")
                .all()
            )

        return [{"period": row[0], "revenue": float(row[1])} for row in result]
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Fetching sales report failed: {str(ex)}")



# GET /reports/attendance → Attendance report
@router.get("/reports/attendance")
def attendance_report(db: Session = Depends(get_db)):
    try:
        result = (
            db.query(
                Attendance.employee_id,
                func.count().label("days_present")
            )
            .filter(Attendance.status == "PRESENT")
            .group_by(Attendance.employee_id)
            .all()
        )

        return [
            {"employee_id": row[0], "days_present": row[1]}
            for row in result
        ]
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Fetching attendance report failed: {str(ex)}")


# GET /reports/salary → Salary report
@router.get("/reports/salary")
def salary_report(db: Session = Depends(get_db)):
    try:
        result = (
            db.query(
                Salary.employee_id,
                func.sum(Salary.net_salary).label("total_salary")
            )
            .group_by(Salary.employee_id)
            .all()
        )
        return [
            {"employee_id": row[0], "total_salary": float(row[1])}
            for row in result
        ]
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Fetching salary report failed: {str(ex)}")
