"""Unit tests for Kiwoom TokenManager."""

from __future__ import annotations

import json
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from cluefin_openapi.kiwoom._auth_types import TokenResponse
from cluefin_openapi.kiwoom._token_manager import TokenManager


@pytest.fixture
def temp_cache_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def valid_token() -> TokenResponse:
    expiry = datetime.now() + timedelta(hours=12)
    return TokenResponse(token="test_token", token_type="Bearer", expires_dt=expiry)


@pytest.fixture
def expiring_token() -> TokenResponse:
    expiry = datetime.now() + timedelta(minutes=30)
    return TokenResponse(token="expiring_token", token_type="Bearer", expires_dt=expiry)


@pytest.fixture
def expired_token() -> TokenResponse:
    expiry = datetime.now() - timedelta(hours=1)
    return TokenResponse(token="expired_token", token_type="Bearer", expires_dt=expiry)


def test_token_manager_initialization(temp_cache_dir):
    manager = TokenManager(cache_dir=temp_cache_dir)

    assert manager.cache_dir == Path(temp_cache_dir)
    assert manager.cache_file == Path(temp_cache_dir) / ".kiwoom_token_cache.json"
    assert manager._token_cache is None


def test_get_or_generate_new_token_when_none_exists(temp_cache_dir, valid_token):
    manager = TokenManager(cache_dir=temp_cache_dir)
    generate_called = False

    def mock_generate():
        nonlocal generate_called
        generate_called = True
        return valid_token

    result = manager.get_or_generate(mock_generate)

    assert generate_called
    assert result == valid_token
    assert manager._token_cache == valid_token


def test_get_or_generate_returns_cached_token_if_valid(temp_cache_dir, valid_token):
    manager = TokenManager(cache_dir=temp_cache_dir)
    manager._save_token(valid_token)

    generate_called = False

    def mock_generate():
        nonlocal generate_called
        generate_called = True
        return TokenResponse(token="new_token", token_type="Bearer", expires_dt=datetime.now() + timedelta(hours=12))

    result = manager.get_or_generate(mock_generate)

    assert not generate_called
    assert result == valid_token


def test_get_or_generate_regenerates_expiring_token(temp_cache_dir, expiring_token, valid_token):
    manager = TokenManager(cache_dir=temp_cache_dir)
    manager._save_token(expiring_token)

    generate_called = False

    def mock_generate():
        nonlocal generate_called
        generate_called = True
        return valid_token

    result = manager.get_or_generate(mock_generate)

    assert generate_called
    assert result == valid_token
    assert manager._token_cache == valid_token


def test_get_or_generate_regenerates_expired_token(temp_cache_dir, expired_token, valid_token):
    manager = TokenManager(cache_dir=temp_cache_dir)
    manager._save_token(expired_token)

    generate_called = False

    def mock_generate():
        nonlocal generate_called
        generate_called = True
        return valid_token

    result = manager.get_or_generate(mock_generate)

    assert generate_called
    assert result == valid_token


def test_token_persistence_to_disk(temp_cache_dir, valid_token):
    manager = TokenManager(cache_dir=temp_cache_dir)
    manager._save_token(valid_token)

    assert manager.cache_file.exists()
    cache_data = json.loads(manager.cache_file.read_text(encoding="utf-8"))

    assert cache_data["token"]["token"] == valid_token.get_token()
    assert cache_data["token"]["token_type"] == valid_token.token_type


def test_token_loading_from_disk(temp_cache_dir, valid_token):
    cache_file = Path(temp_cache_dir) / ".kiwoom_token_cache.json"
    cache_data = {
        "token": {
            "token": valid_token.get_token(),
            "token_type": valid_token.token_type,
            "expires_dt": valid_token.expires_dt.isoformat(),
        },
        "cached_at": datetime.now().isoformat(),
    }
    cache_file.write_text(json.dumps(cache_data), encoding="utf-8")

    manager = TokenManager(cache_dir=temp_cache_dir)

    assert manager._token_cache is not None
    assert manager._token_cache.get_token() == valid_token.get_token()
    assert manager._token_cache.token_type == valid_token.token_type


def test_clear_cache(temp_cache_dir, valid_token):
    manager = TokenManager(cache_dir=temp_cache_dir)
    manager._save_token(valid_token)

    assert manager.cache_file.exists()
    assert manager._token_cache is not None

    manager.clear_cache()

    assert not manager.cache_file.exists()
    assert manager._token_cache is None
    assert manager._last_refresh is None


def test_concurrent_writes_keep_cache_readable(temp_cache_dir):
    token_a = TokenResponse(token="token_a", token_type="Bearer", expires_dt=datetime.now() + timedelta(hours=12))
    token_b = TokenResponse(token="token_b", token_type="Bearer", expires_dt=datetime.now() + timedelta(hours=13))
    manager1 = TokenManager(cache_dir=temp_cache_dir)
    manager2 = TokenManager(cache_dir=temp_cache_dir)

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(manager1._save_token, token_a)
        executor.submit(manager2._save_token, token_b)

    reloaded = TokenManager(cache_dir=temp_cache_dir)
    assert reloaded._token_cache is not None
    assert reloaded._token_cache.get_token() in {"token_a", "token_b"}
