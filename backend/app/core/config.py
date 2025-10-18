# app/core/config.py
"""
Production-Ready Configuration for Key2Key API
Robust, secure, and scalable settings management.
"""

import os
import secrets
from pathlib import Path
from typing import Optional, List
from enum import Enum
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from cryptography.fernet import Fernet
import logging

class LogLevel(str, Enum):
    """Logging level enum."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Environment(str, Enum):
    """Environment enum."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class Settings(BaseSettings):
    """Complete application configuration."""
    
    # === GENERAL ===
    PROJECT_NAME: str = Field(default="Key2Key Backend", description="Application name")
    VERSION: str = Field(default="1.0.0", description="API version")
    API_V1_STR: str = Field(default="/api/v1", description="API version prefix")
    ENVIRONMENT: Environment = Field(default=Environment.DEVELOPMENT)
    
    # === SECURITY ===
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="JWT signing key - MUST be set in production"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=1, le=60*24*7)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, ge=1, le=365)
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    
    # === DATABASE ===
    POSTGRES_SERVER: str = Field(..., description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, ge=1, le=65535)
    POSTGRES_USER: str = Field(..., description="PostgreSQL user")
    POSTGRES_PASSWORD: str = Field(..., description="PostgreSQL password")
    POSTGRES_DB: str = Field(..., description="PostgreSQL database name")
    
    # Connection pooling
    DATABASE_POOL_MIN_SIZE: int = Field(default=5, ge=1)
    DATABASE_POOL_MAX_SIZE: int = Field(default=20, ge=5)
    DATABASE_MAX_OVERFLOW: int = Field(default=10, ge=0)
    
    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Synchronous database URL for migrations/tools."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Async database URL for application."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # === REDIS (Caching/Sessions) ===
    REDIS_URL: Optional[str] = Field(default=None, description="Redis connection URL")
    REDIS_EXPIRE_SECONDS: int = Field(default=3600, ge=60)
    
    # === SECURITY & VALIDATION ===
    SECURITY_SALT: Optional[str] = Field(default=None)
    ALLOWED_HOSTS: List[str] = Field(default_factory=list)
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: List[str] = Field(default_factory=lambda: ["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default_factory=lambda: ["*"])
    
    # === LOGGING ===
    LOG_LEVEL: LogLevel = Field(default=LogLevel.INFO)
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    LOG_FILE: Optional[str] = Field(default=None)
    
    # === API SECURITY ===
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=100, ge=1)
    MAX_PAGE_SIZE: int = Field(default=100, ge=10, le=1000)
    
    # === EMAIL ===
    EMAIL_ENABLED: bool = Field(default=False)
    SMTP_SERVER: Optional[str] = Field(default=None)
    SMTP_PORT: Optional[int] = Field(default=587)
    SMTP_USER: Optional[str] = Field(default=None)
    SMTP_PASSWORD: Optional[str] = Field(default=None)
    EMAIL_FROM: Optional[str] = Field(default=None)
    
    # === FILE STORAGE ===
    MEDIA_ROOT: Path = Field(default=Path("media"))
    MEDIA_URL: str = Field(default="/media/")
    
    # === TESTING ===
    TEST_DATABASE_URL: Optional[str] = Field(default=None)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )
    
    @validator("SECRET_KEY", pre=True, always=True)
    def generate_secret_key(cls, v):
        """Ensure SECRET_KEY is set."""
        if v is None or v == "":
            raise ValueError("SECRET_KEY must be set in production")
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == Environment.PRODUCTION
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == Environment.DEVELOPMENT
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins with validation."""
        if self.is_development:
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS if origin.strip()]
    
    @property
    def database_echo(self) -> bool:
        """Enable SQL logging in development."""
        return self.is_development

settings = Settings()

# Validate critical settings
def validate_settings():
    """Validate required settings."""
    errors = []
    
    if settings.is_production and not settings.SECRET_KEY:
        errors.append("SECRET_KEY must be set in production")
    
    if not settings.POSTGRES_SERVER or not settings.POSTGRES_USER:
        errors.append("Database connection settings are required")
    
    if errors:
        raise RuntimeError(f"Configuration errors: {'; '.join(errors)}")

validate_settings()