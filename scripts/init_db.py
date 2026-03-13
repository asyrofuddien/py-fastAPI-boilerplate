#!/usr/bin/env python3
"""
Initialize database with first migration.
Run this after setting up your .env file.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database import engine, Base
from src.auth.models import User  # Import all models


async def create_tables():
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully!")


async def main():
    """Main function."""
    print("🔄 Creating database tables...")
    try:
        await create_tables()
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    finally:
        await engine.dispose()
    
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n🎉 Database initialization complete!")
        print("You can now start the server with: python -m src.main")
    else:
        print("\n💥 Database initialization failed!")
        sys.exit(1)