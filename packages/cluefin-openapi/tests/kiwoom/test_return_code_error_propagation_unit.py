"""도메인별 대표 메서드 1개씩 HTTP 200 + 실패 return_code 조합을 검증한다.

Kiwoom은 HTTP 200으로 응답하면서 본문 return_code 로 실패를 알린다
(``_client.Client._post``가 상태 코드보다 body 코드를 우선 해석한다). 그 처리 자체는
``test_error_codes_unit.py``가 ``client._post`` 레벨에서 이미 촘촘히 검증하므로, 여기서는
각 도메인 모듈(계좌/차트/ETF/외국인/시황/주문/순위정보/업종/종목정보/테마, 해외 포함)의
대표 메서드 하나가 실제 ``Client``를 통해 호출됐을 때도 동일하게 에러가 전파되는지만
확인한다.
"""

from typing import Any, Dict

import pytest
import requests_mock

from cluefin_openapi.kiwoom._client import Client
from cluefin_openapi.kiwoom._domestic_account import DomesticAccount
from cluefin_openapi.kiwoom._domestic_chart import DomesticChart
from cluefin_openapi.kiwoom._domestic_etf import DomesticETF
from cluefin_openapi.kiwoom._domestic_foreign import DomesticForeign
from cluefin_openapi.kiwoom._domestic_market_condition import DomesticMarketCondition
from cluefin_openapi.kiwoom._domestic_order import DomesticOrder
from cluefin_openapi.kiwoom._domestic_rank_info import DomesticRankInfo
from cluefin_openapi.kiwoom._domestic_sector import DomesticSector
from cluefin_openapi.kiwoom._domestic_stock_info import DomesticStockInfo
from cluefin_openapi.kiwoom._domestic_theme import DomesticTheme
from cluefin_openapi.kiwoom._exceptions import KiwoomValidationError
from cluefin_openapi.kiwoom._overseas_account import OverseasAccount
from cluefin_openapi.kiwoom._overseas_chart import OverseasChart
from cluefin_openapi.kiwoom._overseas_exchange import OverseasExchange
from cluefin_openapi.kiwoom._overseas_investment_info import OverseasInvestmentInfo
from cluefin_openapi.kiwoom._overseas_market_condition import OverseasMarketCondition
from cluefin_openapi.kiwoom._overseas_order import OverseasOrder
from cluefin_openapi.kiwoom._overseas_rank_info import OverseasRankInfo
from cluefin_openapi.kiwoom._overseas_sector import OverseasSector
from cluefin_openapi.kiwoom._overseas_stock_info import OverseasStockInfo
from cluefin_openapi.kiwoom._overseas_watchlist import OverseasWatchlist

# 검증에 쓰는 실패 return_code. 1902는 _VALIDATION_CODES 소속이라 KiwoomValidationError로
# 해석된다 (test_error_codes_unit.py 참고).
FAILING_RETURN_CODE = 1902
FAILING_RESPONSE = {"return_code": FAILING_RETURN_CODE, "return_msg": "종목 정보가 없습니다."}

