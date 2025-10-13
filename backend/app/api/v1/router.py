# app/api/v1/router.py

from fastapi import APIRouter
from .endpoints import healthcheck 
# from .endpoints import user_endpoints # Future endpoint import

# Initialize the main router for API v1
api_router = APIRouter()

# --- INCLUDE ENDPOINTS ---
api_router.include_router(healthcheck.router) 
# api_router.include_router(user_endpoints.router, prefix="/users", tags=["Users"])