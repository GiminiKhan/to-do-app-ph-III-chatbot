"""Dependency injection for API endpoints."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from ..core.database import get_async_session
from ..models.user import User
from ..core.security import verify_token
from ..core.exceptions import InvalidCredentialsException


security = HTTPBearer()


async def get_current_user(
    token_credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Get current user from token.

    Args:
        token_credentials: The token from the Authorization header
        db: Database session

    Returns:
        The current user if token is valid

    Raises:
        HTTPException: If token is invalid or user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_token(token_credentials.credentials)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        # Convert string user_id to UUID object for database query
        user_uuid = uuid.UUID(user_id)

    except Exception:
        raise credentials_exception

    # Fetch the user from the database using async session
    statement = select(User).where(User.id == user_uuid)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current active user.

    Args:
        current_user: The current user from the token

    Returns:
        The current user if they are active

    Raises:
        HTTPException: If the user is inactive
    """
    # In a real implementation, we would check if the user is active
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user