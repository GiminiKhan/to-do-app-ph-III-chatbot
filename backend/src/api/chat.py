"""Chat API endpoints for AI assistant integration."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

# Updated imports to absolute paths for deployment compliance
from src.models.user import User
from src.models.message import Message
from src.api.deps import get_current_user
from src.core.database import get_async_session
from src.api.responses import format_success_response, format_error_response
from src.services.openai_agent_service import openai_agent_service

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None  # Allow for conversation persistence

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: datetime

@router.post("/{user_id}/chat")
async def chat_with_agent(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Chat with the AI assistant for task management.
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to chat for this user"
        )

    try:
        # Generate a conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Store the user's message in the database
        user_message = Message(
            user_id=current_user.id,
            role="user",
            content=request.message,
            conversation_id=conversation_id
        )
        db.add(user_message)
        await db.commit()
        await db.refresh(user_message)

        # Process the user's message using the AI agent
        if not openai_agent_service.assistant:
            await openai_agent_service.initialize_assistant()

        # Process the message using the OpenAI agent service
        response = await openai_agent_service.process_message(
            message=request.message,
            user_id=str(current_user.id),
            conversation_id=conversation_id,
            db_session=db
        )

        # Store the assistant's response in the database
        assistant_message = Message(
            user_id=current_user.id,
            role="assistant",
            content=response,
            conversation_id=conversation_id
        )
        db.add(assistant_message)
        await db.commit()
        await db.refresh(assistant_message)

        # Return the response in the standardized format
        return format_success_response(
            data={
                "response": response,
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow().isoformat()
            },
            message="Message processed successfully"
        )
    except Exception as e:
        return format_error_response(
            error_code="CHAT_PROCESSING_ERROR",
            error_message=f"Error processing chat message: {str(e)}"
        )

@router.get("/{user_id}/chat/{conversation_id}/history")
async def get_conversation_history(
    user_id: str,
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    """
    Get the chat history for a specific conversation.
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to access conversation history for this user"
        )

    try:
        # Get messages for the specified conversation
        statement = select(Message).where(
            Message.user_id == current_user.id,
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        result = await db.execute(statement)
        messages = result.scalars().all()

        return format_success_response(
            data=[message.dict() for message in messages],
            message=f"Retrieved {len(messages)} messages for conversation {conversation_id}"
        )
    except Exception as e:
        return format_error_response(
            error_code="CONVERSATION_HISTORY_ERROR",
            error_message=f"Error retrieving conversation history: {str(e)}"
        )