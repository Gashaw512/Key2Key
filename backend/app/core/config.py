# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # General App Settings
    PROJECT_NAME: str = "Key2Key Backend"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(..., description="Secure token for signing JWTs. Must be set.")
    
    # Database Settings
    POSTGRES_SERVER: str = Field(..., description="PostgreSQL host")
    POSTGRES_USER: str = Field(..., description="PostgreSQL user")
    POSTGRES_PASSWORD: str = Field(..., description="PostgreSQL password")
    POSTGRES_DB: str = Field(..., description="PostgreSQL database name")

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Standard URL for synchronous tools like Alembic."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        )
        
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Async URL with the 'asyncpg' driver for application use."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()