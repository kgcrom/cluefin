"""Unit tests for the broker client factory."""

from __future__ import annotations

from dataclasses import dataclass

from cluefin_openapi.client_factory import BrokerClientConfig, BrokerClientFactory


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("KIS_APP_KEY", "kis-app")
    monkeypatch.setenv("KIS_SECRET_KEY", "kis-secret")
    monkeypatch.setenv("KIS_ENV", "prod")
    monkeypatch.setenv("KIWOOM_APP_KEY", "kiwoom-app")
    monkeypatch.setenv("KIWOOM_SECRET_KEY", "kiwoom-secret")
    monkeypatch.setenv("KIWOOM_ENV", "dev")
    monkeypatch.setenv("DART_AUTH_KEY", "dart-key")
    monkeypatch.setenv("CLUEFIN_OPENAPI_CACHE_DIR", "/tmp/cluefin-cache")
    monkeypatch.setenv("CLUEFIN_OPENAPI_DEBUG", "true")

    config = BrokerClientConfig.from_env()

    assert config.kis_app_key == "kis-app"
    assert config.kis_secret_key == "kis-secret"
    assert config.kis_env == "prod"
    assert config.kiwoom_app_key == "kiwoom-app"
    assert config.kiwoom_secret_key == "kiwoom-secret"
    assert config.kiwoom_env == "dev"
    assert config.dart_auth_key == "dart-key"
    assert config.cache_dir == "/tmp/cluefin-cache"
    assert config.debug is True


@dataclass
class _FakeToken:
    value: str

    def get_token(self) -> str:
        return self.value


def test_factory_creates_kis_client_with_cache_dir(monkeypatch):
    captured = {}

    class FakeKisAuth:
        def __init__(self, app_key, secret_key, env, cache_dir=None):
            captured["kis_auth"] = {
                "app_key": app_key,
                "secret_key": secret_key.get_secret_value(),
                "env": env,
                "cache_dir": cache_dir,
            }

        def generate(self):
            return _FakeToken("kis-token")

    class FakeKisClient:
        def __init__(self, token, app_key, secret_key, env):
            captured["kis_client"] = {
                "token": token,
                "app_key": app_key,
                "secret_key": secret_key.get_secret_value(),
                "env": env,
            }

    monkeypatch.setattr("cluefin_openapi.client_factory.KisAuth", FakeKisAuth)
    monkeypatch.setattr("cluefin_openapi.client_factory.KisHttpClient", FakeKisClient)

    factory = BrokerClientFactory(
        BrokerClientConfig(
            kis_app_key="kis-app",
            kis_secret_key="kis-secret",
            kis_env="prod",
            cache_dir="/tmp/cluefin-cache",
        )
    )

    client = factory.create_kis()

    assert captured["kis_auth"]["cache_dir"] == "/tmp/cluefin-cache"
    assert captured["kis_client"]["token"] == "kis-token"
    assert captured["kis_client"]["env"] == "prod"
    assert client is not None


def test_factory_creates_kiwoom_client_with_cache_dir(monkeypatch):
    captured = {}

    class FakeKiwoomAuth:
        def __init__(self, app_key, secret_key, env, cache_dir=None):
            captured["kiwoom_auth"] = {
                "app_key": app_key,
                "secret_key": secret_key.get_secret_value(),
                "env": env,
                "cache_dir": cache_dir,
            }

        def generate_token(self):
            return _FakeToken("kiwoom-token")

    class FakeKiwoomClient:
        def __init__(self, token, env, debug=False):
            captured["kiwoom_client"] = {
                "token": token,
                "env": env,
                "debug": debug,
            }

    monkeypatch.setattr("cluefin_openapi.client_factory.KiwoomAuth", FakeKiwoomAuth)
    monkeypatch.setattr("cluefin_openapi.client_factory.KiwoomClient", FakeKiwoomClient)

    factory = BrokerClientFactory(
        BrokerClientConfig(
            kiwoom_app_key="kiwoom-app",
            kiwoom_secret_key="kiwoom-secret",
            kiwoom_env="dev",
            cache_dir="/tmp/cluefin-cache",
            debug=True,
        )
    )

    client = factory.create_kiwoom()

    assert captured["kiwoom_auth"]["cache_dir"] == "/tmp/cluefin-cache"
    assert captured["kiwoom_client"]["token"] == "kiwoom-token"
    assert captured["kiwoom_client"]["debug"] is True
    assert client is not None


def test_factory_creates_dart_client_without_cache(monkeypatch):
    captured = {}

    class FakeDartClient:
        def __init__(self, auth_key):
            captured["dart_client"] = {"auth_key": auth_key}

    monkeypatch.setattr("cluefin_openapi.client_factory.DartClient", FakeDartClient)

    factory = BrokerClientFactory(BrokerClientConfig(dart_auth_key="dart-key", cache_dir="/tmp/cluefin-cache"))
    client = factory.create_dart()

    assert captured["dart_client"]["auth_key"] == "dart-key"
    assert client is not None
