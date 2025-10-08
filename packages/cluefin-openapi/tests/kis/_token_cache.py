"""Token cache utility for KIS integration tests.

This module provides persistent token caching to avoid hitting the 1-minute
rate limit when running integration tests multiple times.
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from loguru import logger

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._auth_types import TokenResponse


class TokenCache:
    """Persistent token cache that saves tokens to disk."""

    def __init__(self, auth: Auth, cache_file: Optional[Path] = None, min_interval: int = 65) -> None:
        """
        Initialize the token cache.

        Args:
            auth: Auth instance to generate tokens
            cache_file: Path to cache file (default: .kis_token_cache.json in tests dir)
            min_interval: Minimum seconds between token generations (default: 65)
        """
        self._auth = auth
        self._min_interval = min_interval
        self._cache_file = cache_file or Path(__file__).parent / ".kis_token_cache.json"
        self._token: Optional[TokenResponse] = None
        self._last_generated_at: float = 0.0

    def get(self, force_refresh: bool = False) -> TokenResponse:
        """
        Get a valid token, either from cache or by generating a new one.

        Args:
            force_refresh: If True, force generate a new token

        Returns:
            TokenResponse: A valid access token
        """
        if force_refresh:
            self.clear()

        # Try to load from memory cache first
        if self._token is not None and self._is_token_valid(self._token):
            logger.debug("Using token from memory cache")
            return self._token

        # Try to load from disk cache
        cached_token = self._load_from_disk()
        if cached_token is not None and self._is_token_valid(cached_token):
            logger.debug("Using token from disk cache")
            self._token = cached_token
            return self._token

        # Need to generate a new token
        logger.debug("Generating new token")
        now = time.monotonic()
        if self._last_generated_at and now - self._last_generated_at < self._min_interval:
            wait_time = self._min_interval - (now - self._last_generated_at)
            logger.warning(f"Rate limit: waiting {wait_time:.1f} seconds before generating new token")
            time.sleep(wait_time)

        self._token = self._auth.generate()
        self._last_generated_at = time.monotonic()
        self._save_to_disk(self._token)
        return self._token

    def clear(self) -> None:
        """Clear the token cache (both memory and disk)."""
        self._token = None
        if self._cache_file.exists():
            self._cache_file.unlink()
            logger.debug(f"Cleared token cache file: {self._cache_file}")

    def _is_token_valid(self, token: TokenResponse) -> bool:
        """
        Check if a token is still valid.

        Args:
            token: Token to check

        Returns:
            bool: True if token is still valid
        """
        try:
            # Parse the expiration timestamp
            # Format: "YYYY-MM-DD HH:MM:SS"
            expiry = datetime.strptime(token.access_token_token_expired, "%Y-%m-%d %H:%M:%S")
            # Add a 5-minute buffer to avoid using tokens that are about to expire
            return datetime.now() < (expiry - timedelta(minutes=5))
        except Exception as e:
            logger.warning(f"Failed to parse token expiration: {e}")
            return False

    def _load_from_disk(self) -> Optional[TokenResponse]:
        """
        Load token from disk cache.

        Returns:
            Optional[TokenResponse]: Token if found and valid, None otherwise
        """
        if not self._cache_file.exists():
            return None

        try:
            with open(self._cache_file, "r") as f:
                data = json.load(f)
            token = TokenResponse(**data)
            logger.debug(f"Loaded token from cache file: {self._cache_file}")
            return token
        except Exception as e:
            logger.warning(f"Failed to load token from cache: {e}")
            return None

    def _save_to_disk(self, token: TokenResponse) -> None:
        """
        Save token to disk cache.

        Args:
            token: Token to save
        """
        try:
            with open(self._cache_file, "w") as f:
                json.dump(token.model_dump(), f, indent=2)
            logger.debug(f"Saved token to cache file: {self._cache_file}")
        except Exception as e:
            logger.warning(f"Failed to save token to cache: {e}")
