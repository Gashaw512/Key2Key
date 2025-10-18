# app/api/v1/endpoints/broker.py
"""
BrokerProfile API Endpoints - Production Ready
CRUD for broker profiles linked to users.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from pydantic import UUID4
from starlette.responses import Response

from app.db.session import get_db
from app.models.broker import (
    BrokerProfileCreate, BrokerProfileRead, BrokerProfileUpdate
)
from app.services.broker_service import broker_service
from app.core.logger import logger

router = APIRouter(
    prefix="/brokers",
    tags=["brokers"],
    responses={
        404: {"description": "Broker profile not found"},
        409: {"description": "User already has broker profile"}
    }
)

@router.post(
    "/", 
    response_model=BrokerProfileRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Create Broker Profile"
)
async def create_broker_profile(
    broker_create: BrokerProfileCreate,
    user_id: UUID4,  # From authenticated user or path param
    db: AsyncSession = Depends(get_db)
):
    """Create broker profile for existing user."""
    try:
        broker = await broker_service.create_broker_profile(db, broker_create, user_id)
        logger.info(f"Broker profile created for user {user_id}")
        return broker
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Broker creation failed: {e}")
        raise HTTPException(status_code=500, detail="Internal error")

@router.get(
    "/{broker_id}", 
    response_model=BrokerProfileRead,
    summary="Get Broker Profile by ID"
)
async def get_broker_profile(
    broker_id: UUID4,
    db: AsyncSession = Depends(get_db)
):
    """Get broker profile by ID."""
    broker = await broker_service.get_broker_by_id(db, broker_id)
    if not broker:
        raise HTTPException(status_code=404, detail="Broker profile not found")
    return broker

@router.get(
    "/user/{user_id}", 
    response_model=BrokerProfileRead,
    summary="Get Broker Profile by User ID"
)
async def get_broker_by_user(
    user_id: UUID4,
    db: AsyncSession = Depends(get_db)
):
    """Get broker profile linked to specific user."""
    broker = await broker_service.get_by_user_id(db, user_id)
    if not broker:
        raise HTTPException(status_code=404, detail="No broker profile for this user")
    return broker

@router.patch(
    "/{broker_id}", 
    response_model=BrokerProfileRead,
    summary="Update Broker Profile"
)
async def update_broker_profile(
    broker_id: UUID4,
    broker_update: BrokerProfileUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update broker profile details."""
    updated = await broker_service.update_broker_profile(db, broker_id, broker_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Broker profile not found")
    logger.info(f"Broker profile updated: {broker_id}")
    return updated

@router.delete(
    "/{broker_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Broker Profile"
)
async def delete_broker_profile(
    broker_id: UUID4,
    db: AsyncSession = Depends(get_db)
):
    """Delete broker profile (user remains)."""
    success = await broker_service.delete_broker_profile(db, broker_id)
    if not success:
        raise HTTPException(status_code=404, detail="Broker profile not found")
    logger.warning(f"Broker profile deleted: {broker_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get(
    "/", 
    response_model=List[BrokerProfileRead],
    summary="List Broker Profiles"
)
async def list_broker_profiles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_verified: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List broker profiles with pagination and filtering."""
    brokers = await broker_service.list_broker_profiles(db, skip, limit, is_verified)
    logger.info(f"Listed {len(brokers)} broker profiles")
    return brokers

@router.get("/count", summary="Broker Count")
async def get_broker_count(
    is_verified: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get total broker count."""
    count = await broker_service.get_broker_count(db, is_verified)
    return {"total": count}