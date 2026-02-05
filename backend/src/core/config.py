"""Application configuration."""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database - Will be read from environment variables
    DATABASE_URL: str

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Better Auth (placeholder - actual integration may differ)
    BETTER_AUTH_SECRET: Optional[str] = None
    BETTER_AUTH_URL: str = "http://localhost:8000/api/auth"

    # Application settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # CORS
    BACKEND_CORS_ORIGINS: str = "*"  # Comma-separated origins or "*" for all

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()