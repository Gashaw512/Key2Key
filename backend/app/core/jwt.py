# app/core/jwt.py

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from fastapi import HTTPException, status

from app.core.config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default to the configured expiration time
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiration time to the payload
    to_encode.update({"exp": expire, "sub": "access"})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decodes and validates a JWT access token.
    Raises HTTPException on failure.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        # This catches token errors like signature verification failure or malformed tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or token signature",
            headers={"WWW-Authenticate": "Bearer"},
        )