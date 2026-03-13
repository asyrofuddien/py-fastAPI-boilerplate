#!/usr/bin/env python3
"""
Test script to verify the FastAPI setup is working correctly.
Run this after completing the setup to ensure everything is configured properly.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

async def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")
    try:
        from src.config import settings
        from src.database import engine, get_db
        from src.auth.models import User
        from src.auth.service import UserService
        from src.main import app
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def test_database_connection():
    """Test database connection."""
    print("🔍 Testing database connection...")
    try:
        from src.database import engine
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1 as test")
            row = result.fetchone()
            if row and row[0] == 1:
                print("✅ Database connection successful")
                return True
            else:
                print("❌ Database connection failed - unexpected result")
                return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print("💡 Make sure PostgreSQL is running and .env is configured correctly")
        return False

async def test_environment_variables():
    """Test that required environment variables are set."""
    print("🔍 Testing environment variables...")
    try:
        from src.config import settings
        required_vars = ['DATABASE_URL', 'JWT_SECRET']
        missing_vars = []
        
        for var in required_vars:
            if not hasattr(settings, var) or not getattr(settings, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing environment variables: {missing_vars}")
            print("💡 Check your .env file")
            return False
        else:
            print("✅ All required environment variables are set")
            return True
    except Exception as e:
        print(f"❌ Environment variables error: {e}")
        return False

async def test_jwt_functionality():
    """Test JWT token creation and verification."""
    print("🔍 Testing JWT functionality...")
    try:
        from src.auth.utils import create_access_token, verify_token
        from uuid import uuid4
        
        # Create test token
        test_data = {"sub": str(uuid4()), "username": "testuser"}
        token = create_access_token(test_data)
        
        # Verify token
        decoded_data = verify_token(token)
        
        if decoded_data.user_id == test_data["sub"] and decoded_data.username == test_data["username"]:
            print("✅ JWT functionality working")
            return True
        else:
            print("❌ JWT verification failed")
            return False
    except Exception as e:
        print(f"❌ JWT functionality error: {e}")
        return False

async def test_password_hashing():
    """Test password hashing functionality."""
    print("🔍 Testing password hashing...")
    try:
        from src.auth.utils import hash_password, verify_password
        
        test_password = "testpassword123"
        hashed = hash_password(test_password)
        
        if verify_password(test_password, hashed):
            print("✅ Password hashing working")
            return True
        else:
            print("❌ Password verification failed")
            return False
    except Exception as e:
        print(f"❌ Password hashing error: {e}")
        return False

async def main():
    """Run all tests."""
    print("🚀 FastAPI Setup Verification")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_environment_variables,
        test_database_connection,
        test_jwt_functionality,
        test_password_hashing,
    ]
    
    results = []
    for test in tests:
        result = await test()
        results.append(result)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("📊 Test Summary")
    print("-" * 20)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Start the server: python -m src.main")
        print("2. Visit: http://localhost:8000/docs")
        print("3. Run the test suite: pytest")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("💡 Refer to SETUP_GUIDE.md for troubleshooting.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())