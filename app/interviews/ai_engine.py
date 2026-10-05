# ============================================
# AI Interview System - AI Engine
# ============================================
# Yeh file Gemini AI se baat karti hai.
# Questions generate karti hai, answers evaluate karti hai.
# ============================================

import json
import re
import google.generativeai as genai

from app.config import settings
from app.utils.prompts import (
    QUESTION_GENERATION_PROMPT,
    ANSWER_EVALUATION_PROMPT,
    FOLLOWUP_QUESTION_PROMPT,
    RESUME_PARSING_PROMPT,
)


# ============================================
# 1. GEMINI INITIALIZE
# ============================================

genai.configure(api_key=settings.GEMINI_API_KEY)

# Model setup — flash fast aur free hai
model = genai.GenerativeModel("gemini-3.8-flash")


# ============================================
# 2. HELPER - JSON Clean Karo
# ============================================

def _clean_json_response(text: str) -> str:
    """
    AI ke response se ```json aur ``` hata deta hai.
    """
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


# ============================================
# 3. QUESTION GENERATION
# ============================================

def generate_questions(
    job_role: str,
    skills: list,
    num_questions: int = 5,
    difficulty: str = "medium"
) -> list:
    """
    Role aur skills ke basis pe interview questions banata hai.
    Returns: list of question strings
    """
    skills_str = ", ".join(skills) if skills else "general"
    
    prompt = QUESTION_GENERATION_PROMPT.format(
        num_questions=num_questions,
        job_role=job_role,
        skills=skills_str,
        difficulty=difficulty,
    )
    
    try:
        response = model.generate_content(prompt)
        cleaned = _clean_json_response(response.text)
        questions = json.loads(cleaned)
        
        if not isinstance(questions, list):
            raise ValueError("AI ne list return nahi ki")
        
        return questions[:num_questions]
    
    except json.JSONDecodeError as e:
        print(f"[ai_engine] JSON decode error: {e}")
        print(f"[ai_engine] Raw response: {response.text[:200]}")
        return [f"Tell me about your experience with {job_role}."]
    except Exception as e:
        print(f"[ai_engine] Error: {e}")
        return [f"Explain a challenging project you worked on."]


# ============================================
# 4. ANSWER EVALUATION
# ============================================

def evaluate_answer(question: str, answer: str) -> dict:
    """
    Answer ko evaluate karta hai aur score deta hai.
    Returns: dict with score, feedback, etc.
    """
    prompt = ANSWER_EVALUATION_PROMPT.format(
        question=question,
        answer=answer,
    )
    
    default_response = {
        "score": 5,
        "technical_accuracy": 5,
        "clarity": 5,
        "completeness": 5,
        "strengths": "Answer was provided.",
        "weaknesses": "Could not evaluate in detail.",
        "improvement_tips": "Try to provide more specific examples.",
    }
    
    try:
        response = model.generate_content(prompt)
        cleaned = _clean_json_response(response.text)
        result = json.loads(cleaned)
        return result
    
    except json.JSONDecodeError as e:
        print(f"[ai_engine] JSON decode error: {e}")
        return default_response
    except Exception as e:
        print(f"[ai_engine] Error: {e}")
        return default_response


# ============================================
# 5. FOLLOW-UP QUESTION
# ============================================

def generate_followup(question: str, answer: str) -> str:
    """
    Candidate ke answer pe ek follow-up question banata hai.
    """
    prompt = FOLLOWUP_QUESTION_PROMPT.format(
        question=question,
        answer=answer,
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ai_engine] Error: {e}")
        return "Can you elaborate more on that?"


# ============================================
# 6. RESUME PARSING
# ============================================

def parse_resume(resume_text: str) -> dict:
    """
    Resume text se skills aur experience nikaltа hai.
    """
    default_response = {
        "skills": [],
        "experience_years": 0,
        "summary": "Could not parse resume.",
    }
    
    # Bahut lamba text na bhejo — AI ka limit hai
    truncated_text = resume_text[:4000]
    
    prompt = RESUME_PARSING_PROMPT.format(resume_text=truncated_text)
    
    try:
        response = model.generate_content(prompt)
        cleaned = _clean_json_response(response.text)
        result = json.loads(cleaned)
        return result
    except json.JSONDecodeError as e:
        print(f"[ai_engine] JSON decode error: {e}")
        return default_response
    except Exception as e:
        print(f"[ai_engine] Error: {e}")
        return default_response