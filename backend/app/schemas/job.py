
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str
    description: str
    requirements: str
    location: str
    employment_type: str
    closing_date: datetime | None = None


class JobUpdate(BaseModel):
    title: str
    description: str
    requirements: str
    location: str
    employment_type: str
    closing_date: datetime | None = None


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    requirements: str
    location: str
    employment_type: str
    closing_date: datetime | None
    status: str
    created_at: datetime
