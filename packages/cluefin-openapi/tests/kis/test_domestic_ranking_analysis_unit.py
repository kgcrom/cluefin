"""Unit tests for KIS Domestic Ranking Analysis API."""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from cluefin_openapi.kis._domestic_ranking_analysis import DomesticRankingAnalysis
from cluefin_openapi.kis._domestic_ranking_analysis_types import (
    HtsInquiryTop20,
    StockAfterHoursFluctuationRank,
    StockAfterHoursVolumeRank,
    StockCreditBalanceTop,
    StockDisparityIndexRank,
    StockDividendYieldTop,
    StockExecutionStrengthTop,
    StockExpectedExecutionRiseDeclineTop,
    StockFinanceRatioRank,
    StockFluctuationRank,
    StockHogaQuantityRank,
    StockLargeExecutionCountTop,
    StockMarketCapTop,
    StockMarketPriceRank,
    StockNewHighLowApproachingTop,
    StockPreferredStockRatioTop,
    StockProfitabilityIndicatorRank,
    StockProprietaryTradingTop,
    StockShortSellingTop,
    StockTimeHogaRank,
    StockWatchlistRegistrationTop,
    TradingVolumeRank,
)
from cluefin_openapi.kis._model import KisHttpResponse


def load_test_cases():
    """Load test cases from JSON file."""
    test_file = Path(__file__).parent / "domestic_ranking_analysis_cases.json"
    with open(test_file, "r", encoding="utf-8") as f:
        return json.load(f)


TEST_CASES = load_test_cases()


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[case["method_name"] for case in TEST_CASES])
def test_domestic_ranking_analysis_methods(test_case):
    """Test all domestic ranking analysis methods with parameterized test cases."""
    # Setup mock client
    mock_client = Mock()
    mock_response = Mock()
    mock_response.json.return_value = test_case["response_payload"]
    mock_response.status_code = 200
    mock_response.headers = {
        "content-type": "application/json; charset=utf-8",
        "tr_id": test_case["expected_headers"].get("tr_id", ""),
        "tr_cont": "",
        "gt_uid": None,
    }

    # Configure mock based on HTTP method
    if test_case["method"] == "GET":
        mock_client._get.return_value = mock_response
    else:
        mock_client._post.return_value = mock_response

    # Create ranking analysis instance
    ranking_analysis = DomesticRankingAnalysis(mock_client)

    # Get the method to test
    method = getattr(ranking_analysis, test_case["method_name"])

    # Call the method with test kwargs
    result = method(**test_case["call_kwargs"])

    # Verify the correct client method was called
    if test_case["method"] == "GET":
        mock_client._get.assert_called_once()
        call_args = mock_client._get.call_args

        # Verify endpoint
        assert call_args[0][0] == test_case["endpoint"]

        # Verify headers
        assert call_args[1]["headers"] == test_case["expected_headers"]

        # Verify params (use expected_body as-is, since some methods use lowercase, some uppercase)
        actual_params = call_args[1]["params"]
        expected_params = test_case["expected_body"]
        assert actual_params == expected_params
    else:
        mock_client._post.assert_called_once()
        call_args = mock_client._post.call_args

        # Verify endpoint
        assert call_args[0][0] == test_case["endpoint"]

        # Verify headers
        assert call_args[1]["headers"] == test_case["expected_headers"]

        # Verify body
        assert call_args[1]["json"] == test_case["expected_body"]

    # Verify result type
    response_model_name = test_case["response_model_attr"]
    response_model_class = globals()[response_model_name]
    assert isinstance(result, KisHttpResponse)
    assert isinstance(result.body, response_model_class)


