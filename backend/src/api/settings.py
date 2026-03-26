"""Settings API endpoints for user preferences management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from ..models.user import User
from ..models.settings import UserSettings, UserSettingsBase
from ..api.deps import get_current_user
from ..core.database import get_async_session
from ..api.responses import format_success_response, format_error_response


class UserSettingsUpdate(BaseModel):
    notifications: bool
    theme: str
    language: str


router = APIRouter(prefix='/settings', tags=['settings'])


@router.get('/me', response_model=UserSettings)
async def get_current_user_settings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Get current user's settings. Creates default settings if none exist."""
    statement = select(UserSettings).where(UserSettings.user_id == current_user.id)
    result = await db.execute(statement)
    user_settings = result.scalar_one_or_none()

    if not user_settings:
        # Create default settings for user
        user_settings = UserSettings(
            user_id=current_user.id,
            notifications=True,
            theme="light",
            language="en"
        )
        db.add(user_settings)
        await db.commit()
        await db.refresh(user_settings)

    return user_settings


@router.put('/me', response_model=UserSettings)
async def update_current_user_settings(
    settings_update: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Update current user's settings. Creates settings if they don't exist."""
    statement = select(UserSettings).where(UserSettings.user_id == current_user.id)
    result = await db.execute(statement)
    user_settings = result.scalar_one_or_none()

    if not user_settings:
        # Create new settings for user
        user_settings = UserSettings(
            user_id=current_user.id,
            notifications=settings_update.notifications,
            theme=settings_update.theme,
            language=settings_update.language
        )
    else:
        # Update existing settings
        user_settings.notifications = settings_update.notifications
        user_settings.theme = settings_update.theme
        user_settings.language = settings_update.language

    db.add(user_settings)
    await db.commit()
    await db.refresh(user_settings)

    return user_settings