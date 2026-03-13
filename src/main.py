from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import text
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

# Health check endpoint with database connection test
@app.get("/health")
async def health_check():
    """Health check endpoint with database connection test."""
    from src.database import engine
    from datetime import datetime
    
    health_status = {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "disconnected",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # Test database connection
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1 as test, NOW() as db_time"))
            row = result.fetchone()
            if row and row[0] == 1:
                health_status["database"] = "connected"
                health_status["database_time"] = str(row[1])
            else:
                health_status["database"] = "error"
                health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Return appropriate HTTP status
    status_code = 200 if health_status["status"] == "healthy" else 503
    return JSONResponse(content=health_status, status_code=status_code)

# Detailed health check endpoint
@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system information."""
    from src.database import engine
    from datetime import datetime
    import sys
    
    health_info = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "environment": settings.ENVIRONMENT,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "database": {
            "status": "disconnected",
            "connection_pool": None
        },
        "services": {
            "auth": "available"
        }
    }
    
    # Add system info if psutil is available
    try:
        import psutil
        health_info["system"] = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }
    except ImportError:
        health_info["system"] = {
            "status": "psutil not installed",
            "install_command": "pip install psutil==5.9.6"
        }
    
    # Test database connection with more details
    try:
        async with engine.begin() as conn:
            # Test basic connection
            result = await conn.execute(text("SELECT 1 as test, NOW() as db_time, version() as db_version"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                health_info["database"]["status"] = "connected"
                health_info["database"]["server_time"] = str(row[1])
                health_info["database"]["version"] = str(row[2]).split(' ')[0]  # Just PostgreSQL version
                
                # Get connection pool info (safe version)
                try:
                    pool = engine.pool
                    pool_info = {
                        "size": pool.size(),
                        "checked_in": pool.checkedin(),
                        "checked_out": pool.checkedout(),
                        "overflow": pool.overflow()
                    }
                    
                    # Try to get invalid count if method exists
                    if hasattr(pool, 'invalid'):
                        try:
                            pool_info["invalid"] = pool.invalid()
                        except Exception:
                            pool_info["invalid"] = "method_error"
                    else:
                        pool_info["invalid"] = "method_not_available"
                    
                    health_info["database"]["connection_pool"] = pool_info
                except Exception as pool_error:
                    health_info["database"]["connection_pool"] = f"error: {str(pool_error)}"
            else:
                health_info["database"]["status"] = "error"
                health_info["status"] = "unhealthy"
                
    except Exception as e:
        health_info["database"]["status"] = f"error: {str(e)}"
        health_info["status"] = "unhealthy"
    
    # Return appropriate HTTP status
    status_code = 200 if health_info["status"] == "healthy" else 503
    return JSONResponse(content=health_info, status_code=status_code)

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
        "docs_url": "/docs" if settings.ENVIRONMENT in SHOW_DOCS_ENVIRONMENT else None,
        "health_url": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "local"
    )