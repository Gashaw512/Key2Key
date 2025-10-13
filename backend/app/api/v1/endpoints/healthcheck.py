# app/api/v1/endpoints/healthcheck.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text # Use text() for clean, simple query

from app.db.session import get_db 
from app.core.config import settings

router = APIRouter()

@router.get("/health", tags=["Status"], summary="Check API Status")
async def check_api_status():
    """Returns the API status and project details."""
    return {
        "status": "ok", 
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "detail": "See /api/v1/db-health for database connectivity."
    }

@router.get("/db-health", tags=["Status"], summary="Check Database Connection Status")
async def check_db_connection(db: AsyncSession = Depends(get_db)):
    """
    Tests the database connection by executing a simple SELECT 1 query.
    """
    try:
        # Execute a lightweight query to verify the connection
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Database connection successful."}
    except Exception as e:
        # If the connection fails, raise a 503 Service Unavailable
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed. Details: {e}"
        )