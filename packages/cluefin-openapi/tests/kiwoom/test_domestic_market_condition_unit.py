import pytest

from cluefin_openapi.kiwoom import _domestic_market_condition as market_condition_module
from cluefin_openapi.kiwoom._domestic_market_condition import DomesticMarketCondition

from ._helpers import EndpointCase, run_post_case


def payload(name: str):
    return {"return_code": 0, "return_msg": "OK", "endpoint": name}


BASE_HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json",
}


MARKET_CASES = [
    EndpointCase(
        name=case_name,
        method_name=method_name,
        response_model_attr=response_model,
        api_id=api_id,
        call_kwargs={"stk_cd": "005930"},
        expected_body={"stk_cd": "005930"},
        response_payload=payload(case_name),
    )
    for case_name, method_name, response_model, api_id in [
        ("stock_quote", "get_stock_quote", "DomesticMarketConditionStockQuote", "ka10004"),
        ("stock_quote_by_date", "get_stock_quote_by_date", "DomesticMarketConditionStockQuoteByDate", "ka10005"),
        ("stock_price", "get_stock_price", "DomesticMarketConditionStockPrice", "ka10006"),
        ("market_sentiment_info", "get_market_sentiment_info", "DomesticMarketConditionMarketSentimentInfo", "ka10007"),
        (
            "execution_intensity_time",
            "get_execution_intensity_trend_by_time",
            "DomesticMarketConditionExecutionIntensityTrendByTime",
            "ka10046",
        ),
        (
            "execution_intensity_date",
            "get_execution_intensity_trend_by_date",
            "DomesticMarketConditionExecutionIntensityTrendByDate",
            "ka10047",
        ),
        (
            "after_hours_single_price",
            "get_after_hours_single_price",
            "DomesticMarketConditionAfterHoursSinglePrice",
            "ka10087",
        ),
    ]
]

