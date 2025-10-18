"""
app/api/v1/endpoints/healthcheck.py
-----------------------------------
System health endpoints for API and database connectivity.
Provides lightweight checks for monitoring and diagnostics.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text
from typing import Dict, Any

from app.db.session import get_db
from app.core.config import settings
from app.core.health import health_check as system_health_check
from app.core.logger import logger

router = APIRouter()


@router.get(
    "/health",
    tags=["System"],
    summary="Check API Status",
    description="Basic API health endpoint. Returns project info and API status."
)
async def check_api_status() -> Dict[str, Any]:
    """
    Returns the API service status and version.
    Does not perform DB connectivity checks.
    """
    logger.debug("API status check requested")
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "detail": "For database connectivity, see /api/v1/health/db"
    }


@router.get(
    "/health/db",
    tags=["System"],
    summary="Check Database Connection",
    description="Performs a lightweight database connectivity test."
)
async def check_db_connection(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Verifies database connectivity using a simple `SELECT 1` query.
    Returns 200 OK if successful, 503 Service Unavailable if failed.
    """
    try:
        await db.execute(text("SELECT 1"))
        logger.info("✅ Database connection verified via /health/db")
        return {"status": "ok", "message": "Database connection successful."}
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed. See logs for details."
        )


@router.get(
    "/health/system",
    tags=["System"],
    summary="Comprehensive System Health Check",
    description="Runs a full health check including database and other future services."
)
async def check_full_system_health() -> Dict[str, Any]:
    """
    Returns detailed system health using `app.core.health.health_check`.
    Extensible to include Redis, cache, external APIs, or other services.
    """
    try:
        health_status = await system_health_check()
        logger.info("🩺 Full system health check completed")
        return health_status
    except Exception as e:
        logger.critical(f"💥 Full system health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="System health check failed. See logs for details."
        )
