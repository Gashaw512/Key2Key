# app/core/redis_client.py
"""
Redis client initialization and connection management.
"""

import aioredis
from typing import Optional
from app.core.config import settings
from app.core.logger import logger

redis_client: Optional[aioredis.Redis] = None

async def init_redis():
    """Initialize Redis connection."""
    global redis_client
    
    if not settings.REDIS_URL:
        logger.info("Redis not configured")
        return
    
    try:
        redis_client = await aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            encoding="utf-8",
            socket_connect_timeout=5,
            socket_timeout=5
        )
        
        # Test connection
        await redis_client.ping()
        logger.info(f"✅ Redis connected: {settings.REDIS_URL}")
        
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        redis_client = None

async def close_redis():
    """Close Redis connection."""
    global redis_client
    if redis_client:
        try:
            await redis_client.close()
            logger.info("✅ Redis connection closed")
        except Exception as e:
            logger.error(f"Redis close error: {e}")
        finally:
            redis_client = None

# Make client available globally
__all__ = ["redis_client", "init_redis", "close_redis"]