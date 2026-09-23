import pytest

from cluefin_openapi.kis import _onmarket_bond_basic_quote as onmarket_bond_basic_quote_module
from cluefin_openapi.kis._onmarket_bond_basic_quote import OnmarketBondBasicQuote
from cluefin_openapi.kis._onmarket_bond_basic_quote_types import OnmarketBondPrice, OnmarketBondPriceItem

from ._case_runner import CASE_FIELDS, load_cases, run_case

ONMARKET_BOND_BASIC_QUOTE_CASES = load_cases("onmarket_bond_basic_quote_cases.json", relative_to=__file__)


@pytest.mark.parametrize(CASE_FIELDS, ONMARKET_BOND_BASIC_QUOTE_CASES)
def test_onmarket_bond_basic_quote_builds_request(
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
        module=onmarket_bond_basic_quote_module,
        wrapper_cls=OnmarketBondBasicQuote,
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


def test_bond_price_parses_real_response_model() -> None:
    """run_case 는 DummyResponseModel 로 검증해 실제 응답 모델은 한 번도 파싱되지 않는다."""
    item = {field_name: "" for field_name in OnmarketBondPriceItem.model_fields}
    item["stnd_iscd"] = "KR2033022D33"
    item["hts_kor_isnm"] = "국고채03125-3306(19-3)"
    item["bond_prpr"] = "10250.5"

    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": item,
    }

    body = OnmarketBondPrice.model_validate(payload)

    assert body.output.stnd_iscd == "KR2033022D33"
    assert body.output.hts_kor_isnm == "국고채03125-3306(19-3)"
    assert body.output.bond_prpr == "10250.5"
