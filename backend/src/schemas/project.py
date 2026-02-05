"""Project schemas for the application."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class ProjectBase(BaseModel):
    """Base schema for project items."""
    name: str
    description: Optional[str] = None
    color: str = "#000000"


class ProjectCreate(ProjectBase):
    """Schema for creating project items."""
    name: str


class ProjectUpdate(BaseModel):
    """Schema for updating project items."""
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


class Project(ProjectBase):
    """Schema for project items with ID."""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True