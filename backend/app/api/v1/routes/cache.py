"""
Cache management API endpoints.

Provides endpoints for monitoring and managing the cache service.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from app.utils.cache_utils import get_cache_stats, clear_all_cache, clear_cache_by_prefix, check_cache_health
from app.core.config import settings

router = APIRouter(
    prefix="/cache",
    tags=["cache"]
)


@router.get("/stats", summary="Get Cache Statistics")
async def get_cache_statistics():
    """
    Get comprehensive cache statistics.
    
    Returns:
        dict: Cache performance metrics and configuration
    """
    try:
        stats = get_cache_stats()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get cache statistics: {str(e)}"
        )


@router.get("/health", summary="Check Cache Health")
async def get_cache_health():
    """
    Check the health of the cache service.
    
    Returns:
        dict: Cache health status and diagnostics
    """
    try:
        health = await check_cache_health()
        status_code = 200 if health["status"] == "healthy" else 503
        
        return {
            "success": health["status"] == "healthy",
            "data": health
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cache health check failed: {str(e)}"
        )


@router.post("/clear", summary="Clear All Cache")
async def clear_cache():
    """
    Clear all cache entries.
    
    Returns:
        dict: Operation result
    """
    if not settings.cache_enabled:
        return {
            "success": False,
            "message": "Cache service is disabled"
        }
    
    try:
        await clear_all_cache()
        return {
            "success": True,
            "message": "All cache entries cleared successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )


@router.post("/clear/{prefix}", summary="Clear Cache by Prefix")
async def clear_cache_prefix(prefix: str):
    """
    Clear cache entries by prefix.
    
    Args:
        prefix: Cache prefix to clear
        
    Returns:
        dict: Operation result
    """
    if not settings.cache_enabled:
        return {
            "success": False,
            "message": "Cache service is disabled"
        }
    
    try:
        await clear_cache_by_prefix(prefix)
        return {
            "success": True,
            "message": f"Cache entries with prefix '{prefix}' cleared successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache with prefix '{prefix}': {str(e)}"
        )


@router.get("/config", summary="Get Cache Configuration")
async def get_cache_config():
    """
    Get current cache configuration.
    
    Returns:
        dict: Cache configuration settings
    """
    return {
        "success": True,
        "data": {
            "cache_enabled": settings.cache_enabled,
            "cache_ttl": settings.cache_ttl,
            "cache_max_size": settings.cache_max_size,
            "circuit_breaker_failure_threshold": settings.circuit_breaker_failure_threshold,
            "circuit_breaker_recovery_timeout": settings.circuit_breaker_recovery_timeout,
            "retry_max_attempts": settings.retry_max_attempts,
            "retry_base_delay": settings.retry_base_delay,
            "retry_max_delay": settings.retry_max_delay
        }
    }
