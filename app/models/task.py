from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base



class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    status = Column(String(50), default="open")
    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="tasks")
