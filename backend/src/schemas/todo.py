"""To-do schemas for the application."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class TodoBase(BaseModel):
    """Base schema for to-do items."""
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    due_date: Optional[datetime] = None
    project_id: Optional[uuid.UUID] = None
    tags: Optional[str] = None  # Comma-separated tags
    reminder_time: Optional[datetime] = None  # Reminder time for the task
    completed_at: Optional[datetime] = None  # When the task was completed


class TodoCreate(TodoBase):
    """Schema for creating to-do items."""
    title: str


class TodoUpdate(BaseModel):
    """Schema for updating to-do items."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Todo(TodoBase):
    """Schema for to-do items with ID."""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True