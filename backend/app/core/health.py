"""
app/core/health.py
------------------
Simple, extensible system health check.
Currently validates database connectivity.
"""

from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.core.config import settings
from app.core.database import async_engine
from app.core.logger import logger


async def health_check() -> Dict[str, Any]:
    """Perform system-level health check."""
    checks: Dict[str, Any] = {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "services": {},
    }

    # Database check
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            checks["services"]["database"] = {"status": "healthy"}
    except OperationalError as e:
        checks["status"] = "unhealthy"
        checks["services"]["database"] = {"status": "unhealthy", "error": str(e)}
        logger.error(f"❌ Database unhealthy: {e}")
    except Exception as e:
        checks["status"] = "unhealthy"
        checks["services"]["database"] = {"status": "unhealthy", "error": str(e)}
        logger.error(f"❌ Unexpected DB health check error: {e}")

    logger.info(f"🩺 Health check completed: {checks['status']}")
    return checks
