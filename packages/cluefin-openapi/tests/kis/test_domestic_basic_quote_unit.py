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


def test_get_stock_period_quote_parses_delisted_stock_with_missing_output1_keys() -> None:
    """상장폐지 종목: output1 은 0 채움에 sign/종목명/단축코드 키가 없고 output2 캔들은 온다 (VENDOR_DOC_ERRATA.md)."""
    zero_fields = (
        "prdy_vrss prdy_ctrt stck_prdy_clpr acml_vol acml_tr_pbmn stck_prpr prdy_vol stck_mxpr stck_llam "
        "stck_oprc stck_hgpr stck_lwpr stck_prdy_oprc stck_prdy_hgpr stck_prdy_lwpr askp bidp prdy_vrss_vol "
        "vol_tnrt stck_fcam lstn_stcn cpfn hts_avls per eps pbr"
    ).split()
    output1 = {name: "0" for name in zero_fields}
    output1["itewhol_loan_rmnd_ratem name"] = "0"
    candle = {
        "stck_bsop_date": "20160831",
        "stck_clpr": "1000",
        "stck_oprc": "990",
        "stck_hgpr": "1010",
        "stck_lwpr": "980",
        "acml_vol": "12345",
        "acml_tr_pbmn": "12345000",
        "flng_cls_code": "00",
        "prtt_rate": "0.00",
        "mod_yn": "N",
        "prdy_vrss_sign": "2",
        "prdy_vrss": "10",
        "revl_issu_reas": "00",
    }
    payload = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": output1,
        "output2": [candle, {**candle, "stck_bsop_date": "20160830"}],
    }

    response = DomesticBasicQuote(_mock_client(payload)).get_stock_period_quote(
        fid_cond_mrkt_div_code="J",
        fid_input_iscd="117930",
        fid_input_date_1="20160801",
        fid_input_date_2="20160831",
        fid_period_div_code="D",
        fid_org_adj_prc="0",
    )

    assert response.body.output1 is not None
    assert response.body.output1.prdy_vrss_sign is None
    assert response.body.output1.hts_kor_isnm is None
    assert response.body.output1.stck_shrn_iscd is None
    assert response.body.output1.stck_prpr == "0"
    assert [c.stck_bsop_date for c in response.body.output2] == ["20160831", "20160830"]


def test_get_stock_period_quote_still_rejects_other_missing_output1_keys() -> None:
    """완화는 세 필드뿐이다 — 다른 output1 키가 빠지면 여전히 검증 실패."""
    payload = {"rt_cd": "0", "msg_cd": "MCA00000", "msg1": "정상처리", "output1": {"prdy_vrss": "0"}, "output2": []}

    with pytest.raises(KISValidationError):
        DomesticBasicQuote(_mock_client(payload)).get_stock_period_quote(
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="117930",
            fid_input_date_1="20160801",
            fid_input_date_2="20160831",
            fid_period_div_code="D",
            fid_org_adj_prc="0",
        )
