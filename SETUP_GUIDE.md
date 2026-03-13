# 🚀 Complete Setup Guide - From Installation to Testing

## Prerequisites

Make sure you have:
- Python 3.8+ installed
- PostgreSQL installed and running
- Git (optional, for version control)

## Step 1: Environment Setup

### 1.1 Create and activate virtual environment (recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 1.2 Install dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Database Setup

### 2.1 Create PostgreSQL database
```bash
# Connect to PostgreSQL as superuser
sudo -u postgres psql

# Create database and user
CREATE DATABASE fastapi_db;
CREATE USER fastapi_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
\q
```

### 2.2 Configure environment variables
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

Edit `.env` with your actual values:
```env
DATABASE_URL=postgresql+asyncpg://fastapi_user:your_password@localhost:5432/fastapi_db
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
ENVIRONMENT=local
```

## Step 3: Database Migration

### 3.1 Initialize Alembic (first time only)
```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 3.2 Alternative: Use the init script
```bash
python scripts/init_db.py
```

## Step 4: Start the Application

### 4.1 Using the run script
```bash
python run.py start
```

### 4.2 Using uvicorn directly
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 4.3 Using Makefile
```bash
make dev
```

## Step 5: Test the API

### 5.1 Check if server is running
Open your browser and go to:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

### 5.2 Test with curl commands

#### Register a new user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

#### Login:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword123"
  }'
```

#### Get current user (replace TOKEN with actual token from login):
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Step 6: Run Tests

### 6.1 Run all tests
```bash
pytest
```

### 6.2 Run tests with coverage
```bash
pytest --cov=src --cov-report=html
```

### 6.3 Run specific test file
```bash
pytest tests/test_auth.py -v
```

## Step 7: Code Quality Checks

### 7.1 Format code
```bash
ruff format src tests
```

### 7.2 Lint code
```bash
ruff check src tests
```

### 7.3 Fix linting issues automatically
```bash
ruff check --fix src tests
```

## Troubleshooting

### Common Issues:

#### 1. Database connection error
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server failed
```
**Solution**: Check if PostgreSQL is running and credentials in `.env` are correct.

#### 2. Module not found error
```
ModuleNotFoundError: No module named 'src'
```
**Solution**: Make sure you're running commands from the project root directory.

#### 3. Alembic migration error
```
alembic.util.exc.CommandError: Target database is not up to date
```
**Solution**: Run `alembic upgrade head` to apply pending migrations.

#### 4. JWT secret error
```
ValueError: JWT_SECRET is required
```
**Solution**: Make sure `.env` file exists and contains `JWT_SECRET`.

### Verify Installation:

#### Check Python packages:
```bash
pip list | grep -E "(fastapi|uvicorn|sqlalchemy|alembic)"
```

#### Check database connection:
```bash
python -c "
import asyncio
from src.database import engine
async def test():
    async with engine.begin() as conn:
        result = await conn.execute('SELECT 1')
        print('Database connection: OK')
asyncio.run(test())
"
```

## Development Workflow

### Daily development:
1. Activate virtual environment: `source venv/bin/activate`
2. Start development server: `make dev`
3. Make changes to code
4. Run tests: `pytest`
5. Format code: `make format`
6. Commit changes

### Adding new features:
1. Create new migration: `alembic revision --autogenerate -m "description"`
2. Apply migration: `alembic upgrade head`
3. Write tests first
4. Implement feature
5. Run tests and ensure they pass

## Next Steps

Once everything is working:
1. Explore the API documentation at http://localhost:8000/docs
2. Try creating, updating, and deleting users
3. Add new domains following the same pattern as `auth/`
4. Customize middleware and add more features
5. Deploy to production when ready

## Quick Commands Reference

```bash
# Setup
cp .env.example .env && pip install -r requirements.txt

# Database
alembic upgrade head

# Run
make dev

# Test
pytest

# Format
make format

# All in one setup
make setup
```