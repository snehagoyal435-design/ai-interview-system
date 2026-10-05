# ============================================
# AI Interview System - Database Connection
# ============================================
# Yeh file database se connection banati hai.
# SQLAlchemy use kar rahe hain SQLite ke saath.
# ============================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


# ---- 1. Engine Banao (Database Se Connection) ----
# Engine database ka "driver" hai — saara communication isse hota hai
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite ke liye zaroori
)


# ---- 2. Session Banao (Har Request Ke Liye Temporary Connection) ----
# SessionLocal ek "factory" hai jo naye sessions banata hai
SessionLocal = sessionmaker(
    autocommit=False,   # Manual commit karenge
    autoflush=False,    # Manual flush karenge
    bind=engine         # Is engine se connected
)


# ---- 3. Base Class Banao (Models Ke Liye Parent Class) ----
# Saare database models is Base se inherit karenge
Base = declarative_base()


# ---- 4. Dependency Function (FastAPI Routes Ke Liye) ----
def get_db():
    """
    FastAPI route ko database session deta hai.
    Kaam khatam hone par automatically band kar deta hai.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()