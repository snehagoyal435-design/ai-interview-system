# ============================================
# AI Interview System - Speech to Text
# ============================================
# Yeh file user ki awaaz ko text mein convert karti hai.
# OpenAI Whisper model use kar rahe hain.
# ============================================

# ============================================
# AI Interview System - Speech to Text
# ============================================
# Yeh file user ki awaaz ko text mein convert karti hai.
# OpenAI Whisper model use kar rahe hain.
# ============================================

import os
import whisper
import imageio_ffmpeg
from typing import Optional

# FFmpeg ko Whisper ke liye available karo
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())


# ============================================
# 1. WHISPER MODEL LOAD (LAZY LOADING)
# ============================================

_model = None  # Global variable — ek baar load hoga


def load_whisper_model(model_size: str = "base"):
    """
    Whisper model load karta hai (ek baar).
    """
    global _model
    
    if _model is None:
        print(f"[stt] Loading Whisper model '{model_size}'... (pehli baar download hoga)")
        _model = whisper.load_model(model_size)
        print(f"[stt] Whisper model '{model_size}' loaded successfully!")
    
    return _model


# ============================================
# 2. AUDIO FILE KO TEXT MEIN CONVERT KARO
# ============================================

def transcribe_audio(audio_path: str, language: Optional[str] = None) -> dict:
    """
    Audio file ko text mein convert karta hai.
    """
    # Step 1: Check file exist karti hai
    if not os.path.exists(audio_path):
        return {
            "text": "",
            "language": None,
            "success": False,
            "error": f"Audio file not found: {audio_path}",
        }
    
    # Step 2: File extension check karo
    valid_extensions = [".mp3", ".wav", ".webm", ".m4a", ".ogg", ".flac"]
    ext = os.path.splitext(audio_path)[1].lower()
    
    if ext not in valid_extensions:
        return {
            "text": "",
            "language": None,
            "success": False,
            "error": f"Unsupported audio format: {ext}. Supported: {valid_extensions}",
        }
    
    # Step 3: Model load karo
    try:
        model = load_whisper_model("base")
    except Exception as e:
        return {
            "text": "",
            "language": None,
            "success": False,
            "error": f"Model loading failed: {str(e)}",
        }
    
    # Step 4: FFmpeg path set karo
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_exe)
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
    
    # Step 5: Transcribe karo
    try:
        result = model.transcribe(
            audio_path,
            language=language,
            fp16=False,
            verbose=False,
        )
        
        return {
            "text": result.get("text", "").strip(),
            "language": result.get("language", "unknown"),
            "success": True,
            "error": None,
        }
    
    except Exception as e:
        return {
            "text": "",
            "language": None,
            "success": False,
            "error": f"Transcription failed: {str(e)}",
        }


# ============================================
# 3. HELPER — SUPPORTED FORMATS
# ============================================

def get_supported_formats() -> list:
    """Supported audio formats ki list."""
    return [".mp3", ".wav", ".webm", ".m4a", ".ogg", ".flac"]