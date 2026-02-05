from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..models.user import User
from ..utils.auth import verify_password, get_password_hash
from ..core.security import create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, email: str, password: str):
        statement = select(User).where(User.email == email)
        result = await self.db.execute(statement)
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    async def register_user(self, email: str, name: str, password: str):
        # Check if user already exists
        existing_user = await self.get_user_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = get_password_hash(password)

        # Create new user
        user = User(email=email, name=name, hashed_password=hashed_password)
        self.db.add(user)

        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    async def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()