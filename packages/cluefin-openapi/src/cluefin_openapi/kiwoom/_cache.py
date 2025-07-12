"""Caching utilities for Kiwoom API client."""

import hashlib
import time
from typing import Any, Dict, Optional


class SimpleCache:
    """Simple in-memory cache with TTL support."""

    def __init__(self, default_ttl: int = 300):
        """
        Initialize cache.

        Args:
            default_ttl: Default time-to-live in seconds (default: 5 minutes)
        """
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry["expires_at"]:
                return entry["value"]
            else:
                # Remove expired entry
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        if ttl is None:
            ttl = self.default_ttl

        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
            "created_at": time.time(),
        }

    def delete(self, key: str) -> bool:
        """
        Delete key from cache.

        Args:
            key: Cache key

        Returns:
            True if key was deleted, False if not found
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()

    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache.

        Returns:
            Number of entries removed
        """
        current_time = time.time()
        expired_keys = [key for key, entry in self._cache.items() if current_time >= entry["expires_at"]]

        for key in expired_keys:
            del self._cache[key]

        return len(expired_keys)

    def cache_info(self) -> Dict[str, Any]:
        """Get cache statistics."""
        current_time = time.time()
        valid_entries = sum(1 for entry in self._cache.values() if current_time < entry["expires_at"])

        return {
            "total_entries": len(self._cache),
            "valid_entries": valid_entries,
            "expired_entries": len(self._cache) - valid_entries,
        }


def create_cache_key(url: str, headers: Dict[str, str], body: Dict[str, Any]) -> str:
    """
    Create a cache key from request parameters.

    Args:
        url: Request URL
        headers: Request headers (excluding auth and dynamic headers)
        body: Request body

    Returns:
        Cache key string
    """
    # Filter out dynamic headers that shouldn't affect caching
    cacheable_headers = {
        k: v for k, v in headers.items() if k.lower() not in ["authorization", "user-agent", "content-length"]
    }

    # Create a deterministic string representation
    cache_data = {
        "url": url,
        "headers": sorted(cacheable_headers.items()),
        "body": sorted(body.items()) if isinstance(body, dict) else body,
    }

    # Create hash of the cache data
    cache_string = str(cache_data)
    return hashlib.sha256(cache_string.encode()).hexdigest()[:16]  # First 16 chars for brevity
