from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    user_id: int

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    task_id: int
    created_at: datetime

    class Config:
        from_attributes = True 
        validate_by_name = True  