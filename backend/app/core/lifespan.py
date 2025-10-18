"""
app/core/lifespan.py
--------------------
Production-ready application lifespan manager.
Handles startup and shutdown events, ensuring database connectivity,
schema initialization, and graceful shutdown of async resources.
"""

import asyncio
from contextlib import asynccontextmanager
from sqlalchemy import text, inspect, event
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import configure_mappers
from sqlalchemy.schema import Table
from sqlmodel import SQLModel
from fastapi import FastAPI

from app.core.config import settings
from app.core.database import async_engine, sync_engine
from app.core.logger import logger

# Ensure models are imported to register relationships
try:
    from app import models
    logger.debug("✅ Models imported successfully")
except ImportError as e:
    logger.warning(f"⚠️ Failed to import app.models: {e}")


# -------------------------------
# Event Listeners
# -------------------------------
@event.listens_for(SQLModel.metadata, "before_create")
def skip_existing_indexes(target, connection, **kw):
    """
    Prevent index creation errors during schema setup.
    Skips indexes that already exist in the target database.
    """
    if not isinstance(target, Table):
        return

    try:
        inspector = inspect(connection)
        existing = {idx["name"] for idx in inspector.get_indexes(target.name)}
        for index in list(target.indexes):
            if index.name in existing:
                target.indexes.remove(index)
                logger.info(f"⏭️ Skipping existing index: {index.name}")
    except Exception as e:
        logger.warning(f"⚠️ Failed index check for table '{getattr(target, 'name', '<unknown>')}': {e}")


# -------------------------------
# Database Utilities
# -------------------------------
async def verify_database_connection() -> bool:
    """Verify async database connectivity."""
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection verified")
        return True
    except OperationalError as e:
        logger.error(f"❌ Database connection failed: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected DB verification error: {e}")
    return False


async def initialize_schema() -> bool:
    """
    Initialize database schema safely.
    Ensures UUID extension is enabled and tables are created only if missing.
    """
    try:
        logger.info("🔄 Configuring SQLAlchemy mappers...")
        configure_mappers()
        logger.info("✅ Mappers configured")

        # Enable PostgreSQL UUID extension if applicable
        try:
            async with async_engine.begin() as conn:
                await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
            logger.info("✅ UUID extension verified")
        except Exception as e:
            logger.debug(f"ℹ️ UUID extension skipped: {e}")

        # Create missing tables using synchronous engine
        logger.info("🔄 Creating/verifying database schema...")
        SQLModel.metadata.create_all(bind=sync_engine, checkfirst=True)
        logger.info("✅ Schema creation verified")

        # Verify essential tables exist
        inspector = inspect(sync_engine)
        required_tables = {"users", "broker_profiles", "property_listings", "notifications"}
        missing = required_tables - set(inspector.get_table_names())
        if missing:
            logger.warning(f"⚠️ Missing tables: {sorted(missing)}")
        else:
            logger.info("✅ All critical tables present")

        return True

    except ProgrammingError as e:
        if "already exists" in str(e).lower():
            logger.info("ℹ️ Schema already initialized")
            return True
        logger.error(f"❌ Schema error: {e}")
    except AttributeError as e:
        logger.error(f"❌ Schema initialization failed (attribute error): {e}")
    except Exception as e:
        logger.error(f"❌ Schema initialization failed: {e}")

    return False


async def startup_health_checks() -> dict:
    """Run minimal startup health checks for database and schema."""
    results = {
        "database": await verify_database_connection(),
        "schema": await initialize_schema(),
    }

    failed = [k for k, ok in results.items() if not ok]
    if failed:
        logger.warning(f"⚠️ Health checks failed: {failed}")
        logger.warning("🚀 Continuing startup despite warnings")

    logger.info("✅ Health checks completed")
    return results


# -------------------------------
# Lifespan Manager
# -------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Central lifespan context for FastAPI app.
    Handles startup validation, schema setup, and graceful shutdown.
    """
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"🌍 Environment: {settings.ENVIRONMENT}")

    try:
        await startup_health_checks()
        app.state.async_engine = async_engine
        app.state.sync_engine = sync_engine
        logger.info("✅ Application startup complete")
    except Exception as e:
        logger.critical(f"💥 CRITICAL STARTUP FAILURE: {e}", exc_info=True)
        raise RuntimeError("Application startup aborted") from e

    yield  # App is running

    # Graceful shutdown
    try:
        logger.info("🛑 Shutting down application...")
        await async_engine.dispose()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")


# Export alias
lifespan_manager = lifespan
__all__ = ["lifespan_manager"]
