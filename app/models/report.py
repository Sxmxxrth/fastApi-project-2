# models/report.py
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from app.core.database import Base

class SalesReport(Base):
    __tablename__ = "sales_report"   # optional materialized view
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(String(20))      # e.g. "2026-01" or "2026"
    revenue = Column(Float)

class AttendanceReport(Base):
    __tablename__ = "attendance_report"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer)
    days_present = Column(Integer)

class SalaryReport(Base):
    __tablename__ = "salary_report"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer)
    total_salary = Column(Float)

class InventoryReport(Base):
    __tablename__ = "inventory_report"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer)
    quantity = Column(Integer)