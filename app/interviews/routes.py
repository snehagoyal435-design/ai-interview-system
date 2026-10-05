# ============================================
# AI Interview System - Interview Routes
# ============================================

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, Interview, Question, Profile, Activity
from app.schemas import (
    InterviewCreate,
    InterviewResponse,
    QuestionResponse,
    AnswerSubmit,
)
from app.auth.utils import get_current_user
from app.interviews.ai_engine import generate_questions
from app.evaluation.scorer import score_answer, complete_interview, get_interview_summary
from app.evaluation.report import generate_pdf_report


# ✅ YEH LINE ZAROORI HAI!
router = APIRouter(prefix="/interviews", tags=["Interviews"])


# ============================================
# 1. START NEW INTERVIEW
# ============================================

@router.post("/start", response_model=dict, status_code=status.HTTP_201_CREATED)
def start_interview(
    interview_data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Start new interview. Uses profile skills if none provided."""
    # Get profile for default skills
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()

    # Use provided skills OR profile skills
    skills = interview_data.skills
    if not skills or len(skills) == 0:
        if profile and profile.skills:
            skills = [s.strip() for s in profile.skills.split(",") if s.strip()]

    # Create interview
    interview = Interview(
        user_id=current_user.id,
        job_role=interview_data.job_role,
        status="in_progress",
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)

    # Generate questions
    try:
        questions_list = generate_questions(
            job_role=interview_data.job_role,
            skills=skills or [],
            num_questions=5,
            difficulty=interview_data.difficulty or "medium",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Failed to generate questions: {str(e)}")

    for q_text in questions_list:
        db.add(Question(interview_id=interview.id, question_text=q_text))
    db.commit()

    # Log activity
    db.add(Activity(user_id=current_user.id, action="interview_start",
                    details=f"Started {interview_data.job_role} interview"))
    db.commit()

    questions = db.query(Question).filter(Question.interview_id == interview.id).all()

    return {
        "success": True,
        "interview_id": interview.id,
        "job_role": interview.job_role,
        "status": interview.status,
        "total_questions": len(questions),
        "skills_used": skills,
        "questions": [
            {"id": q.id, "question_text": q.question_text,
             "answer_text": q.answer_text, "score": q.score}
            for q in questions
        ],
    }


# ============================================
# 2. GET INTERVIEW DETAILS
# ============================================

@router.get("/{interview_id}", response_model=dict)
def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()

    if not interview:
        raise HTTPException(404, "Interview not found")
    if interview.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    questions = db.query(Question).filter(Question.interview_id == interview_id).all()

    return {
        "success": True,
        "interview": {
            "id": interview.id,
            "job_role": interview.job_role,
            "status": interview.status,
            "total_score": interview.total_score,
            "created_at": interview.created_at,
        },
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "answer_text": q.answer_text,
                "score": q.score,
                "feedback": q.feedback,
            }
            for q in questions
        ],
    }


# ============================================
# 3. SUBMIT ANSWER
# ============================================

@router.post("/{interview_id}/answer", response_model=dict)
def submit_answer(
    interview_id: int,
    answer_data: AnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(404, "Interview not found")
    if interview.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    question = (
        db.query(Question)
        .filter(
            Question.id == answer_data.question_id,
            Question.interview_id == interview_id,
        )
        .first()
    )
    if not question:
        raise HTTPException(404, "Question not found")

    question.answer_text = answer_data.answer_text
    db.commit()
    db.refresh(question)

    result = score_answer(question.id, db)

    if not result["success"]:
        raise HTTPException(500, result["error"])

    return {
        "success": True,
        "question_id": question.id,
        "score": result["score"],
        "feedback": result["feedback"],
        "details": result.get("details"),
    }


# ============================================
# 4. COMPLETE INTERVIEW
# ============================================

@router.post("/{interview_id}/complete", response_model=dict)
def finish_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()

    if not interview:
        raise HTTPException(404, "Interview not found")
    if interview.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    result = complete_interview(interview_id, db)

    if not result["success"]:
        raise HTTPException(500, result["error"])

    return result


# ============================================
# 5. INTERVIEW SUMMARY
# ============================================

@router.get("/{interview_id}/summary", response_model=dict)
def interview_summary(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()

    if not interview:
        raise HTTPException(404, "Interview not found")
    if interview.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    return get_interview_summary(interview_id, db)


# ============================================
# 6. DOWNLOAD PDF REPORT
# ============================================

@router.get("/{interview_id}/report")
def download_report(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = db.query(Interview).filter(Interview.id == interview_id).first()

    if not interview:
        raise HTTPException(404, "Interview not found")
    if interview.user_id != current_user.id:
        raise HTTPException(403, "Not authorized")

    result = generate_pdf_report(interview_id, db)

    if not result["success"]:
        raise HTTPException(500, result["error"])

    return FileResponse(
        result["file_path"],
        media_type="application/pdf",
        filename=f"interview_report_{interview_id}.pdf",
    )


# ============================================
# 7. LIST MY INTERVIEWS
# ============================================

@router.get("/", response_model=dict)
def list_my_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interviews = (
        db.query(Interview)
        .filter(Interview.user_id == current_user.id)
        .order_by(Interview.created_at.desc())
        .all()
    )

    return {
        "success": True,
        "total": len(interviews),
        "interviews": [
            {
                "id": i.id,
                "job_role": i.job_role,
                "status": i.status,
                "total_score": i.total_score,
                "created_at": i.created_at,
            }
            for i in interviews
        ],
    }