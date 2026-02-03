"""
DosaClub Main Application.

FastAPI application setup, middleware configuration, and route inclusion.
Implements versioned API structure (v1) for scalability.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.utils.cache_utils import initialize_cache, shutdown_cache
from app.api.v1.routes import user, admin, guest, mobile, cache
import logging

# Setup logging with configured level
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance with all middleware and routes.
    """
    
    # Create FastAPI application instance
    app = FastAPI(
        title=settings.app_name,
        description="In-hotel tablet system for health-aware food suggestions",
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    
    # Add CORS middleware for cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    
    # Include versioned API routes
    logger.info(f"Including API v1 routes with prefix: {settings.api_v1_prefix}")
    app.include_router(
        user.router,
        prefix=settings.api_v1_prefix,
        include_in_schema=True
    )
    app.include_router(
        admin.router,
        prefix=settings.api_v1_prefix,
        include_in_schema=True
    )
    app.include_router(
        guest.router,
        prefix=settings.api_v1_prefix,
        include_in_schema=True
    )
    app.include_router(
        mobile.router,
        prefix=settings.api_v1_prefix
    )
    app.include_router(
        cache.router,
        prefix=settings.api_v1_prefix
    )
    
    return app


# Create application instance
app = create_app()


@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    logger.info("Starting DosaClub application...")
    
    # Initialize cache service
    await initialize_cache()
    
    logger.info("DosaClub application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup services on application shutdown."""
    logger.info("Shutting down DosaClub application...")
    
    # Shutdown cache service
    await shutdown_cache()
    
    logger.info("DosaClub application shutdown complete")


@app.get("/", tags=["health"], summary="Root Endpoint")
async def root():
    """
    Root endpoint for API health check.
    
    Returns:
        dict: Service information and status
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "api_version": "v1",
        "docs": "/docs"
    }


@app.get("/health", tags=["health"], summary="Health Check")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Service health status
    """
    return {
        "status": "ok",
        "service": settings.app_name,
        "message": "DosaClub API is running",
        "version": settings.app_version
    }


@app.get("/api/v1", tags=["health"], summary="API v1 Info")
async def api_v1_info():
    """
    API v1 information endpoint.
    
    Returns:
        dict: Available endpoints and API version info
    """
    return {
        "api_version": "v1",
        "base_path": settings.api_v1_prefix,
        "routes": {
            "user": {
                "intake": f"{settings.api_v1_prefix}/user/intake",
                "suggest_item": f"{settings.api_v1_prefix}/user/suggest-item"
            },
            "admin": {
                "menu": f"{settings.api_v1_prefix}/admin/menu",
                "health_rule": f"{settings.api_v1_prefix}/admin/health-rule",
                "users": f"{settings.api_v1_prefix}/admin/users",
                "suggestions": f"{settings.api_v1_prefix}/admin/suggestions"
            }
        },
        "documentation": "/docs"
    }

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info("→ %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("← %s %s %s", request.method, request.url.path, response.status_code)
    return response

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
