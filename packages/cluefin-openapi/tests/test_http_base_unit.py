import pytest
import requests
import requests_mock as rm_mod

from cluefin_openapi._http_base import BaseHttpClient
from cluefin_openapi._rate_limiter import TokenBucket


class _Dummy(BaseHttpClient):
    pass


def _resp(body: bytes, headers=None, status=200):
    r = requests.Response()
    r.status_code = status
    r._content = body
    if headers:
        r.headers.update(headers)
    return r


def test_safe_json_parses_object():
    assert _Dummy()._safe_json(_resp(b'{"a": 1}')) == {"a": 1}


def test_safe_json_returns_none_on_garbage():
    assert _Dummy()._safe_json(_resp(b"not json")) is None


def test_get_retry_after_parses_int():
    assert _Dummy()._get_retry_after(_resp(b"", {"Retry-After": "7"})) == 7


def test_get_retry_after_none_when_absent_or_bad():
    assert _Dummy()._get_retry_after(_resp(b"")) is None
    assert _Dummy()._get_retry_after(_resp(b"", {"Retry-After": "soon"})) is None


# ---------------------------------------------------------------------------
# _execute_with_retry tests
# ---------------------------------------------------------------------------


class _Boom(Exception):
    pass


def _run(client, adapter_setup):
    rl = TokenBucket(capacity=5, refill_rate=100.0)
    with rm_mod.Mocker() as m:
        adapter_setup(m)

        def send():
            return requests.get("https://x.test/p")

        return client._execute_with_retry(
            send,
            rate_limiter=rl,
            timeout=5,
            max_retries=2,
            request_context={"path": "/p"},
            dispatch=lambda r: None if r.status_code == 200 else _Boom(),
            rate_limit_error=lambda: _Boom(),
            timeout_error=lambda e: _Boom(),
            network_error=lambda e: _Boom(),
        )


def test_returns_response_on_200():
    resp = _run(_Dummy(), lambda m: m.get("https://x.test/p", text="ok", status_code=200))
    assert resp.status_code == 200


def test_dispatch_exception_raised_on_4xx():
    with pytest.raises(_Boom):
        _run(_Dummy(), lambda m: m.get("https://x.test/p", status_code=404))


def test_5xx_retries_then_dispatches(monkeypatch):
    import time as _time_mod

    monkeypatch.setattr(_time_mod, "sleep", lambda s: None)
    calls = {"n": 0}

    def cb(request, context):
        calls["n"] += 1
        context.status_code = 500
        return ""

    with pytest.raises(_Boom):
        _run(_Dummy(), lambda m: m.get("https://x.test/p", text=cb))
    assert calls["n"] == 3  # initial + 2 retries


def test_on_response_called_each_attempt():
    seen = []
    rl = TokenBucket(capacity=5, refill_rate=100.0)
    with rm_mod.Mocker() as m:
        m.get("https://x.test/p", status_code=200, text="ok")
        _Dummy()._execute_with_retry(
            lambda: requests.get("https://x.test/p"),
            rate_limiter=rl,
            timeout=5,
            max_retries=2,
            request_context={"path": "/p"},
            dispatch=lambda r: None,
            rate_limit_error=lambda: _Boom(),
            timeout_error=lambda e: _Boom(),
            network_error=lambda e: _Boom(),
            on_response=lambda resp, ctx: seen.append(resp.status_code),
        )
    assert seen == [200]
