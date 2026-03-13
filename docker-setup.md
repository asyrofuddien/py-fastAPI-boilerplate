# 🐳 Docker Setup Guide for PostgreSQL

Since you're using PostgreSQL in Docker on WSL, here's the complete setup:

## Step 1: Start PostgreSQL with Docker Compose

```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Check if container is running
docker ps
```

## Step 2: Verify Database Connection

```bash
# Test connection to PostgreSQL
docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db -c "SELECT version();"
```

## Step 3: Continue with FastAPI Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run setup verification (this will test DB connection)
python test_setup.py

# Apply database migrations
alembic upgrade head

# Start the FastAPI server
python run.py start
```

## Alternative: Manual Docker Commands

If you prefer manual Docker commands instead of docker-compose:

```bash
# Run PostgreSQL container
docker run -d \
  --name fastapi_postgres \
  -e POSTGRES_DB=fastapi_db \
  -e POSTGRES_USER=fastapi_user \
  -e POSTGRES_PASSWORD=fastapi_password \
  -p 5432:5432 \
  postgres:15

# Check if it's running
docker ps

# Connect to database (optional)
docker exec -it fastapi_postgres psql -U fastapi_user -d fastapi_db
```

## Useful Docker Commands

```bash
# Stop PostgreSQL
docker-compose down

# Start PostgreSQL
docker-compose up -d postgres

# View logs
docker-compose logs postgres

# Remove everything (including data)
docker-compose down -v
```

## Environment Variables

Your `.env` file is already configured for the Docker setup:
```env
DATABASE_URL=postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_db
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-make-it-very-long-and-random
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
ENVIRONMENT=local
```

## Troubleshooting

### Connection refused error:
```bash
# Make sure PostgreSQL container is running
docker ps | grep postgres

# Check container logs
docker logs fastapi_postgres
```

### Port already in use:
```bash
# Check what's using port 5432
sudo netstat -tulpn | grep 5432

# Stop any existing PostgreSQL service
sudo systemctl stop postgresql
```

### Container won't start:
```bash
# Remove existing container and start fresh
docker rm -f fastapi_postgres
docker-compose up -d postgres
```