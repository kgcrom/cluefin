from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_output, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# kis.stock_info.product_basic_info
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.stock_info.product_basic_info",
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
    category="kis.stock_info",
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
    name="kis.stock_info.stock_basic_info",
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
    category="kis.stock_info",
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
    name="kis.stock_info.balance_sheet",
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
                "description": "Period type (0:annual, 1:quarterly). Default 0.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.stock_info",
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
    name="kis.stock_info.income_statement",
    description="Get income statement data.",
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
                "description": "Period type (0:annual, 1:quarterly cumulative). Default 0.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.stock_info",
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
    name="kis.stock_info.financial_ratio",
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
                "description": "Period type (0:annual, 1:quarterly). Default 0.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.stock_info",
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
    name="kis.stock_info.profitability_ratio",
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
                "description": "Period type (0:annual, 1:quarterly). Default 0.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.stock_info",
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
    name="kis.stock_info.other_key_ratio",
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
                "description": "Period type (0:annual, 1:quarterly). Default 0.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.stock_info",
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
    name="kis.stock_info.stability_ratio",
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
                "description": "Period type (0:annual, 1:quarterly). Default 0.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.stock_info",
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
    name="kis.stock_info.growth_ratio",
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
                "description": "Period type (0:annual, 1:quarterly). Default 0.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.stock_info",
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
    name="kis.stock_info.margin_tradable_stocks",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_dividend_decision",
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
    category="kis.stock_info",
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
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_stock_dividend_decision
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.stock_info.ksd_stock_dividend_decision",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_merger_split_decision",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_par_value_change_decision",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_capital_reduction_schedule",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_listing_info_schedule",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_ipo_subscription_schedule",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_forfeited_share_schedule",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_deposit_schedule",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_paid_in_capital_increase_schedule",
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
    category="kis.stock_info",
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
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.stock_info.ksd_stock_dividend_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.stock_info.ksd_stock_dividend_schedule",
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
    category="kis.stock_info",
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
    name="kis.stock_info.ksd_shareholder_meeting_schedule",
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
    category="kis.stock_info",
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


@rpc_method(
    name="kis.stock_info.estimated_earnings",
    description="Get estimated earnings for a stock.",
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
    category="kis.stock_info",
    broker="kis",
)
def handle_kis_estimated_earnings(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_stock_info.get_estimated_earnings(params["stock_code"])
    return {
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
        "data_detail": extract_output(response, "output3"),
        "periods": extract_output(response, "output4"),
    }


# ---------------------------------------------------------------------------
# kis.stock_info.stock_loanable_list
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.stock_info.stock_loanable_list",
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
    category="kis.stock_info",
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
    name="kis.stock_info.investment_opinion",
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
    category="kis.stock_info",
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
    name="kis.stock_info.investment_opinion_by_brokerage",
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
    category="kis.stock_info",
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
    handle_kis_stock_loanable_list,
    handle_kis_investment_opinion,
    handle_kis_investment_opinion_by_brokerage,
]


def register_kis_stock_info_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
