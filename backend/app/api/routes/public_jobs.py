
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobResponse

router = APIRouter(
    prefix="/public/jobs",
    tags=["Public Careers"],
)


@router.get("/", response_model=list[JobResponse])
def list_open_jobs(db: Session = Depends(get_db)):
    return (
        db.query(Job)
        .filter(Job.status == "open")
        .order_by(Job.created_at.desc())
        .all()
    )


@router.get("/{job_id}", response_model=JobResponse)
def get_open_job(job_id: int, db: Session = Depends(get_db)):
    job = (
        db.query(Job)
        .filter(Job.id == job_id, Job.status == "open")
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found or no longer available.",
        )

    return job
