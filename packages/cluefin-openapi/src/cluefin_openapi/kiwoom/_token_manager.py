"""Token manager for Kiwoom API authentication with local caching."""

from __future__ import annotations

import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from loguru import logger

from cluefin_openapi._atomic_file import read_json_locked, write_json_atomic
from cluefin_openapi.kiwoom._auth_types import TokenResponse


class TokenManager:
    """Manage Kiwoom API token generation and disk caching."""

    EXPIRY_BUFFER = timedelta(hours=1)
    MAX_CACHE_AGE = timedelta(hours=6)

    @staticmethod
    def _default_cache_dir() -> Path:
        """Return a writable fallback cache directory for token storage."""
        return Path(gettempdir()) / "cluefin-openapi"

    @staticmethod
    def _cache_file_name(env: Optional[str], app_key: Optional[str]) -> str:
        """Build an environment- and credential-scoped cache file name.

        Tokens are not interchangeable between the real (prod) and mock (dev)
        servers, nor between different app keys. Scoping the cache file prevents
        a token minted for one environment/credential from being reused against
        another, which the server rejects with
        "8031:투자구분(실전/모의)이 달라서 Token를 사용할수가 없습니다".
        """
        parts = []
        if env:
            parts.append(env)
        if app_key:
            parts.append(hashlib.sha256(app_key.encode()).hexdigest()[:8])
        suffix = ("_" + "_".join(parts)) if parts else ""
        return f".kiwoom_token_cache{suffix}.json"

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        env: Optional[str] = None,
        app_key: Optional[str] = None,
    ) -> None:
        """Initialize token manager.

        Args:
            cache_dir: Directory to store token cache. Defaults to a writable cache directory.
            env: Target environment ("dev" or "prod"). Scopes the cache file so
                dev and prod tokens are never mixed.
            app_key: Kiwoom app key. Scopes the cache file so different credentials
                do not share a token.
        """
        if cache_dir is None:
            cache_dir = str(self._default_cache_dir())

        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / self._cache_file_name(env, app_key)
        self._token_cache: Optional[TokenResponse] = None
        self._last_refresh: Optional[datetime] = None
        self._load_from_disk()

    def get_or_generate(self, generate_func) -> TokenResponse:
        if self._is_token_valid():
            logger.debug("Using cached Kiwoom token (expires at {})", self._token_cache.expires_dt)
            return self._token_cache

        logger.info("Generating new Kiwoom token (cached token unavailable or expiring)")
        token = generate_func()
        self._save_token(token)
        return token

    def _is_token_valid(self) -> bool:
        if self._token_cache is None:
            return False

        if self._last_refresh is not None:
            age = datetime.now() - self._last_refresh
            if age > self.MAX_CACHE_AGE:
                logger.debug("Kiwoom token cache expired (age: {}, max: {})", age, self.MAX_CACHE_AGE)
                return False

        expiry = getattr(self._token_cache, "expires_dt", None)
        if expiry is None:
            logger.warning("Kiwoom token cache is missing expiry information")
            return False

        expiry_threshold = expiry - self.EXPIRY_BUFFER
        is_valid = datetime.now() < expiry_threshold
        if not is_valid:
            logger.debug(
                "Kiwoom token expiring soon (expires at {}, refresh threshold at {})", expiry, expiry_threshold
            )
        return is_valid

    def _save_token(self, token: TokenResponse) -> None:
        try:
            self._token_cache = token
            self._last_refresh = datetime.now()
            token_data = token.model_dump(mode="json")
            token_data["token"] = token.get_token()
            cache_data = {
                "token": token_data,
                "cached_at": self._last_refresh.isoformat(),
            }
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            write_json_atomic(self.cache_file, cache_data)
            logger.debug("Kiwoom token cached at {}", self.cache_file)
        except Exception as exc:
            logger.error("Failed to save Kiwoom token cache: {}", exc)

    def _load_from_disk(self) -> None:
        if not self.cache_file.exists():
            return

        try:
            cache_data = read_json_locked(self.cache_file)
            token_data = cache_data.get("token")
            if token_data:
                self._token_cache = TokenResponse(**token_data)
                cached_at = cache_data.get("cached_at")
                if cached_at:
                    self._last_refresh = datetime.fromisoformat(cached_at)
                logger.debug("Loaded Kiwoom token from disk (cached at {})", cached_at)
            else:
                logger.warning("Kiwoom token cache file is empty or malformed")
        except (FileNotFoundError, ValueError) as exc:
            logger.warning("Failed to load Kiwoom token cache: {}", exc)

    def clear_cache(self) -> None:
        self._token_cache = None
        self._last_refresh = None
        if self.cache_file.exists():
            self.cache_file.unlink()
            logger.info("Kiwoom token cache cleared")
