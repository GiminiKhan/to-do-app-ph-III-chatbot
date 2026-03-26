from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import create_engine as sync_create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager
import os
import dotenv
from fastapi import Depends
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Create declarative base for SQLAlchemy models
Base = declarative_base()

# Import settings from centralized config
from .config import settings


# Validate that DATABASE_URL is set
if not settings.DATABASE_URL:
    # Try to load from parent directory as well
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))

    if not settings.DATABASE_URL:
        # For development/testing purposes, provide a fallback or raise error
        raise ValueError("DATABASE_URL environment variable is not set. Please check your .env file.")

# Create async engine for PostgreSQL (Neon) - convert sync URL to async if needed
async_db_url = settings.DATABASE_URL

# Parse the URL and remove sslmode parameter if present
parsed_url = urlparse(async_db_url)
query_params = parse_qs(parsed_url.query, keep_blank_values=True)

# Remove sslmode parameter if it exists (case-insensitive)
sslmode_keys = [key for key in query_params.keys() if key.lower() == 'sslmode']
for key in sslmode_keys:
    del query_params[key]

# Also handle the case where sslmode might be part of the URL fragment or other parts
# Reconstruct the query string without sslmode
new_query = urlencode(query_params, doseq=True)

# Reconstruct the full URL
parsed_list = list(parsed_url)
parsed_list[4] = new_query  # Replace query string
cleaned_url = urlunparse(parsed_list)

# Now convert to async if needed
if cleaned_url.startswith("postgresql://"):
    async_db_url = cleaned_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif cleaned_url.startswith("postgres://"):
    async_db_url = cleaned_url.replace("postgres://", "postgresql+asyncpg://", 1)
else:
    async_db_url = cleaned_url

# Configure async engine with proper settings for Neon connection pooling
async_engine = create_async_engine(
    async_db_url,
    echo=False,
    # Pool settings for Neon (PostgreSQL)
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
    pool_size=20,        # Number of connection pools
    max_overflow=30,     # Additional connections beyond pool_size
    pool_timeout=30,     # Timeout for getting connection from pool
    connect_args={
        "server_settings": {
            "application_name": "todo-app",  # Application name for monitoring
        }
    }
)

# Create sync engine for backward compatibility with proper Neon settings
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    # Pool settings for Neon (PostgreSQL)
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
    pool_size=20,        # Number of connection pools
    max_overflow=30,     # Additional connections beyond pool_size
    pool_timeout=30,     # Timeout for getting connection from pool
    connect_args={
        "application_name": "todo-app",  # Application name for monitoring
    }
)


def create_db_and_tables():
    """Create database tables - for sync operations"""
    from ..models.user import User
    from ..models.todo import Todo
    from ..models.project import Project
    from ..models.message import Message
    from ..models.settings import UserSettings
    # Ensure all models are imported before creating tables
    _ = [User, Todo, Project, Message, UserSettings]  # This ensures all models are registered
    SQLModel.metadata.create_all(sync_engine)


# Session factories
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


async def get_async_session() -> AsyncSession:
    """Async session dependency for FastAPI"""
    async with AsyncSessionLocal() as session:
        yield session


def get_session():
    """Sync session generator for backward compatibility"""
    with Session(sync_engine) as session:
        yield session