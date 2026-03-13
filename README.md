# FastAPI Best Practices Boilerplate

A production-ready FastAPI boilerplate following industry best practices for scalable, maintainable applications.

## ✨ Features

- **Domain-driven architecture** - Code organized by business domains
- **Async/await support** - Proper async handling for optimal performance  
- **JWT Authentication** - Secure token-based authentication with bcrypt
- **Database integration** - PostgreSQL with async SQLAlchemy + Alembic migrations
- **Comprehensive testing** - Async test client with pytest
- **Input validation** - Pydantic schemas with built-in validators
- **Middleware support** - CORS, logging, and security middleware
- **Health checks** - Basic and detailed health endpoints with DB monitoring
- **Code quality** - Ruff for formatting and linting
- **Docker support** - Easy PostgreSQL setup with Docker Compose

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo>
cd fastapi-boilerplate
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Database Setup
```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Run migrations
alembic upgrade head
```

### 4. Run Application
```bash
# Development server
python -m src.main

# Or using the helper script
python run.py start
```

Visit:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
src/
├── auth/                 # Authentication domain
│   ├── router.py        # API endpoints
│   ├── schemas.py       # Pydantic models
│   ├── models.py        # Database models
│   ├── service.py       # Business logic
│   ├── dependencies.py  # Route dependencies
│   ├── config.py        # Domain configuration
│   └── utils.py         # Helper functions
├── config.py            # Global configuration
├── database.py          # Database connection
├── exceptions.py        # Global exceptions
├── middleware.py        # Application middleware
└── main.py             # FastAPI app initialization
```

## 🔧 Available Commands

```bash
# Using run.py helper script
python run.py setup        # Install dependencies and setup
python run.py docker-up    # Start PostgreSQL with Docker
python run.py docker-down  # Stop PostgreSQL
python run.py start        # Start development server
python run.py test         # Run tests
python run.py verify       # Verify setup

# Using Makefile
make install    # Install dependencies
make dev        # Start development server
make test       # Run tests
make format     # Format code with ruff
make lint       # Lint code with ruff
```

## 🗄️ Database

### Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Naming Conventions
- Tables: `user`, `post`, `user_profile` (singular, snake_case)
- Columns: `created_at`, `updated_at`, `birth_date`
- Indexes: Auto-generated with descriptive names

## 🔐 Authentication

### Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user profile
- `GET /auth/users/{user_id}` - Get user by ID
- `PUT /auth/users/{user_id}` - Update user (owner only)
- `DELETE /auth/users/{user_id}` - Delete user (owner only)

### Usage Example
```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secret123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secret123"}'

# Use token in subsequent requests
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## 🏗️ Adding New Domains

1. Create domain directory: `src/your_domain/`
2. Add required files: `router.py`, `schemas.py`, `models.py`, `service.py`
3. Register router in `src/main.py`:
```python
from src.your_domain.router import router as your_domain_router
app.include_router(your_domain_router, prefix="/your-domain", tags=["Your Domain"])
```

## 🔍 Health Monitoring

- **Basic**: `GET /health` - Database connection status
- **Detailed**: `GET /health/detailed` - System metrics, connection pool info

## 📦 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `JWT_SECRET` | Secret key for JWT tokens | Required |
| `JWT_ALGORITHM` | JWT algorithm | HS256 |
| `JWT_EXPIRATION_HOURS` | Token expiration time | 24 |
| `ENVIRONMENT` | Application environment | local |

## 🚢 Production Deployment

1. Set `ENVIRONMENT=production`
2. Use strong `JWT_SECRET`
3. Configure proper database connection
4. Set up reverse proxy (nginx)
5. Use process manager (systemd, supervisor)
6. Enable HTTPS with SSL certificates

## 🛠️ Development Guidelines

- Follow domain-driven structure for new features
- Use async routes for I/O operations
- Implement proper error handling
- Write tests for new functionality
- Use dependency injection for validation
- Follow database naming conventions

## 📝 License

MIT License - feel free to use this boilerplate for your projects!