from datetime import datetime

from sqlalchemy import Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CandidateAnalysis(Base):
    __tablename__ = "candidate_analyses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id"),
        nullable=False
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    skills: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    experience: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    education: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    relevant_experience: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    missing_requirements: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    match_analysis: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    requirement_analysis: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
