# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_db
from app.core.auth import login_user

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=dict)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return JWT token."""
    tokens = await login_user(db, request.email, request.password)
    return tokens

@router.post("/logout")
async def logout():
    """Logout (client-side token invalidation)."""
    return {"message": "Logged out successfully"}