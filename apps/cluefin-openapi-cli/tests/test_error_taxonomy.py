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
