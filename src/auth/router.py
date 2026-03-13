from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from src.database import get_db
from src.auth.schemas import UserCreate, UserUpdate, UserResponse, UserLogin, Token
from src.auth.service import UserService
from src.auth.dependencies import get_current_user, validate_user_ownership
from src.auth.models import User


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    description="Register a new user",
    responses={
        status.HTTP_201_CREATED: {"model": UserResponse},
        status.HTTP_400_BAD_REQUEST: {"description": "User already exists"}
    }
)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    user = await UserService.create_user(db, user_data)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=Token,
    description="Login user and get access token",
    responses={
        status.HTTP_200_OK: {"model": Token},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"}
    }
)
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login user and return access token."""
    token = await UserService.authenticate_user(db, login_data.username, login_data.password)
    return token


@router.get(
    "/me",
    response_model=UserResponse,
    description="Get current user profile"
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user profile."""
    return UserResponse.model_validate(current_user)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    description="Get user by ID"
)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get user by ID."""
    user = await UserService.get_by_id(db, user_id)
    if not user:
        from src.exceptions import UserNotFound
        raise UserNotFound()
    return UserResponse.model_validate(user)


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    description="Update user information"
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    user: User = Depends(validate_user_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Update user information (only owner can update)."""
    updated_user = await UserService.update_user(db, user_id, user_data)
    return UserResponse.model_validate(updated_user)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete user account"
)
async def delete_user(
    user_id: UUID,
    user: User = Depends(validate_user_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Delete user account (only owner can delete)."""
    await UserService.delete_user(db, user_id)
    return None