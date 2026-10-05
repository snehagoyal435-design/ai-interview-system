# ============================================
# AI Interview System - Auth Routes
# ============================================

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime

from app.database import get_db
from app.models import User, Activity
from app.schemas import UserCreate, UserResponse, Token
from app.auth.utils import (
    hash_password, verify_password, create_access_token, get_current_user,
)
from app.config import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")

    hashed = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed,
        full_name=user_data.full_name,
        role=user_data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Log activity
    activity = Activity(user_id=new_user.id, action="signup", details="New user registered")
    db.add(activity)
    db.commit()

    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(401, "Invalid email or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")

    # Update last login
    user.last_login = datetime.utcnow()
    activity = Activity(user_id=user.id, action="login", details="User logged in")
    db.add(activity)
    db.commit()

    token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user