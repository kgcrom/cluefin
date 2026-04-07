"""Broker client factory for CLI-style, stateless client construction."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Mapping, Optional

from pydantic import SecretStr

from cluefin_openapi.dart._client import Client as DartClient
from cluefin_openapi.kis._auth import Auth as KisAuth
from cluefin_openapi.kis._http_client import HttpClient as KisHttpClient
from cluefin_openapi.kiwoom._auth import Auth as KiwoomAuth
from cluefin_openapi.kiwoom._client import Client as KiwoomClient

BrokerName = Literal["kis", "kiwoom", "dart"]
BrokerEnv = Literal["dev", "prod"]

__all__ = ["BrokerClientConfig", "BrokerClientFactory", "create_broker_client"]


@dataclass(slots=True)
class BrokerClientConfig:
    """Configuration for broker client creation."""

    kis_app_key: Optional[str] = None
    kis_secret_key: Optional[str] = None
    kis_env: BrokerEnv = "dev"
    kiwoom_app_key: Optional[str] = None
    kiwoom_secret_key: Optional[str] = None
    kiwoom_env: BrokerEnv = "dev"
    dart_auth_key: Optional[str] = None
    cache_dir: Optional[str] = None
    debug: bool = False

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "BrokerClientConfig":
        env = _merge_env_with_dotenv(environ or os.environ)
        return cls(
            kis_app_key=env.get("KIS_APP_KEY"),
            kis_secret_key=env.get("KIS_SECRET_KEY"),
            kis_env=env.get("KIS_ENV", "dev").lower(),
            kiwoom_app_key=env.get("KIWOOM_APP_KEY"),
            kiwoom_secret_key=env.get("KIWOOM_SECRET_KEY"),
            kiwoom_env=env.get("KIWOOM_ENV", "dev").lower(),
            dart_auth_key=env.get("DART_AUTH_KEY"),
            cache_dir=env.get("CLUEFIN_OPENAPI_CACHE_DIR"),
            debug=env.get("CLUEFIN_OPENAPI_DEBUG", "0").lower() in {"1", "true", "yes", "on"},
        )

    def resolved_cache_dir(self) -> Optional[str]:
        if self.cache_dir:
            return str(Path(self.cache_dir).expanduser())
        return None


def _merge_env_with_dotenv(environ: Mapping[str, str]) -> dict[str, str]:
    """Load `.env` from the current working directory, keeping real env precedence."""
    merged = dict(_load_dotenv_file(Path.cwd() / ".env"))
    merged.update(dict(environ))
    return merged


def _load_dotenv_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if value and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]

        values[key] = value

    return values


class BrokerClientFactory:
    """Create broker clients with auth/token caching handled internally."""

    def __init__(self, config: BrokerClientConfig | None = None) -> None:
        self.config = config or BrokerClientConfig.from_env()

    def create(self, broker: BrokerName):
        if broker == "kis":
            return self.create_kis()
        if broker == "kiwoom":
            return self.create_kiwoom()
        if broker == "dart":
            return self.create_dart()
        raise ValueError(f"Unknown broker: {broker}")

    def create_kis(self) -> KisHttpClient:
        if not self.config.kis_app_key or not self.config.kis_secret_key:
            raise ValueError("KIS credentials not configured (kis_app_key, kis_secret_key)")

        auth = KisAuth(
            app_key=self.config.kis_app_key,
            secret_key=SecretStr(self.config.kis_secret_key),
            env=self.config.kis_env,
            cache_dir=self.config.resolved_cache_dir(),
        )
        token = auth.generate()
        return KisHttpClient(
            token=token.get_token(),
            app_key=self.config.kis_app_key,
            secret_key=SecretStr(self.config.kis_secret_key),
            env=self.config.kis_env,
        )

    def create_kiwoom(self) -> KiwoomClient:
        if not self.config.kiwoom_app_key or not self.config.kiwoom_secret_key:
            raise ValueError("Kiwoom credentials not configured (kiwoom_app_key, kiwoom_secret_key)")

        auth = KiwoomAuth(
            app_key=self.config.kiwoom_app_key,
            secret_key=SecretStr(self.config.kiwoom_secret_key),
            env=self.config.kiwoom_env,
            cache_dir=self.config.resolved_cache_dir(),
        )
        token = auth.generate_token()
        return KiwoomClient(
            token=token.get_token(),
            env=self.config.kiwoom_env,
            debug=self.config.debug,
        )

    def create_dart(self) -> DartClient:
        if not self.config.dart_auth_key:
            raise ValueError("DART credentials not configured (dart_auth_key)")
        return DartClient(auth_key=self.config.dart_auth_key)


def create_broker_client(broker: BrokerName, config: BrokerClientConfig | None = None):
    """Convenience helper used by CLI callers."""

    return BrokerClientFactory(config=config).create(broker)
