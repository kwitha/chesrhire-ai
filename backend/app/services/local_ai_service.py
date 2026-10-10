import json
import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def analyze_candidate(
    cv_text: str,
    job_title: str,
    job_requirements: str
) -> dict:

    prompt = f"""
You are an AI recruitment assistant for ChesrHire AI.

Your task is to analyze a candidate's CV against a job's requirements.

JOB TITLE:
{job_title}

JOB REQUIREMENTS:
{job_requirements}

CANDIDATE CV:
{cv_text}

IMPORTANT RULES:

1. Read the ENTIRE CV before making conclusions.

2. Identify every individual requirement from the job requirements.

3. Analyze EACH requirement separately.

4. Search the ENTIRE CV for evidence for every requirement.

5. If evidence exists anywhere in the CV, mark the requirement as "Found".

6. If there is no evidence anywhere in the CV, mark the requirement as "Not Found".

7. Do not mark a requirement as "Not Found" simply because it is missing
from one section of the CV.

8. Recognize equivalent wording where appropriate.

Examples:
- "Python programming" supports Python.
- "Git/GitHub" supports Git.
- "RESTful API development" supports REST APIs.

9. Do NOT assume that related technologies are the same.

Examples:
- MySQL does NOT mean PostgreSQL.
- Laravel does NOT mean FastAPI.
- Eloquent ORM does NOT mean SQLAlchemy.

10. Consider evidence from all CV sections:
- Professional Summary
- Skills
- Work Experience
- Education
- Projects
- Certifications
- Other relevant sections

11. Do not invent qualifications, skills, experience, education,
certifications, or achievements.

12. Use ONLY information present in the CV.

13. For every requirement, provide specific evidence from the CV.

14. If no evidence exists, say:
"No supporting evidence was identified in the CV."

15. The requirement_analysis field MUST contain exactly six objects
for this job:

Python
FastAPI
SQLAlchemy
PostgreSQL
Git
REST APIs

16. The status field MUST be exactly:
"Found"
or
"Not Found"

17. All summary fields must contain REAL information from the CV.

18. NEVER return placeholder instructions as field values.

For example, DO NOT return:

"A concise summary of the candidate."

Instead, write an actual summary based on the CV.

DO NOT return:

"Relevant skills found in the CV."

Instead, list the actual skills found in the CV.

DO NOT return:

"Relevant professional experience found in the CV."

Instead, describe the candidate's actual experience.

DO NOT return:

"Requirements with no supporting evidence."

Instead, list the actual missing requirements.

DO NOT return:

"A concise comparison of the candidate against the job."

Instead, provide an actual comparison based on the CV evidence.

Return ONLY valid JSON.

Use this structure:

{{
    "summary": "Actual concise summary of the candidate based on the CV.",
    "skills": "Actual relevant skills found in the CV.",
    "experience": "Actual professional experience found in the CV.",
    "education": "Actual education found in the CV.",
    "relevant_experience": "Actual experience directly related to the job.",
    "missing_requirements": "Actual requirements for which no supporting evidence was found.",
    "match_analysis": "Actual comparison between the CV evidence and job requirements.",
    "requirement_analysis": [
        {{
            "requirement": "Python",
            "status": "Found",
            "evidence": "Actual evidence from the CV."
        }},
        {{
            "requirement": "FastAPI",
            "status": "Not Found",
            "evidence": "No supporting evidence was identified in the CV."
        }},
        {{
            "requirement": "SQLAlchemy",
            "status": "Not Found",
            "evidence": "No supporting evidence was identified in the CV."
        }},
        {{
            "requirement": "PostgreSQL",
            "status": "Not Found",
            "evidence": "No supporting evidence was identified in the CV."
        }},
        {{
            "requirement": "Git",
            "status": "Found",
            "evidence": "Actual evidence from the CV."
        }},
        {{
            "requirement": "REST APIs",
            "status": "Found",
            "evidence": "Actual evidence from the CV."
        }}
    ]
}}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=600
    )

    response.raise_for_status()

    result = response.json()

    return json.loads(result["response"])
