# ============================================
# AI Interview System - Text to Speech
# ============================================
# Yeh file AI ke text ko awaaz mein convert karti hai.
# Google Text-to-Speech (gTTS) use kar rahe hain.
# ============================================

import os
from gtts import gTTS
from typing import Optional


# ============================================
# 1. OUTPUT FOLDER SETUP
# ============================================

# Audio files yahan save hongi
AUDIO_OUTPUT_DIR = "uploads/audio"


def ensure_audio_dir():
    """Ensure karta hai ki audio folder exist karta hai."""
    os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)


# ============================================
# 2. TEXT TO SPEECH
# ============================================

def text_to_speech(
    text: str,
    output_filename: str,
    language: str = "en",
    slow: bool = False,
) -> dict:
    """
    Text ko audio file mein convert karta hai.
    
    Args:
        text: Jo bolna hai (question, feedback, etc.)
        output_filename: Audio file ka naam (jaise "question_1.mp3")
        language: 'en' for English, 'hi' for Hindi, etc.
        slow: True karo toh dheere bolega
    
    Returns:
        dict with:
        - success: True/False
        - file_path: audio file ka full path
        - error: error message (agar fail ho)
    """
    # Step 1: Text check karo
    if not text or not text.strip():
        return {
            "success": False,
            "file_path": None,
            "error": "Text is empty",
        }
    
    # Step 2: Audio folder banao
    ensure_audio_dir()
    
    # Step 3: Full path banao
    full_path = os.path.join(AUDIO_OUTPUT_DIR, output_filename)
    
    # Step 4: Audio generate karo
    try:
        tts = gTTS(
            text=text,
            lang=language,
            slow=slow,
        )
        tts.save(full_path)
        
        return {
            "success": True,
            "file_path": full_path,
            "error": None,
        }
    
    except Exception as e:
        return {
            "success": False,
            "file_path": None,
            "error": f"TTS failed: {str(e)}",
        }


# ============================================
# 3. QUESTION KO SPEAK KARO (CONVENIENCE)
# ============================================

def speak_question(question_text: str, question_id: int) -> dict:
    """
    Interview question ko audio mein convert karta hai.
    
    Args:
        question_text: Question ka text
        question_id: Question ki ID (file naming ke liye)
    
    Returns:
        dict with success, file_path, error
    """
    filename = f"question_{question_id}.mp3"
    return text_to_speech(question_text, filename)


# ============================================
# 4. FEEDBACK KO SPEAK KARO
# ============================================

def speak_feedback(feedback_text: str, interview_id: int) -> dict:
    """
    Interview feedback ko audio mein convert karta hai.
    
    Args:
        feedback_text: Feedback ka text
        interview_id: Interview ki ID
    
    Returns:
        dict with success, file_path, error
    """
    filename = f"feedback_{interview_id}.mp3"
    return text_to_speech(feedback_text, filename, slow=False)


# ============================================
# 5. AUDIO FILE DELETE KARO
# ============================================

def delete_audio_file(file_path: str) -> bool:
    """
    Audio file delete karta hai (cleanup ke liye).
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"[tts] Failed to delete {file_path}: {e}")
        return False


# ============================================
# 6. SUPPORTED LANGUAGES
# ============================================

def get_supported_languages() -> list:
    """Common supported languages ki list."""
    return [
        {"code": "en", "name": "English"},
        {"code": "hi", "name": "Hindi"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},
        {"code": "ja", "name": "Japanese"},
        {"code": "zh-CN", "name": "Chinese (Simplified)"},
        {"code": "ar", "name": "Arabic"},
    ]