import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.application import Application
from app.models.job import Job
from app.models.candidate_analysis import CandidateAnalysis
from app.schemas.candidate_analysis import CandidateAnalysisResponse
from app.services.local_ai_service import analyze_candidate


def convert_to_text(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)

    return str(value)


router = APIRouter(
    prefix="/candidate-analysis",
    tags=["Candidate Analysis"]
)


@router.post(
    "/generate/{application_id}",
    response_model=CandidateAnalysisResponse
)
def generate_candidate_analysis(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    job = db.query(Job).filter(
        Job.id == application.job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    if not application.cv_text:
        raise HTTPException(
            status_code=400,
            detail="Application does not contain extracted CV text."
        )

    ai_result = analyze_candidate(
        cv_text=application.cv_text,
        job_title=job.title,
        job_requirements=job.requirements
    )

    requirement_analysis = ai_result.get(
        "requirement_analysis"
    )

    if not requirement_analysis:
        raise HTTPException(
            status_code=500,
            detail=(
                "AI analysis did not return "
                "requirement-by-requirement analysis."
            )
        )

    analysis = db.query(CandidateAnalysis).filter(
        CandidateAnalysis.application_id == application.id
    ).first()

    if analysis:
        analysis.summary = convert_to_text(
            ai_result.get(
                "summary",
                "Not provided by AI."
            )
        )

        analysis.skills = convert_to_text(
            ai_result.get(
                "skills",
                "Not provided by AI."
            )
        )

        analysis.experience = convert_to_text(
            ai_result.get(
                "experience",
                "Not provided by AI."
            )
        )

        analysis.education = convert_to_text(
            ai_result.get(
                "education",
                "Not provided by AI."
            )
        )

        analysis.relevant_experience = convert_to_text(
            ai_result.get(
                "relevant_experience",
                "Not provided by AI."
            )
        )

        analysis.missing_requirements = convert_to_text(
            ai_result.get(
                "missing_requirements",
                "Not provided by AI."
            )
        )

        analysis.match_analysis = convert_to_text(
            ai_result.get(
                "match_analysis",
                "Not provided by AI."
            )
        )

        analysis.requirement_analysis = requirement_analysis

    else:
        analysis = CandidateAnalysis(
            application_id=application.id,

            summary=convert_to_text(
                ai_result.get(
                    "summary",
                    "Not provided by AI."
                )
            ),

            skills=convert_to_text(
                ai_result.get(
                    "skills",
                    "Not provided by AI."
                )
            ),

            experience=convert_to_text(
                ai_result.get(
                    "experience",
                    "Not provided by AI."
                )
            ),

            education=convert_to_text(
                ai_result.get(
                    "education",
                    "Not provided by AI."
                )
            ),

            relevant_experience=convert_to_text(
                ai_result.get(
                    "relevant_experience",
                    "Not provided by AI."
                )
            ),

            missing_requirements=convert_to_text(
                ai_result.get(
                    "missing_requirements",
                    "Not provided by AI."
                )
            ),

            match_analysis=convert_to_text(
                ai_result.get(
                    "match_analysis",
                    "Not provided by AI."
                )
            ),

            requirement_analysis=requirement_analysis
        )

        db.add(analysis)

    db.commit()
    db.refresh(analysis)

    return analysis


@router.post(
    "/",
    response_model=CandidateAnalysisResponse
)
def create_candidate_analysis(
    analysis: dict,
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(
        Application.id == analysis["application_id"]
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found."
        )

    requirement_analysis = analysis.get(
        "requirement_analysis"
    )

    if not requirement_analysis:
        raise HTTPException(
            status_code=400,
            detail="Requirement analysis is required."
        )

    existing_analysis = db.query(CandidateAnalysis).filter(
        CandidateAnalysis.application_id == application.id
    ).first()

    if existing_analysis:
        existing_analysis.summary = convert_to_text(
            analysis["summary"]
        )

        existing_analysis.skills = convert_to_text(
            analysis["skills"]
        )

        existing_analysis.experience = convert_to_text(
            analysis["experience"]
        )

        existing_analysis.education = convert_to_text(
            analysis["education"]
        )

        existing_analysis.relevant_experience = convert_to_text(
            analysis["relevant_experience"]
        )

        existing_analysis.missing_requirements = convert_to_text(
            analysis["missing_requirements"]
        )

        existing_analysis.match_analysis = convert_to_text(
            analysis["match_analysis"]
        )

        existing_analysis.requirement_analysis = requirement_analysis

        db.commit()
        db.refresh(existing_analysis)

        return existing_analysis

    new_analysis = CandidateAnalysis(
        application_id=analysis["application_id"],

        summary=convert_to_text(
            analysis["summary"]
        ),

        skills=convert_to_text(
            analysis["skills"]
        ),

        experience=convert_to_text(
            analysis["experience"]
        ),

        education=convert_to_text(
            analysis["education"]
        ),

        relevant_experience=convert_to_text(
            analysis["relevant_experience"]
        ),

        missing_requirements=convert_to_text(
            analysis["missing_requirements"]
        ),

        match_analysis=convert_to_text(
            analysis["match_analysis"]
        ),

        requirement_analysis=requirement_analysis
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return new_analysis


@router.get(
    "/{application_id}",
    response_model=CandidateAnalysisResponse
)
def get_candidate_analysis(
    application_id: int,
    db: Session = Depends(get_db)
):
    analysis = db.query(CandidateAnalysis).filter(
        CandidateAnalysis.application_id == application_id
    ).order_by(
        CandidateAnalysis.created_at.desc()
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Candidate analysis not found."
        )

    return analysis
