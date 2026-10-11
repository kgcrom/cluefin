"""Unit tests for the SEC EDGAR client: User-Agent, host guard, rate limit and retry."""

from unittest.mock import patch

import pytest
import requests
import requests_mock

from cluefin_openapi.sec import (
    Client,
    SecAPIError,
    SecAuthorizationError,
    SecClientError,
    SecNetworkError,
    SecNotFoundError,
    SecRateLimitError,
    SecServerError,
    SecTimeoutError,
)

USER_AGENT = "Cluefin Test test@example.com"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK0000320193.json"


@pytest.fixture
def client() -> Client:
    return Client(user_agent=USER_AGENT)


class TestClientInitialization:
    def test_default_values(self, client: Client):
        assert client.user_agent == USER_AGENT
        assert client.timeout == 30
        assert client.max_retries == 3
        assert client._rate_limiter.refill_rate == 8.0
        assert client._rate_limiter.capacity == 8

    def test_user_agent_is_stripped_and_sent(self):
        client = Client(user_agent=f"  {USER_AGENT}  ")
        assert client._session.headers["User-Agent"] == USER_AGENT

    @pytest.mark.parametrize("user_agent", ["", "   ", "Cluefin Research", None])
    def test_user_agent_without_email_is_rejected(self, user_agent):
        with pytest.raises(ValueError, match="User-Agent"):
            Client(user_agent=user_agent)  # type: ignore[arg-type]

    @pytest.mark.parametrize("rate", [0, -1, 10.5, 20])
    def test_rate_above_sec_limit_is_rejected(self, rate):
        with pytest.raises(ValueError, match="rate_limit_requests_per_second"):
            Client(user_agent=USER_AGENT, rate_limit_requests_per_second=rate)

    @pytest.mark.parametrize("burst", [0, 11])
    def test_burst_out_of_range_is_rejected(self, burst):
        with pytest.raises(ValueError, match="rate_limit_burst"):
            Client(user_agent=USER_AGENT, rate_limit_burst=burst)

    def test_sec_limit_itself_is_allowed(self):
        client = Client(user_agent=USER_AGENT, rate_limit_requests_per_second=10, rate_limit_burst=10)
        assert client._rate_limiter.refill_rate == 10


class TestRequests:
    def test_get_json_sends_user_agent(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, json={"cik": "320193"})
            assert client._get_json(SUBMISSIONS_URL) == {"cik": "320193"}
            assert m.last_request.headers["User-Agent"] == USER_AGENT

    def test_get_bytes_returns_raw_body(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(TICKERS_URL, content=b"\x00\x01raw")
            assert client._get_bytes(TICKERS_URL) == b"\x00\x01raw"

    @pytest.mark.parametrize(
        "url",
        [
            "http://www.sec.gov/files/company_tickers.json",
            "https://example.com/files/company_tickers.json",
            "https://efts.sec.gov/LATEST/search-index",
            "https://www.sec.gov.evil.example/x",
        ],
    )
    def test_non_sec_urls_are_rejected_before_sending(self, client: Client, url):
        with requests_mock.Mocker() as m:
            with pytest.raises(ValueError, match="sec.gov"):
                client._get_json(url)
            assert m.call_count == 0


class TestErrorMapping:
    def test_403_maps_to_authorization_error_without_retry(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, status_code=403, text="Undeclared Automated Tool")
            with pytest.raises(SecAuthorizationError) as exc_info:
                client._get_json(SUBMISSIONS_URL)
            assert m.call_count == 1
        assert exc_info.value.status_code == 403
        assert "User-Agent" in exc_info.value.message

    def test_404_maps_to_not_found(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, status_code=404)
            with pytest.raises(SecNotFoundError) as exc_info:
                client._get_json(SUBMISSIONS_URL)
        assert exc_info.value.request_context["url"] == SUBMISSIONS_URL

    def test_other_4xx_maps_to_client_error(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, status_code=400)
            with pytest.raises(SecClientError):
                client._get_json(SUBMISSIONS_URL)

    def test_unexpected_status_maps_to_api_error(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, status_code=302)
            with pytest.raises(SecAPIError):
                client._get_json(SUBMISSIONS_URL)

    def test_error_context_does_not_carry_user_agent(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, status_code=404)
            with pytest.raises(SecNotFoundError) as exc_info:
                client._get_json(SUBMISSIONS_URL)
        assert USER_AGENT not in str(exc_info.value.request_context)
        assert exc_info.value.request_context == {
            "url": SUBMISSIONS_URL,
            "path": "/submissions/CIK0000320193.json",
            "method": "GET",
        }


class TestRetry:
    @patch("time.sleep")
    def test_429_is_retried_then_succeeds(self, mock_sleep, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, [{"status_code": 429}, {"status_code": 200, "json": {"ok": True}}])
            assert client._get_json(SUBMISSIONS_URL) == {"ok": True}
        mock_sleep.assert_called_once_with(1)

    @patch("time.sleep")
    def test_429_honours_retry_after(self, mock_sleep, client: Client):
        with requests_mock.Mocker() as m:
            m.get(
                SUBMISSIONS_URL,
                [{"status_code": 429, "headers": {"Retry-After": "7"}}, {"status_code": 200, "json": {}}],
            )
            client._get_json(SUBMISSIONS_URL)
        mock_sleep.assert_called_once_with(7)

    @patch("time.sleep")
    def test_429_exhausted_raises_rate_limit_error(self, mock_sleep, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, status_code=429)
            with pytest.raises(SecRateLimitError):
                client._get_json(SUBMISSIONS_URL)
            assert m.call_count == client.max_retries + 1

    @patch("time.sleep")
    def test_5xx_exhausted_raises_server_error(self, mock_sleep, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, status_code=503)
            with pytest.raises(SecServerError):
                client._get_json(SUBMISSIONS_URL)
            assert m.call_count == client.max_retries + 1

    @patch("time.sleep")
    def test_timeout_exhausted_raises_timeout_error(self, mock_sleep, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, exc=requests.exceptions.Timeout)
            with pytest.raises(SecTimeoutError):
                client._get_json(SUBMISSIONS_URL)

    @patch("time.sleep")
    def test_connection_error_exhausted_raises_network_error(self, mock_sleep, client: Client):
        with requests_mock.Mocker() as m:
            m.get(SUBMISSIONS_URL, exc=requests.exceptions.ConnectionError)
            with pytest.raises(SecNetworkError):
                client._get_json(SUBMISSIONS_URL)

    def test_rate_limiter_timeout_raises_rate_limit_error(self, client: Client):
        with patch.object(client._rate_limiter, "wait_for_tokens", return_value=False):
            with pytest.raises(SecRateLimitError, match="Rate limit timeout"):
                client._get_json(SUBMISSIONS_URL)


def test_exception_str_includes_status():
    assert str(SecNotFoundError("missing")) == "SEC API Error [404]: missing"
    assert str(SecTimeoutError()) == "SEC API Error: Request timeout"


def test_close_closes_session(client: Client):
    with patch.object(client._session, "close") as close:
        client.close()
    close.assert_called_once()
