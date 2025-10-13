# app/db/session.py

from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import AsyncSessionLocal 

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Dependency: Provides an asynchronous SQLModel session.
    Manages session creation, yielding, commit/rollback, and closing.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback() 
            raise