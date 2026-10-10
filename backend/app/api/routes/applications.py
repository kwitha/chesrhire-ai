import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.application import Application
from app.schemas.application import (
    ApplicationResponse,
    ApplicationStatusUpdate
)
from app.services.pdf_service import extract_text_from_pdf


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post(
    "/",
    response_model=ApplicationResponse
)
def create_application(
    job_id: int = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    cover_letter: str = Form(...),
    cv: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if cv.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF CV files are allowed."
        )

    upload_directory = "uploads/cvs"

    os.makedirs(
        upload_directory,
        exist_ok=True
    )

    unique_filename = f"{uuid.uuid4()}.pdf"

    file_path = os.path.join(
        upload_directory,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            cv.file,
            buffer
        )

    cv_text = extract_text_from_pdf(
        file_path
    )

    new_application = Application(
        job_id=job_id,
        full_name=full_name,
        email=email,
        phone=phone,
        cv_filename=cv.filename,
        cv_text=cv_text,
        cover_letter=cover_letter
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@router.get(
    "/",
    response_model=list[ApplicationResponse]
)
def get_applications(
    db: Session = Depends(get_db)
):
    applications = db.query(
        Application
    ).all()

    return applications


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.query(
        Application
    ).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    return application


@router.patch(
    "/{application_id}/status",
    response_model=ApplicationResponse
)
def update_application_status(
    application_id: int,
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db)
):
    allowed_statuses = {
        "pending",
        "reviewing",
        "shortlisted",
        "interview",
        "rejected",
        "hired"
    }

    new_status = status_update.status.lower().strip()

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid application status. "
                "Allowed statuses: pending, reviewing, "
                "shortlisted, interview, rejected, hired."
            )
        )

    application = db.query(
        Application
    ).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    application.status = new_status

    db.commit()
    db.refresh(application)

    return application
