# ============================================
# AI Interview System - Resume Routes
# ============================================
# Yeh file resume upload karne ka API banati hai.
# ============================================

import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.utils import get_current_user
from app.resume.parser import safe_parse_resume
from app.schemas import ResumeParseResponse


router = APIRouter(prefix="/resume", tags=["Resume"])


# ============================================
# 1. UPLOAD FOLDER SETUP
# ============================================

UPLOAD_DIR = "uploads/resumes"


def ensure_upload_dir():
    """Uploads folder banao agar nahi hai."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============================================
# 2. RESUME UPLOAD ENDPOINT
# ============================================

@router.post("/upload", response_model=dict)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Resume PDF upload karta hai aur skills extract karta hai.
    """
    # Step 1: File type check karo
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided",
        )
    
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )
    
    # Step 2: Upload folder banao
    ensure_upload_dir()
    
    # Step 3: File save karo (unique naam se)
    safe_filename = f"user_{current_user.id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )
    
    # Step 4: Resume parse karo
    try:
        parsed = safe_parse_resume(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse resume: {str(e)}",
        )
    
    # Step 5: Response return karo
    return {
        "success": True,
        "filename": file.filename,
        "saved_as": safe_filename,
        "file_path": file_path,
        "skills": parsed.get("skills", []),
        "experience_years": parsed.get("experience_years", 0),
        "summary": parsed.get("summary", ""),
    }


# ============================================
# 3. SUPPORTED FORMATS
# ============================================

@router.get("/supported-formats", response_model=dict)
def get_supported_formats():
    """Supported resume formats ki list."""
    return {
        "formats": [".pdf"],
        "max_size_mb": 5,
        "note": "Only PDF files are supported for now",
    }