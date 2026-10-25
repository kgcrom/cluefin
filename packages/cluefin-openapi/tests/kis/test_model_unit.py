import logging

import pytest
from pydantic import BaseModel

from cluefin_openapi.kis._exceptions import KISValidationError
from cluefin_openapi.kis._model import validate_kis_response


class _Body(BaseModel):
    rt_cd: str
    output: list[str]


def test_validate_kis_response_returns_model_on_valid_data() -> None:
    body = validate_kis_response(_Body, {"rt_cd": "0", "output": ["a"]})
    assert body.output == ["a"]


def test_validate_kis_response_wraps_validation_error_with_raw_response() -> None:
    raw = {"rt_cd": "0", "output": {"unexpected": "dict"}}
    with pytest.raises(KISValidationError) as exc_info:
        validate_kis_response(_Body, raw)

    err = exc_info.value
    assert err.response_data is raw
    assert "_Body validation failed" in err.message
    assert "output" in err.message
    assert isinstance(err.__cause__, Exception)


def test_validate_kis_response_does_not_log_the_raw_response(caplog) -> None:
    """원문은 예외로만 전달한다. 로그로도 남기면 잡아서 처리하는 호출부에서도 계좌 응답 원문이 찍힌다."""
    raw = {"rt_cd": "0", "output": {"acnt_no": "secret-account"}}
    caplog.set_level(logging.DEBUG, logger="cluefin_openapi")
    with pytest.raises(KISValidationError):
        validate_kis_response(_Body, raw)

    assert caplog.records == []
