from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.config import settings
from src.middleware import setup_middleware
from src.auth.router import router as auth_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine if docs should be shown
SHOW_DOCS_ENVIRONMENT = ("local", "staging")

# App configuration
app_configs = {
    "title": "FastAPI Best Practices API",
    "description": "A FastAPI application following best practices",
    "version": "1.0.0"
}

if settings.ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
    app_configs["openapi_url"] = None

# Create FastAPI app
app = FastAPI(**app_configs)

# Setup middleware
setup_middleware(app)

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

# Include routers
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "FastAPI Best Practices API",
        "version": "1.0.0",
        "docs_url": "/docs" if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "local"
    )