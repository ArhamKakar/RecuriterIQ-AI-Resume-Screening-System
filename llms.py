import requests
import json
import re
import os

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


def score_candidate(resume_data: dict, job_description: str) -> dict:
    prompt = f"""<s>[INST]
You are a senior technical recruiter. Evaluate this candidate against the job description.

JOB DESCRIPTION:
{job_description[:800]}

CANDIDATE SKILLS:
{', '.join(resume_data['skills']) if resume_data['skills'] else 'No skills detected'}

RESUME TEXT:
{resume_data['raw_text'][:800]}

Return ONLY a JSON object with NO extra text, no markdown, no explanation:
{{
  "score": <integer 0-100>,
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "summary": "<2 sentence overall evaluation>",
  "recommendation": "Strong Fit",
  "strengths": [
    "Strong Python and backend development experience demonstrated through...",
    "Hands-on ML project experience with..."
  ],
  "weaknesses": [
    "No evidence of cloud deployment experience (AWS/GCP)",
    "Missing containerization skills like Docker/Kubernetes"
  ],
  "improvements": [
    "Add quantified achievements e.g. 'Reduced inference time by 40%'",
    "Include links to GitHub projects or deployed demos",
    "Add keywords: LangChain, FastAPI, vector databases"
  ]
}}

recommendation must be exactly one of: "Strong Fit", "Possible Fit", "Not a Fit"
strengths, weaknesses, improvements must each have 2-3 items.
[/INST]</s>"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 600,
            "temperature": 0.1,
            "return_full_text": False,
            "do_sample": False
        }
    }

    try:
        print(f"Scoring: {resume_data.get('name', 'unknown')}")
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=90)
        response.raise_for_status()

        raw = response.json()[0]["generated_text"]
        print(f"Raw response: {raw[:300]}")

        raw = re.sub(r"```json|```", "", raw).strip()

        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            if "score" in parsed:
                return parsed

        parsed = json.loads(raw)
        return parsed

    except json.JSONDecodeError as e:
        print(f"JSON error: {e} | raw: {raw[:200]}")
    except requests.exceptions.Timeout:
        print("HF API timed out — retrying with fallback")
    except Exception as e:
        print(f"HF API error: {e}")

    return fallback_score(resume_data, job_description)


def fallback_score(resume_data: dict, job_description: str) -> dict:
    jd_lower = job_description.lower()
    candidate_skills = [s.lower() for s in resume_data.get("skills", [])]

    common_tech = [
        "python", "java", "javascript", "react", "sql", "docker",
        "kubernetes", "aws", "machine learning", "nlp", "fastapi",
        "tensorflow", "pytorch", "git", "linux", "mongodb", "langchain",
        "deep learning", "scikit-learn", "pandas", "numpy"
    ]

    jd_keywords  = [k for k in common_tech if k in jd_lower]
    matching     = [s for s in candidate_skills if s in jd_lower]
    missing      = [k for k in jd_keywords if k not in candidate_skills]

    score = int((len(matching) / max(len(jd_keywords), 1)) * 100) if jd_keywords else 20
    score = max(5, min(score, 95))

    if score >= 70:
        rec = "Strong Fit"
    elif score >= 40:
        rec = "Possible Fit"
    else:
        rec = "Not a Fit"

    strengths = (
        [f"Candidate has {s} experience which matches the job requirements" for s in matching[:2]]
        or ["Candidate profile was processed with keyword matching due to API limits"]
    )

    weaknesses = (
        [f"Missing {m} which is required for this role" for m in missing[:2]]
        or ["Could not perform deep analysis — try again for full insights"]
    )

    improvements = [
        "Add more specific technical keywords from the job description",
        "Include measurable outcomes and project impact in your resume",
        "List certifications and tools explicitly in a dedicated skills section"
    ]

    return {
        "score": score,
        "matching_skills": matching,
        "missing_skills": missing[:5],
        "summary": f"Keyword-based evaluation: {len(matching)} of {len(jd_keywords)} required skills matched.",
        "recommendation": rec,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improvements": improvements
    }


def rank_candidates(candidates: list[dict]) -> list[dict]:
    return sorted(candidates, key=lambda c: c["score"], reverse=True)