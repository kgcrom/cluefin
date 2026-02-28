"""Session management for broker API clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger
from pydantic import SecretStr

if TYPE_CHECKING:
    from cluefin_openapi.dart._client import Client as DartClient
    from cluefin_openapi.kis._http_client import HttpClient as KisHttpClient
    from cluefin_openapi.kiwoom._client import Client as KiwoomClient

    from cluefin_rpc.config import RpcSettings


class SessionNotInitialized(Exception):
    """Raised when a broker session has not been initialized."""


class SessionManager:
    def __init__(self, settings: RpcSettings) -> None:
        self.settings = settings
        self._kis: KisHttpClient | None = None
        self._kiwoom: KiwoomClient | None = None
        self._dart: DartClient | None = None

    def initialize(self, broker: str) -> dict:
        if broker == "kis":
            return self._init_kis()
        elif broker == "kiwoom":
            return self._init_kiwoom()
        elif broker == "dart":
            return self._init_dart()
        else:
            raise ValueError(f"Unknown broker: {broker}")

    def _init_kis(self) -> dict:
        from cluefin_openapi.kis._auth import Auth as KisAuth
        from cluefin_openapi.kis._http_client import HttpClient as KisHttpClient

        s = self.settings
        if not s.kis_app_key or not s.kis_secret_key:
            raise ValueError("KIS credentials not configured (kis_app_key, kis_secret_key)")

        auth = KisAuth(
            app_key=s.kis_app_key,
            secret_key=SecretStr(s.kis_secret_key),
            env=s.kis_env,
        )
        token_response = auth.generate()
        self._kis = KisHttpClient(
            token=token_response.get_token(),
            app_key=s.kis_app_key,
            secret_key=s.kis_secret_key,
            env=s.kis_env,
        )
        logger.info("KIS session initialized (env={})", s.kis_env)
        return {"broker": "kis", "status": "initialized", "env": s.kis_env}

    def _init_kiwoom(self) -> dict:
        from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
        from cluefin_openapi.kiwoom._client import Client as KiwoomClient

        s = self.settings
        if not s.kiwoom_app_key or not s.kiwoom_secret_key:
            raise ValueError("Kiwoom credentials not configured (kiwoom_app_key, kiwoom_secret_key)")

        auth = KiwoomAuth(
            app_key=s.kiwoom_app_key,
            secret_key=SecretStr(s.kiwoom_secret_key),
            env=s.kiwoom_env,
        )
        token = auth.generate_token()
        self._kiwoom = KiwoomClient(token=token.get_token(), env=s.kiwoom_env)
        logger.info("Kiwoom session initialized (env={})", s.kiwoom_env)
        return {"broker": "kiwoom", "status": "initialized", "env": s.kiwoom_env}

    def _init_dart(self) -> dict:
        from cluefin_openapi.dart._client import Client as DartClient

        s = self.settings
        if not s.dart_auth_key:
            raise ValueError("DART credentials not configured (dart_auth_key)")

        self._dart = DartClient(auth_key=s.dart_auth_key)
        logger.info("DART session initialized")
        return {"broker": "dart", "status": "initialized"}

    def get_kis(self) -> KisHttpClient:
        if self._kis is None:
            raise SessionNotInitialized("KIS session not initialized. Call session.initialize with broker='kis' first.")
        return self._kis

    def get_kiwoom(self) -> KiwoomClient:
        if self._kiwoom is None:
            raise SessionNotInitialized(
                "Kiwoom session not initialized. Call session.initialize with broker='kiwoom' first."
            )
        return self._kiwoom

    def get_dart(self) -> DartClient:
        if self._dart is None:
            raise SessionNotInitialized(
                "DART session not initialized. Call session.initialize with broker='dart' first."
            )
        return self._dart

    def status(self) -> dict:
        return {
            "kis": self._kis is not None,
            "kiwoom": self._kiwoom is not None,
            "dart": self._dart is not None,
        }

    def close(self, broker: str | None = None) -> dict:
        if broker is None:
            return self.close_all()
        if broker == "kis":
            self._kis = None
        elif broker == "kiwoom":
            self._kiwoom = None
        elif broker == "dart":
            self._dart = None
        else:
            raise ValueError(f"Unknown broker: {broker}")
        logger.info("Closed {} session", broker)
        return {"broker": broker, "status": "closed"}

    def close_all(self) -> dict:
        self._kis = None
        self._kiwoom = None
        self._dart = None
        logger.info("All sessions closed")
        return {"status": "all_closed"}
