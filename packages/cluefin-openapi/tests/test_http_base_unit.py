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
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.request_context = kwargs.get("request_context")


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
            timeout_error_cls=_Boom,
            network_error_cls=_Boom,
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


def test_5xx_retry_emits_warning_log(monkeypatch):
    import time as _time_mod

    from loguru import logger as _logger

    monkeypatch.setattr(_time_mod, "sleep", lambda s: None)
    records = []
    sink_id = _logger.add(lambda msg: records.append(str(msg)), level="WARNING")
    try:
        rl = TokenBucket(capacity=5, refill_rate=100.0)
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
                dispatch=lambda r: None if r.status_code == 200 else _Boom(),
                rate_limit_error=lambda: _Boom(),
                timeout_error_cls=_Boom,
                network_error_cls=_Boom,
            )
    finally:
        _logger.remove(sink_id)
    assert any("Server error 500, retrying" in r for r in records)


def test_terminal_5xx_with_none_dispatch_returns_response(monkeypatch):
    import time as _time_mod

    monkeypatch.setattr(_time_mod, "sleep", lambda s: None)
    rl = TokenBucket(capacity=5, refill_rate=100.0)
    with rm_mod.Mocker() as m:
        m.get("https://x.test/p", status_code=503, text="degraded")
        resp = _Dummy()._execute_with_retry(
            lambda: requests.get("https://x.test/p"),
            rate_limiter=rl,
            timeout=5,
            max_retries=1,
            request_context={"path": "/p"},
            dispatch=lambda r: None,  # accept even terminal 5xx
            rate_limit_error=lambda: _Boom(),
            timeout_error_cls=_Boom,
            network_error_cls=_Boom,
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

    rl = TokenBucket(capacity=5, refill_rate=100.0)

    def run():
        _Dummy()._execute_with_retry(
            send,
            rate_limiter=rl,
            timeout=5,
            max_retries=max_retries,
            request_context={"path": "/p"},
            dispatch=lambda r: None,
            rate_limit_error=lambda: _Boom(),
            timeout_error_cls=_TimeoutBoom,
            network_error_cls=_NetBoom,
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
            dispatch=lambda r: None,
            rate_limit_error=lambda: _Boom(),
            timeout_error_cls=_TimeoutBoom,
            network_error_cls=_NetBoom,
        )
    assert sent == []  # send_fn never called


def test_429_retry_honors_retry_after_header(monkeypatch):
    import time as _time_mod

    sleeps = []
    monkeypatch.setattr(_time_mod, "sleep", lambda s: sleeps.append(s))
    rl = TokenBucket(capacity=5, refill_rate=100.0)
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
            dispatch=lambda r: None if r.status_code == 200 else _Boom(),
            rate_limit_error=lambda: _Boom(),
            timeout_error_cls=_TimeoutBoom,
            network_error_cls=_NetBoom,
        )
    assert resp.status_code == 200
    assert sleeps == [7]  # Retry-After wins over exponential backoff


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
            timeout_error_cls=_Boom,
            network_error_cls=_Boom,
            on_response=lambda resp, ctx: seen.append(resp.status_code),
        )
    assert seen == [200]
