# combines all endpoints into a single router
# from fastapi import APIRouter

# app/api/v1/router.py

from fastapi import APIRouter

# Initialize the main router for API v1
api_router = APIRouter()

# NOTE: In subsequent steps (Week 3), you will add:
# from .endpoints import auth, users, ...
# api_router.include_router(auth.router, tags=["auth"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])

# For now, it remains simple:
pass