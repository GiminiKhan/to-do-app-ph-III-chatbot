from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, todos, projects
from .core.config import settings
from .core.database import async_engine
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: nothing specific needed for Neon connection
    yield
    # Shutdown: close database engine
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

# Parse CORS origins from settings
# Allow multiple origins separated by commas, or use '*' for all
cors_origins = []
if settings.BACKEND_CORS_ORIGINS:
    if settings.BACKEND_CORS_ORIGINS == "*":
        cors_origins = ["*"]
    else:
        # Split comma-separated origins and strip whitespace
        cors_origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(projects.router)

@app.get('/')
def root():
    return {'status': 'online'}