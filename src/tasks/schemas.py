from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from src.auth.schemas import datetime_to_gmt_str


class TasksBase(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: datetime_to_gmt_str},
        populate_by_name=True,
        from_attributes=True
    )


class TasksCreate(TasksBase):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    status: str = "todo"

class TasksUpdate(TasksBase):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    status: Optional[str] = None


class TasksResponse(TasksBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
