# ============================================
# AI Interview System - Auth Utilities
# ============================================
# Yeh file password hashing aur JWT tokens handle karti hai.
# ============================================

from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db


# ============================================
# 1. PASSWORD HASHING SETUP
# ============================================

# bcrypt algorithm use kar rahe hain (secure hai)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Plain password ko hash karke return karta hai.
    Signup ke time use hoga.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check karta hai ki plain password hashed password se match karta hai ya nahi.
    Login ke time use hoga.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================
# 2. JWT TOKEN SETUP
# ============================================

# OAuth2 scheme — FastAPI ko batata hai token kahan se aayega
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT token banata hai.
    Login ke baad user ko yeh token milega.
    """
    to_encode = data.copy()
    
    # Expiry set karo
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    
    # Token encode karo
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Token ko decode karta hai.
    Valid hai toh data return karega, warna None.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


# ============================================
# 3. CURRENT USER NIKALNA
# ============================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Token se current user nikaltа hai.
    Har protected route mein use hoga.
    """
    # Import yahan kiya — circular import se bachne ke liye
    from app.models import User
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Token decode karo
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Email nikalo
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    # Database se user dhoondo
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user