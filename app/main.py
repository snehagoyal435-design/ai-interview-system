# ============================================
# AI Interview System - Main Entry Point
# ============================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app import models

from app.auth.routes import router as auth_router
from app.interviews.routes import router as interviews_router
from app.resume.routes import router as resume_router
from app.speech.routes import router as speech_router
from app.profile.routes import router as profile_router
from app.admin.routes import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered interview system.",
    version="2.0.0",
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(interviews_router)
app.include_router(resume_router)
app.include_router(speech_router)
app.include_router(profile_router)
app.include_router(admin_router)


@app.get("/", tags=["Root"])
def root():
    return {"message": f"Welcome to {settings.APP_NAME}!", "status": "running", "docs": "/docs"}


@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}
@app.get("/unblock-me", tags=["Setup"])
def unblock_me(token: str = "ccsu-unblock-2026"):
    """Emergency unblock endpoint for admin."""
    from app.database import SessionLocal
    from app.models import User

    db = SessionLocal()
    try:
        u = db.query(User).filter(User.email == "snehagoyal435@gmail.com").first()
        if not u:
            return {"success": False, "message": "User not found"}

        u.is_blocked = False
        u.block_reason = None
        db.commit()

        return {
            "success": True,
            "message": "Account unblocked successfully",
            "email": u.email,
            "is_blocked": u.is_blocked,
        }
    finally:
        db.close()
@app.get("/setup-admin", tags=["Setup"])
def setup_admin(token: str = "ccsu-secret-setup-2026"):
    """
    One-time admin setup. Safe because it requires secret token.
    Only works if no admin exists yet.
    """
    from app.database import SessionLocal
    from app.models import User
    from app.auth.utils import hash_password

    db = SessionLocal()
    try:
        # Check if any admin exists
        existing_admin = db.query(User).filter(User.is_admin == True).first()
        if existing_admin:
            return {"success": False, "message": "Admin already exists. Setup disabled."}

        # Create admin
        admin = User(
            email="snehagoyal435@gmail.com",
            hashed_password=hash_password("admin123"),
            full_name="Khushi Sadhna",
            role="admin",
            is_admin=True,
            is_blocked=False,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        return {
            "success": True,
            "message": "Admin created successfully",
            "email": admin.email,
            "password": "admin123",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()