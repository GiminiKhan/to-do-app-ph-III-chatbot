"""Message model for storing chat conversation history."""

from sqlalchemy import Column, String, DateTime, Text
from sqlmodel import Field, SQLModel
from datetime import datetime
import uuid


class MessageBase(SQLModel):
    """Base model for message fields."""
    role: str  # 'user' or 'assistant'
    content: str
    conversation_id: str


class Message(MessageBase, table=True):
    """Message model for storing conversation history."""
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    role: str = Field(sa_column=Column(String, nullable=False))  # 'user' or 'assistant'
    content: str = Field(sa_column=Column(Text, nullable=False))
    conversation_id: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    )