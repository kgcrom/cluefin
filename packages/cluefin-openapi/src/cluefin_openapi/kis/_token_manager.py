"""Token manager for KIS API authentication with local caching."""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from loguru import logger

from cluefin_openapi.kis._auth_types import TokenResponse


class TokenManager:
    """Manages KIS API token generation and caching.

    Caches tokens locally to avoid rate limiting (1 request per minute).
    Token validity is 1 day (86400 seconds). Refreshes token when expiry
    is within 1 hour.
    """

    # Expiry buffer: refresh token if expiry is within this duration
    EXPIRY_BUFFER = timedelta(hours=1)

    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize token manager.

        Args:
            cache_dir: Directory to store token cache. Defaults to <project_root>/data
        """
        if cache_dir is None:
            # Use project root directory for cache, same as DuckDB
            project_root = Path(__file__).parent.parent.parent.parent.parent.parent
            cache_dir = str(project_root / "data")

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / ".kis_token_cache.json"

        # In-memory cache
        self._token_cache: Optional[TokenResponse] = None
        self._last_refresh: Optional[datetime] = None

        # Load cached token on initialization
        self._load_from_disk()

    def get_or_generate(self, generate_func) -> TokenResponse:
        """Get cached token or generate a new one if expired.

        Args:
            generate_func: Callable that generates a new token. Should return TokenResponse.
                          Called only if cached token is unavailable or expired.

        Returns:
            TokenResponse: Valid access token
        """
        # Check if cached token is still valid
        if self._is_token_valid():
            logger.debug(f"Using cached token (expires at {self._token_cache.access_token_token_expired})")
            return self._token_cache

        # Token is missing, expired, or expiring soon - generate new one
        logger.info("Generating new KIS API token (cached token unavailable or expiring)")
        token = generate_func()
        self._save_token(token)
        return token

    def _is_token_valid(self) -> bool:
        """Check if cached token is valid and not expiring soon.

        Token is considered valid if:
        1. Token exists in memory or disk cache
        2. Expiry time is more than EXPIRY_BUFFER in the future

        Returns:
            True if token can be used, False if new token needed
        """
        if self._token_cache is None:
            return False

        try:
            expiry = datetime.strptime(self._token_cache.access_token_token_expired, "%Y-%m-%d %H:%M:%S")
            # Check if token expires within buffer period
            now = datetime.now()
            expiry_threshold = expiry - self.EXPIRY_BUFFER

            is_valid = now < expiry_threshold
            if not is_valid:
                logger.debug(f"Token expiring soon (expires at {expiry}, refresh threshold at {expiry_threshold})")
            return is_valid
        except (ValueError, AttributeError) as e:
            logger.warning(f"Error checking token validity: {e}")
            return False

    def _save_token(self, token: TokenResponse) -> None:
        """Save token to disk cache and memory.

        Args:
            token: TokenResponse object to cache
        """
        try:
            self._token_cache = token
            self._last_refresh = datetime.now()

            # Serialize to disk
            cache_data = {
                "token": token.model_dump(),
                "cached_at": self._last_refresh.isoformat(),
            }

            with open(self.cache_file, "w") as f:
                json.dump(cache_data, f, indent=2)

            logger.debug(f"Token cached at {self.cache_file}")
        except Exception as e:
            logger.error(f"Failed to save token cache: {e}")
            # Continue without disk cache, token is still in memory

    def _load_from_disk(self) -> None:
        """Load cached token from disk if available."""
        if not self.cache_file.exists():
            logger.debug(f"No cached token found at {self.cache_file}")
            return

        try:
            with open(self.cache_file, "r") as f:
                cache_data = json.load(f)

            token_data = cache_data.get("token")
            if token_data:
                self._token_cache = TokenResponse(**token_data)
                cached_at = cache_data.get("cached_at")
                logger.debug(f"Loaded cached token from disk (cached at {cached_at})")
            else:
                logger.warning("Token cache file is empty or malformed")
        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
            logger.warning(f"Failed to load token cache: {e}")
            # Cache will be regenerated on next request

    def clear_cache(self) -> None:
        """Clear both memory and disk cache."""
        try:
            self._token_cache = None
            self._last_refresh = None

            if self.cache_file.exists():
                self.cache_file.unlink()
                logger.info("Token cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear token cache: {e}")
