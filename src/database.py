from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import text
from src.config import settings
from typing import AsyncIterator

# For SQLAlchemy compatibility
try:
    from sqlalchemy.ext.asyncio import async_sessionmaker
except ImportError:
    # Fallback for older SQLAlchemy versions - create a simple wrapper
    def async_sessionmaker(bind, **kwargs):
        return sessionmaker(bind=bind, **kwargs)


# Database engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "local",
    future=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


# Dependency to get database session
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()