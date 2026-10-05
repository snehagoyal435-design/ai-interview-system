# ============================================
# AI Interview System - Profile Routes
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Profile, Activity
from app.schemas import ProfileUpdate, ProfileResponse
from app.auth.utils import get_current_user


router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me", response_model=dict)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        return {"success": True, "exists": False, "profile": None}

    return {
        "success": True,
        "exists": True,
        "profile": {
            "id": profile.id,
            "user_id": profile.user_id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "status": profile.status,
            "education": profile.education,
            "target_role": profile.target_role,
            "experience_years": profile.experience_years,
            "skills": profile.skills.split(",") if profile.skills else [],
            "bio": profile.bio,
            "updated_at": profile.updated_at,
        },
    }


@router.post("/me", response_model=dict)
def upsert_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()

    is_new = False
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)
        is_new = True

    profile.status = data.status or "Student"
    profile.education = data.education
    profile.target_role = data.target_role
    profile.experience_years = data.experience_years or 0
    profile.skills = data.skills or ""
    profile.bio = data.bio

    if data.full_name:
        current_user.full_name = data.full_name

    db.commit()
    db.refresh(profile)

    activity = Activity(
        user_id=current_user.id,
        action="profile_update" if not is_new else "profile_create",
        details=f"Profile {'updated' if not is_new else 'created'}",
    )
    db.add(activity)
    db.commit()

    return {"success": True, "message": "Profile saved", "is_new": is_new}