from datetime import datetime

from pydantic import BaseModel, EmailStr


class ApplicationCreate(BaseModel):
    job_id: int
    full_name: str
    email: str
    phone: str
    cv_filename: str
    cover_letter: str


class ApplicationStatusUpdate(BaseModel):
    status: str


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    full_name: str
    email: EmailStr
    phone: str
    cv_filename: str
    cv_text: str | None
    cover_letter: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
