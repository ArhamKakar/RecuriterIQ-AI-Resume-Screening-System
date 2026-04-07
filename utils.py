import fitz  # PyMuPDF
import spacy
import re

nlp = spacy.load("en_core_web_sm")

# --- Skill keyword bank ---
SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "react", "node.js",
    "sql", "postgresql", "mongodb", "docker", "kubernetes", "aws",
    "machine learning", "deep learning", "nlp", "fastapi", "django",
    "git", "linux", "tensorflow", "pytorch", "pandas", "scikit-learn",
]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Concept: PDF parsing
    PyMuPDF opens the binary PDF and extracts raw text page by page.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()


def extract_skills(text: str) -> list[str]:
    """
    Concept: Keyword matching + NLP entity recognition
    We use two strategies:
      1. Simple keyword matching against a known skill list
      2. spaCy NER to catch org/product names we haven't hardcoded
    """
    text_lower = text.lower()
    matched_skills = [skill for skill in SKILL_KEYWORDS if skill in text_lower]

    # spaCy pass — catch tech names as ORG or PRODUCT entities
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("ORG", "PRODUCT"):
            matched_skills.append(ent.text.lower())

    return list(set(matched_skills))  # deduplicate


def extract_candidate_name(text: str) -> str:
    """
    Concept: Named Entity Recognition (NER)
    spaCy labels sequences of tokens with entity types.
    PERSON is the label for human names.
    """
    doc = nlp(text[:500])  # Names are usually near the top
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown Candidate"


def extract_email(text: str) -> str:
    """
    Concept: Regular expressions (regex)
    A regex pattern describes the *shape* of an email address.
    re.search scans the text and returns the first match.
    """
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(pattern, text)
    return match.group() if match else "N/A"


def parse_resume(file_bytes: bytes) -> dict:
    """
    Orchestrator: runs all extractors and returns a structured dict.
    This is what the API endpoint will call.
    """
    text = extract_text_from_pdf(file_bytes)
    return {
        "raw_text": text,
        "name": extract_candidate_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
    }