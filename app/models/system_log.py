from sqlalchemy import Column, Integer, Enum, Text, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SystemLog(Base):
    __tablename__ = "system_log"

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    log_type = Column(Enum("INFO", "ERROR", "WARNING", name="log_type_enum"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
