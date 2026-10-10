import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is not configured."
    )

client = OpenAI(api_key=api_key)


def analyze_candidate(
    cv_text: str,
    job_title: str,
    job_requirements: str
) -> dict:

    prompt = f"""
You are an AI recruitment assistant for ChesrHire AI.

Analyze the candidate's CV against the job requirements.

JOB TITLE:
{job_title}

JOB REQUIREMENTS:
{job_requirements}

CANDIDATE CV:
{cv_text}

Return ONLY valid JSON using exactly these fields:

{{
    "summary": "...",
    "skills": "...",
    "experience": "...",
    "education": "...",
    "relevant_experience": "...",
    "missing_requirements": "...",
    "match_analysis": "..."
}}

Use only information present in the CV and job description.
Do not invent qualifications, experience, skills, or achievements.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    result = json.loads(response.output_text)

    return result
