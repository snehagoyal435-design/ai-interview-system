# ============================================
# AI Interview System - Admin Routes
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.database import get_db
from app.models import User, Interview, Profile, Activity, Question
from app.auth.utils import get_current_user
from app.schemas import BlockUserRequest


router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin and current_user.role != "admin":
        raise HTTPException(403, "Admin access required")
    return current_user


@router.get("/users", response_model=dict)
def list_users(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    users = db.query(User).order_by(User.created_at.desc()).all()

    result = []
    for u in users:
        interviews = db.query(Interview).filter(Interview.user_id == u.id).all()
        scores = [i.total_score for i in interviews if i.total_score]
        avg = round(sum(scores) / len(scores), 1) if scores else 0

        acts = db.query(Activity).filter(Activity.user_id == u.id).count()
        profile = db.query(Profile).filter(Profile.user_id == u.id).first()

        result.append({
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_admin": u.is_admin,
            "is_blocked": u.is_blocked,
            "block_reason": u.block_reason,
            "created_at": u.created_at,
            "last_login": u.last_login,
            "total_interviews": len(interviews),
            "avg_score": avg,
            "total_activities": acts,
            "target_role": profile.target_role if profile else None,
        })

    return {"success": True, "total": len(result), "users": result}


@router.get("/stats", response_model=dict)
def global_stats(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    total_users = db.query(User).count()
    blocked_users = db.query(User).filter(User.is_blocked == True).count()
    total_interviews = db.query(Interview).count()
    completed_interviews = db.query(Interview).filter(Interview.status == "completed").count()

    scores = [i.total_score for i in db.query(Interview).filter(Interview.total_score > 0).all()]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    today = datetime.utcnow().date()
    logins_today = db.query(Activity).filter(
        Activity.action == "login",
        func.date(Activity.timestamp) == today,
    ).count()

    return {
        "success": True,
        "total_users": total_users,
        "blocked_users": blocked_users,
        "total_interviews": total_interviews,
        "completed_interviews": completed_interviews,
        "average_score": avg_score,
        "logins_today": logins_today,
    }


@router.get("/user/{user_id}", response_model=dict)
def user_detail(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    interviews = db.query(Interview).filter(Interview.user_id == user_id).order_by(Interview.created_at.desc()).all()
    activities = db.query(Activity).filter(Activity.user_id == user_id).order_by(Activity.timestamp.desc()).limit(100).all()

    # Detailed interviews with questions
    interviews_detail = []
    for iv in interviews:
        questions = db.query(Question).filter(Question.interview_id == iv.id).all()
        interviews_detail.append({
            "id": iv.id,
            "job_role": iv.job_role,
            "status": iv.status,
            "total_score": iv.total_score,
            "created_at": iv.created_at.isoformat() if iv.created_at else None,
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
        })

    return {
        "success": True,
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_admin": user.is_admin,
            "is_blocked": user.is_blocked,
            "block_reason": user.block_reason,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
        },
        "profile": {
            "status": profile.status,
            "education": profile.education,
            "target_role": profile.target_role,
            "experience_years": profile.experience_years,
            "skills": profile.skills,
            "bio": profile.bio,
        } if profile else None,
        "interviews": interviews_detail,
        "activities": [
            {
                "action": a.action,
                "details": a.details,
                "timestamp": a.timestamp.isoformat() if a.timestamp else None,
            }
            for a in activities
        ],
    }


@router.post("/user/{user_id}/block", response_model=dict)
def block_user(
    user_id: int,
    data: BlockUserRequest,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == admin.id:
        raise HTTPException(400, "Cannot block yourself")

    user.is_blocked = True
    user.block_reason = data.reason or "Violation of terms"
    db.commit()

    db.add(Activity(
        user_id=admin.id,
        action="block_user",
        details=f"Blocked user {user.email}: {user.block_reason}"
    ))
    db.commit()

    return {"success": True, "message": f"User {user.email} blocked"}


@router.post("/user/{user_id}/unblock", response_model=dict)
def unblock_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    user.is_blocked = False
    user.block_reason = None
    db.commit()

    db.add(Activity(
        user_id=admin.id,
        action="unblock_user",
        details=f"Unblocked user {user.email}"
    ))
    db.commit()

    return {"success": True, "message": f"User {user.email} unblocked"}


@router.delete("/user/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.id == admin.id:
        raise HTTPException(400, "Cannot delete yourself")

    email = user.email
    db.delete(user)
    db.commit()

    db.add(Activity(
        user_id=admin.id,
        action="delete_user",
        details=f"Deleted user {email}"
    ))
    db.commit()

    return {"success": True, "message": f"User {email} deleted"}


@router.post("/make-admin/{user_id}", response_model=dict)
def make_admin(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    user.is_admin = True
    user.role = "admin"
    db.commit()

    return {"success": True, "message": f"{user.email} is now admin"}