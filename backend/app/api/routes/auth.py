from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    get_current_recruiter,
    verify_password,
)
from app.models.recruiter import Recruiter
from app.schemas.auth import LoginRequest, LoginResponse, RecruiterResponse

router = APIRouter(
    prefix="/auth",
    tags=["Recruiter Authentication"]
)


@router.post("/login", response_model=LoginResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    recruiter = db.query(Recruiter).filter(
        Recruiter.email == str(login_data.email).lower()
    ).first()

    if (
        recruiter is None
        or not recruiter.is_active
        or not verify_password(
            login_data.password,
            recruiter.hashed_password
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

    token = create_access_token(recruiter.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "recruiter": recruiter
    }


@router.get("/me", response_model=RecruiterResponse)
def get_my_account(
    recruiter: Recruiter = Depends(get_current_recruiter)
):
    return recruiter
