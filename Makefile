.PHONY: install dev test lint format clean migrate upgrade setup new-domain list-domains

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

# Create new domain structure
new-domain:
	@if [ -z "$(name)" ]; then \
		echo "❌ Error: Domain name is required"; \
		echo "Usage: make new-domain name=your_domain_name"; \
		exit 1; \
	fi
	@if [ -d "src/$(name)" ]; then \
		echo "❌ Error: Domain '$(name)' already exists"; \
		exit 1; \
	fi
	@echo "🚀 Creating new domain: $(name)"
	@mkdir -p src/$(name)
	@echo "# $(name) domain" > src/$(name)/__init__.py
	@echo "from sqlalchemy import Column, Integer, String, DateTime, Boolean" > src/$(name)/models.py
	@echo "from sqlalchemy.ext.declarative import declarative_base" >> src/$(name)/models.py
	@echo "from datetime import datetime" >> src/$(name)/models.py
	@echo "" >> src/$(name)/models.py
	@echo "Base = declarative_base()" >> src/$(name)/models.py
	@echo "" >> src/$(name)/models.py
	@echo "" >> src/$(name)/models.py
	@echo "class $(shell echo $(name) | sed 's/.*/\u&/')(Base):" >> src/$(name)/models.py
	@echo "    __tablename__ = \"$(name)s\"" >> src/$(name)/models.py
	@echo "" >> src/$(name)/models.py
	@echo "    id = Column(Integer, primary_key=True, index=True)" >> src/$(name)/models.py
	@echo "    created_at = Column(DateTime, default=datetime.utcnow)" >> src/$(name)/models.py
	@echo "    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)" >> src/$(name)/models.py
	@echo "from pydantic import BaseModel" > src/$(name)/schemas.py
	@echo "from datetime import datetime" >> src/$(name)/schemas.py
	@echo "from typing import Optional" >> src/$(name)/schemas.py
	@echo "" >> src/$(name)/schemas.py
	@echo "" >> src/$(name)/schemas.py
	@echo "class $(shell echo $(name) | sed 's/.*/\u&/')Base(BaseModel):" >> src/$(name)/schemas.py
	@echo "    pass" >> src/$(name)/schemas.py
	@echo "" >> src/$(name)/schemas.py
	@echo "" >> src/$(name)/schemas.py
	@echo "class $(shell echo $(name) | sed 's/.*/\u&/')Create($(shell echo $(name) | sed 's/.*/\u&/')Base):" >> src/$(name)/schemas.py
	@echo "    pass" >> src/$(name)/schemas.py
	@echo "" >> src/$(name)/schemas.py
	@echo "" >> src/$(name)/schemas.py
	@echo "class $(shell echo $(name) | sed 's/.*/\u&/')Update($(shell echo $(name) | sed 's/.*/\u&/')Base):" >> src/$(name)/schemas.py
	@echo "    pass" >> src/$(name)/schemas.py
	@echo "" >> src/$(name)/schemas.py
	@echo "" >> src/$(name)/schemas.py
	@echo "class $(shell echo $(name) | sed 's/.*/\u&/')Response($(shell echo $(name) | sed 's/.*/\u&/')Base):" >> src/$(name)/schemas.py
	@echo "    id: int" >> src/$(name)/schemas.py
	@echo "    created_at: datetime" >> src/$(name)/schemas.py
	@echo "    updated_at: datetime" >> src/$(name)/schemas.py
	@echo "" >> src/$(name)/schemas.py
	@echo "    class Config:" >> src/$(name)/schemas.py
	@echo "        from_attributes = True" >> src/$(name)/schemas.py
	@echo "from sqlalchemy.orm import Session" > src/$(name)/service.py
	@echo "from typing import List, Optional" >> src/$(name)/service.py
	@echo "from . import models, schemas" >> src/$(name)/service.py
	@echo "" >> src/$(name)/service.py
	@echo "" >> src/$(name)/service.py
	@echo "class $(shell echo $(name) | sed 's/.*/\u&/')Service:" >> src/$(name)/service.py
	@echo "    def __init__(self, db: Session):" >> src/$(name)/service.py
	@echo "        self.db = db" >> src/$(name)/service.py
	@echo "" >> src/$(name)/service.py
	@echo "    def get_all(self) -> List[models.$(shell echo $(name) | sed 's/.*/\u&/')]:" >> src/$(name)/service.py
	@echo "        return self.db.query(models.$(shell echo $(name) | sed 's/.*/\u&/')).all()" >> src/$(name)/service.py
	@echo "" >> src/$(name)/service.py
	@echo "    def get_by_id(self, id: int) -> Optional[models.$(shell echo $(name) | sed 's/.*/\u&/')]:" >> src/$(name)/service.py
	@echo "        return self.db.query(models.$(shell echo $(name) | sed 's/.*/\u&/')).filter(models.$(shell echo $(name) | sed 's/.*/\u&/').id == id).first()" >> src/$(name)/service.py
	@echo "" >> src/$(name)/service.py
	@echo "    def create(self, data: schemas.$(shell echo $(name) | sed 's/.*/\u&/')Create) -> models.$(shell echo $(name) | sed 's/.*/\u&/'):" >> src/$(name)/service.py
	@echo "        db_obj = models.$(shell echo $(name) | sed 's/.*/\u&/')(**data.dict())" >> src/$(name)/service.py
	@echo "        self.db.add(db_obj)" >> src/$(name)/service.py
	@echo "        self.db.commit()" >> src/$(name)/service.py
	@echo "        self.db.refresh(db_obj)" >> src/$(name)/service.py
	@echo "        return db_obj" >> src/$(name)/service.py
	@echo "from fastapi import APIRouter, Depends, HTTPException" > src/$(name)/router.py
	@echo "from sqlalchemy.orm import Session" >> src/$(name)/router.py
	@echo "from typing import List" >> src/$(name)/router.py
	@echo "from ..database import get_db" >> src/$(name)/router.py
	@echo "from . import schemas, service" >> src/$(name)/router.py
	@echo "" >> src/$(name)/router.py
	@echo "" >> src/$(name)/router.py
	@echo "router = APIRouter(prefix=\"/$(name)\", tags=[\"$(name)\"])" >> src/$(name)/router.py
	@echo "" >> src/$(name)/router.py
	@echo "" >> src/$(name)/router.py
	@echo "@router.get(\"/\", response_model=List[schemas.$(shell echo $(name) | sed 's/.*/\u&/')Response])" >> src/$(name)/router.py
	@echo "def get_$(name)s(db: Session = Depends(get_db)):" >> src/$(name)/router.py
	@echo "    $(name)_service = service.$(shell echo $(name) | sed 's/.*/\u&/')Service(db)" >> src/$(name)/router.py
	@echo "    return $(name)_service.get_all()" >> src/$(name)/router.py
	@echo "" >> src/$(name)/router.py
	@echo "" >> src/$(name)/router.py
	@echo "@router.get(\"/{id}\", response_model=schemas.$(shell echo $(name) | sed 's/.*/\u&/')Response)" >> src/$(name)/router.py
	@echo "def get_$(name)(id: int, db: Session = Depends(get_db)):" >> src/$(name)/router.py
	@echo "    $(name)_service = service.$(shell echo $(name) | sed 's/.*/\u&/')Service(db)" >> src/$(name)/router.py
	@echo "    $(name) = $(name)_service.get_by_id(id)" >> src/$(name)/router.py
	@echo "    if not $(name):" >> src/$(name)/router.py
	@echo "        raise HTTPException(status_code=404, detail=\"$(shell echo $(name) | sed 's/.*/\u&/') not found\")" >> src/$(name)/router.py
	@echo "    return $(name)" >> src/$(name)/router.py
	@echo "" >> src/$(name)/router.py
	@echo "" >> src/$(name)/router.py
	@echo "@router.post(\"/\", response_model=schemas.$(shell echo $(name) | sed 's/.*/\u&/')Response)" >> src/$(name)/router.py
	@echo "def create_$(name)(data: schemas.$(shell echo $(name) | sed 's/.*/\u&/')Create, db: Session = Depends(get_db)):" >> src/$(name)/router.py
	@echo "    $(name)_service = service.$(shell echo $(name) | sed 's/.*/\u&/')Service(db)" >> src/$(name)/router.py
	@echo "    return $(name)_service.create(data)" >> src/$(name)/router.py
	@mkdir -p tests/$(name)
	@echo "# Tests for $(name) domain" > tests/$(name)/__init__.py
	@echo "import pytest" > tests/$(name)/test_$(name).py
	@echo "from fastapi.testclient import TestClient" >> tests/$(name)/test_$(name).py
	@echo "from src.main import app" >> tests/$(name)/test_$(name).py
	@echo "" >> tests/$(name)/test_$(name).py
	@echo "" >> tests/$(name)/test_$(name).py
	@echo "client = TestClient(app)" >> tests/$(name)/test_$(name).py
	@echo "" >> tests/$(name)/test_$(name).py
	@echo "" >> tests/$(name)/test_$(name).py
	@echo "def test_get_$(name)s():" >> tests/$(name)/test_$(name).py
	@echo "    response = client.get(\"/$(name)/\")" >> tests/$(name)/test_$(name).py
	@echo "    assert response.status_code == 200" >> tests/$(name)/test_$(name).py
	@echo "    assert isinstance(response.json(), list)" >> tests/$(name)/test_$(name).py
	@echo "✅ Domain '$(name)' created successfully!"
	@echo ""
	@echo "📁 Created files:"
	@echo "   src/$(name)/__init__.py"
	@echo "   src/$(name)/models.py"
	@echo "   src/$(name)/schemas.py"
	@echo "   src/$(name)/service.py"
	@echo "   src/$(name)/router.py"
	@echo "   tests/$(name)/__init__.py"
	@echo "   tests/$(name)/test_$(name).py"
	@echo ""
	@echo "📝 Next steps:"
	@echo "1. Add your domain-specific fields to models.py and schemas.py"
	@echo "2. Import and include the router in src/main.py:"
	@echo "   from src.$(name).router import router as $(name)_router"
	@echo "   app.include_router($(name)_router)"
	@echo "3. Create and run migration: make migrate msg='Add $(name) domain'"
	@echo "4. Run tests: make test"

# List all existing domains
list-domains:
	@echo "📂 Existing domains:"
	@for dir in src/*/; do \
		if [ -d "$$dir" ] && [ "$$(basename $$dir)" != "__pycache__" ]; then \
			domain=$$(basename $$dir); \
			echo "   - $$domain"; \
		fi \
	done
	@echo ""
	@echo "💡 To create a new domain: make new-domain name=your_domain_name"