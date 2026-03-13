from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.database import get_db
from src.auth.utils import verify_token
from src.auth.service import UserService
from src.auth.models import User
from src.auth.schemas import TokenData
from src.exceptions import InvalidCredentials, UserNotFound


security = HTTPBearer()


async def get_current_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """Extract and validate JWT token."""
    token = credentials.credentials
    return verify_token(token)


async def get_current_user(
    token_data: TokenData = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    user = await UserService.get_by_id(db, token_data.user_id)
    if not user:
        raise UserNotFound()
    
    if not user.is_active:
        raise InvalidCredentials()
    
    return user


async def validate_user_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> User:
    """Validate that user exists and return user object."""
    user = await UserService.get_by_id(db, user_id)
    if not user:
        raise UserNotFound()
    return user


async def validate_user_ownership(
    user: User = Depends(validate_user_id),
    current_user: User = Depends(get_current_user)
) -> User:
    """Validate that current user owns the resource."""
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    return user