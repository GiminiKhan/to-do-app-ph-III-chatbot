"""SQLModel for Project entity."""

from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from typing import Optional


class ProjectBase(SQLModel):
    """Base model for Project with shared attributes."""
    name: str = Field(nullable=False, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    color: str = Field(default="#000000", max_length=7)  # Hex color code


class Project(ProjectBase, table=True):
    """Project model with database table configuration."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)