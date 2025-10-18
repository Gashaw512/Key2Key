# app/api/v1/router.py
"""
Main API router with modular endpoint inclusion.
"""

from fastapi import APIRouter
from app.core.config import settings

# Import endpoints
from .endpoints import (
    healthcheck, 
    users, 
    auth, 
    brokers,
    properties  # Will add later
)

# Main API router
api_router = APIRouter()

# Include routers with proper prefixes and tags
routers = [
    (healthcheck.router, "", ["health"]),
    (auth.router, "/auth", ["auth"]),
    (users.router, "/users", ["users"]),
    (brokers.router, "/broker", ["broker"]),
    # (properties.router, "/properties", ["properties"]),  # Add when ready
]

for router, prefix, tags in routers:
    api_router.include_router(
        router, 
        prefix=prefix, 
        tags=tags,
        dependencies=[]  
    )

# Version info endpoint
@api_router.get("/version")
async def api_version():
    """API version information."""
    return {
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "api_prefix": settings.API_V1_STR
    }