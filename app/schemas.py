# ============================================
# AI Interview System - Pydantic Schemas
# ============================================

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


# ---- USER ----
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    role: str = "candidate"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: str
    is_admin: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# ---- TOKEN ----
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---- PROFILE ----
class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    status: Optional[str] = "Student"
    education: Optional[str] = None
    target_role: Optional[str] = None
    experience_years: Optional[int] = 0
    skills: Optional[str] = ""
    bio: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    status: str
    education: Optional[str]
    target_role: Optional[str]
    experience_years: int
    skills: str
    bio: Optional[str]
    updated_at: datetime

    class Config:
        from_attributes = True


# ---- INTERVIEW ----
class InterviewCreate(BaseModel):
    job_role: str = Field(..., min_length=2)
    skills: Optional[List[str]] = []
    difficulty: Optional[str] = "medium"


class InterviewResponse(BaseModel):
    id: int
    user_id: int
    job_role: str
    status: str
    total_score: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---- QUESTION ----
class QuestionResponse(BaseModel):
    id: int
    interview_id: int
    question_text: str
    answer_text: Optional[str] = None
    score: Optional[int] = None
    feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnswerSubmit(BaseModel):
    question_id: int
    answer_text: str = Field(..., min_length=1)


# ---- EVALUATION ----
class EvaluationResponse(BaseModel):
    score: int
    technical_accuracy: int
    clarity: int
    strengths: str
    weaknesses: str
    improvement_tips: str


# ---- SPEECH ----
class SpeakRequest(BaseModel):
    text: str
    filename: str = "output.mp3"


# ---- RESUME ----
class ResumeParseResponse(BaseModel):
    skills: List[str]
    experience_years: Optional[int] = None
    summary: Optional[str] = None


# ---- ADMIN ----
class AdminUserInfo(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: str
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime]
    total_interviews: int
    avg_score: float
    total_activities: int