def test_get_trading_volume_rank_detailed():
    """Detailed test for get_trading_volume_rank method."""
    # Setup
    mock_client = Mock()
    mock_response = Mock()
    mock_response.json.return_value = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": [
            {
                "hts_kor_isnm": "삼성전자",
                "mksc_shrn_iscd": "005930",
                "data_rank": "1",
                "stck_prpr": "70000",
                "prdy_vrss_sign": "2",
                "prdy_vrss": "1000",
                "prdy_ctrt": "1.43",
                "acml_vol": "10000000",
                "prdy_vol": "9500000",
                "lstn_stcn": "5969782550",
                "avrg_vol": "9000000",
                "n_befr_clpr_vrss_prpr_rate": "1.5",
                "vol_inrt": "5.26",
                "vol_tnrt": "0.17",
                "nday_vol_tnrt": "0.85",
                "avrg_tr_pbmn": "630000000000",
                "tr_pbmn_tnrt": "0.11",
                "nday_tr_pbmn_tnrt": "0.55",
                "acml_tr_pbmn": "700000000000",
            }
        ],
    }
    mock_response.status_code = 200
    mock_response.headers = {
        "content-type": "application/json; charset=utf-8",
        "tr_id": "FHPST01710000",
        "tr_cont": "",
        "gt_uid": None,
    }
    mock_client._get.return_value = mock_response

    # Execute
    ranking_analysis = DomesticRankingAnalysis(mock_client)
    result = ranking_analysis.get_trading_volume_rank(
        fid_cond_mrkt_div_code="J",
        fid_cond_scr_div_code="20171",
        fid_input_iscd="0000",
        fid_div_cls_code="0",
        fid_blng_cls_code="0",
        fid_trgt_cls_code="111111111",
        fid_trgt_exls_cls_code="0000000000",
        fid_input_price_1="",
        fid_input_price_2="",
        fid_vol_cnt="",
        fid_input_date_1="",
    )

    # Verify
    assert isinstance(result, KisHttpResponse)
    assert isinstance(result.body, TradingVolumeRank)
    mock_client._get.assert_called_once_with(
        "/uapi/domestic-stock/v1/quotations/volume-rank",
        headers={"tr_id": "FHPST01710000"},
        params={
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_COND_SCR_DIV_CODE": "20171",
            "FID_INPUT_ISCD": "0000",
            "FID_DIV_CLS_CODE": "0",
            "FID_BLNG_CLS_CODE": "0",
            "FID_TRGT_CLS_CODE": "111111111",
            "FID_TRGT_EXLS_CLS_CODE": "0000000000",
            "FID_INPUT_PRICE_1": "",
            "FID_INPUT_PRICE_2": "",
            "FID_VOL_CNT": "",
            "FID_INPUT_DATE_1": "",
        },
    )


def test_get_stock_fluctuation_rank_detailed():
    """Detailed test for get_stock_fluctuation_rank method."""
    # Setup
    mock_client = Mock()
    mock_response = Mock()
    mock_response.json.return_value = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": [
            {
                "stck_shrn_iscd": "000660",
                "data_rank": "1",
                "hts_kor_isnm": "SK하이닉스",
                "stck_prpr": "120000",
                "prdy_vrss": "5000",
                "prdy_vrss_sign": "2",
                "prdy_ctrt": "4.35",
                "acml_vol": "5000000",
                "stck_hgpr": "121000",
                "hgpr_hour": "140000",
                "acml_hgpr_date": "20250115",
                "stck_lwpr": "119000",
                "lwpr_hour": "093000",
                "acml_lwpr_date": "20250115",
                "lwpr_vrss_prpr_rate": "0.84",
                "dsgt_date_clpr_vrss_prpr_rate": "4.35",
                "cnnt_ascn_dynu": "3",
                "hgpr_vrss_prpr_rate": "-0.83",
                "cnnt_down_dynu": "0",
                "oprc_vrss_prpr_sign": "2",
                "oprc_vrss_prpr": "1000",
                "oprc_vrss_prpr_rate": "0.84",
                "prd_rsfl": "5000",
                "prd_rsfl_rate": "4.35",
            }
        ],
    }
    mock_response.status_code = 200
    mock_response.headers = {
        "content-type": "application/json; charset=utf-8",
        "tr_id": "FHPST01700000",
        "tr_cont": "",
        "gt_uid": None,
    }
    mock_client._get.return_value = mock_response

    # Execute
    ranking_analysis = DomesticRankingAnalysis(mock_client)
    result = ranking_analysis.get_stock_fluctuation_rank(
        fid_rsfl_rate2="",
        fid_cond_mrkt_div_code="J",
        fid_cond_scr_div_code="20170",
        fid_input_iscd="0001",
        fid_rank_sort_cls_code="0",
        fid_input_cnt_1="0",
        fid_prc_cls_code="0",
        fid_input_price_1="",
        fid_input_price_2="",
        fid_vol_cnt="",
        fid_trgt_cls_code="0",
        fid_trgt_exls_cls_code="0",
        fid_div_cls_code="0",
        fid_rsfl_rate1="",
    )

    # Verify
    assert isinstance(result, KisHttpResponse)
    assert isinstance(result.body, StockFluctuationRank)
    mock_client._get.assert_called_once_with(
        "/uapi/domestic-stock/v1/ranking/fluctuation",
        headers={"tr_id": "FHPST01700000"},
        params={
            "fid_rsfl_rate2": "",
            "fid_cond_mrkt_div_code": "J",
            "fid_cond_scr_div_code": "20170",
            "fid_input_iscd": "0001",
            "fid_rank_sort_cls_code": "0",
            "fid_input_cnt_1": "0",
            "fid_prc_cls_code": "0",
            "fid_input_price_1": "",
            "fid_input_price_2": "",
            "fid_vol_cnt": "",
            "fid_trgt_cls_code": "0",
            "fid_trgt_exls_cls_code": "0",
            "fid_div_cls_code": "0",
            "fid_rsfl_rate1": "",
        },
    )


