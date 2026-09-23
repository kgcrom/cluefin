"""Unit tests for the broker client factory."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from cluefin_openapi.client_factory import (
    BrokerClientConfig,
    BrokerClientFactory,
    _load_dotenv_file,
)


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


def test_config_from_env_reads_dotenv_from_cwd(tmp_path, monkeypatch):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text(
        "KIS_APP_KEY=dotenv-kis\n"
        "KIS_SECRET_KEY=dotenv-secret\n"
        "KIWOOM_APP_KEY=dotenv-kiwoom\n"
        "KIWOOM_SECRET_KEY=dotenv-kiwoom-secret\n"
        "DART_AUTH_KEY=dotenv-dart\n"
        "CLUEFIN_OPENAPI_CACHE_DIR=.cache/cluefin\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("KIS_APP_KEY", raising=False)
    monkeypatch.delenv("KIS_SECRET_KEY", raising=False)
    monkeypatch.delenv("KIWOOM_APP_KEY", raising=False)
    monkeypatch.delenv("KIWOOM_SECRET_KEY", raising=False)
    monkeypatch.delenv("DART_AUTH_KEY", raising=False)
    monkeypatch.delenv("CLUEFIN_OPENAPI_CACHE_DIR", raising=False)

    config = BrokerClientConfig.from_env()

    assert config.kis_app_key == "dotenv-kis"
    assert config.kis_secret_key == "dotenv-secret"
    assert config.kiwoom_app_key == "dotenv-kiwoom"
    assert config.kiwoom_secret_key == "dotenv-kiwoom-secret"
    assert config.dart_auth_key == "dotenv-dart"
    assert config.cache_dir == ".cache/cluefin"


def test_environment_overrides_dotenv(tmp_path, monkeypatch):
    (tmp_path / ".env").write_text("KIS_APP_KEY=dotenv-kis\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("KIS_APP_KEY", "process-kis")

    config = BrokerClientConfig.from_env()

    assert config.kis_app_key == "process-kis"


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


def test_factory_creates_nhplug_client_with_cache_dir(monkeypatch):
    captured = {}

    class FakeNHPlugAuth:
        def __init__(self, app_key, secret_key, cache_dir=None):
            captured["nhplug_auth"] = {
                "app_key": app_key,
                "secret_key": secret_key.get_secret_value(),
                "cache_dir": cache_dir,
            }

        def generate(self):
            return _FakeToken("nhplug-token")

    class FakeNHPlugClient:
        def __init__(self, token, app_key, secret_key, env, debug=False):
            captured["nhplug_client"] = {
                "token": token,
                "app_key": app_key,
                "secret_key": secret_key.get_secret_value(),
                "env": env,
                "debug": debug,
            }

    monkeypatch.setattr("cluefin_openapi.client_factory.NHPlugAuth", FakeNHPlugAuth)
    monkeypatch.setattr("cluefin_openapi.client_factory.NHPlugHttpClient", FakeNHPlugClient)

    factory = BrokerClientFactory(
        BrokerClientConfig(
            nhplug_app_key="nhplug-app",
            nhplug_secret_key="nhplug-secret",
            nhplug_env="prod",
            cache_dir="/tmp/cluefin-cache",
            debug=True,
        )
    )

    client = factory.create_nhplug()

    assert captured["nhplug_auth"]["cache_dir"] == "/tmp/cluefin-cache"
    assert captured["nhplug_client"]["token"] == "nhplug-token"
    assert captured["nhplug_client"]["env"] == "prod"
    assert captured["nhplug_client"]["debug"] is True
    assert client is not None


def test_create_dispatches_to_the_matching_create_method(monkeypatch):
    factory = BrokerClientFactory(BrokerClientConfig())
    calls = []
    monkeypatch.setattr(factory, "create_kis", lambda: calls.append("kis") or "kis-client")
    monkeypatch.setattr(factory, "create_kiwoom", lambda: calls.append("kiwoom") or "kiwoom-client")
    monkeypatch.setattr(factory, "create_dart", lambda: calls.append("dart") or "dart-client")
    monkeypatch.setattr(factory, "create_nhplug", lambda: calls.append("nhplug") or "nhplug-client")

    assert factory.create("kis") == "kis-client"
    assert factory.create("kiwoom") == "kiwoom-client"
    assert factory.create("dart") == "dart-client"
    assert factory.create("nhplug") == "nhplug-client"
    assert calls == ["kis", "kiwoom", "dart", "nhplug"]


def test_create_raises_value_error_for_unknown_broker():
    factory = BrokerClientFactory(BrokerClientConfig())

    with pytest.raises(ValueError, match="Unknown broker"):
        factory.create("upbit")  # type: ignore[arg-type]


def test_resolved_cache_dir_expands_home(monkeypatch):
    monkeypatch.setenv("HOME", "/home/tester")
    config = BrokerClientConfig(cache_dir="~/cluefin-cache")

    assert config.resolved_cache_dir() == "/home/tester/cluefin-cache"


def test_resolved_cache_dir_none_when_unset():
    config = BrokerClientConfig()

    assert config.resolved_cache_dir() is None


def test_load_dotenv_file_missing_returns_empty(tmp_path):
    assert _load_dotenv_file(tmp_path / "does-not-exist.env") == {}


def test_load_dotenv_file_skips_comments_and_blank_lines(tmp_path):
    path = tmp_path / ".env"
    path.write_text(
        "\n# a comment\nKIS_APP_KEY=value1\n\n  \nDART_AUTH_KEY=value2\n",
        encoding="utf-8",
    )

    assert _load_dotenv_file(path) == {"KIS_APP_KEY": "value1", "DART_AUTH_KEY": "value2"}


def test_load_dotenv_file_strips_matching_quotes(tmp_path):
    path = tmp_path / ".env"
    path.write_text(
        "DOUBLE_QUOTED=\"hello world\"\nSINGLE_QUOTED='hello world'\nUNQUOTED=plain\n",
        encoding="utf-8",
    )

    values = _load_dotenv_file(path)

    assert values["DOUBLE_QUOTED"] == "hello world"
    assert values["SINGLE_QUOTED"] == "hello world"
    assert values["UNQUOTED"] == "plain"


def test_load_dotenv_file_value_containing_equals_sign(tmp_path):
    path = tmp_path / ".env"
    # partition splits on the FIRST "=", so everything after it (including more
    # "=" signs) belongs to the value.
    path.write_text("CONNECTION_STRING=key=abc123&other=def456\n", encoding="utf-8")

    values = _load_dotenv_file(path)

    assert values["CONNECTION_STRING"] == "key=abc123&other=def456"


def test_load_dotenv_file_lines_without_equals_are_ignored(tmp_path):
    path = tmp_path / ".env"
    path.write_text("this line has no equals sign\nVALID_KEY=valid_value\n", encoding="utf-8")

    assert _load_dotenv_file(path) == {"VALID_KEY": "valid_value"}


def test_load_dotenv_file_blank_key_is_skipped(tmp_path):
    path = tmp_path / ".env"
    path.write_text("=value-with-no-key\nREAL_KEY=real_value\n", encoding="utf-8")

    assert _load_dotenv_file(path) == {"REAL_KEY": "real_value"}
