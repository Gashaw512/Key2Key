# app/core/auth.py
"""
Authentication utilities for Key2Key API
JWT token generation, verification, and FastAPI dependencies.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.security import pwd_context, verify_password
from app.core.config import settings  # You'll need this config
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import user_service
from app.core.logger import logger

# JWT Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10030  # Short-lived access token

# Security scheme for FastAPI
security = HTTPBearer(
    scheme_name="JWT",
    description="JWT Authorization header using the Bearer scheme.",
    auto_error=False  # We'll handle errors manually
)

class TokenData(BaseModel):
    """Token payload data."""
    sub: Optional[str] = None  # User ID
    email: Optional[str] = None

class UserAuth(BaseModel):
    """Authenticated user response."""
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool

async def authenticate_user(
    db: AsyncSession, 
    email: str, 
    password: str
) -> Optional[User]:
    """Authenticate user credentials."""
    user = await user_service.get_user_by_email(db, email)
    if not user:
        logger.warning(f"Auth attempt failed - user not found: {email}")
        return None
    
    if not user.verified:
        logger.warning(f"Auth attempt failed - user not verified: {email}")
        return None
    
    if not verify_password(password, user.password_hash):
        logger.warning(f"Auth attempt failed - invalid password: {email}")
        return None
    
    logger.info(f"User authenticated: {email}")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not credentials:
        raise credentials_exception
    
    try:
        # Decode JWT
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        token_data = TokenData(**payload)
        
        if not token_data.sub:
            raise credentials_exception
        
    except JWTError:
        logger.warning(f"Invalid JWT token")
        raise credentials_exception
    
    # Get user from database
    user = await user_service.get_user_by_id(db, token_data.sub)
    if not user:
        logger.warning(f"Token user not found: {token_data.sub}")
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user is active."""
    if not current_user.verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# Utility functions
def verify_token(token: str) -> dict:
    """Verify JWT token without database access."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return {}

async def login_user(db: AsyncSession, email: str, password: str):
    """Login user and return tokens."""
    user = await authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserAuth(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.verified
        )
    }