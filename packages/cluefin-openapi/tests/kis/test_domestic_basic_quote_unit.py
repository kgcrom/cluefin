from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from cluefin_openapi.kis import _domestic_basic_quote as domestic_basic_quote_module
from cluefin_openapi.kis._domestic_basic_quote import DomesticBasicQuote
from cluefin_openapi.kis._exceptions import KISValidationError

from ._case_runner import CASE_FIELDS, load_cases, run_case

DOMESTIC_BASIC_QUOTE_CASES = load_cases("domestic_basic_quote_cases.json", relative_to=__file__)


@pytest.mark.parametrize(CASE_FIELDS, DOMESTIC_BASIC_QUOTE_CASES)
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
    run_case(
        module=domestic_basic_quote_module,
        wrapper_cls=DomesticBasicQuote,
        monkeypatch=monkeypatch,
        method_name=method_name,
        response_model_attr=response_model_attr,
        endpoint=endpoint,
        method=method,
        call_kwargs=call_kwargs,
        expected_headers=expected_headers,
        expected_body=expected_body,
        response_payload=response_payload,
    )


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
