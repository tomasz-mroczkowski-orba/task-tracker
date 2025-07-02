import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class StatusEnum(str, Enum):
    pending: str = "pending",
    in_progress: str = "in_progress",
    completed: str = "completed"

class TaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, min_length=1, max_length=100)
    status: StatusEnum = Field(description="Status of the task, must be pending, in_progres or done")
    due_date: Optional[datetime.datetime] = Field(default=None)

