# app/core/lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel 
from app.core.config import settings
from app.core.database import async_engine
from app.core.logger import logger # Use the logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown events."""
    logger.info(f"[{settings.PROJECT_NAME}] Application Startup...")
    
    # 1. Database Table Creation (Development/Testing only)
    try:
        logger.info("Verifying database schema...")
        async with async_engine.begin() as conn:
            # Create tables only if they don't exist
            await conn.run_sync(SQLModel.metadata.create_all) 
        logger.info("Database schema successfully verified.")
    except Exception as e:
        logger.error(f"CRITICAL: Database setup failed. Ensure DB is reachable. Details: {e}")

    # 2. Setup Logging/Middleware (Example placeholder)
    # setup_logging() # Already done implicitly by logger.py import
    # init_redis_pool() 

    yield # Application is running
    
    # --- SHUTDOWN LOGIC ---
    logger.info(f"[{settings.PROJECT_NAME}] Application Shutdown...")
    # await close_redis_pool()