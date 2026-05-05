"""Unit tests for KIS HttpClient debug capture."""

from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

from cluefin_openapi.kis._exceptions import (
    KISAPIError,
    KISAuthenticationError,
    KISAuthorizationError,
    KISNetworkError,
    KISRateLimitError,
    KISServerError,
    KISTimeoutError,
    KISValidationError,
)
from cluefin_openapi.kis._http_client import HttpClient


@pytest.fixture
def client() -> HttpClient:
    """Create a lightweight HttpClient for debug capture tests."""
    return HttpClient(
        token="test_token",
        app_key="test_app_key",
        secret_key="test_secret_key",
        env="dev",
    )


def test_get_records_last_response_debug(client: HttpClient, requests_mock):
    """Successful responses should leave a readable raw-response artifact."""
    requests_mock.get(
        "https://openapivts.koreainvestment.com:29443/uapi/test-debug",
        json={"rt_cd": "0", "msg_cd": "0000", "msg1": "OK", "output": [{"foo": "bar"}]},
    )

    client._get("/uapi/test-debug", headers={"tr_id": "FHKST00000000"}, params={"FID_INPUT_ISCD": "005930"})

    debug = client.last_response_debug
    assert debug is not None
    assert debug["request"]["tr_id"] == "FHKST00000000"
    assert debug["request"]["path"] == "/uapi/test-debug"
    assert debug["artifact_path"] is not None
    assert Path(debug["artifact_path"]).exists()
    assert '"foo": "bar"' in debug["preview"]

    formatted = client.format_last_response_debug()
    assert "artifact_path:" in formatted
    assert "tr_id: FHKST00000000" in formatted
    assert "authorization" not in formatted
    assert "appsecret" not in formatted


def test_get_records_last_response_debug_on_http_error(client: HttpClient, requests_mock):
    """HTTP errors should still leave the last raw response available for inspection."""
    requests_mock.get(
        "https://openapivts.koreainvestment.com:29443/uapi/test-debug-error",
        status_code=400,
        json={"rt_cd": "1", "msg_cd": "EGW001", "msg1": "Bad request"},
    )

    with pytest.raises(KISValidationError):
        client._get("/uapi/test-debug-error", headers={"tr_id": "FHKST99999999"}, params={"FID_INPUT_ISCD": "0000"})

    debug = client.last_response_debug
    assert debug is not None
    assert debug["status_code"] == 400
    assert debug["artifact_path"] is not None
    assert Path(debug["artifact_path"]).exists()
    assert '"msg1": "Bad request"' in debug["preview"]


def test_client_domain_properties_return_wrappers(client: HttpClient):
    assert client.domestic_account.client is client
    assert client.domestic_basic_quote.client is client
    assert client.domestic_issue_other.client is client
    assert client.domestic_stock_info.client is client
    assert client.domestic_market_analysis.client is client
    assert client.domestic_ranking_analysis.client is client
    assert client.onmarket_bond_basic_quote.client is client
    assert client.overseas_account.client is client
    assert client.overseas_basic_quote.client is client
    assert client.overseas_market_analysis.client is client


def test_http_client_helpers(client: HttpClient):
    headers = client._build_headers({"tr_id": "FHKST00000000"})
    assert headers["authorization"] == "Bearer test_token"
    assert headers["appkey"] == "test_app_key"
    assert headers["appsecret"] == "test_secret_key"
    assert headers["tr_id"] == "FHKST00000000"

    response = requests.Response()
    response._content = b"not-json"
    assert client._safe_json(response) is None

    retry_response = requests.Response()
    retry_response.headers["Retry-After"] = "3"
    assert client._get_retry_after(retry_response) == 3
    retry_response.headers["Retry-After"] = "soon"
    assert client._get_retry_after(retry_response) is None

    sanitized = client._sanitize_request_context(
        {
            "method": "GET",
            "path": "/uapi/test",
            "url": "https://example.test/uapi/test",
            "headers": {"authorization": "secret", "tr_id": "TR123"},
            "params": {"FID_INPUT_ISCD": "005930"},
            "body": {"foo": "bar"},
        }
    )
    assert sanitized == {
        "method": "GET",
        "path": "/uapi/test",
        "url": "https://example.test/uapi/test",
        "tr_id": "TR123",
        "params": {"FID_INPUT_ISCD": "005930"},
        "body": {"foo": "bar"},
    }
    assert client._serialize_payload({"한글": "값"}) == '{\n  "한글": "값"\n}'
    assert client.format_last_response_debug() == ""


def test_write_debug_artifact_ignores_os_errors(client: HttpClient, monkeypatch):
    monkeypatch.setattr(Path, "mkdir", Mock(side_effect=OSError("no permission")))

    response = requests.Response()
    response.status_code = 200
    response.headers["content-type"] = "application/json"

    assert client._write_debug_artifact({"path": "/uapi/test", "tr_id": "TR"}, response, {"ok": True}) is None


