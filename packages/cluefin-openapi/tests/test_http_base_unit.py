import requests

from cluefin_openapi._http_base import BaseHttpClient


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
