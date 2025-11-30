"""Unit tests for DART client rate limiting and retry functionality."""

import json
from unittest.mock import Mock, patch

import pytest
import requests
import requests_mock

from cluefin_openapi.dart._client import Client
from cluefin_openapi.dart._exceptions import (
    DartAuthenticationError,
    DartAuthorizationError,
    DartClientError,
    DartNetworkError,
    DartRateLimitError,
    DartServerError,
    DartTimeoutError,
)


@pytest.fixture
def client() -> Client:
    """Create a DART client for testing."""
    return Client(auth_key="test-auth-key", timeout=30, max_retries=3)


class TestClientInitialization:
    """Tests for client initialization."""

    def test_default_values(self):
        client = Client(auth_key="test-key")
        assert client.auth_key == "test-key"
        assert client.timeout == 30
        assert client.max_retries == 3
        assert client._rate_limiter is not None

    def test_custom_rate_limit_values(self):
        client = Client(
            auth_key="test-key",
            rate_limit_requests_per_second=2.0,
            rate_limit_burst=5,
        )
        assert client._rate_limiter.capacity == 5
        assert client._rate_limiter.refill_rate == 2.0


class TestSuccessfulRequests:
    """Tests for successful request handling."""

    def test_get_json_success(self, client: Client):
        expected_data = {"status": "000", "data": [{"key": "value"}]}

        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                json=expected_data,
                status_code=200,
            )

            result = client._get("/api/test", params={"param1": "value1"})

            assert result == expected_data
            assert m.last_request.qs["crtfc_key"] == ["test-auth-key"]
            assert m.last_request.qs["param1"] == ["value1"]

    def test_get_bytes_success(self, client: Client):
        expected_content = b"binary content"

        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/document",
                content=expected_content,
                status_code=200,
            )

            result = client._get_bytes("/api/document")

            assert result == expected_content


class TestAuthenticationErrors:
    """Tests for authentication and authorization errors."""

    def test_authentication_error_401(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                json={"error": "Unauthorized"},
                status_code=401,
            )

            with pytest.raises(DartAuthenticationError) as exc_info:
                client._get("/api/test")

            assert exc_info.value.status_code == 401
            assert "Authentication failed" in str(exc_info.value)

    def test_authorization_error_403(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                json={"error": "Forbidden"},
                status_code=403,
            )

            with pytest.raises(DartAuthorizationError) as exc_info:
                client._get("/api/test")

            assert exc_info.value.status_code == 403
            assert "Access forbidden" in str(exc_info.value)

    def test_client_error_400(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                text="Bad Request",
                status_code=400,
            )

            with pytest.raises(DartClientError) as exc_info:
                client._get("/api/test")

            assert exc_info.value.status_code == 400


class TestRateLimitHandling:
    """Tests for rate limit handling."""

    @patch("time.sleep")
    def test_rate_limit_429_retry_success(self, mock_sleep, client: Client):
        """Test that 429 responses trigger retry with eventual success."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                [
                    {"status_code": 429, "json": {"error": "Too Many Requests"}},
                    {"status_code": 429, "json": {"error": "Too Many Requests"}},
                    {"status_code": 200, "json": {"data": "success"}},
                ],
            )

            result = client._get("/api/test")

            assert result == {"data": "success"}
            assert mock_sleep.call_count == 2
            # Exponential backoff: 2^0=1, 2^1=2
            mock_sleep.assert_any_call(1)
            mock_sleep.assert_any_call(2)

    @patch("time.sleep")
    def test_rate_limit_429_with_retry_after_header(self, mock_sleep, client: Client):
        """Test that Retry-After header is respected."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                [
                    {
                        "status_code": 429,
                        "json": {"error": "Too Many Requests"},
                        "headers": {"Retry-After": "5"},
                    },
                    {"status_code": 200, "json": {"data": "success"}},
                ],
            )

            result = client._get("/api/test")

            assert result == {"data": "success"}
            mock_sleep.assert_called_with(5)

    @patch("time.sleep")
    def test_rate_limit_429_max_retries_exceeded(self, mock_sleep, client: Client):
        """Test that DartRateLimitError is raised after max retries."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                [
                    {"status_code": 429, "json": {"error": "Too Many Requests"}},
                    {"status_code": 429, "json": {"error": "Too Many Requests"}},
                    {"status_code": 429, "json": {"error": "Too Many Requests"}},
                    {"status_code": 429, "json": {"error": "Too Many Requests"}},
                ],
            )

            with pytest.raises(DartRateLimitError) as exc_info:
                client._get("/api/test")

            assert exc_info.value.status_code == 429
            assert "Rate limit exceeded" in str(exc_info.value)

    def test_rate_limit_timeout_raises_error(self):
        """Test that rate limit timeout raises DartRateLimitError."""
        # Create client with very low rate limit
        client = Client(
            auth_key="test-key",
            timeout=0.1,  # Very short timeout
            rate_limit_requests_per_second=0.01,  # Very slow refill
            rate_limit_burst=1,
        )

        # Consume all tokens
        client._rate_limiter.consume(tokens=1)

        with pytest.raises(DartRateLimitError) as exc_info:
            client._get("/api/test")

        assert "Rate limit timeout" in str(exc_info.value)


class TestServerErrorRetry:
    """Tests for server error retry handling."""

    @patch("time.sleep")
    def test_server_error_500_retry_success(self, mock_sleep, client: Client):
        """Test that 5xx responses trigger retry with eventual success."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                [
                    {"status_code": 500, "text": "Internal Server Error"},
                    {"status_code": 503, "text": "Service Unavailable"},
                    {"status_code": 200, "json": {"data": "success"}},
                ],
            )

            result = client._get("/api/test")

            assert result == {"data": "success"}
            assert mock_sleep.call_count == 2

    @patch("time.sleep")
    def test_server_error_max_retries_exceeded(self, mock_sleep, client: Client):
        """Test that DartServerError is raised after max retries."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                [
                    {"status_code": 500, "text": "Internal Server Error"},
                    {"status_code": 500, "text": "Internal Server Error"},
                    {"status_code": 500, "text": "Internal Server Error"},
                    {"status_code": 500, "text": "Internal Server Error"},
                ],
            )

            with pytest.raises(DartServerError) as exc_info:
                client._get("/api/test")

            assert exc_info.value.status_code == 500


class TestTimeoutAndNetworkErrors:
    """Tests for timeout and network error handling."""

    @patch("time.sleep")
    def test_timeout_retry_success(self, mock_sleep, client: Client):
        """Test that timeout errors trigger retry with eventual success."""
        call_count = 0

        def request_callback(request, context):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise requests.exceptions.Timeout("Connection timed out")
            context.status_code = 200
            return {"data": "success"}

        with requests_mock.Mocker() as m:
            m.get("https://opendart.fss.or.kr/api/test", json=request_callback)

            result = client._get("/api/test")

            assert result == {"data": "success"}
            assert mock_sleep.call_count == 2

    @patch("time.sleep")
    def test_timeout_max_retries_exceeded(self, mock_sleep, client: Client):
        """Test that DartTimeoutError is raised after max retries."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                exc=requests.exceptions.Timeout("Connection timed out"),
            )

            with pytest.raises(DartTimeoutError) as exc_info:
                client._get("/api/test")

            assert "timeout" in str(exc_info.value).lower()

    @patch("time.sleep")
    def test_connection_error_retry_success(self, mock_sleep, client: Client):
        """Test that connection errors trigger retry with eventual success."""
        call_count = 0

        def request_callback(request, context):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise requests.exceptions.ConnectionError("Connection refused")
            context.status_code = 200
            return {"data": "success"}

        with requests_mock.Mocker() as m:
            m.get("https://opendart.fss.or.kr/api/test", json=request_callback)

            result = client._get("/api/test")

            assert result == {"data": "success"}

    @patch("time.sleep")
    def test_connection_error_max_retries_exceeded(self, mock_sleep, client: Client):
        """Test that DartNetworkError is raised after max retries."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                exc=requests.exceptions.ConnectionError("Connection refused"),
            )

            with pytest.raises(DartNetworkError) as exc_info:
                client._get("/api/test")

            assert "Network connection failed" in str(exc_info.value)

    def test_generic_request_exception(self, client: Client):
        """Test that generic RequestException raises DartNetworkError."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                exc=requests.exceptions.RequestException("Unknown error"),
            )

            with pytest.raises(DartNetworkError) as exc_info:
                client._get("/api/test")

            assert "Request failed" in str(exc_info.value)


