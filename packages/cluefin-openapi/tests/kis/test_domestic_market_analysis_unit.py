import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from cluefin_openapi.kis import _domestic_market_analysis as domestic_market_analysis_module
from cluefin_openapi.kis._domestic_market_analysis import DomesticMarketAnalysis
from cluefin_openapi.kis._domestic_market_analysis_types import ForeignNetBuyTrendByStock


def load_domestic_market_analysis_cases():
    path = Path(__file__).with_name("domestic_market_analysis_cases.json")
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


DOMESTIC_MARKET_ANALYSIS_CASES = load_domestic_market_analysis_cases()


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
    DOMESTIC_MARKET_ANALYSIS_CASES,
)
def test_domestic_market_analysis_builds_request(
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

    monkeypatch.setattr(domestic_market_analysis_module, response_model_attr, DummyResponseModel)

    market_analysis = DomesticMarketAnalysis(client)
    result = getattr(market_analysis, method_name)(**call_kwargs)

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


def _make_mock_response(tr_id: str = "FHKST11300006") -> Mock:
    mock_response = Mock()
    mock_response.json.return_value = {"rt_cd": "0", "msg_cd": "0000", "msg1": "OK", "output": []}
    mock_response.status_code = 200
    mock_response.text = ""
    mock_response.headers = {
        "content-type": "application/json; charset=utf-8",
        "tr_id": tr_id,
        "tr_cont": "",
        "gt_uid": None,
    }
    return mock_response


def _install_dummy_watchlist_model(monkeypatch):
    class DummyResponseModel:
        @classmethod
        def model_validate(cls, data):
            return cls()

    monkeypatch.setattr(domestic_market_analysis_module, "WatchlistMultiQuote", DummyResponseModel)


def test_get_watchlist_multi_quote_includes_populated_optional_pairs(monkeypatch):
    _install_dummy_watchlist_model(monkeypatch)

    client = Mock()
    client._get.return_value = _make_mock_response()

    market_analysis = DomesticMarketAnalysis(client)
    market_analysis.get_watchlist_multi_quote(
        fid_cond_mrkt_div_code_1="J",
        fid_input_iscd_1="005930",
        fid_cond_mrkt_div_code_2="J",
        fid_input_iscd_2="000660",
    )

    client._get.assert_called_once_with(
        "/uapi/domestic-stock/v1/quotations/intstock-multprice",
        headers={"tr_id": "FHKST11300006"},
        params={
            "FID_COND_MRKT_DIV_CODE_1": "J",
            "FID_INPUT_ISCD_1": "005930",
            "FID_COND_MRKT_DIV_CODE_2": "J",
            "FID_INPUT_ISCD_2": "000660",
        },
    )


def test_get_watchlist_multi_quote_rejects_incomplete_optional_pair(monkeypatch):
    _install_dummy_watchlist_model(monkeypatch)

    client = Mock()
    market_analysis = DomesticMarketAnalysis(client)

    with pytest.raises(ValueError, match="must be provided together"):
        market_analysis.get_watchlist_multi_quote(
            fid_cond_mrkt_div_code_1="J",
            fid_input_iscd_1="005930",
            fid_cond_mrkt_div_code_2="J",
        )

    client._get.assert_not_called()


def test_foreign_net_buy_trend_by_stock_matches_live_output_schema():
    payload = {
        "rt_cd": "0",
        "msg_cd": "0000",
        "msg1": "OK",
        "output": [
            {
                "bsop_hour": "153049",
                "stck_prpr": "179700",
                "prdy_vrss": "-400",
                "prdy_vrss_sign": "5",
                "prdy_ctrt": "-0.22",
                "acml_vol": "29102559",
                "frgn_seln_vol": "9155337",
                "frgn_shnu_vol": "511586",
                "glob_ntby_qty": "-8643751",
                "frgn_ntby_qty_icdc": "-596817",
            }
        ],
    }

    body = ForeignNetBuyTrendByStock.model_validate(payload)

    assert len(body.output) == 1
    assert body.output[0].bsop_hour == "153049"
    assert body.output[0].acml_vol == "29102559"
    assert body.output[0].glob_ntby_qty == "-8643751"