# (도메인 이름, API 클래스, 경로, 대표 메서드, 호출 kwargs)
DOMAIN_CASES: list[tuple[str, type, str, str, Dict[str, Any]]] = [
    ("account", DomesticAccount, "/api/dostk/acnt", "get_deposit_balance_details", {"qry_tp": "3"}),
    (
        "chart",
        DomesticChart,
        "/api/dostk/chart",
        "get_individual_stock_institutional_chart",
        {"dt": "20240101", "stk_cd": "005930", "amt_qty_tp": "1", "trde_tp": "0", "unit_tp": "1000"},
    ),
    (
        "etf",
        DomesticETF,
        "/api/dostk/etf",
        "get_etf_return_rate",
        {"stk_cd": "069500", "etfobjt_idex_cd": "001", "dt": 0},
    ),
    (
        "foreign",
        DomesticForeign,
        "/api/dostk/frgnistt",
        "get_foreign_investor_trading_trend_by_stock",
        {"stk_cd": "005930"},
    ),
    ("market_conditions", DomesticMarketCondition, "/api/dostk/mrkcond", "get_stock_quote", {"stk_cd": "005930"}),
    (
        "order",
        DomesticOrder,
        "/api/dostk/ordr",
        "request_buy_order",
        {
            "dmst_stex_tp": "KRX",
            "stk_cd": "005930",
            "ord_qty": "10",
            "trde_tp": "0",
            "ord_uv": "70000",
            "cond_uv": "69000",
        },
    ),
    (
        "rank_info",
        DomesticRankInfo,
        "/api/dostk/rkinfo",
        "get_top_remaining_order_quantity",
        {
            "mrkt_tp": "001",
            "sort_tp": "1",
            "trde_qty_tp": "0000",
            "stk_cnd": "0",
            "crd_cnd": "0",
            "stex_tp": "1",
        },
    ),
    ("sector", DomesticSector, "/api/dostk/sect", "get_industry_program", {"stk_cd": "005930"}),
    ("stock_info", DomesticStockInfo, "/api/dostk/stkinfo", "get_stock_info", {"stk_cd": "005930"}),
    (
        "theme",
        DomesticTheme,
        "/api/dostk/thme",
        "get_theme_group",
        {"qry_tp": "1", "date_tp": "1", "thema_nm": "test", "flu_pl_amt_tp": "1", "stex_tp": "1"},
    ),
    (
        "overseas_account",
        OverseasAccount,
        "/api/us/acnt",
        "get_daily_account_profit_rate",
        {"from_dt": "20240102", "to": "20240131"},
    ),
    (
        "overseas_chart",
        OverseasChart,
        "/api/us/chart",
        "get_tick_chart",
        {"stex_tp": "ND", "stk_cd": "AAPL", "tic_scope": "1", "upd_stkpc_tp": "0", "exrt_appl_tp": "0"},
    ),
    ("overseas_exchange", OverseasExchange, "/api/us/exchange", "get_exchange_rate", {"exch_tp": "1"}),
    ("overseas_investment_info", OverseasInvestmentInfo, "/api/us/invtinfo", "get_research", {"qry_tp": "0"}),
    (
        "overseas_market_condition",
        OverseasMarketCondition,
        "/api/us/mrkcond",
        "get_current_price_stock_info",
        {"stex_tp": "ND", "stk_cd": "AAPL"},
    ),
    (
        "overseas_order",
        OverseasOrder,
        "/api/us/ordr",
        "request_buy_order",
        {"stex_tp": "ND", "stk_cd": "AAPL", "ord_qty": "1", "trde_tp": "00", "ord_uv": "1.00"},
    ),
    (
        "overseas_rank_info",
        OverseasRankInfo,
        "/api/us/rkinfo",
        "get_realtime_symbol_query_rank",
        {"svc_type": "B286"},
    ),
    (
        "overseas_sector",
        OverseasSector,
        "/api/us/sect",
        "get_industry_period_profit_rate",
        {"stex_tp": "3", "inds_cd": "000"},
    ),
    ("overseas_stock_info", OverseasStockInfo, "/api/us/stkinfo", "get_exchange_list", {"stk_cd": "AAPL"}),
    ("overseas_watchlist", OverseasWatchlist, "/api/us/watchlist", "get_watchlist_group_list", {}),
]


@pytest.mark.parametrize(
    "domain_name,api_cls,path,method_name,call_kwargs", DOMAIN_CASES, ids=[c[0] for c in DOMAIN_CASES]
)
def test_domain_method_raises_on_failing_return_code_with_http_200(
    domain_name, api_cls, path, method_name, call_kwargs
):
    client = Client(token="test_token", env="dev")
    api = api_cls(client)

    with requests_mock.Mocker() as m:
        m.post(f"https://mockapi.kiwoom.com{path}", json=FAILING_RESPONSE, status_code=200)

        with pytest.raises(KiwoomValidationError) as exc_info:
            getattr(api, method_name)(**call_kwargs)

    assert exc_info.value.return_code == FAILING_RETURN_CODE
    assert exc_info.value.status_code == 200
