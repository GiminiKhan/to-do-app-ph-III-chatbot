"""SQLModel for User Settings entity."""

from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class UserSettingsBase(SQLModel):
    """Base model for User Settings with shared attributes."""
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    notifications: bool = Field(default=True)
    theme: str = Field(default="light", max_length=20)
    language: str = Field(default="en", max_length=10)


class UserSettings(UserSettingsBase, table=True):
    """User Settings model with database table configuration."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)