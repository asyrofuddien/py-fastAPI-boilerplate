.PHONY: install dev test lint format clean migrate upgrade setup

# Install dependencies
install:
	pip install -r requirements.txt

# Run development server
dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=src --cov-report=html

# Lint code
lint:
	ruff check src tests

# Format code
format:
	ruff format src tests
	ruff check --fix src tests

# Create migration
migrate:
	alembic revision --autogenerate -m "$(msg)"

# Apply migrations
upgrade:
	alembic upgrade head

# Clean cache files
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Setup project (first time)
setup: install
	@echo "✅ Dependencies installed!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Copy .env.example to .env and configure"
	@echo "2. Start PostgreSQL: docker-compose up -d postgres"
	@echo "3. Run migrations: make upgrade"
	@echo "4. Start server: make dev"