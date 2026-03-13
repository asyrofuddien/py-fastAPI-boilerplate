# FastAPI Best Practices Project Structure

## 📁 Complete Project Layout

```
fastapi-best-practices/
├── 📁 src/                          # Main source code
│   ├── 📁 auth/                     # Authentication domain
│   │   ├── __init__.py
│   │   ├── config.py                # Auth-specific configuration
│   │   ├── dependencies.py          # Auth dependencies & validation
│   │   ├── models.py                # User database model
│   │   ├── router.py                # Auth API endpoints
│   │   ├── schemas.py               # Pydantic models for auth
│   │   ├── service.py               # Auth business logic
│   │   └── utils.py                 # Password hashing, JWT utils
│   ├── __init__.py
│   ├── config.py                    # Global configuration
│   ├── database.py                  # Database connection & session
│   ├── exceptions.py                # Global custom exceptions
│   ├── main.py                      # FastAPI app initialization
│   └── middleware.py                # CORS, logging, security middleware
├── 📁 tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Test configuration & fixtures
│   └── test_auth.py                 # Authentication tests
├── 📁 alembic/                      # Database migrations
│   ├── 📁 versions/                 # Migration files
│   │   └── .gitkeep
│   ├── env.py                       # Alembic environment
│   └── script.py.mako               # Migration template
├── 📁 scripts/                      # Utility scripts
│   └── init_db.py                   # Database initialization
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── alembic.ini                      # Alembic configuration
├── Makefile                         # Development commands
├── PROJECT_STRUCTURE.md             # This file
├── pytest.ini                      # Pytest configuration
├── pyproject.toml                   # Project metadata & tools config
├── README.md                        # Project documentation
├── requirements.txt                 # Python dependencies
└── run.py                          # Quick start script
```

## 🚀 Quick Start Commands

### Setup
```bash
# 1. Install dependencies
make install
# or: pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env with your database credentials

# 3. Create PostgreSQL database
createdb fastapi_db

# 4. Run migrations
make upgrade
# or: alembic upgrade head
```

### Development
```bash
# Start development server
make dev
# or: uvicorn src.main:app --reload

# Run tests
make test
# or: pytest

# Format code
make format
# or: ruff format src tests

# Lint code
make lint
# or: ruff check src tests
```

## 🏗️ Architecture Highlights

### Domain-Driven Structure
- Code organized by business domains (auth, posts, etc.)
- Each domain has its own models, schemas, services, and routes
- Clear separation of concerns

### Best Practices Implemented
- ✅ Async/await for non-blocking I/O
- ✅ Dependency injection for validation
- ✅ JWT-based authentication
- ✅ Proper error handling
- ✅ Database migrations with Alembic
- ✅ Comprehensive testing
- ✅ Code formatting and linting
- ✅ Security middleware
- ✅ Environment-based configuration

### API Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Current user profile
- `GET /auth/users/{user_id}` - Get user by ID
- `PUT /auth/users/{user_id}` - Update user
- `DELETE /auth/users/{user_id}` - Delete user
- `GET /health` - Health check
- `GET /` - API info

## 🔧 Key Features

### Authentication & Authorization
- JWT token-based authentication
- Password hashing with bcrypt
- User registration and login
- Protected routes with dependencies
- User ownership validation

### Database
- PostgreSQL with async SQLAlchemy
- Proper naming conventions
- Database migrations with Alembic
- Connection pooling

### Testing
- Async test client
- In-memory SQLite for tests
- Comprehensive test coverage
- Fixtures for database setup

### Code Quality
- Ruff for formatting and linting
- Type hints throughout
- Pydantic validation
- Error handling with custom exceptions

This project serves as a solid foundation for building scalable FastAPI applications following industry best practices.