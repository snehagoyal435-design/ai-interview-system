# ============================================
# AI Interview System - Answer Scorer
# ============================================
# Yeh file answer ko AI se evaluate karwati hai
# aur database mein score save karti hai.
# ============================================

from sqlalchemy.orm import Session
from app.models import Interview, Question
from app.interviews.ai_engine import evaluate_answer


# ============================================
# 1. SINGLE ANSWER SCORE KARO
# ============================================

def score_answer(
    question_id: int,
    db: Session,
    generate_followup: bool = False,
) -> dict:
    """
    Ek answer ko evaluate karta hai aur DB mein save karta hai.
    
    Args:
        question_id: Question ki ID
        db: Database session
        generate_followup: True karo toh follow-up question bhi banayega
    
    Returns:
        dict with:
        - success: True/False
        - score: int (0-10)
        - feedback: str
        - error: error message (agar fail ho)
    """
    # Step 1: Question dhoondo
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        return {
            "success": False,
            "score": None,
            "feedback": None,
            "error": f"Question {question_id} not found",
        }
    
    # Step 2: Check karo answer hai ya nahi
    if not question.answer_text or not question.answer_text.strip():
        return {
            "success": False,
            "score": None,
            "feedback": None,
            "error": "Answer text is empty",
        }
    
    # Step 3: AI se evaluate karwao
    try:
        evaluation = evaluate_answer(
            question=question.question_text,
            answer=question.answer_text,
        )
    except Exception as e:
        return {
            "success": False,
            "score": None,
            "feedback": None,
            "error": f"AI evaluation failed: {str(e)}",
        }
    
    # Step 4: Score aur feedback save karo
    try:
        question.score = evaluation.get("score", 0)
        
        # Feedback combine karo
        feedback_parts = []
        if evaluation.get("strengths"):
            feedback_parts.append(f"Strengths: {evaluation['strengths']}")
        if evaluation.get("weaknesses"):
            feedback_parts.append(f"Weaknesses: {evaluation['weaknesses']}")
        if evaluation.get("improvement_tips"):
            feedback_parts.append(f"Tips: {evaluation['improvement_tips']}")
        
        question.feedback = "\n\n".join(feedback_parts)
        
        db.commit()
        db.refresh(question)
    
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "score": None,
            "feedback": None,
            "error": f"DB save failed: {str(e)}",
        }
    
    # Step 5: Interview ka total score update karo
    update_interview_total_score(question.interview_id, db)
    
    # Step 6: Response return karo
    return {
        "success": True,
        "score": question.score,
        "feedback": question.feedback,
        "details": evaluation,
        "error": None,
    }


# ============================================
# 2. INTERVIEW KA TOTAL SCORE UPDATE KARO
# ============================================

def update_interview_total_score(interview_id: int, db: Session) -> int:
    """
    Interview ke saare questions ka average score calculate karta hai
    aur Interview table mein save karta hai.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        return 0
    
    # Saare scored questions dhoondo
    scored_questions = (
        db.query(Question)
        .filter(Question.interview_id == interview_id)
        .filter(Question.score.isnot(None))
        .all()
    )
    
    if not scored_questions:
        return 0
    
    # Average calculate karo
    total = sum(q.score for q in scored_questions)
    avg_score = int(total / len(scored_questions))
    
    # Update karo
    interview.total_score = avg_score
    db.commit()
    
    return avg_score


# ============================================
# 3. INTERVIEW COMPLETE KARO
# ============================================

def complete_interview(interview_id: int, db: Session) -> dict:
    """
    Interview ko complete mark karta hai aur final score set karta hai.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    
    if not interview:
        return {
            "success": False,
            "error": f"Interview {interview_id} not found",
        }
    
    # Total score update karo
    final_score = update_interview_total_score(interview_id, db)
    
    # Status complete karo
    interview.status = "completed"
    db.commit()
    db.refresh(interview)
    
    return {
        "success": True,
        "interview_id": interview_id,
        "final_score": final_score,
        "status": interview.status,
        "error": None,
    }


# ============================================
# 4. INTERVIEW KI SUMMARY NIKALO
# ============================================

def get_interview_summary(interview_id: int, db: Session) -> dict:
    """
    Interview ki poori summary return karta hai.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    
    if not interview:
        return {"success": False, "error": "Interview not found"}
    
    questions = (
        db.query(Question)
        .filter(Question.interview_id == interview_id)
        .all()
    )
    
    # Stats nikalo
    total_questions = len(questions)
    answered = len([q for q in questions if q.answer_text])
    scored = len([q for q in questions if q.score is not None])
    
    scores = [q.score for q in questions if q.score is not None]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0
    max_score = max(scores) if scores else 0
    min_score = min(scores) if scores else 0
    
    return {
        "success": True,
        "interview_id": interview_id,
        "job_role": interview.job_role,
        "status": interview.status,
        "total_questions": total_questions,
        "answered": answered,
        "scored": scored,
        "average_score": avg_score,
        "max_score": max_score,
        "min_score": min_score,
        "questions": [
            {
                "id": q.id,
                "question": q.question_text,
                "answer": q.answer_text,
                "score": q.score,
                "feedback": q.feedback,
            }
            for q in questions
        ],
        "error": None,
    }