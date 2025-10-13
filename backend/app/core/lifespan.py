# app/core/lifespan.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel 

from app.core.config import settings
from app.core.database import engine # Import the engine from the configuration

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events (DB table creation, Redis setup, etc.).
    """
    print(f"[{settings.PROJECT_NAME}] Application Startup...")
    
    # --- STARTUP LOGIC ---
    
    # 1. Create SQLModel Tables (for development/testing)
    try:
        print("Creating database tables if they do not exist...")
        # Note: This uses the synchronous engine imported from database.py
        SQLModel.metadata.create_all(engine) 
    except Exception as e:
        print(f"ERROR: Could not complete DB setup. Ensure PostgreSQL is reachable. Details: {e}")

    # 2. Other initialization (e.g., Redis)
    # init_redis_pool() 

    yield # Application is running
    
    # --- SHUTDOWN LOGIC ---
    
    print(f"[{settings.PROJECT_NAME}] Application Shutdown...")
    # close_redis_pool()