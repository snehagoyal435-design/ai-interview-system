
# ============================================
# AI Interview System - Speech Routes
# ============================================

import os
import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS

from app.auth.utils import get_current_user
from app.models import User


router = APIRouter(prefix="/speech", tags=["Speech"])


class SpeakRequest(BaseModel):
    text: str
    filename: str = "output.mp3"


@router.post("/speak")
async def speak(
    request: SpeakRequest,
    current_user: User = Depends(get_current_user),
):
    """Text ko audio mein convert karta hai — memory mein (no disk)."""
    if not request.text or not request.text.strip():
        raise HTTPException(400, "Text is empty")
    
    try:
        # gTTS se audio generate karo — memory mein
        tts = gTTS(text=request.text, lang="en", slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"inline; filename={request.filename}",
                "Cache-Control": "no-cache",
            },
        )
    
    except Exception as e:
        raise HTTPException(500, f"TTS failed: {str(e)}")


@router.post("/transcribe", response_model=dict)
async def transcribe(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Audio file ko text mein convert karta hai."""
    try:
        from app.speech.stt import transcribe_audio
    except Exception as e:
        raise HTTPException(
            503,
            f"Speech-to-text is not available on this server. "
            f"This feature works only locally. Error: {str(e)}"
        )
    
    # Save uploaded file temporarily
    upload_dir = "/tmp/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    safe_name = f"user_{current_user.id}_{file.filename}"
    file_path = os.path.join(upload_dir, safe_name)
    
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(500, f"Failed to save audio: {str(e)}")
    
    # Transcribe
    result = transcribe_audio(file_path)
    
    # Cleanup
    try:
        os.remove(file_path)
    except:
        pass
    
    if not result.get("success"):
        raise HTTPException(500, result.get("error", "Transcription failed"))
    
    return {
        "success": True,
        "text": result["text"],
        "language": result.get("language", "unknown"),
    }