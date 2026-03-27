from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500))
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="tasks")
