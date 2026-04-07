from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio

from utils import parse_resume
from llms import score_candidate, rank_candidates

app = FastAPI(title="Resume Screener API")

# Concept: CORS middleware
# Browsers block cross-origin requests by default.
# This tells FastAPI to allow requests from your Streamlit frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/screen")
async def screen_resumes(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    """
    Concept: Async file handling
    `await file.read()` doesn't block the server while reading.
    Multiple resumes are processed concurrently with asyncio.gather().
    
    Concept: Multipart form data
    The frontend sends files + text together as multipart/form-data,
    not JSON — because JSON can't carry binary file content.
    """

    async def process_one(file: UploadFile) -> dict:
        content = await file.read()
        parsed = parse_resume(content)           # extract skills/name
        scored = score_candidate(parsed, job_description)  # LLM scoring
        return {
            "filename": file.filename,
            "name": parsed["name"],
            "email": parsed["email"],
            "skills": parsed["skills"],
            **scored  # merge score, summary, recommendation
        }

    # Concept: Concurrent execution
    # asyncio.gather runs all PDF processings in parallel,
    # so 10 resumes don't take 10x the time.
    results = await asyncio.gather(*[process_one(f) for f in files])
    ranked = rank_candidates(list(results))

    return {"total": len(ranked), "candidates": ranked}