"""Token manager for NH PLUG API authentication with local caching.

NH guidance: the token is valid for 24h and MUST be cached across processes —
unnecessary re-issuance piles up security alerts on the account. Re-issue only
when the cached token is missing/expiring, or on a 401. Token generation is
also rate-limited server-side (1 request per second).
"""

import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from loguru import logger

from cluefin_openapi._atomic_file import read_json_locked, write_json_atomic
from cluefin_openapi.nhplug._auth_types import TokenResponse


class TokenManager:
    """Manages NH PLUG API token generation and caching.

    Unlike KIS there is no early server-side invalidation to defend against,
    so the token is reused for its full `expires_in` window (minus a buffer).
    Expiry is computed from the cache timestamp + `expires_in` because the
    token response carries no absolute expiry field.
    """

    # Expiry buffer: refresh token if expiry is within this duration
    EXPIRY_BUFFER = timedelta(hours=1)

    @staticmethod
    def _default_cache_dir() -> Path:
        """Return a writable fallback cache directory for token storage."""
        return Path(gettempdir()) / "cluefin-openapi"

    @staticmethod
    def _cache_file_name(app_key: Optional[str]) -> str:
        """Build a credential-scoped cache file name.

        NH PLUG tokens are issued on the live domain only and are shared by
        live and mock calls, so the cache is scoped by app_key only (no env).
        """
        suffix = ""
        if app_key:
            suffix = "_" + hashlib.sha256(app_key.encode()).hexdigest()[:8]
        return f".nhplug_token_cache{suffix}.json"

    def __init__(self, cache_dir: Optional[str] = None, app_key: Optional[str] = None):
        """Initialize token manager.

        Args:
            cache_dir: Directory to store token cache. Defaults to a writable cache directory.
            app_key: NH PLUG app key. Scopes the cache file so different credentials
                do not share a token.
        """
        if cache_dir is None:
            cache_dir = str(self._default_cache_dir())

        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / self._cache_file_name(app_key)

        # In-memory cache
        self._token_cache: Optional[TokenResponse] = None
        self._last_refresh: Optional[datetime] = None

        # Ensure the configured cache directory is ready even before the first save.
        self.cache_dir.mkdir(parents=True, exist_ok=True)

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
        if self._is_token_valid():
            logger.debug("Using cached NH PLUG token")
            return self._token_cache

        logger.info("Generating new NH PLUG API token (cached token unavailable or expiring)")
        token = generate_func()
        self._save_token(token)
        return token

    def _is_token_valid(self) -> bool:
        """Check if cached token is valid and not expiring soon."""
        if self._token_cache is None or self._last_refresh is None:
            return False

        try:
            expiry = self._last_refresh + timedelta(seconds=self._token_cache.expires_in)
            expiry_threshold = expiry - self.EXPIRY_BUFFER

            is_valid = datetime.now() < expiry_threshold
            if not is_valid:
                logger.debug(f"Token expiring soon (expires at {expiry}, refresh threshold at {expiry_threshold})")
            return is_valid
        except (TypeError, AttributeError) as e:
            logger.warning(f"Error checking token validity: {e}")
            return False

    def _save_token(self, token: TokenResponse) -> None:
        """Save token to disk cache and memory."""
        try:
            self._token_cache = token
            self._last_refresh = datetime.now()

            cache_data = {
                "token": token.model_dump(),
                "cached_at": self._last_refresh.isoformat(),
            }

            self.cache_dir.mkdir(parents=True, exist_ok=True)
            write_json_atomic(self.cache_file, cache_data)

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
            cache_data = read_json_locked(self.cache_file)

            token_data = cache_data.get("token")
            if token_data:
                self._token_cache = TokenResponse(**token_data)
                cached_at = cache_data.get("cached_at")
                if cached_at:
                    self._last_refresh = datetime.fromisoformat(cached_at)
                logger.debug(f"Loaded cached token from disk (cached at {cached_at})")
            else:
                logger.warning("Token cache file is empty or malformed")
        except (FileNotFoundError, ValueError) as e:
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
