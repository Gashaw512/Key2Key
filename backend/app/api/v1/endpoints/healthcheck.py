# app/api/v1/endpoints/healthcheck.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db # Import the dependency
from app.core.config import settings

router = APIRouter()

@router.get("/health", tags=["Health"], summary="Check API Status")
def check_api_status():
    """Returns the API status and project details."""
    return {
        "status": "ok", 
        "service": settings.PROJECT_NAME,
        "version": "v1.0.0",
        "database_status": "untested (see /db-health for connection check)"
    }

@router.get("/db-health", tags=["Health"], summary="Check Database Connection Status")
def check_db_connection(db: Session = Depends(get_db)):
    """
    Attempts a simple database query to verify connection status.
    Uses the get_db dependency.
    """
    try:
        # Attempt a simple query (e.g., SELECT 1)
        db.execute("SELECT 1")
        return {"status": "ok", "message": "Database connection successful."}
    except Exception as e:
        # If the connection fails, raise a 503 Service Unavailable error
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed. Details: {e}"
        )