from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from ..core.database import get_async_session
from ..services.auth_service import AuthService
from ..models.user import User
from ..core.config import settings
from ..core.security import create_access_token

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    name: str
    password: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

class RegisterResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login', response_model=LoginResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(data.email, data.password)

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post('/register', response_model=RegisterResponse)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(db)
    try:
        user = await auth_service.register_user(data.email, data.name, data.password)

        # Create access token for new user
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/logout')
async def logout():
    # In a real implementation, you might want to add the token to a blacklist
    # or implement other logout mechanisms
    return {"message": "Successfully logged out"}


@router.post('/forgot-password')
async def forgot_password(request: PasswordResetRequest, db: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(db)
    # Placeholder for password reset functionality
    # In a real implementation, you would send an email with a reset token
    return {"message": "If an account with that email exists, a password reset link has been sent"}


@router.post('/reset-password')
async def reset_password(request: PasswordResetConfirm, db: AsyncSession = Depends(get_async_session)):
    # Placeholder for password reset functionality
    # In a real implementation, you would verify the token and update the password
    return {"message": "Password reset successfully"}