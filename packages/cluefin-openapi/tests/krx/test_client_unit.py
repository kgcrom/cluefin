"""Unit tests for KRX Client rate limiting and retry functionality."""

from unittest.mock import patch

import pytest
import requests_mock

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._exceptions import (
    KrxAuthenticationError,
    KrxAuthorizationError,
    KrxClientError,
    KrxNetworkError,
    KrxRateLimitError,
    KrxServerError,
    KrxTimeoutError,
)


class TestClientInitialization:
    """Tests for Client initialization."""

    def test_default_parameters(self):
        """Test client initialization with default parameters."""
        client = Client(auth_key="test_key")

        assert client.auth_key == "test_key"
        assert client.base_url == "https://data-dbg.krx.co.kr"
        assert client.timeout == 30
        assert client.max_retries == 3
        assert client.debug is False
        assert client._rate_limiter is not None
        assert client._session is not None

    def test_custom_parameters(self):
        """Test client initialization with custom parameters."""
        client = Client(
            auth_key="test_key",
            timeout=60,
            max_retries=5,
            debug=True,
            rate_limit_requests_per_second=10.0,
            rate_limit_burst=20,
        )

        assert client.timeout == 60
        assert client.max_retries == 5
        assert client.debug is True
        assert client._rate_limiter.capacity == 20
        assert client._rate_limiter.refill_rate == 10.0

    def test_session_headers(self):
        """Test that session headers are properly set."""
        client = Client(auth_key="test_key")

        assert client._session.headers["Accept"] == "application/json"
        assert client._session.headers["User-Agent"] == "cluefin-openapi/1.0"


class TestRateLimiting:
    """Tests for rate limiting functionality."""

    def test_rate_limiter_integration(self):
        """Test that rate limiter is properly integrated."""
        client = Client(
            auth_key="test_key",
            rate_limit_requests_per_second=5.0,
            rate_limit_burst=10,
        )

        # Verify rate limiter is configured correctly
        assert client._rate_limiter.capacity == 10
        assert client._rate_limiter.refill_rate == 5.0
        assert client._rate_limiter.available_tokens == 10

    def test_rate_limit_timeout_raises_error(self):
        """Test that rate limit timeout raises KrxRateLimitError."""
        client = Client(
            auth_key="test_key",
            timeout=1,
            rate_limit_requests_per_second=0.1,
            rate_limit_burst=1,
        )

        # Consume all tokens
        client._rate_limiter.consume()

        with pytest.raises(KrxRateLimitError) as exc_info:
            client._get("/test")

        assert "Rate limit timeout" in str(exc_info.value)


