from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Optional
from src.auth.models import User
from src.auth.schemas import UserCreate, UserUpdate, Token
from src.auth.utils import hash_password, verify_password, create_access_token
from src.exceptions import UserNotFound, UserAlreadyExists, InvalidCredentials


class UserService:
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = await UserService.get_by_username(db, user_data.username)
        if existing_user:
            raise UserAlreadyExists()
            
        existing_email = await UserService.get_by_email(db, user_data.email)
        if existing_email:
            raise UserAlreadyExists()
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username."""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: UUID, user_data: UserUpdate) -> User:
        """Update user information."""
        user = await UserService.get_by_id(db, user_id)
        if not user:
            raise UserNotFound()
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
        """Delete a user."""
        user = await UserService.get_by_id(db, user_id)
        if not user:
            raise UserNotFound()
        
        await db.delete(user)
        await db.commit()
        return True
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Token:
        """Authenticate user and return token."""
        user = await UserService.get_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentials()
        
        if not user.is_active:
            raise InvalidCredentials()
        
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username}
        )
        
        return Token(access_token=access_token)