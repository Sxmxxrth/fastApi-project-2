from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class LogType(str, Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    CODE500 = "500"
class SystemLogBase(BaseModel):
    log_type: LogType
    message: str

class SystemLogCreate(SystemLogBase):
    pass

class SystemLogRead(SystemLogBase):
    log_id: int
    created_at: datetime

    class Config:
        orm_mode = True