class TestRetryLogic:
    """Tests for retry logic."""

    @patch("time.sleep")
    def test_rate_limit_429_retry(self, mock_sleep):
        """Test retry logic for 429 rate limit responses."""
        client = Client(auth_key="test_key", max_retries=2)

        with requests_mock.Mocker() as m:
            # First two calls return 429, third succeeds
            m.get(
                "https://data-dbg.krx.co.kr/test",
                [
                    {"status_code": 429, "json": {"error": "Rate Limited"}},
                    {"status_code": 429, "json": {"error": "Rate Limited"}},
                    {"status_code": 200, "json": {"success": True}},
                ],
            )

            result = client._get("/test")

            assert result == {"success": True}
            assert mock_sleep.call_count == 2

    @patch("time.sleep")
    def test_rate_limit_429_max_retries_exceeded(self, mock_sleep):
        """Test that exceeding max retries raises KrxRateLimitError."""
        client = Client(auth_key="test_key", max_retries=2)

        with requests_mock.Mocker() as m:
            # All calls return 429
            m.get(
                "https://data-dbg.krx.co.kr/test",
                status_code=429,
                json={"error": "Rate Limited"},
            )

            with pytest.raises(KrxRateLimitError) as exc_info:
                client._get("/test")

            assert "Rate limit exceeded after 2 retries" in str(exc_info.value)

    @patch("time.sleep")
    def test_server_error_retry(self, mock_sleep):
        """Test retry logic for 5xx server errors."""
        client = Client(auth_key="test_key", max_retries=2)

        with requests_mock.Mocker() as m:
            # First two calls return 500, third succeeds
            m.get(
                "https://data-dbg.krx.co.kr/test",
                [
                    {"status_code": 500, "text": "Internal Server Error"},
                    {"status_code": 500, "text": "Internal Server Error"},
                    {"status_code": 200, "json": {"success": True}},
                ],
            )

            result = client._get("/test")

            assert result == {"success": True}
            assert mock_sleep.call_count == 2

    @patch("time.sleep")
    def test_server_error_max_retries_exceeded(self, mock_sleep):
        """Test that exceeding max retries raises KrxServerError."""
        client = Client(auth_key="test_key", max_retries=2)

        with requests_mock.Mocker() as m:
            # All calls return 500
            m.get(
                "https://data-dbg.krx.co.kr/test",
                status_code=500,
                text="Internal Server Error",
            )

            with pytest.raises(KrxServerError) as exc_info:
                client._get("/test")

            assert exc_info.value.status_code == 500

    @patch("time.sleep")
    def test_timeout_retry(self, mock_sleep):
        """Test retry logic for timeout errors."""
        client = Client(auth_key="test_key", max_retries=2, timeout=1)

        with requests_mock.Mocker() as m:
            # First two calls timeout, third succeeds
            m.get(
                "https://data-dbg.krx.co.kr/test",
                [
                    {"exc": Exception("Timeout")},  # Will be caught as Timeout
                    {"exc": Exception("Timeout")},
                    {"status_code": 200, "json": {"success": True}},
                ],
            )

            # Need to mock the actual timeout exception
            import requests

            with patch.object(
                client._session,
                "get",
                side_effect=[
                    requests.exceptions.Timeout("Timeout"),
                    requests.exceptions.Timeout("Timeout"),
                    type(
                        "MockResponse",
                        (),
                        {
                            "status_code": 200,
                            "json": lambda self: {"success": True},
                        },
                    )(),
                ],
            ):
                result = client._get("/test")

            assert result == {"success": True}
            assert mock_sleep.call_count == 2

    @patch("time.sleep")
    def test_timeout_max_retries_exceeded(self, mock_sleep):
        """Test that exceeding max retries for timeout raises KrxTimeoutError."""
        client = Client(auth_key="test_key", max_retries=2, timeout=1)

        import requests

        with patch.object(
            client._session,
            "get",
            side_effect=requests.exceptions.Timeout("Timeout"),
        ):
            with pytest.raises(KrxTimeoutError) as exc_info:
                client._get("/test")

            assert "Request timeout after 2 retries" in str(exc_info.value)

    @patch("time.sleep")
    def test_connection_error_retry(self, mock_sleep):
        """Test retry logic for connection errors."""
        client = Client(auth_key="test_key", max_retries=2)

        import requests

        with patch.object(
            client._session,
            "get",
            side_effect=[
                requests.exceptions.ConnectionError("Connection refused"),
                requests.exceptions.ConnectionError("Connection refused"),
                type(
                    "MockResponse",
                    (),
                    {
                        "status_code": 200,
                        "json": lambda self: {"success": True},
                    },
                )(),
            ],
        ):
            result = client._get("/test")

        assert result == {"success": True}
        assert mock_sleep.call_count == 2

    @patch("time.sleep")
    def test_connection_error_max_retries_exceeded(self, mock_sleep):
        """Test that exceeding max retries for connection error raises KrxNetworkError."""
        client = Client(auth_key="test_key", max_retries=2)

        import requests

        with patch.object(
            client._session,
            "get",
            side_effect=requests.exceptions.ConnectionError("Connection refused"),
        ):
            with pytest.raises(KrxNetworkError) as exc_info:
                client._get("/test")

            assert "Network connection failed" in str(exc_info.value)

    def test_retry_after_header_parsing(self):
        """Test that Retry-After header is properly parsed."""
        client = Client(auth_key="test_key")

        # Create a mock response with Retry-After header
        mock_response = type(
            "MockResponse",
            (),
            {
                "headers": {"Retry-After": "5"},
            },
        )()

        result = client._get_retry_after(mock_response)
        assert result == 5

    def test_retry_after_header_invalid(self):
        """Test handling of invalid Retry-After header."""
        client = Client(auth_key="test_key")

        mock_response = type(
            "MockResponse",
            (),
            {
                "headers": {"Retry-After": "invalid"},
            },
        )()

        result = client._get_retry_after(mock_response)
        assert result is None

    def test_retry_after_header_missing(self):
        """Test handling of missing Retry-After header."""
        client = Client(auth_key="test_key")

        mock_response = type(
            "MockResponse",
            (),
            {
                "headers": {},
            },
        )()

        result = client._get_retry_after(mock_response)
        assert result is None


