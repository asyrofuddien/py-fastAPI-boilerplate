#!/usr/bin/env python3
"""
Quick start script for the FastAPI Best Practices project.
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
        if result.stderr and check:
            print(f"Warning: {result.stderr}")
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(e.stderr)
        return False


def check_prerequisites():
    """Check if prerequisites are installed."""
    print("🔍 Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} found")
    
    # Check if Docker is available
    try:
        subprocess.run("docker --version", shell=True, check=True, capture_output=True)
        print("✅ Docker found")
    except subprocess.CalledProcessError:
        print("⚠️  Docker not found in PATH")
    
    # Check if PostgreSQL is available (local or docker)
    try:
        subprocess.run("psql --version", shell=True, check=True, capture_output=True)
        print("✅ PostgreSQL client found")
    except subprocess.CalledProcessError:
        print("ℹ️  PostgreSQL client not in PATH (using Docker setup)")
    
    return True


def setup_project():
    """Set up the project."""
    print("\n🚀 Setting up FastAPI Best Practices project...")
    
    if not check_prerequisites():
        return False
    
    # Check if .env exists
    if not Path(".env").exists():
        print("\n📝 Creating .env file from template...")
        if Path(".env.example").exists():
            run_command("cp .env.example .env", "Copying .env template", check=False)
            print("⚠️  Please edit .env file with your database credentials!")
            print("   Required: DATABASE_URL, JWT_SECRET")
        else:
            print("❌ .env.example not found")
            return False
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    print("\n📋 Setup completed! Next steps:")
    print("1. Start PostgreSQL: python run.py docker-up")
    print("2. Run setup verification: python run.py verify")
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
    
    # Wait a moment for container to be ready
    print("⏳ Waiting for PostgreSQL to be ready...")
    import time
    time.sleep(5)
    
    # Test connection
    test_cmd = 'docker exec fastapi_postgres pg_isready -U fastapi_user -d fastapi_db'
    if run_command(test_cmd, "Testing PostgreSQL connection", check=False):
        print("✅ PostgreSQL is ready!")
        return True
    else:
        print("⚠️  PostgreSQL might still be starting up. Try again in a few seconds.")
        return True


def stop_docker_db():
    """Stop PostgreSQL Docker container."""
    print("\n� Stopping PostgreSQL Docker container...")
    return run_command("docker-compose down", "Stopping PostgreSQL container")


def start_server():
    """Start the FastAPI server."""
    print("\n🌟 Starting FastAPI server...")
    
    # Check if .env exists
    if not Path(".env").exists():
        print("❌ .env file not found. Run 'python run.py setup' first")
        return False
    
    # Start the server
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
    """Run setup verification."""
    print("\n🔍 Running setup verification...")
    return run_command("python test_setup.py", "Setup verification")


def show_help():
    """Show help information."""
    print("""
🚀 FastAPI Best Practices - Quick Start Script

Usage: python run.py [command]

Commands:
  setup       - Install dependencies and setup project
  docker-up   - Start PostgreSQL with Docker
  docker-down - Stop PostgreSQL Docker container
  start       - Start the FastAPI development server
  test        - Run the test suite
  verify      - Verify setup is working correctly
  help        - Show this help message

Docker Workflow:
  python run.py setup        # First time setup
  python run.py docker-up    # Start PostgreSQL
  python run.py verify       # Check if everything works
  python run.py start        # Start FastAPI server

Examples:
  python run.py setup        # First time setup
  python run.py docker-up    # Start PostgreSQL in Docker
  python run.py verify       # Check if everything is working
  python run.py start        # Start the server
  python run.py test         # Run tests

For detailed setup instructions, see SETUP_GUIDE.md or docker-setup.md
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