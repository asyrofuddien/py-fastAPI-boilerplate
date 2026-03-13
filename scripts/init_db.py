#!/usr/bin/env python3
"""
Initialize database tables (alternative to Alembic for quick setup).
Use this only for development/testing. For production, use Alembic migrations.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database import engine, Base
from src.auth.models import User
from sqlalchemy import text


async def test_connection():
    """Test database connection."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            if row and row[0] == 1:
                print("✅ Database connection successful!")
                return True
            else:
                print("❌ Database connection failed!")
                return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False


async def create_tables():
    """Create all tables in the database."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False


async def main():
    """Main function."""
    print("🔄 Testing database connection...")
    if not await test_connection():
        return False
    
    print("🔄 Creating database tables...")
    if not await create_tables():
        return False
    
    await engine.dispose()
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n🎉 Database initialization complete!")
        print("You can now start the server: python -m src.main")
    else:
        print("\n💥 Database initialization failed!")
        print("Check your database connection and try again.")
        sys.exit(1)