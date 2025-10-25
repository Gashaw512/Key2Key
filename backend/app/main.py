# app/main.py
"""
🚀 Key2Key Backend - FastAPI Application Entry Point
Structured for scalability, observability, and security.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

# --- Core Imports ---
from app.core.config import settings
from app.core.lifespan import lifespan_manager
from app.core.logger import setup_logging, logger
from app.core.health import health_check

# --- API Router ---
from app.api.v1.router import api_router9


# ---------------------------------------------------------
# ✅ APPLICATION FACTORY
# ---------------------------------------------------------
def create_application() -> FastAPI:
    """
    Factory to create and configure a FastAPI application.
    Ensures modular design and consistent setup across environments.
    """
    # Initialize structured logging
    setup_logging()
    logger.info("[Key2Key Backend] Application Startup...")

    # Initialize FastAPI instance
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Key2Key Real Estate Platform API",
        lifespan=lifespan_manager,
        docs_url=f"{settings.API_V1_STR}/docs" if settings.is_development else None,
        redoc_url=f"{settings.API_V1_STR}/redoc" if settings.is_development else None,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    # -----------------------------------------------------
    # 🧩 MIDDLEWARE CONFIGURATION
    # -----------------------------------------------------

    # ✅ Restrict allowed hosts (security best practice)
    if settings.ALLOWED_HOSTS:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS,
        )
        logger.info(f"Trusted hosts enabled: {settings.ALLOWED_HOSTS}")

    # ✅ Configure CORS for frontend & external API access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins(),
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    logger.info("CORS middleware initialized successfully.")

    # -----------------------------------------------------
    # 🔌 ROUTER REGISTRATION
    # -----------------------------------------------------
    app.include_router(api_router, prefix=settings.API_V1_STR)
    logger.info("API routers registered under prefix: %s", settings.API_V1_STR)

    # -----------------------------------------------------
    # ❤️ HEALTH & ROOT ENDPOINTS
    # -----------------------------------------------------

    @app.get("/health", tags=["Health"])
    async def health():
        """Lightweight health check endpoint."""
        return await health_check()

    @app.get("/", tags=["Root"])
    async def root():
        """API root endpoint (for quick verification)."""
        return {
            "message": f"Welcome to {settings.PROJECT_NAME}",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "docs": f"{settings.API_V1_STR}/docs" if settings.is_development else None,
            "health": "/health",
        }

    return app


# ---------------------------------------------------------
# 🧠 APPLICATION INSTANCE
# ---------------------------------------------------------
app = create_application()


# ---------------------------------------------------------
# 🧰 DEV ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    """
    Allows `python app/main.py` to launch the app in development.
    In production, run via:
        uvicorn app.main:app --host 0.0.0.0 --port 8000
    """
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.is_development,
        log_level="info",
    )
