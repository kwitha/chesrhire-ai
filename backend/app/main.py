from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.jobs import router as jobs_router
from app.api.routes.applications import router as applications_router
from app.api.routes.candidate_analysis import router as candidate_analysis_router
from app.models.candidate_analysis import CandidateAnalysis
from app.api.routes.auth import router as auth_router
from app.api.routes.public_jobs import router as public_jobs_router
app = FastAPI(
    title="ChesrHire AI",
    description="AI-Powered Recruitment and Talent Management Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_router)
app.include_router(applications_router)
app.include_router(candidate_analysis_router)
app.include_router(auth_router)
app.include_router(public_jobs_router)
@app.get("/")
def home():
    return {
        "message": "Welcome to ChesrHire AI",
        "status": "API is running"
    }
