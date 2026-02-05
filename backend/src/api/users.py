from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from ..models.user import User
from ..core.database import get_async_session
from ..api.deps import get_current_user

class UserProfileUpdate(BaseModel):
    name: str
    email: str

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/me', response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile information."""
    return current_user

@router.put('/me', response_model=User)
async def update_current_user_profile(
    user_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Update current user's profile information."""
    # Update user fields
    current_user.name = user_update.name
    current_user.email = user_update.email

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user

@router.get('/', response_model=List[User])
async def get_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Get list of all users (for admin functionality)."""
    # In a real implementation, you might want to check if the user has admin privileges
    result = await db.execute(select(User))
    users = result.all()
    return users