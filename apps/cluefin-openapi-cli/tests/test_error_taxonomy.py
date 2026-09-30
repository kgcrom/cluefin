"""How broker exceptions map onto the CLI exit-code taxonomy.

Matching is by class-name suffix because kis/kiwoom/dart exception hierarchies are
parallel copies, so the stubs below only need the right name and payload attributes.
"""

from __future__ import annotations

import pytest

from cluefin_openapi_cli.errors import (
    EXIT_BROKER,
    EXIT_CREDENTIALS,
    EXIT_RATE_LIMIT,
    EXIT_UNEXPECTED,
    classify_exception,
)


class _RateLimitError(Exception):
    retry_after = 7


class _KISAuthenticationError(Exception):
    status_code = 401


class _KiwoomNetworkError(Exception):
    pass


class _KISAPIError(Exception):
    response_data = {"rt_cd": "1", "msg_cd": "EGW00123", "msg1": "token mismatch"}


@pytest.mark.parametrize(
    ("exc", "exit_code", "error_type", "retryable"),
    [
        (_RateLimitError("slow down"), EXIT_RATE_LIMIT, "RateLimitError", True),
        (_KISAuthenticationError("401"), EXIT_CREDENTIALS, "AuthenticationError", False),
        (
            ValueError("KIS credentials not configured (kis_app_key, kis_secret_key)"),
            EXIT_CREDENTIALS,
            "CredentialsMissing",
            False,
        ),
        (_KiwoomNetworkError("boom"), EXIT_BROKER, "BrokerUnavailable", True),
        (_KISAPIError("bad"), EXIT_BROKER, "BrokerApiError", False),
        (ValueError("KIS API Error [OPSQ0001]: no data (rt_cd=1)"), EXIT_BROKER, "BrokerApiError", False),
        (RuntimeError("weird"), EXIT_UNEXPECTED, "ExecutionError", False),
    ],
)
def test_classify_exception_maps_to_exit_codes(exc, exit_code, error_type, retryable) -> None:
    error = classify_exception(exc, command="kis.stock.current-price", broker="kis")

    assert error.exit_code == exit_code
    assert error.error_type == error_type
    assert error.retryable is retryable
    payload = error.to_payload()["error"]
    assert payload["exit_code"] == exit_code
    assert payload["data"]["command"] == "kis.stock.current-price"


def test_classify_rate_limit_and_api_error_carry_broker_detail() -> None:
    rate = classify_exception(_RateLimitError("slow"), command="c", broker="kis")
    assert rate.data["retry_after"] == 7
    api = classify_exception(_KISAPIError("bad"), command="c", broker="kis")
    assert api.data["msg_cd"] == "EGW00123"


def test_classify_pydantic_response_parse_error() -> None:
    from pydantic import BaseModel, ValidationError

    class Model(BaseModel):
        a: int
        b: str

    with pytest.raises(ValidationError) as exc_info:
        Model.model_validate({})
    error = classify_exception(exc_info.value, command="kis.stock.current-price", broker="kis")

    assert error.exit_code == EXIT_BROKER
    assert error.error_type == "ResponseParseError"
    assert error.data["fields"] == ["a", "b"]
    assert error.data["model"] == "Model"
    assert "field errors" in error.message


class _DartAPIError(Exception):
    def __init__(self, message: str, status: str) -> None:
        super().__init__(message)
        self.response_data = {"status": status, "message": message}


def test_dart_request_limit_status_is_exit_5_with_daily_quota_hint() -> None:
    error = classify_exception(_DartAPIError("요청 제한을 초과하였습니다.", "020"), command="dart.x", broker="dart")

    assert error.exit_code == EXIT_RATE_LIMIT
    assert error.error_type == "RateLimitError"
    assert error.retryable is True
    assert error.data["status"] == "020"
    assert "daily" in (error.hint or "")
    assert "retry_after" not in error.data


def test_dart_other_status_keeps_generic_api_error_bucket() -> None:
    error = classify_exception(_DartAPIError("조회된 데이타가 없습니다.", "013"), command="dart.x", broker="dart")

    assert error.exit_code == EXIT_BROKER
    assert error.error_type == "BrokerApiError"


def test_status_020_on_non_api_error_class_is_not_rate_limited() -> None:
    class _Odd(Exception):
        response_data = {"status": "020"}

    assert classify_exception(_Odd("x"), command="c", broker="dart").exit_code == EXIT_UNEXPECTED
