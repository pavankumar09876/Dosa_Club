"""
Cache Service for DynamoDB Operations.

Provides intelligent caching with TTL, size limits, and fallback capabilities.
Supports both in-memory and distributed caching strategies.
"""

import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import hashlib

from app.core.config import settings
from app.utils.exceptions import CacheException

logger = logging.getLogger(__name__)


class CacheStrategy(Enum):
    """Cache eviction strategies."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    FIFO = "fifo"  # First In First Out
    TTL = "ttl"  # Time To Live only


@dataclass
class CacheItem:
    """Cache item with metadata."""
    value: Any
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    ttl: Optional[int] = None  # TTL in seconds
    
    def is_expired(self) -> bool:
        """Check if item is expired based on TTL."""
        if self.ttl is None:
            return False
        return (datetime.utcnow() - self.created_at).total_seconds() > self.ttl
    
    def touch(self):
        """Update access metadata."""
        self.last_accessed = datetime.utcnow()
        self.access_count += 1


@dataclass
class CacheConfig:
    """Configuration for cache service."""
    max_size: int = 1000
    default_ttl: int = 300  # 5 minutes
    strategy: CacheStrategy = CacheStrategy.LRU
    enable_stats: bool = True
    cleanup_interval: int = 60  # seconds


class CacheStats:
    """Cache statistics."""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.sets = 0
        self.deletes = 0
        self.evictions = 0
        self.start_time = datetime.utcnow()
    
    def get_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        return {
            "hits": self.hits,
            "misses": self.misses,
            "sets": self.sets,
            "deletes": self.deletes,
            "evictions": self.evictions,
            "hit_rate": self.get_hit_rate(),
            "uptime_seconds": uptime,
            "hits_per_second": self.hits / uptime if uptime > 0 else 0
        }


class InMemoryCache:
    """
    In-memory cache implementation with multiple eviction strategies.
    """
    
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self._cache: Dict[str, CacheItem] = {}
        self._access_order: List[str] = []  # For LRU/FIFO
        self._stats = CacheStats() if self.config.enable_stats else None
        self._cleanup_task: Optional[asyncio.Task] = None
        self._running = False
    
    async def start(self):
        """Start the cache service."""
        if self._running:
            return
        
        self._running = True
        if self.config.cleanup_interval > 0:
            self._cleanup_task = asyncio.create_task(self._cleanup_expired())
        logger.info(f"Cache service started with max_size={self.config.max_size}")
    
    async def stop(self):
        """Stop the cache service."""
        self._running = False
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        logger.info("Cache service stopped")
    
    def _make_key(self, key: str, prefix: Optional[str] = None) -> str:
        """Create a cache key with optional prefix."""
        if prefix:
            return f"{prefix}:{key}"
        return key
    
    def _evict_item(self) -> Optional[str]:
        """Evict an item based on the configured strategy."""
        if not self._cache:
            return None
        
        if self.config.strategy == CacheStrategy.LRU:
            # Find least recently used item
            oldest_key = min(self._cache.keys(), 
                           key=lambda k: self._cache[k].last_accessed)
            return oldest_key
        
        elif self.config.strategy == CacheStrategy.LFU:
            # Find least frequently used item
            least_used_key = min(self._cache.keys(), 
                               key=lambda k: self._cache[k].access_count)
            return least_used_key
        
        elif self.config.strategy == CacheStrategy.FIFO:
            # Remove first item added
            return self._access_order[0] if self._access_order else None
        
        elif self.config.strategy == CacheStrategy.TTL:
            # Find expired item first, then oldest
            for key, item in self._cache.items():
                if item.is_expired():
                    return key
            # Fallback to oldest
            oldest_key = min(self._cache.keys(), 
                           key=lambda k: self._cache[k].created_at)
            return oldest_key
        
        return None
    
    def _enforce_size_limit(self):
        """Enforce maximum cache size."""
        while len(self._cache) >= self.config.max_size:
            evicted_key = self._evict_item()
            if evicted_key:
                del self._cache[evicted_key]
                if evicted_key in self._access_order:
                    self._access_order.remove(evicted_key)
                if self._stats:
                    self._stats.evictions += 1
                logger.debug(f"Evicted cache item: {evicted_key}")
            else:
                break
    
    async def get(self, key: str, prefix: Optional[str] = None) -> Optional[Any]:
        """Get item from cache."""
        cache_key = self._make_key(key, prefix)
        
        if cache_key not in self._cache:
            if self._stats:
                self._stats.misses += 1
            return None
        
        item = self._cache[cache_key]
        
        # Check if expired
        if item.is_expired():
            del self._cache[cache_key]
            if cache_key in self._access_order:
                self._access_order.remove(cache_key)
            if self._stats:
                self._stats.misses += 1
            return None
        
        # Update access metadata
        item.touch()
        if self._stats:
            self._stats.hits += 1
        
        logger.debug(f"Cache hit: {cache_key}")
        return item.value
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None,
        prefix: Optional[str] = None
    ):
        """Set item in cache."""
        cache_key = self._make_key(key, prefix)
        
        # Use default TTL if not provided
        if ttl is None:
            ttl = self.config.default_ttl
        
        # Enforce size limit before adding new item
        self._enforce_size_limit()
        
        # Create cache item
        item = CacheItem(
            value=value,
            created_at=datetime.utcnow(),
            last_accessed=datetime.utcnow(),
            ttl=ttl
        )
        
        self._cache[cache_key] = item
        
        # Update access order for FIFO/LRU
        if cache_key not in self._access_order:
            self._access_order.append(cache_key)
        
        if self._stats:
            self._stats.sets += 1
        
        logger.debug(f"Cache set: {cache_key} (TTL: {ttl}s)")
    
    async def delete(self, key: str, prefix: Optional[str] = None):
        """Delete item from cache."""
        cache_key = self._make_key(key, prefix)
        
        if cache_key in self._cache:
            del self._cache[cache_key]
            if cache_key in self._access_order:
                self._access_order.remove(cache_key)
            if self._stats:
                self._stats.deletes += 1
            logger.debug(f"Cache delete: {cache_key}")
    
    async def clear(self, prefix: Optional[str] = None):
        """Clear cache items, optionally by prefix."""
        if prefix:
            keys_to_delete = [k for k in self._cache.keys() if k.startswith(f"{prefix}:")]
            for key in keys_to_delete:
                del self._cache[key]
                if key in self._access_order:
                    self._access_order.remove(key)
            logger.debug(f"Cleared cache items with prefix: {prefix}")
        else:
            self._cache.clear()
            self._access_order.clear()
            logger.debug("Cleared all cache items")
    
    async def _cleanup_expired(self):
        """Background task to cleanup expired items."""
        while self._running:
            try:
                expired_keys = [
                    key for key, item in self._cache.items() 
                    if item.is_expired()
                ]
                
                for key in expired_keys:
                    del self._cache[key]
                    if key in self._access_order:
                        self._access_order.remove(key)
                    if self._stats:
                        self._stats.evictions += 1
                
                if expired_keys:
                    logger.debug(f"Cleaned up {len(expired_keys)} expired cache items")
                
                await asyncio.sleep(self.config.cleanup_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Cache cleanup error: {e}")
                await asyncio.sleep(self.config.cleanup_interval)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = {
            "size": len(self._cache),
            "max_size": self.config.max_size,
            "strategy": self.config.strategy.value,
            "config": {
                "default_ttl": self.config.default_ttl,
                "cleanup_interval": self.config.cleanup_interval
            }
        }
        
        if self._stats:
            stats.update(self._stats.get_stats())
        
        return stats
    
    def get_keys(self, prefix: Optional[str] = None) -> List[str]:
        """Get all cache keys, optionally filtered by prefix."""
        if prefix:
            return [k for k in self._cache.keys() if k.startswith(f"{prefix}:")]
        return list(self._cache.keys())


# Global cache instance
_cache: Optional[InMemoryCache] = None


def get_cache() -> InMemoryCache:
    """Get or create global cache instance."""
    global _cache
    if _cache is None:
        config = CacheConfig(
            max_size=settings.cache_max_size,
            default_ttl=settings.cache_ttl,
            strategy=CacheStrategy.LRU,
            enable_stats=True,
            cleanup_interval=60
        )
        _cache = InMemoryCache(config)
    return _cache


async def cache_get(key: str, prefix: Optional[str] = None) -> Optional[Any]:
    """Convenience function to get from cache."""
    cache = get_cache()
    return await cache.get(key, prefix)


async def cache_set(
    key: str, 
    value: Any, 
    ttl: Optional[int] = None,
    prefix: Optional[str] = None
):
    """Convenience function to set in cache."""
    cache = get_cache()
    await cache.set(key, value, ttl, prefix)


async def cache_delete(key: str, prefix: Optional[str] = None):
    """Convenience function to delete from cache."""
    cache = get_cache()
    await cache.delete(key, prefix)


async def cache_clear(prefix: Optional[str] = None):
    """Convenience function to clear cache."""
    cache = get_cache()
    await cache.clear(prefix)


def cache_key(*args, **kwargs) -> str:
    """Generate a consistent cache key from arguments."""
    # Create a deterministic string representation
    key_parts = []
    
    # Add positional arguments
    for arg in args:
        if isinstance(arg, (str, int, float, bool)):
            key_parts.append(str(arg))
        else:
            key_parts.append(json.dumps(arg, sort_keys=True, default=str))
    
    # Add keyword arguments
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}={v}")
    
    # Create hash for long keys
    key_string = ":".join(key_parts)
    if len(key_string) > 100:
        key_string = hashlib.md5(key_string.encode()).hexdigest()
    
    return key_string
