"""피드 공용 HTTP 도우미: 재시도·예외 변환·호출 간격."""

from unittest.mock import patch

import pytest
import requests
import requests_mock

from cluefin_feeds import (
    FeedClientError,
    FeedNetworkError,
    FeedRateLimitError,
    FeedServerError,
    FeedTimeoutError,
    HttpClient,
)

URL = "https://example.gov/data"


@pytest.fixture(autouse=True)
def no_sleep():
    with patch("cluefin_feeds._http.time.sleep") as sleep:
        yield sleep


def _client(max_retries: int = 2) -> HttpClient:
    return HttpClient(max_retries=max_retries, min_interval=0)


def test_get_sends_user_agent_and_params():
    with requests_mock.Mocker() as m:
        m.get(URL, text="ok")
        assert _client().get(URL, {"a": "1"}).text == "ok"
        assert m.last_request.qs == {"a": ["1"]}
        assert m.last_request.headers["User-Agent"].startswith("cluefin-feeds/")


def test_post_json_body():
    with requests_mock.Mocker() as m:
        m.post(URL, json={"ok": True})
        _client().post_json(URL, {"seriesid": ["X"]})
        assert m.last_request.json() == {"seriesid": ["X"]}


@pytest.mark.parametrize(("status", "error"), [(429, FeedRateLimitError), (503, FeedServerError)])
def test_retryable_status_is_retried_then_raised(status, error):
    with requests_mock.Mocker() as m:
        m.get(URL, status_code=status)
        with pytest.raises(error) as info:
            _client(max_retries=2).get(URL)
        assert m.call_count == 3
    assert info.value.status_code == status
    assert info.value.url == URL


def test_retry_then_success(no_sleep):
    with requests_mock.Mocker() as m:
        m.get(URL, [{"status_code": 429, "headers": {"Retry-After": "7"}}, {"text": "ok"}])
        assert _client().get(URL).text == "ok"
    no_sleep.assert_any_call(7)


def test_client_error_is_not_retried():
    with requests_mock.Mocker() as m:
        m.get(URL, status_code=404)
        with pytest.raises(FeedClientError):
            _client().get(URL)
        assert m.call_count == 1


@pytest.mark.parametrize(
    ("exc", "error"),
    [(requests.exceptions.ConnectTimeout, FeedTimeoutError), (requests.exceptions.ConnectionError, FeedNetworkError)],
)
def test_transport_errors_are_retried_then_raised(exc, error):
    with requests_mock.Mocker() as m:
        m.get(URL, exc=exc)
        with pytest.raises(error) as info:
            _client(max_retries=1).get(URL)
        assert m.call_count == 2
    assert info.value.__cause__ is None


def test_min_interval_spaces_calls(no_sleep):
    client = HttpClient(max_retries=0, min_interval=10)
    with requests_mock.Mocker() as m:
        m.get(URL, text="ok")
        client.get(URL)
        client.get(URL)
    assert any(call.args[0] > 9 for call in no_sleep.call_args_list)
