# FastAPI Best Practices Project

A FastAPI application following industry best practices for scalable, maintainable web applications.

## Features

- **Domain-driven architecture** - Code organized by business domains
- **Async/await support** - Proper async handling for optimal performance
- **JWT Authentication** - Secure token-based authentication
- **Database migrations** - Alembic for database schema management
- **Comprehensive testing** - Async test client with pytest
- **Input validation** - Pydantic schemas with built-in validators
- **Middleware support** - CORS, logging, and security middleware
- **API documentation** - Auto-generated OpenAPI docs

## Project Structure

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

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and JWT secret
   ```

3. **Set up PostgreSQL database:**
   ```bash
   # Create database
   createdb fastapi_db
   ```

4. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the application:**
   ```bash
   python -m src.main
   # or
   uvicorn src.main:app --reload
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user profile
- `GET /auth/users/{user_id}` - Get user by ID
- `PUT /auth/users/{user_id}` - Update user (owner only)
- `DELETE /auth/users/{user_id}` - Delete user (owner only)

### Health Check
- `GET /health` - Application health status
- `GET /` - API information

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src
```

## Code Quality

Format code:
```bash
ruff format src tests
```

Lint code:
```bash
ruff check src tests
```

Fix linting issues:
```bash
ruff check --fix src tests
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `JWT_SECRET` | Secret key for JWT tokens | Required |
| `JWT_ALGORITHM` | JWT algorithm | HS256 |
| `JWT_EXPIRATION_HOURS` | Token expiration time | 24 |
| `ENVIRONMENT` | Application environment | local |

## Best Practices Implemented

- **Async routes** for non-blocking I/O operations
- **Dependency injection** for validation and authentication
- **Domain-driven structure** for better code organization
- **Proper error handling** with custom exceptions
- **Database naming conventions** following PostgreSQL standards
- **Security middleware** for CORS and trusted hosts
- **Comprehensive logging** with request/response tracking
- **Type hints** throughout the codebase
- **Pydantic validation** with built-in validators

## Production Deployment

1. Set `ENVIRONMENT=production` in your environment
2. Configure proper database connection string
3. Set up reverse proxy (nginx)
4. Use process manager (systemd, supervisor)
5. Enable HTTPS with SSL certificates
6. Configure monitoring and logging

## Contributing

1. Follow the established project structure
2. Write tests for new features
3. Use proper async/await patterns
4. Follow naming conventions
5. Update documentation as needed