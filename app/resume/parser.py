# ============================================
# AI Interview System - Resume Parser
# ============================================

import pdfplumber
import os

from app.interviews.ai_engine import parse_resume


def extract_text_from_pdf(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            pt = page.extract_text()
            if pt:
                text += pt + "\n"

    if not text.strip():
        raise ValueError("PDF has no extractable text")

    return text.strip()


def extract_skills_simple(text: str) -> list:
    """Fallback — keyword based skill extraction."""
    common = [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "php",
        "html", "css", "react", "angular", "vue", "node", "express",
        "django", "flask", "fastapi", "spring", "sql", "mysql", "postgresql",
        "mongodb", "sqlite", "redis", "oracle", "sql server", "mssql",
        "git", "github", "docker", "kubernetes", "aws", "azure", "gcp",
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "pandas", "numpy", "scikit-learn", "data analysis", "power bi",
        "tableau", "excel", "rest api", "graphql", "microservices",
        "linux", "bash", "devops", "ci/cd", "jenkins", "terraform",
        "backup", "recovery", "replication", "mirroring", "performance tuning",
        "database administration", "dba", "query optimization", "automation",
        "scripting", "networking", "security", "access control",
    ]
    text_lower = text.lower()
    found = []
    for skill in common:
        if skill in text_lower:
            found.append(skill.title())
    return sorted(list(set(found)))


def safe_parse_resume(file_path: str) -> dict:
    """Parse resume with fallback."""
    try:
        raw = extract_text_from_pdf(file_path)
    except Exception as e:
        print(f"[parser] PDF extraction failed: {e}")
        return {"skills": [], "experience_years": 0,
                "summary": "Could not parse resume", "raw_text": ""}

    # Try AI first
    try:
        ai_result = parse_resume(raw)
        if ai_result.get("skills"):
            return {
                "skills": ai_result.get("skills", []),
                "experience_years": ai_result.get("experience_years", 0),
                "summary": ai_result.get("summary", ""),
                "raw_text": raw,
            }
    except Exception as e:
        print(f"[parser] AI parse failed: {e}")

    # Fallback — simple extraction
    skills = extract_skills_simple(raw)
    return {
        "skills": skills,
        "experience_years": 0,
        "summary": f"Extracted {len(skills)} skills using fallback parser.",
        "raw_text": raw,
    }


def parse_resume_pdf(file_path: str) -> dict:
    return safe_parse_resume(file_path)