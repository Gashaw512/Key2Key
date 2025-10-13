# app/main.py (Professional Version)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # New Import

from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine # New Import for startup
# from app.db.base import Base # Re-export SQLModel as Base
from sqlmodel import SQLModel # Use SQLModel directly for table creation

# ====================================================================
# 1. LIFESPAN CONTEXT MANAGER (The Professional Approach)
# ====================================================================

# This function runs when the server starts and stops
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    """
    print(f"[{settings.PROJECT_NAME}] Application Startup...")
    
    # 1.1. Database Startup Logic (Create tables for development/testing)
    # This block ensures all SQLModel tables are created if they don't exist.
    # NOTE: In production, Alembic migrations usually handle this.
    try:
        print("Creating database tables (if they do not exist)...")
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"ERROR: Could not create database tables. Ensure DB is running. Details: {e}")

    # 1.2. Logging/Other Setup Logic (e.g., Redis connection)
    # setup_logging() 
    # init_redis()
    
    yield # Application is running

    # 1.3. Shutdown Logic
    print(f"[{settings.PROJECT_NAME}] Application Shutdown...")
    # close_redis_connection()


# ====================================================================
# 2. CREATE APPLICATION FUNCTION
# ====================================================================

def create_application() -> FastAPI:
    """
    Initializes the FastAPI application with configuration, routers, and middleware.
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0", # Added Version
        description="Core backend service for the Key2Key ecosystem.", # Added Description
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan # Attach the lifespan manager
    )
    
    # 2.1. CORS Middleware (Standard for professional APIs)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Be specific in production! e.g., ["http://localhost:3000"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 2.2. Custom Middleware (e.g., Logging, Request ID)
    # setup_middleware(application) # To be implemented in Task 4
    
    # 2.3. Include the main API router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application

app = create_application()

# ====================================================================
# 3. ROOT ENDPOINT (Simple Health Check)
# ====================================================================

# A simple root endpoint is fine, but it's better to move it to a healthcheck.py
@app.get("/", tags=["Health"])
async def read_root():
    """Returns the API status and project name."""
    return {
        "status": "ok", 
        "project": settings.PROJECT_NAME,
        "version": "v1"
    }