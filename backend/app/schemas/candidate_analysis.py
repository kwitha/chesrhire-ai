from datetime import datetime

from pydantic import BaseModel


class CandidateAnalysisCreate(BaseModel):
    application_id: int
    summary: str
    skills: str
    experience: str
    education: str
    relevant_experience: str
    missing_requirements: str
    match_analysis: str
    requirement_analysis: list


class CandidateAnalysisResponse(BaseModel):
    id: int
    application_id: int
    summary: str
    skills: str
    experience: str
    education: str
    relevant_experience: str
    missing_requirements: str
    match_analysis: str
    requirement_analysis: list
    created_at: datetime

    class Config:
        from_attributes = True