class TestErrorHandling:
    """Tests for HTTP error handling."""

    def test_401_authentication_error(self):
        """Test that 401 response raises KrxAuthenticationError."""
        client = Client(auth_key="test_key")

        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/test",
                status_code=401,
                json={"error": "Unauthorized"},
            )

            with pytest.raises(KrxAuthenticationError) as exc_info:
                client._get("/test")

            assert exc_info.value.status_code == 401

    def test_403_authorization_error(self):
        """Test that 403 response raises KrxAuthorizationError."""
        client = Client(auth_key="test_key")

        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/test",
                status_code=403,
                json={"error": "Forbidden"},
            )

            with pytest.raises(KrxAuthorizationError) as exc_info:
                client._get("/test")

            assert exc_info.value.status_code == 403

    def test_400_client_error(self):
        """Test that 400 response raises KrxClientError."""
        client = Client(auth_key="test_key")

        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/test",
                status_code=400,
                text="Bad Request",
            )

            with pytest.raises(KrxClientError) as exc_info:
                client._get("/test")

            assert exc_info.value.status_code == 400

    def test_request_exception_raises_network_error(self):
        """Test that RequestException raises KrxNetworkError."""
        client = Client(auth_key="test_key")

        import requests

        with patch.object(
            client._session,
            "get",
            side_effect=requests.exceptions.RequestException("Request failed"),
        ):
            with pytest.raises(KrxNetworkError) as exc_info:
                client._get("/test")

            assert "Request failed" in str(exc_info.value)


class TestSuccessfulRequests:
    """Tests for successful request handling."""

    def test_successful_json_response(self):
        """Test successful JSON response handling."""
        client = Client(auth_key="test_key")

        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/test",
                status_code=200,
                json={"data": [{"id": 1}]},
            )

            result = client._get("/test")

            assert result == {"data": [{"id": 1}]}

    def test_successful_text_response(self):
        """Test successful text response handling (non-JSON)."""
        client = Client(auth_key="test_key")

        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/test",
                status_code=200,
                text="Plain text response",
            )

            result = client._get("/test")

            assert result == "Plain text response"

    def test_request_with_params(self):
        """Test request with query parameters."""
        client = Client(auth_key="test_key")

        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/test",
                status_code=200,
                json={"success": True},
            )

            result = client._get("/test", params={"basDd": "20241201"})

            assert result == {"success": True}
            assert m.last_request.qs == {"basdd": ["20241201"]}

    def test_auth_key_in_headers(self):
        """Test that AUTH_KEY is included in request headers."""
        client = Client(auth_key="my_secret_key")

        with requests_mock.Mocker() as m:
            m.get(
                "https://data-dbg.krx.co.kr/test",
                status_code=200,
                json={"success": True},
            )

            client._get("/test")

            assert m.last_request.headers["AUTH_KEY"] == "my_secret_key"


class TestSessionManagement:
    """Tests for session management."""

    def test_close_session(self):
        """Test that close() properly closes the session."""
        client = Client(auth_key="test_key")

        # Verify session exists
        assert client._session is not None

        # Close should not raise
        client.close()

    def test_close_without_session(self):
        """Test that close() handles missing session gracefully."""
        client = Client(auth_key="test_key")
        del client._session

        # Should not raise
        client.close()


class TestSafeJson:
    """Tests for safe JSON parsing."""

    def test_safe_json_valid(self):
        """Test _safe_json with valid JSON response."""
        client = Client(auth_key="test_key")

        mock_response = type(
            "MockResponse",
            (),
            {
                "json": lambda self: {"data": "value"},
            },
        )()

        result = client._safe_json(mock_response)
        assert result == {"data": "value"}

    def test_safe_json_invalid(self):
        """Test _safe_json with invalid JSON response."""
        client = Client(auth_key="test_key")

        mock_response = type(
            "MockResponse",
            (),
            {
                "json": lambda self: (_ for _ in ()).throw(ValueError("No JSON")),
            },
        )()

        result = client._safe_json(mock_response)
        assert result is None
