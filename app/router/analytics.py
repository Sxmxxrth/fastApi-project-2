from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.analytics import ReportCache, ProductView
from app.schema.analytics import ReportCacheOut, ProductViewOut
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/reports", tags=["Analytics & Reports"])

# GET /reports/sales → Sales Report
@router.get("/sales", response_model=list[ReportCacheOut])
def sales_report(db: Session = Depends(get_db)):
    try:
        return db.query(ReportCache).filter(ReportCache.report_type == "sales").all()
    except Exception as ex:
        logger.exception(f"Error fetching sales report: {ex}")
        raise HTTPException(status_code=500, detail="Error fetching sales report")


# GET /reports/users → User Growth Report
@router.get("/users", response_model=list[ReportCacheOut])
def user_growth_report(db: Session = Depends(get_db)):
    try:
        return db.query(ReportCache).filter(ReportCache.report_type == "users").all()
    except Exception as ex:
        logger.exception(f"Error fetching user growth report: {ex}")
        raise HTTPException(status_code=500, detail="Error fetching user growth report")


# GET /reports/products → Top Products Report
@router.get("/products", response_model=list[ProductViewOut])
def top_products_report(limit: int = 10, db: Session = Depends(get_db)):
    try:
        result = (
            db.query(ProductView.product_id, func.count(ProductView.view_id).label("views"))
            .group_by(ProductView.product_id)
            .order_by(func.count(ProductView.view_id).desc())
            .limit(limit)
            .all()
        )
        return [{"product_id": row[0], "views": row[1]} for row in result]
    except Exception as ex:
        logger.exception(f"Error fetching top products report: {ex}")
        raise HTTPException(status_code=500, detail="Error fetching top products report")
# GET /reports/revenue → Revenue Report
@router.get("/revenue", response_model=list[ReportCacheOut])
def revenue_report(db: Session = Depends(get_db)):
    try:
        return db.query(ReportCache).filter(ReportCache.report_type == "revenue").all()
    except Exception as ex:
        logger.exception(f"Error fetching revenue report: {ex}")
        raise HTTPException(status_code=500, detail="Error fetching revenue report")    
    