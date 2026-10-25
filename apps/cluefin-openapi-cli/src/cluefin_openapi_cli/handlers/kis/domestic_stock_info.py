from __future__ import annotations

from datetime import datetime, timedelta

from cluefin_openapi_cli import opinions, statements
from cluefin_openapi_cli.clock import KST
from cluefin_openapi_cli.errors import EXIT_BROKER, CliError
from cluefin_openapi_cli.handlers import dart as dart_handlers
from cluefin_openapi_cli.handlers._base import DispatcherProtocol, extract_output, rpc_method
from cluefin_openapi_cli.ohlcv import fetch_kis_daily_series

# Appended to every financial command's div_cls_code description.
_QUARTERLY_COVERAGE_NOTE = (
    " Quarterly rows exist only for stocks KIS covers in depth; small caps may return annual "
    "rows regardless, lagging the latest DART filing. Use dart financial-major-accounts "
    "when the newest period is missing."
)

# ---------------------------------------------------------------------------
# kis.stock_info.product_basic_info
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.product_info",
    description="Get product basic information.",
    parameters={
        "type": "object",
        "properties": {
            "pdno": {
                "type": "string",
                "description": "Product number (e.g. stock:000660, futures:KR4101SC0009, US:AAPL)",
            },
            "prdt_type_cd": {
                "type": "string",
                "description": "Product type code (300:stock, 301:futures/options, 302:bond, 512:US NASDAQ, 513:US NYSE, etc.)",
            },
        },
        "required": ["pdno", "prdt_type_cd"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_product_basic_info(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_product_basic_info(params["pdno"], params["prdt_type_cd"])
    result = extract_output(response, "output")
    if result is None:
        return {"error": "No data returned"}
    return {**result}


# ---------------------------------------------------------------------------
# kis.stock_info.stock_basic_info
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.basic_info",
    description="Get stock basic information.",
    parameters={
        "type": "object",
        "properties": {
            "prdt_type_cd": {
                "type": "string",
                "description": "Product type code (300:stock/ETF/ETN/ELW, 301:futures/options, 302:bond, 306:ELS). Default 300.",
            },
            "pdno": {
                "type": "string",
                "description": "Product number (6-digit stock code, ETN starts with Q e.g. Q500001)",
            },
        },
        "required": ["pdno"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_basic_info(params: dict, session) -> dict:
    kis = session.get_kis()
    prdt_type_cd = params.get("prdt_type_cd", "300")
    response = kis.domestic_stock_info.get_stock_basic_info(prdt_type_cd, params["pdno"])
    result = extract_output(response, "output")
    if result is None:
        return {"error": "No data returned"}
    return {**result}


# ---------------------------------------------------------------------------
# kis.stock_info.balance_sheet
# ---------------------------------------------------------------------------


@rpc_method(
    name="financial.balance_sheet",
    description="Get balance sheet data.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "6-digit stock code",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
            "div_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Period type (0:annual, 1:quarterly). Default 0." + _QUARTERLY_COVERAGE_NOTE,
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="financial",
    broker="kis",
)
def handle_kis_balance_sheet(params: dict, session) -> dict:
    kis = session.get_kis()
    div_cls_code = params.get("div_cls_code", "0")
    market = params.get("market", "J")
    response = kis.domestic_stock_info.get_balance_sheet(div_cls_code, market, params["stock_code"])
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.income_statement
# ---------------------------------------------------------------------------


@rpc_method(
    name="financial.income_statement",
    description=(
        "Get income statement data. Two response fields are named against their meaning: "
        "bsop_prti is 영업이익 (operating income) and op_prfi is 경상이익 (pre-tax ordinary income), "
        "not operating profit; 당기순이익 is thtr_ntin. A field KIS does not supply comes back as "
        "99.99, which is a placeholder and not a value."
    ),
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "6-digit stock code",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
            "div_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Period type (0:annual, 1:quarterly cumulative). Default 0." + _QUARTERLY_COVERAGE_NOTE,
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="financial",
    broker="kis",
)
def handle_kis_income_statement(params: dict, session) -> dict:
    kis = session.get_kis()
    div_cls_code = params.get("div_cls_code", "0")
    market = params.get("market", "J")
    response = kis.domestic_stock_info.get_income_statement(div_cls_code, market, params["stock_code"])
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.financial_ratio
# ---------------------------------------------------------------------------


@rpc_method(
    name="financial.ratio",
    description="Get financial ratio data.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "6-digit stock code",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
            "div_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Period type (0:annual, 1:quarterly). Default 0." + _QUARTERLY_COVERAGE_NOTE,
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="financial",
    broker="kis",
)
def handle_kis_financial_ratio(params: dict, session) -> dict:
    kis = session.get_kis()
    div_cls_code = params.get("div_cls_code", "0")
    market = params.get("market", "J")
    response = kis.domestic_stock_info.get_financial_ratio(div_cls_code, market, params["stock_code"])
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.profitability_ratio
# ---------------------------------------------------------------------------


@rpc_method(
    name="financial.profitability",
    description="Get profitability ratio data.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "6-digit stock code",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
            "div_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Period type (0:annual, 1:quarterly). Default 0." + _QUARTERLY_COVERAGE_NOTE,
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="financial",
    broker="kis",
)
def handle_kis_profitability_ratio(params: dict, session) -> dict:
    kis = session.get_kis()
    div_cls_code = params.get("div_cls_code", "0")
    market = params.get("market", "J")
    response = kis.domestic_stock_info.get_profitability_ratio(params["stock_code"], div_cls_code, market)
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.other_key_ratio
# ---------------------------------------------------------------------------


@rpc_method(
    name="financial.other_key",
    description="Get other key ratio data (payout ratio, EVA, EBITDA).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "6-digit stock code",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
            "div_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Period type (0:annual, 1:quarterly). Default 0." + _QUARTERLY_COVERAGE_NOTE,
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="financial",
    broker="kis",
)
def handle_kis_other_key_ratio(params: dict, session) -> dict:
    kis = session.get_kis()
    div_cls_code = params.get("div_cls_code", "0")
    market = params.get("market", "J")
    response = kis.domestic_stock_info.get_other_key_ratio(params["stock_code"], div_cls_code, market)
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.stability_ratio
# ---------------------------------------------------------------------------


@rpc_method(
    name="financial.stability",
    description="Get stability ratio data (debt ratio, current ratio, quick ratio).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "6-digit stock code",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
            "div_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Period type (0:annual, 1:quarterly). Default 0." + _QUARTERLY_COVERAGE_NOTE,
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="financial",
    broker="kis",
)
def handle_kis_stability_ratio(params: dict, session) -> dict:
    kis = session.get_kis()
    div_cls_code = params.get("div_cls_code", "0")
    market = params.get("market", "J")
    response = kis.domestic_stock_info.get_stability_ratio(params["stock_code"], div_cls_code, market)
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.growth_ratio
# ---------------------------------------------------------------------------


@rpc_method(
    name="financial.growth",
    description="Get growth ratio data (revenue growth, operating profit growth).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "6-digit stock code",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
            "div_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Period type (0:annual, 1:quarterly). Default 0." + _QUARTERLY_COVERAGE_NOTE,
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="financial",
    broker="kis",
)
def handle_kis_growth_ratio(params: dict, session) -> dict:
    kis = session.get_kis()
    div_cls_code = params.get("div_cls_code", "0")
    market = params.get("market", "J")
    response = kis.domestic_stock_info.get_growth_ratio(params["stock_code"], div_cls_code, market)
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.margin_tradable_stocks
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.margin_tradable",
    description="Get margin-tradable stock list.",
    parameters={
        "type": "object",
        "properties": {
            "rank_sort_cls_code": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Sort order (0:by code, 1:by name). Default 0.",
            },
            "slct_yn": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Selection (0:margin-tradable, 1:margin-restricted). Default 0.",
            },
            "stock_code": {
                "type": "string",
                "description": "Stock code (0000:all, 0001:KRX, 1001:KOSDAQ, 2001:KOSPI200, 4001:KRX100). Default 0000.",
            },
            "cond_scr_div_code": {
                "type": "string",
                "description": "Screen division code (unique key: 20477). Default 20477.",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
        },
        "required": [],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_margin_tradable_stocks(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_margin_tradable_stocks(
        params.get("rank_sort_cls_code", "0"),
        params.get("slct_yn", "0"),
        params.get("stock_code", "0000"),
        params.get("cond_scr_div_code", "20477"),
        params.get("market", "J"),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_dividend_decision
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.dividend",
    description="Get KSD dividend decision information.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "gb1": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Query type (0:all dividends, 1:settlement dividend, 2:interim dividend). Default 0.",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
            "high_gb": {
                "type": "string",
                "description": "High dividend flag. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_dividend_decision(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_dividend_decision(
        params.get("cts", ""),
        params.get("gb1", "0"),
        params["start_date"],
        params["end_date"],
        params.get("stock_code", ""),
        params.get("high_gb", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_stock_dividend_decision
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.stock_dividend",
    description="Get KSD stock dividend purchase request decision.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_stock_dividend_decision(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_stock_dividend_decision(
        params.get("stock_code", ""),
        params["end_date"],
        params["start_date"],
        params.get("cts", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_merger_split_decision
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.merger_split",
    description="Get KSD merger/split decision information.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_merger_split_decision(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_merger_split_decision(
        params.get("cts", ""),
        params["start_date"],
        params["end_date"],
        params.get("stock_code", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_par_value_change_decision
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.par_value_change",
    description="Get KSD par value change (reverse split) decision.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "market_gb": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Market (0:all, 1:KOSPI, 2:KOSDAQ). Default 0.",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_par_value_change_decision(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_par_value_change_decision(
        params.get("stock_code", ""),
        params.get("cts", ""),
        params["start_date"],
        params["end_date"],
        params.get("market_gb", "0"),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_capital_reduction_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.capital_reduction",
    description="Get KSD capital reduction schedule.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_capital_reduction_schedule(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_capital_reduction_schedule(
        params.get("cts", ""),
        params["start_date"],
        params["end_date"],
        params.get("stock_code", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_listing_info_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.listing",
    description="Get KSD listing information schedule.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_listing_info_schedule(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_listing_info_schedule(
        params.get("stock_code", ""),
        params["end_date"],
        params["start_date"],
        params.get("cts", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_ipo_subscription_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.ipo_subscription",
    description="Get KSD IPO subscription schedule.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_ipo_subscription_schedule(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_ipo_subscription_schedule(
        params.get("stock_code", ""),
        params.get("cts", ""),
        params["start_date"],
        params["end_date"],
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_forfeited_share_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.forfeited_share",
    description="Get KSD forfeited share schedule.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_forfeited_share_schedule(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_forfeited_share_schedule(
        params.get("stock_code", ""),
        params["end_date"],
        params["start_date"],
        params.get("cts", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_deposit_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.deposit",
    description="Get KSD mandatory deposit schedule.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_deposit_schedule(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_deposit_schedule(
        params["end_date"],
        params.get("stock_code", ""),
        params["start_date"],
        params.get("cts", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_paid_in_capital_increase_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.capital_increase",
    description="Get KSD paid-in capital increase schedule.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "gb1": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Query type (1:by subscription date, 2:by record date). Default 1.",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_paid_in_capital_increase_schedule(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_paid_in_capital_increase_schedule(
        params.get("cts", ""),
        params.get("gb1", "1"),
        params["start_date"],
        params["end_date"],
        params.get("stock_code", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_stock_dividend_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.bonus_issue",
    description="Get KSD stock dividend (bonus issue) schedule.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_stock_dividend_schedule(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_stock_dividend_schedule(
        params.get("cts", ""),
        params["start_date"],
        params["end_date"],
        params.get("stock_code", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_shareholder_meeting_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="schedule.shareholder_meeting",
    description="Get KSD shareholder meeting schedule.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all). Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "cts": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": ["start_date", "end_date"],
    },
    returns={"type": "object"},
    category="schedule",
    broker="kis",
)
def handle_kis_ksd_shareholder_meeting_schedule(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_ksd_shareholder_meeting_schedule(
        params.get("cts", ""),
        params["start_date"],
        params["end_date"],
        params.get("stock_code", ""),
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# kis.stock_info.estimated_earnings
# ---------------------------------------------------------------------------


# KIS labels output2/output3 rows only as DATA1..5. Row order and scale were identified against
# DART actuals (005930 FY2023, 192820) — see cluefin-openapi VENDOR_DOC_ERRATA.md "국내주식 종목추정실적".
# Money rows arrive in 억원; growth, per-share, multiples and ratios arrive ×10.
_ESTIMATE_ROWS = (
    ("revenue", "억원", 1),
    ("revenue_growth_yoy", "%", 10),
    ("operating_income", "억원", 1),
    ("operating_income_growth_yoy", "%", 10),
    ("net_income_owners", "억원", 1),
    ("net_income_owners_growth_yoy", "%", 10),
)
_ESTIMATE_DETAIL_ROWS = (
    ("ebitda", "억원", 1),
    ("eps", "원", 10),
    ("eps_growth_yoy", "%", 10),
    ("per", "배", 10),
    ("ev_ebitda", "배", 10),
    ("roe", "%", 10),
    ("debt_ratio", "%", 10),
    ("interest_coverage", "배", 10),
)
_ESTIMATE_NOTE = (
    "Estimates of one brokerage (Korea Investment & Securities research; summary.name1 is the analyst), "
    "not a consensus. Broker-by-broker ratings and target prices come from kis stock investment-opinion."
)


def _estimate_number(value, scale: int) -> float | None:
    try:
        return float(str(value).replace(",", "")) / scale
    except (TypeError, ValueError):
        return None


def _estimate_rows(block) -> list[dict]:
    """The dict rows of an output block; anything else (missing block, odd shape) counts as no rows."""
    return [row for row in block if isinstance(row, dict)] if isinstance(block, list) else []


def _estimate_table(rows, layout, periods: list[str]) -> list[dict]:
    """Label the unlabelled DATA1..5 rows by position; a layout row without a response row is skipped."""
    table = []
    for (metric, unit, scale), row in zip(layout, _estimate_rows(rows), strict=False):
        values = {period: _estimate_number(row.get(f"data{i + 1}"), scale) for i, period in enumerate(periods)}
        table.append({"metric": metric, "unit": unit, "values": values})
    return table


@rpc_method(
    name="stock.estimated_earnings",
    description=(
        "Get one brokerage's earnings estimates for a stock (국내주식 종목추정실적): three reported fiscal "
        "years and two estimate years (periods ending in E) of revenue, operating income, net income, "
        "EBITDA, EPS, PER, EV/EBITDA, ROE, debt ratio and interest coverage. These are Korea Investment & "
        "Securities research estimates (summary.name1 is the analyst), not a consensus; for ratings and "
        "target prices across brokers use kis stock investment-opinion. `data`/`data_detail` are the raw "
        "DATA1..5 rows (money in 억원, everything else ×10); `table` labels them with unit and scale applied."
    ),
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "6-digit stock code",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_estimated_earnings(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_estimated_earnings(params["stock_code"])
    data = extract_output(response, "output2")
    detail = extract_output(response, "output3")
    periods = [row.get("dt") for row in _estimate_rows(extract_output(response, "output4"))]
    return {
        "summary": extract_output(response, "output1"),
        "data": data,
        "data_detail": detail,
        "periods": extract_output(response, "output4"),
        "table": _estimate_table(data, _ESTIMATE_ROWS, periods)
        + _estimate_table(detail, _ESTIMATE_DETAIL_ROWS, periods),
        "note": _ESTIMATE_NOTE,
    }


# ---------------------------------------------------------------------------
# kis.stock_info.stock_loanable_list
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.loanable",
    description="Get loanable stock list for short selling.",
    parameters={
        "type": "object",
        "properties": {
            "excg_dvsn_cd": {
                "type": "string",
                "enum": ["00", "02", "03"],
                "description": "Exchange code (00:all, 02:KRX, 03:KOSDAQ). Default 00.",
            },
            "pdno": {
                "type": "string",
                "description": "Product number / stock code (blank for all). Default empty.",
            },
            "thco_stln_psbl_yn": {
                "type": "string",
                "description": "Loanable flag. Default Y.",
            },
            "inqr_dvsn_1": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Query type (0:all, 1:sorted by code). Default 0.",
            },
            "ctx_area_fk200": {
                "type": "string",
                "description": "Continuation search condition. Default empty.",
            },
            "ctx_area_nk100": {
                "type": "string",
                "description": "Continuation key. Default empty.",
            },
        },
        "required": [],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_loanable_list(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_stock_loanable_list(
        params.get("excg_dvsn_cd", "00"),
        params.get("pdno", ""),
        params.get("thco_stln_psbl_yn", "Y"),
        params.get("inqr_dvsn_1", "0"),
        params.get("ctx_area_fk200", ""),
        params.get("ctx_area_nk100", ""),
    )
    return {
        "data": extract_output(response, "output1"),
        "summary": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# kis.stock_info.investment_opinion
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.investment_opinion",
    description="Get investment opinion for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "6-digit stock code",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (format: 0020231113)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (format: 0020240513)",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
            "cond_scr_div_code": {
                "type": "string",
                "description": "Screen division code (unique key: 16633). Default 16633.",
            },
        },
        "required": ["stock_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_investment_opinion(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    cond_scr_div_code = params.get("cond_scr_div_code", "16633")
    response = kis.domestic_stock_info.get_investment_opinion(
        market, cond_scr_div_code, params["stock_code"], params["start_date"], params["end_date"]
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.investment_opinion_by_brokerage
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.investment_opinion_by_brokerage",
    description="Get investment opinion by brokerage.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "Brokerage member code",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (format: 0020231113)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (format: 0020240513)",
            },
            "div_cls_code": {
                "type": "string",
                "enum": ["0", "1", "2", "3"],
                "description": "Classification (0:all, 1:buy, 2:neutral, 3:sell). Default 0.",
            },
            "market": {
                "type": "string",
                "description": "Market division code (J for stocks). Default J.",
            },
            "cond_scr_div_code": {
                "type": "string",
                "description": "Screen division code (unique key: 16634). Default 16634.",
            },
        },
        "required": ["stock_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_investment_opinion_by_brokerage(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    cond_scr_div_code = params.get("cond_scr_div_code", "16634")
    div_cls_code = params.get("div_cls_code", "0")
    response = kis.domestic_stock_info.get_investment_opinion_by_brokerage(
        market, cond_scr_div_code, params["stock_code"], div_cls_code, params["start_date"], params["end_date"]
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# kis.stock_info.opinion_summary — computes from investment_opinion rows
# ---------------------------------------------------------------------------

_OPINION_DEFAULT_DAYS = 90


def _kst_today() -> str:
    return datetime.now(KST).strftime("%Y%m%d")


def _days_before(day: str, days: int) -> str:
    return (datetime.strptime(day, "%Y%m%d") - timedelta(days=days)).strftime("%Y%m%d")


@rpc_method(
    name="stock.opinion_summary",
    description=(
        "Summarize broker opinions for a stock over a window (default 90 days): each brokerage's latest "
        "rating, previous rating and target price, plus mean/median/max/min target and a rating count. "
        "Computed from kis stock investment-opinion in one call. This is the cross-broker view; "
        "kis stock estimated-earnings is a single brokerage's estimate."
    ),
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "pattern": "^[0-9]{6}$", "description": "6-digit stock code"},
            "as_of": {
                "type": "string",
                "pattern": "^[0-9]{8}$",
                "description": "End of the window (YYYYMMDD). Default today (KST).",
            },
            "days": {
                "type": "integer",
                "minimum": 7,
                "maximum": 365,
                "default": _OPINION_DEFAULT_DAYS,
                "description": f"Window length in calendar days ending at as_of. Default {_OPINION_DEFAULT_DAYS}.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_opinion_summary(params: dict, session) -> dict:
    kis = session.get_kis()
    as_of = params.get("as_of") or _kst_today()
    since = _days_before(as_of, int(params.get("days", _OPINION_DEFAULT_DAYS)))
    response = kis.domestic_stock_info.get_investment_opinion(
        "J", "16633", params["stock_code"], f"00{since}", f"00{as_of}"
    )
    rows = extract_output(response, "output")
    summary = opinions.summarize(rows if isinstance(rows, list) else [], since)
    return {"stock_code": params["stock_code"], "as_of": as_of, **summary}


# ---------------------------------------------------------------------------
# kis.stock_info.valuation — KIS close × DART share count over DART statements
# ---------------------------------------------------------------------------

_VALUATION_NOTES = (
    "시가총액 = 기준 종가(수정 전 원주가) × 보통주 발행주식총수(DART 주식의 총수, 최신 정기보고서). 우선주는 빼고 센다.",
    "per_ttm 은 시가총액 ÷ 최근 4개 분기 지배주주순이익 합, pbr 은 시가총액 ÷ 최신 보고 기간 지배주주지분. 분모가 0 이하면 null.",
    "per_by_year 의 EPS 는 한국투자증권 리서치 추정(kis stock estimated-earnings)이지 컨센서스가 아니다. 실적 연도 PER 도 기준 종가로 다시 계산한 값이다.",
    "재무 수치는 dart financial-summary 와 같은 규칙(최신 정정본, 연결 우선)이다.",
)


def _ratio_if_positive(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def _common_shares(rows: list[dict]) -> dict | None:
    common = next((row for row in rows if str(row.get("se") or "").strip() == "보통주"), None)
    if common is None:
        return None
    return {
        "issued": statements.won(common.get("istc_totqy")),
        "treasury": statements.won(common.get("tesstk_co")),
        "outstanding": statements.won(common.get("distb_stock_co")),
    }


@rpc_method(
    name="stock.valuation",
    description=(
        "Value a stock at a reference close: market cap, TTM PER, PBR, and PER on each year of the KIS "
        "research estimate (periods ending in E are estimates). Combines the KIS close (unadjusted, as of a "
        "date), the DART common share count of the latest periodic report, and dart financial-summary's "
        "quarters. Needs corp_code as well as stock_code. About 11 calls (1 KIS price, 8+1 DART, 1 KIS "
        "estimate); call once per stock and reuse."
    ),
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "pattern": "^[0-9]{6}$", "description": "6-digit stock code"},
            "corp_code": {
                "type": "string",
                "pattern": "^[0-9]{8}$",
                "description": "DART corporate unique code (8 digits, from dart corp-code-lookup)",
            },
            "as_of": {
                "type": "string",
                "pattern": "^[0-9]{8}$",
                "description": "Reference date (YYYYMMDD): last close on or before it, reports received by it. Default today (KST).",
            },
        },
        "required": ["stock_code", "corp_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_valuation(params: dict, session) -> dict:
    """Return multiples at a reference close, not the inputs. Arithmetic lives here; statement rules in `statements`."""
    stock_code = params["stock_code"]
    corp_code = params["corp_code"]
    as_of = params.get("as_of") or _kst_today()
    kis = session.get_kis()

    series = fetch_kis_daily_series(kis, stock_code, count=1, end_date=as_of, adjusted=False)
    if not series.candles:
        raise CliError(
            f"No daily close for {stock_code} on or before {as_of}",
            exit_code=EXIT_BROKER,
            error_type="NotFound",
            data={"stock_code": stock_code, "as_of": as_of},
            hint="Check the code with kis stock basic-info; a newly listed or delisted code has no close in the window.",
        )
    last = series.candles[-1]
    close = last.close

    dart = session.get_dart()
    basis, reports, dart_calls = dart_handlers.collect_reports(dart, corp_code, int(as_of[:4]), as_of, ("CFS", "OFS"))
    if not reports:
        raise CliError(
            f"No periodic report of {corp_code} received by {as_of}",
            exit_code=EXIT_BROKER,
            error_type="NotFound",
            data={"corp_code": corp_code, "as_of": as_of, "calls": 1 + dart_calls},
            hint="Check the corp_code with dart company-overview; it must belong to the same company as stock_code.",
        )
    latest_report = max(reports, key=lambda r: r.order)
    share_rows = dart_handlers.dart_rows(
        dart.periodic_report_key_information.get_total_number_of_shares(
            corp_code=corp_code, bsns_year=str(latest_report.year), reprt_code=latest_report.reprt_code
        )
    )
    shares = _common_shares(share_rows)
    issued = shares["issued"] if shares else None

    quarter_list = statements.quarters(reports)
    ttm_net_income = statements.trailing(quarter_list, "net_income_owners")
    equity_owners = statements.latest(latest_report)["equity_owners"]
    market_cap = None if issued is None else close * issued

    estimate = kis.domestic_stock_info.get_estimated_earnings(stock_code)
    periods = [row.get("dt") for row in _estimate_rows(extract_output(estimate, "output4"))]
    eps_row = next(
        (
            row
            for row in _estimate_table(extract_output(estimate, "output3"), _ESTIMATE_DETAIL_ROWS, periods)
            if row["metric"] == "eps"
        ),
        None,
    )
    per_by_year = [
        {
            "period": period,
            "estimate": str(period).endswith("E"),
            "eps": eps,
            "per": _ratio_if_positive(close, eps),
        }
        for period, eps in (eps_row["values"].items() if eps_row else ())
    ]

    eok = statements.EOK
    return {
        "stock_code": stock_code,
        "corp_code": corp_code,
        "as_of": as_of,
        "price": {"close": close, "date": last.timestamp[:8], "adjusted": False},
        "shares": {**shares, "report": f"{latest_report.year}-{latest_report.reprt_code}"} if shares else None,
        "statement_basis": basis,
        "unit": "억원",
        "market_cap": None if market_cap is None else market_cap / eok,
        "ttm_net_income_owners": None if ttm_net_income is None else ttm_net_income / eok,
        "equity_owners": None if equity_owners is None else equity_owners / eok,
        "per_ttm": _ratio_if_positive(market_cap, ttm_net_income),
        "pbr": _ratio_if_positive(market_cap, equity_owners),
        "per_by_year": per_by_year,
        "calls": 1 + dart_calls + 1 + 1,
        "notes": list(_VALUATION_NOTES),
    }


_ALL_HANDLERS = [
    handle_kis_product_basic_info,
    handle_kis_stock_basic_info,
    handle_kis_balance_sheet,
    handle_kis_income_statement,
    handle_kis_financial_ratio,
    handle_kis_profitability_ratio,
    handle_kis_other_key_ratio,
    handle_kis_stability_ratio,
    handle_kis_growth_ratio,
    handle_kis_margin_tradable_stocks,
    handle_kis_ksd_dividend_decision,
    handle_kis_ksd_stock_dividend_decision,
    handle_kis_ksd_merger_split_decision,
    handle_kis_ksd_par_value_change_decision,
    handle_kis_ksd_capital_reduction_schedule,
    handle_kis_ksd_listing_info_schedule,
    handle_kis_ksd_ipo_subscription_schedule,
    handle_kis_ksd_forfeited_share_schedule,
    handle_kis_ksd_deposit_schedule,
    handle_kis_ksd_paid_in_capital_increase_schedule,
    handle_kis_ksd_stock_dividend_schedule,
    handle_kis_ksd_shareholder_meeting_schedule,
    handle_kis_estimated_earnings,
    handle_kis_opinion_summary,
    handle_kis_stock_valuation,
    handle_kis_stock_loanable_list,
    handle_kis_investment_opinion,
    handle_kis_investment_opinion_by_brokerage,
]


def register_kis_stock_info_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
