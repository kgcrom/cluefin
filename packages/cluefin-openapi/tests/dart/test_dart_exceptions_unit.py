import pytest

from cluefin_openapi.dart._exceptions import (
    DartAPIError,
    DartAuthenticationError,
    DartClientError,
    DartServerError,
)


def test_base_accepts_request_context_and_defaults_empty():
    err = DartAPIError("boom")
    assert err.request_context == {}
    err2 = DartAPIError("boom", status_code=500, request_context={"path": "/x"})
    assert err2.request_context == {"path": "/x"}


def test_str_format_is_unchanged():
    assert str(DartAPIError("oops", status_code=404)) == "DART API Error [404]: oops"
    assert str(DartAPIError("oops")) == "DART API Error: oops"


def test_subclasses_accept_request_context_kwarg():
    for exc_cls in (DartAuthenticationError, DartClientError, DartServerError):
        e = exc_cls("m", status_code=400, response_data={"k": "v"}, request_context={"p": 1})
        assert e.request_context == {"p": 1}
        assert e.response_data == {"k": "v"}
