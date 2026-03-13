.PHONY: install run test lint format clean migrate

# Install dependencies
install:
	pip install -r requirements.txt

# Run the application
run:
	python -m src.main

# Run with uvicorn
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

# Rollback migration
downgrade:
	alembic downgrade -1

# Clean cache files
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Setup project
setup: install
	@echo "Project setup complete!"
	@echo "Next steps:"
	@echo "1. Copy .env.example to .env and configure"
	@echo "2. Create PostgreSQL database"
	@echo "3. Run 'make upgrade' to apply migrations"
	@echo "4. Run 'make dev' to start development server"