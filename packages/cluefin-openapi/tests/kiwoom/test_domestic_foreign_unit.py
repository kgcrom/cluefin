import pytest

from cluefin_openapi.kiwoom import _domestic_foreign as domestic_foreign_module
from cluefin_openapi.kiwoom._domestic_foreign import DomesticForeign

from ._helpers import EndpointCase, run_post_case

FOREIGN_CASES = [
    EndpointCase(
        name="investor_trading_trend",
        method_name="get_foreign_investor_trading_trend_by_stock",
        response_model_attr="DomesticForeignInvestorTradingTrendByStock",
        api_id="ka10008",
        call_kwargs={"stk_cd": "005930"},
        expected_body={"stk_cd": "005930"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "stk_frgnr": [{"dt": "20240105", "close_pric": "135300"}],
        },
    ),
    EndpointCase(
        name="stock_institution",
        method_name="get_stock_institution",
        response_model_attr="DomesticForeignStockInstitution",
        api_id="ka10009",
        call_kwargs={"stk_cd": "005930"},
        expected_body={"stk_cd": "005930"},
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "date": "20240105",
            "close_pric": "135300",
        },
    ),
    EndpointCase(
        name="consecutive_net_buy_sell_status",
        method_name="get_consecutive_net_buy_sell_status_by_institution_foreigner",
        response_model_attr="DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner",
        api_id="ka10131",
        call_kwargs={
            "dt": "1",
            "mrkt_tp": "001",
            "stk_inds_tp": "0",
            "amt_qty_tp": "0",
            "stex_tp": "1",
            "netslmt_tp": "2",
            "strt_dt": "20240101",
            "end_dt": "20240105",
        },
        expected_body={
            "dt": "1",
            "strt_dt": "20240101",
            "end_dt": "20240105",
            "mrkt_tp": "001",
            "stk_inds_tp": "0",
            "amt_qty_tp": "0",
            "stex_tp": "1",
            "netslmt_tp": "2",
        },
        response_payload={
            "return_code": 0,
            "return_msg": "OK",
            "orgn_frgnr_cont_trde_prst": [{"rank": "1", "stk_cd": "005930"}],
        },
        cont_flag_key=None,
        next_key=None,
    ),
]


@pytest.mark.parametrize("case", FOREIGN_CASES, ids=lambda case: case.name)
def test_domestic_foreign_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        domestic_foreign_module,
        DomesticForeign,
        case,
        base_headers={
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
        },
    )