@pytest.mark.parametrize(
    ("status_code", "exception_type"),
    [
        (400, KISValidationError),
        (401, KISAuthenticationError),
        (403, KISAuthorizationError),
        (429, KISRateLimitError),
        (500, KISServerError),
        (418, KISAPIError),
    ],
)
def test_get_raises_typed_errors(client: HttpClient, requests_mock, status_code, exception_type):
    client.max_retries = 0
    requests_mock.get(
        "https://openapivts.koreainvestment.com:29443/uapi/error",
        status_code=status_code,
        headers={"Retry-After": "7"},
        json={"rt_cd": "1", "msg_cd": "ERR", "msg1": "error"},
    )

    with pytest.raises(exception_type) as exc_info:
        client._get("/uapi/error", headers={"tr_id": "TR"}, params={"p": "v"})

    assert exc_info.value.request_context["method"] == "GET"
    if status_code == 429:
        assert exc_info.value.retry_after == 7


def test_get_retries_server_error_then_succeeds(client: HttpClient, requests_mock, monkeypatch):
    monkeypatch.setattr("cluefin_openapi.kis._http_client.time.sleep", Mock())
    client.max_retries = 1
    requests_mock.get(
        "https://openapivts.koreainvestment.com:29443/uapi/retry",
        [
            {"status_code": 500, "json": {"rt_cd": "1", "msg1": "server"}},
            {"status_code": 200, "json": {"rt_cd": "0", "msg1": "OK"}},
        ],
    )

    response = client._get("/uapi/retry", headers={"tr_id": "TR"}, params={})

    assert response.status_code == 200
    assert requests_mock.call_count == 2


@pytest.mark.parametrize(
    ("side_effect", "exception_type"),
    [
        (requests.exceptions.Timeout("timeout"), KISTimeoutError),
        (requests.exceptions.ConnectionError("connection"), KISNetworkError),
        (requests.exceptions.RequestException("request"), KISNetworkError),
    ],
)
def test_get_translates_request_exceptions(client: HttpClient, side_effect, exception_type):
    client.max_retries = 0
    client._session.get = Mock(side_effect=side_effect)

    with pytest.raises(exception_type):
        client._get("/uapi/network", headers={"tr_id": "TR"}, params={})


@pytest.mark.parametrize("method_name", ["_get", "_post"])
def test_requests_raise_when_rate_limiter_times_out(client: HttpClient, method_name):
    client._rate_limiter.wait_for_tokens = Mock(return_value=False)

    with pytest.raises(KISRateLimitError):
        if method_name == "_get":
            client._get("/uapi/rate", headers={}, params={})
        else:
            client._post("/uapi/rate", headers={}, body={})


def test_post_success_records_debug(client: HttpClient, requests_mock):
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/uapi/post-debug",
        json={"rt_cd": "0", "msg_cd": "0000", "msg1": "OK"},
    )

    response = client._post("/uapi/post-debug", headers={"tr_id": "POST_TR"}, body={"ord": "1"})

    assert response.status_code == 200
    assert client.last_response_debug["request"]["body"] == {"ord": "1"}


@pytest.mark.parametrize(
    ("status_code", "exception_type"),
    [
        (400, KISValidationError),
        (401, KISAuthenticationError),
        (403, KISAuthorizationError),
        (429, KISRateLimitError),
        (500, KISServerError),
        (418, KISAPIError),
    ],
)
def test_post_raises_typed_errors(client: HttpClient, requests_mock, status_code, exception_type):
    client.max_retries = 0
    requests_mock.post(
        "https://openapivts.koreainvestment.com:29443/uapi/post-error",
        status_code=status_code,
        headers={"Retry-After": "5"},
        json={"rt_cd": "1", "msg_cd": "ERR", "msg1": "error"},
    )

    with pytest.raises(exception_type) as exc_info:
        client._post("/uapi/post-error", headers={"tr_id": "TR"}, body={"p": "v"})

    assert exc_info.value.request_context["method"] == "POST"
    if status_code == 429:
        assert exc_info.value.retry_after == 5


@pytest.mark.parametrize(
    ("side_effect", "exception_type"),
    [
        (requests.exceptions.Timeout("timeout"), KISTimeoutError),
        (requests.exceptions.ConnectionError("connection"), KISNetworkError),
        (requests.exceptions.RequestException("request"), KISNetworkError),
    ],
)
def test_post_translates_request_exceptions(client: HttpClient, side_effect, exception_type):
    client.max_retries = 0
    client._session.post = Mock(side_effect=side_effect)

    with pytest.raises(exception_type):
        client._post("/uapi/network", headers={"tr_id": "TR"}, body={})


def test_close_closes_underlying_session(client: HttpClient):
    client._session.close = Mock()

    client.close()

    client._session.close.assert_called_once()
