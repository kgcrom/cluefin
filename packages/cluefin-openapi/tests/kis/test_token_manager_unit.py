"""Unit tests for TokenManager."""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from cluefin_openapi.kis._auth_types import TokenResponse
from cluefin_openapi.kis._token_manager import TokenManager


@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def valid_token() -> TokenResponse:
    """Create a valid token that doesn't expire soon."""
    expiry = datetime.now() + timedelta(hours=12)
    return TokenResponse(
        access_token="test_access_token",
        token_type="Bearer",
        expires_in=86400,
        access_token_token_expired=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )


@pytest.fixture
def expiring_token() -> TokenResponse:
    """Create a token that expires within the buffer (1 hour)."""
    expiry = datetime.now() + timedelta(minutes=30)
    return TokenResponse(
        access_token="expiring_token",
        token_type="Bearer",
        expires_in=86400,
        access_token_token_expired=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )


@pytest.fixture
def expired_token() -> TokenResponse:
    """Create an expired token."""
    expiry = datetime.now() - timedelta(hours=1)
    return TokenResponse(
        access_token="expired_token",
        token_type="Bearer",
        expires_in=86400,
        access_token_token_expired=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )


def test_token_manager_initialization(temp_cache_dir):
    """Test TokenManager initialization with custom cache directory."""
    manager = TokenManager(cache_dir=temp_cache_dir)

    assert manager.cache_dir == Path(temp_cache_dir)
    assert manager.cache_file == Path(temp_cache_dir) / ".kis_token_cache.json"
    assert manager._token_cache is None


def test_get_or_generate_new_token_when_none_exists(temp_cache_dir, valid_token):
    """Test generating new token when no cache exists."""
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
    """Test that cached valid token is returned without regenerating."""
    manager = TokenManager(cache_dir=temp_cache_dir)
    manager._save_token(valid_token)

    generate_called = False

    def mock_generate():
        nonlocal generate_called
        generate_called = True
        return TokenResponse(
            access_token="new_token",
            token_type="Bearer",
            expires_in=86400,
            access_token_token_expired=(datetime.now() + timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S"),
        )

    result = manager.get_or_generate(mock_generate)

    assert not generate_called
    assert result == valid_token


def test_get_or_generate_regenerates_expiring_token(temp_cache_dir, expiring_token, valid_token):
    """Test that expiring token triggers regeneration."""
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
    """Test that expired token triggers regeneration."""
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
    """Test that tokens are persisted to disk."""
    manager = TokenManager(cache_dir=temp_cache_dir)
    manager._save_token(valid_token)

    # Verify cache file exists
    assert manager.cache_file.exists()

    # Verify cache file content
    with open(manager.cache_file, "r") as f:
        cache_data = json.load(f)

    assert cache_data["token"]["access_token"] == valid_token.access_token
    assert cache_data["token"]["token_type"] == valid_token.token_type


def test_token_loading_from_disk(temp_cache_dir, valid_token):
    """Test that tokens are loaded from disk on initialization."""
    # Create a cache file first
    cache_file = Path(temp_cache_dir) / ".kis_token_cache.json"
    cache_data = {
        "token": valid_token.model_dump(),
        "cached_at": datetime.now().isoformat(),
    }
    with open(cache_file, "w") as f:
        json.dump(cache_data, f)

    # Create new manager and verify it loads the token
    manager = TokenManager(cache_dir=temp_cache_dir)

    assert manager._token_cache is not None
    assert manager._token_cache.access_token == valid_token.access_token
    assert manager._token_cache.token_type == valid_token.token_type


def test_clear_cache(temp_cache_dir, valid_token):
    """Test clearing both memory and disk cache."""
    manager = TokenManager(cache_dir=temp_cache_dir)
    manager._save_token(valid_token)

    assert manager.cache_file.exists()
    assert manager._token_cache is not None

    manager.clear_cache()

    assert not manager.cache_file.exists()
    assert manager._token_cache is None
    assert manager._last_refresh is None


def test_invalid_cache_file_handling(temp_cache_dir, valid_token):
    """Test handling of malformed cache file."""
    # Create invalid cache file
    cache_file = Path(temp_cache_dir) / ".kis_token_cache.json"
    with open(cache_file, "w") as f:
        f.write("invalid json content {[")

    # Manager should handle gracefully
    manager = TokenManager(cache_dir=temp_cache_dir)
    assert manager._token_cache is None

    # Should be able to generate and save new token
    manager._save_token(valid_token)
    assert manager._token_cache == valid_token


def test_cache_dir_creation(temp_cache_dir):
    """Test that cache directory is created if it doesn't exist."""
    non_existent_dir = Path(temp_cache_dir) / "nested" / "cache" / "dir"
    assert not non_existent_dir.exists()

    manager = TokenManager(cache_dir=str(non_existent_dir))

    assert non_existent_dir.exists()
    assert manager.cache_dir == non_existent_dir


def test_expiry_buffer_calculation():
    """Test that expiry buffer is correctly applied (1 hour)."""
    assert TokenManager.EXPIRY_BUFFER == timedelta(hours=1)


def test_concurrent_cache_access(temp_cache_dir, valid_token):
    """Test that multiple managers share the same cache file."""
    manager1 = TokenManager(cache_dir=temp_cache_dir)
    manager1._save_token(valid_token)

    # Create second manager - should load the cached token
    manager2 = TokenManager(cache_dir=temp_cache_dir)

    assert manager2._token_cache is not None
    assert manager2._token_cache.access_token == valid_token.access_token
