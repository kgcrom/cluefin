"""Tests for the improved Client class."""

import json
import time
from unittest.mock import Mock, patch

import pytest
import requests
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._exceptions import (
    KiwoomAPIError,
    KiwoomAuthenticationError,
    KiwoomAuthorizationError,
    KiwoomNetworkError,
    KiwoomRateLimitError,
    KiwoomServerError,
    KiwoomTimeoutError,
    KiwoomValidationError,
)


@pytest.fixture
def client():
    """Create a Client instance for testing."""
    return Client(token="test_token", env="dev", debug=True)


def test_client_initialization():
    """Test client initialization with different parameters."""
    client = Client("token", "dev")
    assert client.token == "token"
    assert client.url == "https://mockapi.kiwoom.com"
    assert client.timeout == 30
    assert client.max_retries == 3
    assert not client.debug

    client_prod = Client("token", "prod", timeout=60, max_retries=5, debug=True)
    assert client_prod.url == "https://api.kiwoom.com"
    assert client_prod.timeout == 60
    assert client_prod.max_retries == 5
    assert client_prod.debug


def test_client_session_headers():
    """Test that client sets up session with correct headers."""
    client = Client("token", "dev")
    expected_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "cluefin-kiwoom/0.1.0",
    }
    for key, value in expected_headers.items():
        assert client._session.headers[key] == value


def test_successful_post_request(client):
    """Test successful POST request."""
    response_data = {"return_code": 0, "return_msg": "Success", "data": "test"}

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/test",
            json=response_data,
            status_code=200,
            headers={"cont-yn": "N", "next-key": "", "api-id": "test"},
        )

        headers = {"api-id": "test", "cont-yn": "N", "next-key": ""}
        body = {"test": "data"}

        response = client._post("/test", headers, body)

        assert response.status_code == 200
        assert response.json() == response_data


def test_authentication_error(client):
    """Test 401 authentication error handling."""
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/test",
            json={"error": "Unauthorized"},
            status_code=401,
        )

        with pytest.raises(KiwoomAuthenticationError) as exc_info:
            client._post("/test", {}, {})

        assert exc_info.value.status_code == 401
        assert "Authentication failed" in str(exc_info.value)


def test_authorization_error(client):
    """Test 403 authorization error handling."""
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/test",
            json={"error": "Forbidden"},
            status_code=403,
        )

        with pytest.raises(KiwoomAuthorizationError) as exc_info:
            client._post("/test", {}, {})

        assert exc_info.value.status_code == 403
        assert "Access forbidden" in str(exc_info.value)


def test_validation_error(client):
    """Test 400 validation error handling."""
    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/test",
            json={"error": "Bad Request"},
            status_code=400,
        )

        with pytest.raises(KiwoomValidationError) as exc_info:
            client._post("/test", {}, {})

        assert exc_info.value.status_code == 400
        assert "Bad request" in str(exc_info.value)


def test_rate_limit_error_no_retry(client):
    """Test 429 rate limit error without retries."""
    client.max_retries = 0

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/test",
            json={"error": "Too Many Requests"},
            status_code=429,
            headers={"Retry-After": "60"},
        )

        with pytest.raises(KiwoomRateLimitError) as exc_info:
            client._post("/test", {}, {})

        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 60


def test_server_error_with_retry(client):
    """Test 500 server error with retry logic."""
    client.max_retries = 1

    with requests_mock.Mocker() as m:
        # First call returns 500, second call succeeds
        m.post(
            "https://mockapi.kiwoom.com/test",
            [
                {"status_code": 500, "json": {"error": "Server Error"}},
                {"status_code": 200, "json": {"success": True}},
            ],
        )

        # Should succeed after retry
        response = client._post("/test", {}, {})
        assert response.status_code == 200
        assert response.json() == {"success": True}


def test_timeout_error(client):
    """Test timeout error handling."""
    client.max_retries = 0

    with requests_mock.Mocker() as m:
        m.post("https://mockapi.kiwoom.com/test", exc=requests.exceptions.Timeout)

        with pytest.raises(KiwoomTimeoutError):
            client._post("/test", {}, {})


def test_connection_error(client):
    """Test connection error handling."""
    client.max_retries = 0

    with requests_mock.Mocker() as m:
        m.post("https://mockapi.kiwoom.com/test", exc=requests.exceptions.ConnectionError)

        with pytest.raises(KiwoomNetworkError):
            client._post("/test", {}, {})


def test_safe_json_parsing(client):
    """Test safe JSON parsing utility method."""
    # Test valid JSON
    mock_response = Mock()
    mock_response.json.return_value = {"test": "data"}
    result = client._safe_json(mock_response)
    assert result == {"test": "data"}

    # Test invalid JSON
    mock_response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)
    result = client._safe_json(mock_response)
    assert result is None


def test_get_retry_after(client):
    """Test retry-after header extraction."""
    mock_response = Mock()

    # Test with valid retry-after header
    mock_response.headers = {"Retry-After": "60"}
    result = client._get_retry_after(mock_response)
    assert result == 60

    # Test with invalid retry-after header
    mock_response.headers = {"Retry-After": "invalid"}
    result = client._get_retry_after(mock_response)
    assert result is None

    # Test without retry-after header
    mock_response.headers = {}
    result = client._get_retry_after(mock_response)
    assert result is None


def test_client_close(client):
    """Test client session cleanup."""
    assert hasattr(client, "_session")
    client.close()
    # Session should still exist but be closed
    assert hasattr(client, "_session")


def test_header_merging(client):
    """Test that headers are properly merged with authentication."""
    test_headers = {"api-id": "test", "custom-header": "value"}

    with requests_mock.Mocker() as m:
        m.post(
            "https://mockapi.kiwoom.com/test",
            json={"success": True},
            status_code=200,
        )

        response = client._post("/test", test_headers, {})
        assert response.status_code == 200

        # Verify the request was made with correct headers
        assert len(m.request_history) == 1
        request = m.request_history[0]

        # Check that our headers are present along with auth
        assert request.headers["Authorization"] == "Bearer test_token"
        assert request.headers["api-id"] == "test"
        assert request.headers["custom-header"] == "value"
        assert request.headers["Content-Type"] == "application/json"


@patch("time.sleep")  # Mock sleep to speed up tests
def test_rate_limit_retry_logic(mock_sleep, client):
    """Test rate limit retry logic with exponential backoff."""
    client.max_retries = 2

    with requests_mock.Mocker() as m:
        # First two calls return 429, third succeeds
        m.post(
            "https://mockapi.kiwoom.com/test",
            [
                {"status_code": 429, "json": {"error": "Rate Limited"}},
                {"status_code": 429, "json": {"error": "Rate Limited"}},
                {"status_code": 200, "json": {"success": True}},
            ],
        )

        response = client._post("/test", {}, {})
        assert response.status_code == 200

        # Verify sleep was called for retries
        assert mock_sleep.call_count == 2
        # Check exponential backoff: first retry waits 1s, second waits 2s
        mock_sleep.assert_any_call(1)
        mock_sleep.assert_any_call(2)
