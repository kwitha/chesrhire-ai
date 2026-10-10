
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_recruiter
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse, JobUpdate


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_recruiter=Depends(get_current_recruiter),
):
    new_job = Job(
        title=job.title,
        description=job.description,
        requirements=job.requirements,
        location=job.location,
        employment_type=job.employment_type,
        closing_date=job.closing_date,
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@router.get("/", response_model=list[JobResponse])
def get_jobs(
    db: Session = Depends(get_db),
    current_recruiter=Depends(get_current_recruiter),
):
    return db.query(Job).order_by(Job.created_at.desc()).all()


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_recruiter=Depends(get_current_recruiter),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )

    return job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_recruiter=Depends(get_current_recruiter),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )

    job.title = job_data.title
    job.description = job_data.description
    job.requirements = job_data.requirements
    job.location = job_data.location
    job.employment_type = job_data.employment_type
    job.closing_date = job_data.closing_date

    db.commit()
    db.refresh(job)

    return job
