# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logger import setup_logging # Import logging setup
from app.api.v1.router import api_router

def create_application() -> FastAPI:
    """Initializes the FastAPI application object."""
    # CALL THE SETUP FUNCTION HERE!
    setup_logging() 
    
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="Core backend service for the Key2Key ecosystem, built for scale.",
        lifespan=lifespan, 
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc", 
    )
    
    # CORE MIDDLEWARE
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # ROUTER INCLUSION
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application

app = create_application()

@app.get("/", tags=["Status"])
async def root_status():
    """Simple status endpoint pointing to docs."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}. See status at {settings.API_V1_STR}/health"
    }