class TestHelperMethods:
    """Tests for helper methods."""

    def test_safe_json_valid(self, client: Client):
        mock_response = Mock()
        mock_response.json.return_value = {"test": "data"}

        result = client._safe_json(mock_response)

        assert result == {"test": "data"}

    def test_safe_json_invalid(self, client: Client):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")

        result = client._safe_json(mock_response)

        assert result is None

    def test_safe_json_decode_error(self, client: Client):
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)

        result = client._safe_json(mock_response)

        assert result is None

    def test_get_retry_after_header_present(self, client: Client):
        mock_response = Mock()
        mock_response.headers = {"Retry-After": "60"}

        result = client._get_retry_after(mock_response)

        assert result == 60

    def test_get_retry_after_header_missing(self, client: Client):
        mock_response = Mock()
        mock_response.headers = {}

        result = client._get_retry_after(mock_response)

        assert result is None

    def test_get_retry_after_header_invalid(self, client: Client):
        mock_response = Mock()
        mock_response.headers = {"Retry-After": "invalid"}

        result = client._get_retry_after(mock_response)

        assert result is None

    def test_close_session(self, client: Client):
        """Test that close() properly closes the session."""
        client.close()
        # Should not raise any errors


class TestNoRetryScenarios:
    """Tests for scenarios where retries should not occur."""

    def test_no_retry_on_auth_error(self, client: Client):
        """Authentication errors should not be retried."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                json={"error": "Unauthorized"},
                status_code=401,
            )

            with pytest.raises(DartAuthenticationError):
                client._get("/api/test")

            # Should only be called once (no retries)
            assert m.call_count == 1

    def test_no_retry_on_client_error(self, client: Client):
        """Client errors (4xx except 429) should not be retried."""
        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                text="Bad Request",
                status_code=400,
            )

            with pytest.raises(DartClientError):
                client._get("/api/test")

            # Should only be called once (no retries)
            assert m.call_count == 1


class TestZeroRetries:
    """Tests with max_retries=0."""

    def test_server_error_no_retry(self):
        """With max_retries=0, server errors should fail immediately."""
        client = Client(auth_key="test-key", max_retries=0)

        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                text="Internal Server Error",
                status_code=500,
            )

            with pytest.raises(DartServerError):
                client._get("/api/test")

            assert m.call_count == 1

    def test_rate_limit_no_retry(self):
        """With max_retries=0, 429 errors should fail immediately."""
        client = Client(auth_key="test-key", max_retries=0)

        with requests_mock.Mocker() as m:
            m.get(
                "https://opendart.fss.or.kr/api/test",
                json={"error": "Too Many Requests"},
                status_code=429,
            )

            with pytest.raises(DartRateLimitError):
                client._get("/api/test")

            assert m.call_count == 1
