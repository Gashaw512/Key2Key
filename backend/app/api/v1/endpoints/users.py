# app/api/v1/endpoints/users.py
"""
Users API Endpoint (Production-Ready)
Handles CRUD operations with validation, authentication, and pagination.
"""

from typing import List, Optional
from fastapi import (
    APIRouter, Depends, HTTPException, Query, Response, status
)
from pydantic import UUID4
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_db
from app.models.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import user_service
from app.core.logger import logger
from app.core.auth import get_current_active_user

router = APIRouter(
    tags=["users"],
    responses={
        404: {"description": "User not found"},
        400: {"description": "Invalid input"},
        409: {"description": "Conflict (duplicate email)"}
    }
)

# --------------------------------------------------------------------------
# 🧩 PUBLIC ENDPOINTS
# --------------------------------------------------------------------------

@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user account"
)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user with hashed password and unique email."""
    try:
        return await user_service.create_user(db, user_in)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating user {user_in.email}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during user creation"
        )

@router.post("/verify_user/{user_id}", summary="Manually verify user (dev only)")
async def verify_user(user_id: UUID4, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.verified = True
    await db.commit()
    return {"status": "verified"}

# --------------------------------------------------------------------------
# 🔐 AUTHENTICATED USER ENDPOINTS
# --------------------------------------------------------------------------

@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user profile"
)
async def get_current_user_profile(
    current_user: UserRead = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Return the authenticated user's profile (with relations)."""
    user = await user_service.get_user_by_id(db, current_user.id, include_relations=True)
    return user

# --------------------------------------------------------------------------
# 👥 ADMIN & GENERAL USER MANAGEMENT
# --------------------------------------------------------------------------

@router.get(
    "/",
    response_model=List[UserRead],
    summary="List all users (Admin)"
)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    role: Optional[str] = Query(None),
    verified: Optional[bool] = Query(None),
    email_contains: Optional[str] = Query(None),
    sort_by: str = Query("created_at", regex="^(created_at|email|full_name)$"),
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_active_user)
):
    """List users with pagination, filtering, and sorting (admin access)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    try:
        users = await user_service.get_users_paginated(
            db, skip, limit, role, verified, email_contains, sort_by
        )
        logger.info(f"Admin retrieved {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

@router.get(
    "/count",
    summary="Get total user count"
)
async def get_user_count(
    role: Optional[str] = Query(None),
    verified: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Return total user count with optional filters."""
    try:
        count = await user_service.get_user_count(db, role, verified)
        return {"total": count}
    except Exception as e:
        logger.error(f"Error counting users: {e}")
        raise HTTPException(status_code=500, detail="Failed to count users")

# --------------------------------------------------------------------------
# 🔍 SINGLE USER OPERATIONS
# --------------------------------------------------------------------------

@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get user by ID"
)
async def get_user_by_id(
    user_id: UUID4,
    include_relations: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.get_user_by_id(db, user_id, include_relations)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch(
    "/{user_id}",
    response_model=UserRead,
    summary="Update user details"
)
async def update_user(
    user_id: UUID4,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_user = await user_service.update_user(db, user_id, user_in)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user account"
)
async def delete_user(
    user_id: UUID4,
    db: AsyncSession = Depends(get_db)
):
    success = await user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)

# --------------------------------------------------------------------------
# 📊 STATS & SEARCH
# --------------------------------------------------------------------------

@router.get("/{user_id}/stats", summary="Get user statistics")
async def get_user_stats(user_id: UUID4, db: AsyncSession = Depends(get_db)):
    return await user_service.get_user_stats(db, user_id)

@router.get("/search", response_model=List[UserRead])
async def search_users(
    query: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    if len(query) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters long.")
    return await user_service.search_users(db, query, skip, limit)
