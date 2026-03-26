from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, todos, projects, chat, users
from .api.settings import router as settings_router
from .core.config import settings
from .core.database import async_engine
from .services.openai_agent_service import openai_agent_service
import json
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize OpenAI assistant
    try:
        await openai_agent_service.initialize_assistant()
    except Exception as e:
        print(f"Warning: Could not initialize OpenAI Assistant: {e}")
        print("Assistant will be initialized on first use.")

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
app.include_router(chat.router)
app.include_router(users.router)
app.include_router(settings_router)

@app.get('/')
def root():
    return {'status': 'online'}