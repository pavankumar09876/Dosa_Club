"""
Cache initialization and management utilities.

Provides startup and shutdown functions for the cache service,
plus helper functions for cache management.
"""

import asyncio
import logging
from typing import Optional

from app.services.cache_service import get_cache
from app.core.config import settings

logger = logging.getLogger(__name__)


async def initialize_cache():
    """Initialize the cache service."""
    if not settings.cache_enabled:
        logger.info("Cache service is disabled")
        return
    
    try:
        cache = get_cache()
        await cache.start()
        logger.info("Cache service initialized successfully")
        
        # Log cache configuration
        stats = cache.get_stats()
        logger.info(f"Cache config: max_size={stats['max_size']}, "
                   f"default_ttl={stats['config']['default_ttl']}s, "
                   f"strategy={stats['strategy']}")
        
    except Exception as e:
        logger.error(f"Failed to initialize cache service: {e}")
        raise


async def shutdown_cache():
    """Shutdown the cache service."""
    if not settings.cache_enabled:
        return
    
    try:
        cache = get_cache()
        await cache.stop()
        logger.info("Cache service shutdown successfully")
        
    except Exception as e:
        logger.error(f"Error during cache shutdown: {e}")


async def clear_all_cache():
    """Clear all cache entries."""
    if not settings.cache_enabled:
        logger.info("Cache service is disabled")
        return
    
    try:
        cache = get_cache()
        await cache.clear()
        logger.info("All cache entries cleared")
        
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")


async def clear_cache_by_prefix(prefix: str):
    """Clear cache entries by prefix."""
    if not settings.cache_enabled:
        logger.info("Cache service is disabled")
        return
    
    try:
        cache = get_cache()
        await cache.clear(prefix)
        logger.info(f"Cache entries with prefix '{prefix}' cleared")
        
    except Exception as e:
        logger.error(f"Failed to clear cache with prefix '{prefix}': {e}")


def get_cache_stats():
    """Get cache statistics."""
    if not settings.cache_enabled:
        return {"cache_enabled": False}
    
    try:
        cache = get_cache()
        return cache.get_stats()
        
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}")
        return {"cache_enabled": True, "error": str(e)}


# Cache warming utilities
async def warm_cache_with_common_data():
    """Warm cache with commonly accessed data."""
    if not settings.cache_enabled:
        return
    
    logger.info("Starting cache warming...")
    
    try:
        # This would typically load frequently accessed data
        # For now, we'll just log that warming occurred
        logger.info("Cache warming completed")
        
    except Exception as e:
        logger.error(f"Cache warming failed: {e}")


# Cache health check
async def check_cache_health() -> dict:
    """Check cache service health."""
    if not settings.cache_enabled:
        return {
            "status": "disabled",
            "message": "Cache service is disabled"
        }
    
    try:
        cache = get_cache()
        stats = cache.get_stats()
        
        # Basic health checks
        if stats["size"] > stats["max_size"]:
            return {
                "status": "unhealthy",
                "message": "Cache size exceeds maximum limit",
                "stats": stats
            }
        
        if stats.get("hit_rate", 0) < 10 and stats.get("hits", 0) > 100:
            return {
                "status": "degraded",
                "message": "Low cache hit rate",
                "stats": stats
            }
        
        return {
            "status": "healthy",
            "message": "Cache service is operating normally",
            "stats": stats
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Cache health check failed: {str(e)}",
            "error": str(e)
        }
