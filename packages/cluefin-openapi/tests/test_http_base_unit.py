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


@pytest.fixture
def rl():
    """A fast-refilling TokenBucket shared by most _execute_with_retry tests."""
    return TokenBucket(capacity=5, refill_rate=100.0)


def _retry_kwargs(**overrides):
    """Common dispatch/error_cls kwargs for _execute_with_retry, with per-test overrides."""
    kwargs = dict(
        dispatch=lambda r: None if r.status_code == 200 else _Boom(),
        rate_limit_error=lambda: _Boom(),
        timeout_error_cls=_Boom,
        network_error_cls=_Boom,
    )
    kwargs.update(overrides)
    return kwargs


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.request_context = kwargs.get("request_context")


def _run(client, adapter_setup):
    bucket = TokenBucket(capacity=5, refill_rate=100.0)
    with rm_mod.Mocker() as m:
        adapter_setup(m)

        def send():
            return requests.get("https://x.test/p")

        return client._execute_with_retry(
            send,
            rate_limiter=bucket,
            timeout=5,
            max_retries=2,
            request_context={"path": "/p"},
            **_retry_kwargs(),
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


def test_5xx_retry_emits_warning_log(monkeypatch, rl):
    import time as _time_mod

    from loguru import logger as _logger

    monkeypatch.setattr(_time_mod, "sleep", lambda s: None)
    records = []
    sink_id = _logger.add(lambda msg: records.append(str(msg)), level="WARNING")
    try:
        with rm_mod.Mocker() as m:
            m.get(
                "https://x.test/p",
                [{"status_code": 500, "text": "boom"}, {"status_code": 200, "text": "ok"}],
            )
            _Dummy()._execute_with_retry(
                lambda: requests.get("https://x.test/p"),
                rate_limiter=rl,
                timeout=5,
                max_retries=2,
                request_context={"path": "/p"},
                **_retry_kwargs(),
            )
    finally:
        _logger.remove(sink_id)
    assert any("Server error 500, retrying" in r for r in records)


def test_terminal_5xx_with_none_dispatch_returns_response(monkeypatch, rl):
    import time as _time_mod

    monkeypatch.setattr(_time_mod, "sleep", lambda s: None)
    with rm_mod.Mocker() as m:
        m.get("https://x.test/p", status_code=503, text="degraded")
        resp = _Dummy()._execute_with_retry(
            lambda: requests.get("https://x.test/p"),
            rate_limiter=rl,
            timeout=5,
            max_retries=1,
            request_context={"path": "/p"},
            **_retry_kwargs(dispatch=lambda r: None),  # accept even terminal 5xx
        )
    assert resp.status_code == 503


class _TimeoutBoom(_Boom):
    pass


class _NetBoom(_Boom):
    pass


def _run_raising(exc_to_raise, monkeypatch, max_retries=2):
    """Build a runner whose send_fn always raises; returns (run, attempts)."""
    import time as _time_mod

    monkeypatch.setattr(_time_mod, "sleep", lambda s: None)
    attempts = {"n": 0}

    def send():
        attempts["n"] += 1
        raise exc_to_raise

    bucket = TokenBucket(capacity=5, refill_rate=100.0)

    def run():
        _Dummy()._execute_with_retry(
            send,
            rate_limiter=bucket,
            timeout=5,
            max_retries=max_retries,
            request_context={"path": "/p"},
            **_retry_kwargs(
                dispatch=lambda r: None,
                timeout_error_cls=_TimeoutBoom,
                network_error_cls=_NetBoom,
            ),
        )

    return run, attempts


def test_timeout_retries_then_raises_timeout_error(monkeypatch):
    run, attempts = _run_raising(requests.exceptions.Timeout(), monkeypatch)
    with pytest.raises(_TimeoutBoom) as exc_info:
        run()
    assert attempts["n"] == 3  # initial + 2 retries
    assert exc_info.value.request_context == {"path": "/p"}


def test_connection_error_retries_then_raises_network_error(monkeypatch):
    run, attempts = _run_raising(requests.exceptions.ConnectionError("refused"), monkeypatch)
    with pytest.raises(_NetBoom) as exc_info:
        run()
    assert attempts["n"] == 3  # initial + 2 retries
    assert exc_info.value.request_context == {"path": "/p"}


def test_request_exception_raises_immediately_without_retry(monkeypatch):
    run, attempts = _run_raising(requests.exceptions.RequestException("bad"), monkeypatch)
    with pytest.raises(_NetBoom):
        run()
    assert attempts["n"] == 1  # no retry for generic RequestException


def test_rate_limiter_preflight_failure_raises_before_sending():
    class _NoTokens:
        def wait_for_tokens(self, timeout):
            return False

    sent = []
    with pytest.raises(_Boom):
        _Dummy()._execute_with_retry(
            lambda: sent.append(1),
            rate_limiter=_NoTokens(),
            timeout=5,
            max_retries=2,
            request_context={"path": "/p"},
            **_retry_kwargs(
                dispatch=lambda r: None,
                timeout_error_cls=_TimeoutBoom,
                network_error_cls=_NetBoom,
            ),
        )
    assert sent == []  # send_fn never called


def test_429_retry_honors_retry_after_header(monkeypatch, rl):
    import time as _time_mod

    sleeps = []
    monkeypatch.setattr(_time_mod, "sleep", lambda s: sleeps.append(s))
    with rm_mod.Mocker() as m:
        m.get(
            "https://x.test/p",
            [
                {"status_code": 429, "text": "slow down", "headers": {"Retry-After": "7"}},
                {"status_code": 200, "text": "ok"},
            ],
        )
        resp = _Dummy()._execute_with_retry(
            lambda: requests.get("https://x.test/p"),
            rate_limiter=rl,
            timeout=5,
            max_retries=2,
            request_context={"path": "/p"},
            **_retry_kwargs(timeout_error_cls=_TimeoutBoom, network_error_cls=_NetBoom),
        )
    assert resp.status_code == 200
    assert sleeps == [7]  # Retry-After wins over exponential backoff


def test_on_response_called_each_attempt(rl):
    seen = []
    with rm_mod.Mocker() as m:
        m.get("https://x.test/p", status_code=200, text="ok")
        _Dummy()._execute_with_retry(
            lambda: requests.get("https://x.test/p"),
            rate_limiter=rl,
            timeout=5,
            max_retries=2,
            request_context={"path": "/p"},
            **_retry_kwargs(dispatch=lambda r: None),
            on_response=lambda resp, ctx: seen.append(resp.status_code),
        )
    assert seen == [200]


# ---------------------------------------------------------------------------
# _dispatch_by_status tests
# ---------------------------------------------------------------------------


class _DispatchErr(Exception):
    """Mimics the (message, status_code=, response_data=, request_context=) contract
    that real per-broker exception classes must satisfy for _dispatch_by_status."""

    def __init__(self, message, *, status_code=None, response_data=None, request_context=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data
        self.request_context = request_context


class _ValidationErr(_DispatchErr):
    pass


class _AuthErr(_DispatchErr):
    pass


class _AuthzErr(_DispatchErr):
    pass


class _RateLimitErr(_DispatchErr):
    def __init__(self, message, *, retry_after=None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class _ServerErr(_DispatchErr):
    pass


class _ApiErr(_DispatchErr):
    pass


_ERROR_TYPES = {
    "validation": _ValidationErr,
    "auth": _AuthErr,
    "authz": _AuthzErr,
    "rate_limit": _RateLimitErr,
    "server": _ServerErr,
    "api": _ApiErr,
}


def _dispatch_client():
    client = _Dummy()
    client.max_retries = 2
    return client


@pytest.mark.parametrize(
    "status,expected_cls",
    [
        (400, _ValidationErr),
        (401, _AuthErr),
        (403, _AuthzErr),
        (404, _ApiErr),  # fallback bucket, no dedicated "not_found" key
        (429, _RateLimitErr),
        (500, _ServerErr),
        (503, _ServerErr),
    ],
)
def test_dispatch_by_status_maps_status_to_exception_class(status, expected_cls, monkeypatch):
    """Exercise _dispatch_by_status through the real _execute_with_retry dispatch path."""
    import time as _time_mod

    monkeypatch.setattr(_time_mod, "sleep", lambda s: None)
    client = _dispatch_client()
    bucket = TokenBucket(capacity=5, refill_rate=100.0)

    with rm_mod.Mocker() as m:
        headers = {"Retry-After": "9"} if status == 429 else {}
        m.get("https://x.test/p", status_code=status, text="body", headers=headers)

        with pytest.raises(expected_cls) as exc_info:
            client._execute_with_retry(
                lambda: requests.get("https://x.test/p"),
                rate_limiter=bucket,
                timeout=5,
                # max_retries=0 so the terminal (non-200) response is dispatched
                # immediately instead of retried.
                max_retries=0,
                request_context={"path": "/p"},
                dispatch=lambda r: client._dispatch_by_status(r, {"path": "/p"}, _ERROR_TYPES),
                rate_limit_error=lambda: _Boom(),
                timeout_error_cls=_Boom,
                network_error_cls=_Boom,
            )

    exc = exc_info.value
    assert exc.status_code == status
    assert exc.request_context == {"path": "/p"}
    if status == 429:
        assert exc.retry_after == 9
        assert "Rate limit exceeded after 2 retries" in str(exc)
    elif status == 400:
        assert "Bad request" in str(exc)
    elif status == 401:
        assert "Authentication failed" in str(exc)
    elif status == 403:
        assert "Access forbidden" in str(exc)
    elif 500 <= status < 600:
        assert "Server error" in str(exc)
    else:
        assert "Unexpected status code" in str(exc)


def test_dispatch_by_status_rate_limit_retry_after_absent(monkeypatch):
    client = _dispatch_client()
    resp = _resp(b"slow down", status=429)

    exc = client._dispatch_by_status(resp, {"path": "/p"}, _ERROR_TYPES)

    assert isinstance(exc, _RateLimitErr)
    assert exc.retry_after is None


# ---------------------------------------------------------------------------
# _sanitize_request_context tests
# ---------------------------------------------------------------------------


def test_sanitize_request_context_strips_headers_keeps_params_and_body():
    client = _Dummy()
    raw = {
        "method": "POST",
        "path": "/uapi/test",
        "url": "https://example.test/uapi/test",
        "headers": {"authorization": "Bearer secret", "tr_id": "TR123"},
        "params": {"symbol": "005930"},
        "body": {"account": "12345678-01"},
    }

    sanitized = client._sanitize_request_context(raw)

    assert "headers" not in sanitized
    assert "authorization" not in sanitized
    assert sanitized == {
        "method": "POST",
        "path": "/uapi/test",
        "url": "https://example.test/uapi/test",
        "tr_id": "TR123",
        "params": {"symbol": "005930"},
        "body": {"account": "12345678-01"},
    }


def test_sanitize_request_context_omits_params_and_body_when_absent():
    client = _Dummy()
    sanitized = client._sanitize_request_context({"method": "GET", "path": "/p"})

    assert "params" not in sanitized
    assert "body" not in sanitized
    assert sanitized["tr_id"] is None


def test_sanitize_request_context_is_idempotent():
    client = _Dummy()
    raw = {
        "method": "GET",
        "path": "/p",
        "url": "https://example.test/p",
        "headers": {"api-id": "ABC"},
        "params": {"a": 1},
        "body": {"b": 2},
    }

    once = client._sanitize_request_context(raw)
    twice = client._sanitize_request_context(once)

    assert once == twice
