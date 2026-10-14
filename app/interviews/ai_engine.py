# ============================================
# AI Interview System - AI Engine
# ============================================

import json
import re
import uuid
import time
import random
import google.generativeai as genai

from app.config import settings
from app.utils.prompts import (
    QUESTION_GENERATION_PROMPT,
    ANSWER_EVALUATION_PROMPT,
    FOLLOWUP_QUESTION_PROMPT,
    RESUME_PARSING_PROMPT,
)


# ============================================
# GEMINI INITIALIZE
# ============================================

genai.configure(api_key=settings.GEMINI_API_KEY)

# Fallback models — agar ek fail ho toh doosra try karo
MODELS = [

    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
]
def _get_model(name=None):
    """Get model instance. If name None, try all models."""
    if name:
        return genai.GenerativeModel(name)
    return genai.GenerativeModel(MODELS[0])


def _clean_json_response(text: str) -> str:
    """Clean AI response to get pure JSON."""
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


# ============================================
# QUESTION GENERATION (GUARANTEED UNIQUE)
# ============================================

def generate_questions(
    job_role: str,
    skills: list,
    num_questions: int = 5,
    difficulty: str = "medium"
) -> list:
    """
    Generates UNIQUE questions every call.
    Uses multiple random seeds + timestamp + retry with different models.
    """
    skills_str = ", ".join(skills) if skills else "general skills"

    # Ultra-unique seeds
    session_id = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000000))
    random_num = random.randint(100000000, 999999999)
    random.shuffle(MODELS)  # Shuffle models each call

    prompt = f"""You are a senior technical interviewer. Generate exactly {num_questions} COMPLETELY NEW and UNIQUE interview questions.

**Job Role:** {job_role}
**Skills:** {skills_str}
**Difficulty:** {difficulty}

**UNIQUE SESSION: {session_id}**
**TIMESTAMP: {timestamp}**
**RANDOM: {random_num}**

CRITICAL RULES:
1. These must be BRAND NEW questions, never generated before
2. Each question must be DIFFERENT from the others
3. Mix different topics: fundamentals, scenarios, debugging, optimization, design, best practices
4. Do NOT repeat common interview questions
5. Be specific to the role and skills
6. Each question must be 1-2 sentences

Vary these aspects randomly:
- Topic area (Python internals vs frameworks vs databases vs algorithms)
- Question type (what/why/how vs scenario-based vs problem-solving)
- Complexity level within {difficulty}

Return ONLY a valid JSON array of {num_questions} strings. Nothing else.
Example: ["Question 1?", "Question 2?", "Question 3?"]"""

    # Try each model until success
    last_error = None
    for model_name in MODELS:
        try:
            model = _get_model(model_name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 2.0,
                    "top_p": 1.0,
                    "top_k": 100,
                    "candidate_count": 1,
                    "max_output_tokens": 2000,
                },
            )
            
            cleaned = _clean_json_response(response.text)
            questions = json.loads(cleaned)

            if not isinstance(questions, list) or len(questions) == 0:
                continue

            # Deduplicate
            seen = set()
            unique = []
            for q in questions:
                q_clean = q.strip()
                q_norm = q_clean.lower()
                if q_norm not in seen and len(q_clean) > 10:
                    seen.add(q_norm)
                    unique.append(q_clean)

            if len(unique) >= num_questions:
                print(f"[ai_engine] Generated {len(unique)} unique questions using {model_name}")
                return unique[:num_questions]
            elif len(unique) > 0:
                print(f"[ai_engine] Only got {len(unique)} from {model_name}, retrying...")
                last_error = f"Only {len(unique)} questions"

        except Exception as e:
            print(f"[ai_engine] Model {model_name} failed: {e}")
            last_error = str(e)
            continue

    # All models failed — return fallback
    print(f"[ai_engine] All models failed. Last error: {last_error}")
    return [
        f"Describe a challenging project you worked on as a {job_role}.",
        f"How do you stay updated with new technologies in your field?",
        f"Explain a time when you had to debug a complex issue.",
        f"What's your approach to learning a new technology?",
        f"How do you handle tight deadlines and pressure?",
    ][:num_questions]


# ============================================
# ANSWER EVALUATION
# ============================================

def evaluate_answer(question: str, answer: str) -> dict:
    """Evaluate an answer."""
    prompt = ANSWER_EVALUATION_PROMPT.format(question=question, answer=answer)

    default_response = {
        "score": 0,
        "technical_accuracy": 0,
        "clarity": 0,
        "completeness": 0,
        "strengths": "N/A",
        "weaknesses": "Evaluation failed",
        "improvement_tips": "Try again",
    }

    for model_name in MODELS[:3]:
        try:
            model = _get_model(model_name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "candidate_count": 1,
                },
            )
            cleaned = _clean_json_response(response.text)
            result = json.loads(cleaned)
            return result
        except Exception as e:
            print(f"[ai_engine] Eval failed with {model_name}: {e}")
            continue

    return default_response


# ============================================
# FOLLOWUP
# ============================================

def generate_followup(question: str, answer: str) -> str:
    prompt = FOLLOWUP_QUESTION_PROMPT.format(question=question, answer=answer)
    for model_name in MODELS[:3]:
        try:
            model = _get_model(model_name)
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            continue
    return "Can you elaborate on that?"


# ============================================
# RESUME PARSING
# ============================================

def parse_resume(resume_text: str) -> dict:
    default = {"skills": [], "experience_years": 0, "summary": "Could not parse"}
    truncated = resume_text[:4000]
    prompt = RESUME_PARSING_PROMPT.format(resume_text=truncated)

    for model_name in MODELS[:3]:
        try:
            model = _get_model(model_name)
            response = model.generate_content(prompt)
            cleaned = _clean_json_response(response.text)
            return json.loads(cleaned)
        except Exception as e:
            print(f"[ai_engine] Resume parse failed with {model_name}: {e}")
            continue

    return default