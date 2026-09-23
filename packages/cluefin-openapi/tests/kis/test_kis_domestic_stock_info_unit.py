import pytest

from cluefin_openapi.kis import _domestic_stock_info as domestic_stock_info_module
from cluefin_openapi.kis._domestic_stock_info import DomesticStockInfo
from cluefin_openapi.kis._domestic_stock_info_types import StockBasicInfoItem

from ._case_runner import CASE_FIELDS, load_cases, run_case

DOMESTIC_STOCK_INFO_CASES = load_cases("domestic_stock_info_cases.json", relative_to=__file__)


@pytest.mark.parametrize(CASE_FIELDS, DOMESTIC_STOCK_INFO_CASES)
def test_domestic_stock_info_builds_request(
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
        module=domestic_stock_info_module,
        wrapper_cls=DomesticStockInfo,
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


def test_stock_basic_info_accepts_five_digit_ocr_no():
    stock_basic_info = {field_name: "" for field_name in StockBasicInfoItem.model_fields}
    stock_basic_info["ocr_no"] = "01147"

    result = StockBasicInfoItem.model_validate(stock_basic_info)

    assert result.ocr_no == "01147"
