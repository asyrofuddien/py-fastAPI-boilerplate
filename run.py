#!/usr/bin/env python3
"""
Quick start script for the FastAPI Best Practices project.
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(e.stderr)
        return False


def main():
    """Main setup and run function."""
    print("🚀 FastAPI Best Practices Project Setup")
    print("=" * 50)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("\n⚠️  .env file not found. Please create one from .env.example")
        print("   cp .env.example .env")
        print("   Then edit .env with your database credentials")
        return
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return
    
    # Check if we can connect to database (optional)
    print("\n📋 Next steps:")
    print("1. Make sure PostgreSQL is running")
    print("2. Create database: createdb fastapi_db")
    print("3. Run migrations: alembic upgrade head")
    print("4. Start the server: python run.py start")
    
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        print("\n🌟 Starting FastAPI server...")
        os.system("python -m src.main")


if __name__ == "__main__":
    main()