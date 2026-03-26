import sys
import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.middleware import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

# Path Fix to make sure Python finds the 'src' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- UPDATED: Imports using absolute paths with src ---
from src.services.openai_agent_service import openai_agent_service
from src.core.database import get_db

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend is running with Agent and Neon DB"}

class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None

@app.post("/chat")
async def chat_with_agent(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        response = await openai_agent_service.process_message(
            request.message, 
            request.user_id, 
            request.conversation_id or "new",
            db
        )
        return {
            "conversation_id": request.conversation_id or "new",
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))