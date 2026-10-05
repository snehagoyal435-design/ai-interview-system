# ============================================
# AI Interview System - Speech Routes
# ============================================

import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.auth.utils import get_current_user
from app.models import User
# Lazy imports — only load when actually needed
def _get_stt():
    try:
        from app.speech.stt import transcribe_audio
        return transcribe_audio
    except Exception as e:
        print(f"[speech] STT unavailable: {e}")
        return None

def _get_tts():
    try:
        from app.speech.tts import text_to_speech
        return text_to_speech
    except Exception as e:
        print(f"[speech] TTS unavailable: {e}")
        return None


router = APIRouter(prefix="/speech", tags=["Speech"])


UPLOAD_DIR = "uploads/audio"


class SpeakRequest(BaseModel):
    text: str
    filename: str = "output.mp3"


@router.post("/transcribe", response_model=dict)
async def transcribe(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Audio file ko text mein convert karta hai."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe_name = f"user_{current_user.id}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, safe_name)
    
    try:
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(500, f"Save failed: {e}")
    
    result = transcribe_audio(path)
    
    if not result["success"]:
        raise HTTPException(500, result.get("error", "Transcription failed"))
    
    return {
        "success": True,
        "text": result["text"],
        "language": result.get("language", "unknown"),
    }


@router.post("/speak")
async def speak(
    request: SpeakRequest,
    current_user: User = Depends(get_current_user),
):
    """Text ko audio mein convert karta hai."""
    result = text_to_speech(request.text, request.filename)
    
    if not result["success"]:
        raise HTTPException(500, result.get("error", "TTS failed"))
    
    return FileResponse(
        result["file_path"],
        media_type="audio/mpeg",
        filename=request.filename,
    )