# app/core/database.py (REVISED for SQLModel)

from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# 1. SQLAlchemy Engine Setup (Sync)
# We use the standard sync engine for traditional ORM operations (like Alembic migrations)
# The URL remains the same as defined in settings.
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    # Echo=True is great for debugging, set to False for production
    echo=False, 
    pool_pre_ping=True
)

# 2. Synchronous Session Factory
# This is mainly used for Alembic migrations and synchronous dependencies.
# SQLModel models work seamlessly with the standard SQLAlchemy Session.
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=Session # Ensure it's a standard SQLAlchemy Session
)

# 3. FastAPI Dependency (Sync Database Session)
def get_db() -> Session:
    """
    Dependency that provides a synchronous SQLAlchemy session for use in FastAPI routes.
    The session is automatically closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# You can add an asynchronous setup here later if you opt for async database access,
# but the synchronous approach is the standard for getting started with SQLModel/FastAPI.