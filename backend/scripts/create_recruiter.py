from getpass import getpass

from sqlalchemy import func

from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.job import Job
from app.models.application import Application
from app.models.candidate_analysis import CandidateAnalysis
from app.models.recruiter import Recruiter


def main():
    Base.metadata.create_all(bind=engine)

    full_name = input("Recruiter full name: ").strip()
    email = input("Recruiter email: ").strip().lower()
    password = getpass("Create recruiter password: ")
    confirm_password = getpass("Confirm recruiter password: ")

    if not full_name or not email:
        print("Name and email are required.")
        return

    if len(password) < 12:
        print("Use a password with at least 12 characters.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    db = SessionLocal()

    try:
        existing = db.query(Recruiter).filter(
            func.lower(Recruiter.email) == email
        ).first()

        if existing:
            print("A recruiter with that email already exists.")
            return

        recruiter = Recruiter(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            is_active=True
        )

        db.add(recruiter)
        db.commit()

        print("Recruiter account created successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