def test_get_hts_inquiry_top_20_detailed():
    """Detailed test for get_hts_inquiry_top_20 method (no parameters)."""
    # Setup
    mock_client = Mock()
    mock_response = Mock()
    mock_response.json.return_value = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": [
            {
                "mrkt_div_cls_code": "J",
                "mksc_shrn_iscd": "005930",
            }
        ],
    }
    mock_response.status_code = 200
    mock_response.headers = {
        "content-type": "application/json; charset=utf-8",
        "tr_id": "HHMCM000100C0",
        "tr_cont": "",
        "gt_uid": None,
    }
    mock_client._get.return_value = mock_response

    # Execute
    ranking_analysis = DomesticRankingAnalysis(mock_client)
    result = ranking_analysis.get_hts_inquiry_top_20()

    # Verify
    assert isinstance(result, KisHttpResponse)
    assert isinstance(result.body, HtsInquiryTop20)
    mock_client._get.assert_called_once_with(
        "/uapi/domestic-stock/v1/ranking/hts-top-view", headers={"tr_id": "HHMCM000100C0"}, params={}
    )


def test_get_stock_market_cap_top_detailed():
    """Detailed test for get_stock_market_cap_top method."""
    # Setup
    mock_client = Mock()
    mock_response = Mock()
    mock_response.json.return_value = {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": [
            {
                "mksc_shrn_iscd": "005930",
                "data_rank": "1",
                "hts_kor_isnm": "삼성전자",
                "stck_prpr": "70000",
                "prdy_vrss": "1000",
                "prdy_vrss_sign": "2",
                "prdy_ctrt": "1.43",
                "acml_vol": "10000000",
                "lstn_stcn": "5969782550",
                "stck_avls": "417884778500000",
                "mrkt_whol_avls_rlim": "15.5",
            }
        ],
    }
    mock_response.status_code = 200
    mock_response.headers = {
        "content-type": "application/json; charset=utf-8",
        "tr_id": "FHPST01740000",
        "tr_cont": "",
        "gt_uid": None,
    }
    mock_client._get.return_value = mock_response

    # Execute
    ranking_analysis = DomesticRankingAnalysis(mock_client)
    result = ranking_analysis.get_stock_market_cap_top(
        fid_input_price_2="",
        fid_cond_mrkt_div_code="J",
        fid_cond_scr_div_code="20174",
        fid_div_cls_code="0",
        fid_input_iscd="0001",
        fid_trgt_cls_code="0",
        fid_trgt_exls_cls_code="0",
        fid_input_price_1="",
        fid_vol_cnt="",
    )

    # Verify
    assert isinstance(result, KisHttpResponse)
    assert isinstance(result.body, StockMarketCapTop)
    mock_client._get.assert_called_once()


def test_domestic_ranking_analysis_init():
    """Test DomesticRankingAnalysis initialization."""
    mock_client = Mock()
    ranking_analysis = DomesticRankingAnalysis(mock_client)
    assert ranking_analysis.client == mock_client
