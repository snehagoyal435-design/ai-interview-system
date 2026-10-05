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