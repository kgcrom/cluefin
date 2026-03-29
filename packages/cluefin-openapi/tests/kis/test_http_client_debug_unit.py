"""Unit tests for KIS HttpClient debug capture."""

from pathlib import Path

import pytest

from cluefin_openapi.kis._exceptions import KISValidationError
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
