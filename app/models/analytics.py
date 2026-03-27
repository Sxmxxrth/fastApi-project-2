from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ReportCache(Base):
    __tablename__ = "report_cache"

    report_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_type = Column(String(100), nullable=False)
    data = Column(JSON, nullable=False)
    generated_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


class ProductView(Base):
    __tablename__ = "product_views"

    view_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    viewed_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="views")
    user = relationship("User", back_populates="views")