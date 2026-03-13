#!/usr/bin/env python3
"""
FastAPI Best Practices Boilerplate - Quick Start Script
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(e.stderr)
        return False


def setup_project():
    """Set up the project."""
    print("\n🚀 Setting up FastAPI Best Practices project...")
    
    # Check if .env exists
    if not Path(".env").exists():
        print("\n📝 Creating .env file from template...")
        if Path(".env.example").exists():
            run_command("cp .env.example .env", "Copying .env template", check=False)
            print("⚠️  Please edit .env file with your database credentials!")
        else:
            print("❌ .env.example not found")
            return False
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    print("\n📋 Setup completed! Next steps:")
    print("1. Edit .env file with your database credentials")
    print("2. Start PostgreSQL: python run.py docker-up")
    print("3. Apply migrations: alembic upgrade head")
    print("4. Start server: python run.py start")
    
    return True


def start_docker_db():
    """Start PostgreSQL using Docker Compose."""
    print("\n🐳 Starting PostgreSQL with Docker...")
    
    if not Path("docker-compose.yml").exists():
        print("❌ docker-compose.yml not found")
        return False
    
    # Start PostgreSQL container
    if not run_command("docker-compose up -d postgres", "Starting PostgreSQL container"):
        return False
    
    print("⏳ Waiting for PostgreSQL to be ready...")
    import time
    time.sleep(5)
    
    print("✅ PostgreSQL is ready!")
    return True


def stop_docker_db():
    """Stop PostgreSQL Docker container."""
    print("\n🛑 Stopping PostgreSQL Docker container...")
    return run_command("docker-compose down", "Stopping PostgreSQL container")


def start_server():
    """Start the FastAPI server."""
    print("\n🌟 Starting FastAPI server...")
    
    if not Path(".env").exists():
        print("❌ .env file not found. Run 'python run.py setup' first")
        return False
    
    try:
        print("Server starting at http://localhost:8000")
        print("API docs available at http://localhost:8000/docs")
        print("Press Ctrl+C to stop the server")
        os.system("python -m src.main")
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    
    return True


def run_tests():
    """Run the test suite."""
    print("\n🧪 Running tests...")
    return run_command("pytest -v", "Running test suite")


def verify_setup():
    """Run basic verification."""
    print("\n🔍 Verifying setup...")
    
    # Check if main files exist
    required_files = [
        "src/main.py",
        "src/config.py", 
        "src/database.py",
        "requirements.txt",
        ".env"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    print("✅ Setup verification completed")
    return True


def show_help():
    """Show help information."""
    print("""
🚀 FastAPI Best Practices Boilerplate

Usage: python run.py [command]

Commands:
  setup       - Install dependencies and setup project
  docker-up   - Start PostgreSQL with Docker
  docker-down - Stop PostgreSQL Docker container
  start       - Start the FastAPI development server
  test        - Run the test suite
  verify      - Verify setup is working correctly
  help        - Show this help message

Quick Start:
  python run.py setup        # First time setup
  python run.py docker-up    # Start PostgreSQL
  alembic upgrade head       # Apply migrations
  python run.py start        # Start server

For detailed instructions, see README.md
""")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        setup_project()
    elif command == "docker-up":
        start_docker_db()
    elif command == "docker-down":
        stop_docker_db()
    elif command == "start":
        start_server()
    elif command == "test":
        run_tests()
    elif command == "verify":
        verify_setup()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()