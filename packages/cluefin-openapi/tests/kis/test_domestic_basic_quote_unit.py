import json
from pathlib import Path
from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from cluefin_openapi.kis import _domestic_basic_quote as domestic_basic_quote_module
from cluefin_openapi.kis._domestic_basic_quote import DomesticBasicQuote
from cluefin_openapi.kis._exceptions import KISValidationError


def load_domestic_basic_quote_cases():
    path = Path(__file__).with_name("domestic_basic_quote_cases.json")
    with path.open(encoding="utf-8") as case_file:
        raw_cases = json.load(case_file)

    return [
        (
            case["method_name"],
            case["response_model_attr"],
            case["endpoint"],
            case["method"],
            case["call_kwargs"],
            case["expected_headers"],
            case["expected_body"],
            case["response_payload"],
        )
        for case in raw_cases
    ]


DOMESTIC_BASIC_QUOTE_CASES = load_domestic_basic_quote_cases()


@pytest.mark.parametrize(
    (
        "method_name",
        "response_model_attr",
        "endpoint",
        "method",
        "call_kwargs",
        "expected_headers",
        "expected_body",
        "response_payload",
    ),
    DOMESTIC_BASIC_QUOTE_CASES,
)
def test_domestic_basic_quote_builds_request(
    monkeypatch,
    method_name,
    response_model_attr,
    endpoint,
    method,
    call_kwargs,
    expected_headers,
    expected_body,
    response_payload,
):
    # Mock response object with json() method
    mock_response = Mock()
    mock_response.json.return_value = response_payload
    mock_response.status_code = 200
    mock_response.text = ""
    mock_response.headers = {
        "content-type": "application/json; charset=utf-8",
        "tr_id": expected_headers.get("tr_id", ""),
        "tr_cont": expected_headers.get("tr_cont", ""),
        "gt_uid": None,
    }

    client = Mock()
    client._post.return_value = mock_response
    client._get.return_value = mock_response
    captured_instances = []

    class DummyResponseModel:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            captured_instances.append(self)

        @classmethod
        def model_validate(cls, data):
            return cls(**data)

    monkeypatch.setattr(domestic_basic_quote_module, response_model_attr, DummyResponseModel)

    basic_quote = DomesticBasicQuote(client)
    result = getattr(basic_quote, method_name)(**call_kwargs)

    if method == "POST":
        client._post.assert_called_once_with(
            endpoint,
            headers=expected_headers,
            body=expected_body,
        )
    else:
        client._get.assert_called_once_with(
            endpoint,
            headers=expected_headers,
            params=expected_body,
        )

    assert len(captured_instances) == 1
    assert result.body is captured_instances[0]
    assert captured_instances[0].kwargs == response_payload


def _mock_client(payload: dict) -> Mock:
    response = Mock()
    response.json.return_value = payload
    response.headers = {"content-type": "application/json; charset=utf-8", "tr_id": "FHKST01010100"}
    client = Mock()
    client._get.return_value = response
    return client


def test_get_stock_current_price_wraps_broken_payload_in_kis_validation_error() -> None:
    """실제 모델로 검증한다. 누가 model_validate 로 되돌리면 pydantic ValidationError 가 그대로 새어 나온다."""
    payload = {"rt_cd": "0", "msg_cd": "MCA00000", "msg1": "정상처리", "output": "not-a-dict"}
    basic_quote = DomesticBasicQuote(_mock_client(payload))

    with pytest.raises(KISValidationError) as exc_info:
        basic_quote.get_stock_current_price(fid_cond_mrkt_div_code="J", fid_input_iscd="005930")

    err = exc_info.value
    assert err.response_data is payload
    assert "DomesticStockCurrentPrice validation failed" in err.message
    assert isinstance(err.__cause__, ValidationError)


def test_get_stock_current_price_wraps_broken_header_in_kis_validation_error() -> None:
    payload = {"rt_cd": "0", "msg_cd": "MCA00000", "msg1": "정상처리", "output": {}}
    client = _mock_client(payload)
    client._get.return_value.headers = {"content-type": "application/json"}  # tr_id 누락

    with pytest.raises(KISValidationError, match="KisHttpHeader validation failed"):
        DomesticBasicQuote(client).get_stock_current_price(fid_cond_mrkt_div_code="J", fid_input_iscd="005930")
