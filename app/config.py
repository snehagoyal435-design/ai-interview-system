# ============================================
# AI Interview System - Configuration
# ============================================
# Yeh file .env file se saari settings padhti hai
# aur ek jagah par rakh deti hai.
# ============================================

import os
from dotenv import load_dotenv

# .env file load karo (project ke root se)
load_dotenv()


class Settings:
    """Saari settings ek class mein."""
    
    # ---- App Info ----
    APP_NAME: str = os.getenv("APP_NAME", "AI Interview System")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # ---- Security ----
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )
    
    # ---- Database ----
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./interview.db")
    
    # ---- AI (Gemini) ----
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")


# Ek single instance banao — pure project mein use hoga
settings = Settings()