MARKET_CASES.extend(
    [
        EndpointCase(
            name="new_stock_warrant_price",
            method_name="get_new_stock_warrant_price",
            response_model_attr="DomesticMarketConditionNewStockWarrantPrice",
            api_id="ka10011",
            call_kwargs={"newstk_recvrht_tp": "00"},
            expected_body={"newstk_recvrht_tp": "00"},
            response_payload=payload("new_stock_warrant_price"),
        ),
        EndpointCase(
            name="daily_institutional_trading_items",
            method_name="get_daily_institutional_trading_items",
            response_model_attr="DomesticMarketConditionDailyInstitutionalTrading",
            api_id="ka10044",
            call_kwargs={
                "strt_dt": "20240101",
                "end_dt": "20240105",
                "trde_tp": "1",
                "mrkt_tp": "001",
                "stex_tp": "1",
            },
            expected_body={
                "strt_dt": "20240101",
                "end_dt": "20240105",
                "trde_tp": "1",
                "mrkt_tp": "001",
                "stex_tp": "1",
            },
            response_payload=payload("daily_institutional_trading_items"),
        ),
        EndpointCase(
            name="institutional_trading_trend_by_stock",
            method_name="get_institutional_trading_trend_by_stock",
            response_model_attr="DomesticMarketConditionInstitutionalTradingTrendByStock",
            api_id="ka10045",
            call_kwargs={
                "stk_cd": "005930",
                "strt_dt": "20240101",
                "end_dt": "20240105",
                "orgn_prsm_unp_tp": "1",
                "for_prsm_unp_tp": "1",
            },
            expected_body={
                "stk_cd": "005930",
                "strt_dt": "20240101",
                "end_dt": "20240105",
                "orgn_prsm_unp_tp": "1",
                "for_prsm_unp_tp": "1",
            },
            response_payload=payload("institutional_trading_trend_by_stock"),
        ),
        EndpointCase(
            name="intraday_trading_by_investor",
            method_name="get_intraday_trading_by_investor",
            response_model_attr="DomesticMarketConditionIntradayTradingByInvestor",
            api_id="ka10063",
            call_kwargs={
                "mrkt_tp": "000",
                "amt_qty_tp": "1",
                "invsr": "6",
                "frgn_all": "1",
                "smtm_netprps_tp": "0",
                "stex_tp": "1",
            },
            expected_body={
                "mrkt_tp": "000",
                "amt_qty_tp": "1",
                "invsr": "6",
                "frgn_all": "1",
                "smtm_netprps_tp": "0",
                "stex_tp": "1",
            },
            response_payload=payload("intraday_trading_by_investor"),
        ),
        EndpointCase(
            name="after_market_trading_by_investor",
            method_name="get_after_market_trading_by_investor",
            response_model_attr="DomesticMarketConditionAfterMarketTradingByInvestor",
            api_id="ka10066",
            call_kwargs={
                "mrkt_tp": "000",
                "amt_qty_tp": "1",
                "trde_tp": "0",
                "stex_tp": "1",
            },
            expected_body={
                "mrkt_tp": "000",
                "amt_qty_tp": "1",
                "trde_tp": "0",
                "stex_tp": "1",
            },
            response_payload=payload("after_market_trading_by_investor"),
        ),
        EndpointCase(
            name="securities_firm_trading_trend_by_stock",
            method_name="get_securities_firm_trading_trend_by_stock",
            response_model_attr="DomesticMarketConditionSecuritiesFirmTradingTrendByStock",
            api_id="ka10078",
            call_kwargs={
                "mmcm_cd": "001",
                "stk_cd": "005930",
                "strt_dt": "20240101",
                "end_dt": "20240105",
            },
            expected_body={
                "mmcm_cd": "001",
                "stk_cd": "005930",
                "strt_dt": "20240101",
                "end_dt": "20240105",
            },
            response_payload=payload("securities_firm_trading_trend_by_stock"),
        ),
        EndpointCase(
            name="daily_stock_price",
            method_name="get_daily_stock_price",
            response_model_attr="DomesticMarketConditionDailyStockPrice",
            api_id="ka10086",
            call_kwargs={"stk_cd": "005930", "qry_dt": "20240105", "indc_tp": "0"},
            expected_body={"stk_cd": "005930", "qry_dt": "20240105", "indc_tp": "0"},
            response_payload=payload("daily_stock_price"),
        ),
        EndpointCase(
            name="program_trading_trend_by_time",
            method_name="get_program_trading_trend_by_time",
            response_model_attr="DomesticMarketConditionProgramTradingTrendByTime",
            api_id="ka90005",
            call_kwargs={
                "date": "20240105",
                "amt_qty_tp": "1",
                "mrkt_tp": "P00101",
                "min_tic_tp": "0",
                "stex_tp": "1",
            },
            expected_body={
                "date": "20240105",
                "amt_qty_tp": "1",
                "mrkt_tp": "P00101",
                "min_tic_tp": "0",
                "stex_tp": "1",
            },
            response_payload=payload("program_trading_trend_by_time"),
        ),
        EndpointCase(
            name="program_trading_arbitrage_balance_trend",
            method_name="get_program_trading_arbitrage_balance_trend",
            response_model_attr="DomesticMarketConditionProgramTradingArbitrageBalanceTrend",
            api_id="ka90006",
            call_kwargs={"date": "20240105", "stex_tp": "1"},
            expected_body={"date": "20240105", "stex_tp": "1"},
            response_payload=payload("program_trading_arbitrage_balance_trend"),
        ),
        EndpointCase(
            name="program_trading_cumulative_trend",
            method_name="get_program_trading_cumulative_trend",
            response_model_attr="DomesticMarketConditionProgramTradingCumulativeTrend",
            api_id="ka90007",
            call_kwargs={
                "date": "20240105",
                "amt_qty_tp": "1",
                "mrkt_tp": "0",
                "stex_tp": "1",
            },
            expected_body={
                "date": "20240105",
                "amt_qty_tp": "1",
                "mrkt_tp": "0",
                "stex_tp": "1",
            },
            response_payload=payload("program_trading_cumulative_trend"),
        ),
        EndpointCase(
            name="program_trading_trend_by_stock_and_time",
            method_name="get_program_trading_trend_by_stock_and_time",
            response_model_attr="DomesticMarketConditionProgramTradingTrendByStockAndTime",
            api_id="ka90008",
            call_kwargs={"amt_qty_tp": "1", "stk_cd": "005930", "date": "20240105"},
            expected_body={"amt_qty_tp": "1", "stk_cd": "005930", "date": "20240105"},
            response_payload=payload("program_trading_trend_by_stock_and_time"),
        ),
        EndpointCase(
            name="program_trading_trend_by_date",
            method_name="get_program_trading_trend_by_date",
            response_model_attr="DomesticMarketConditionProgramTradingTrendByDate",
            api_id="ka90010",
            call_kwargs={
                "date": "20240105",
                "amt_qty_tp": "1",
                "mrkt_tp": "P00101",
                "min_tic_tp": "0",
                "stex_tp": "1",
            },
            expected_body={
                "date": "20240105",
                "amt_qty_tp": "1",
                "mrkt_tp": "P00101",
                "min_tic_tp": "0",
                "stex_tp": "1",
            },
            response_payload=payload("program_trading_trend_by_date"),
        ),
        EndpointCase(
            name="program_trading_trend_by_stock_and_date",
            method_name="get_program_trading_trend_by_stock_and_date",
            response_model_attr="DomesticMarketConditionProgramTradingTrendByStockAndDate",
            api_id="ka90013",
            call_kwargs={"amt_qty_tp": "1", "stk_cd": "005930", "date": "20240105"},
            expected_body={"amt_qty_tp": "1", "stk_cd": "005930", "date": "20240105"},
            response_payload=payload("program_trading_trend_by_stock_and_date"),
        ),
    ]
)


@pytest.mark.parametrize("case", MARKET_CASES, ids=lambda case: case.name)
def test_domestic_market_condition_requests(monkeypatch, case: EndpointCase):
    run_post_case(
        monkeypatch,
        market_condition_module,
        DomesticMarketCondition,
        case,
        base_headers=BASE_HEADERS,
    )
