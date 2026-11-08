from __future__ import annotations

from datetime import datetime, timedelta
from statistics import mean

from cluefin_openapi_cli import band as valuation_band
from cluefin_openapi_cli import implied, investor_metrics, opinions, quality, statements
from cluefin_openapi_cli.cache import store as cache_store
from cluefin_openapi_cli.cache.read import read_ohlcv
from cluefin_openapi_cli.clock import KST
from cluefin_openapi_cli.errors import EXIT_BROKER, CliError
from cluefin_openapi_cli.handlers import dart as dart_handlers
from cluefin_openapi_cli.handlers._base import DispatcherProtocol, extract_output, rpc_method
from cluefin_openapi_cli.handlers.ecos import to_number
from cluefin_openapi_cli.ohlcv import fetch_kis_daily_series

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


def _enterprise_value(market_cap: float | None, borrowings: float | None, cash: float | None) -> float | None:
    """시가총액 + 차입금 − 현금. 차입금·현금을 못 읽었으면 0 으로 메우지 않고 None (EV 가 조용히 틀린다)."""
    if market_cap is None or borrowings is None or cash is None:
        return None
    return market_cap + borrowings - cash


def _enterprise_value_reason(market_cap: float | None, borrowings: float | None, cash: float | None) -> str | None:
    missing = [
        name
        for name, value in (("market_cap", market_cap), ("borrowings", borrowings), ("cash", cash))
        if value is None
    ]
    return None if not missing else f"{'·'.join(missing)} 결측 — EV 를 계산하지 않는다(0 으로 메우지 않음)"


def _ratio_if_positive(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def _common_shares(rows: list[dict]) -> dict | None:
    # 공시마다 라벨이 다르다: "보통주", "보통주식\n(의결권 있는주식)" 등.
    common = next((row for row in rows if str(row.get("se") or "").strip().startswith("보통주")), None)
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


# ---------------------------------------------------------------------------
# kis.stock_info.implied_expectations — RIM 내재 ROE, 역DCF 내재 성장률
# ---------------------------------------------------------------------------

_DEFAULT_BETA = 1.0
_DEFAULT_FADE_YEARS = 10
_DEFAULT_HORIZON_YEARS = 10
_DEFAULT_TERMINAL_GROWTH = 1.0  # %, conservative and independent of risk-free on purpose
_DEFAULT_PAYOUT_RATIO = 30.0  # %, used only when DART dividends/net income is not usable
_DEFAULT_TAX_RATE = 24.2  # %, Korean effective corporate tax (incl. local tax) when Damodaran is unavailable
_DEFAULT_SALES_TO_CAPITAL = 2.0  # Damodaran convention default

_RATE_STAT_CODE = "817Y002"  # 시장금리(일별)
_KTB_10Y_ITEM = "010210000"
_CORP_AA_3Y_ITEM = "010300000"

_IMPLIED_EXPECTATIONS_NOTES = (
    "계산값이다 — 추천·라벨(싸다/비싸다)을 내지 않는다. RIM·역DCF 는 가정(ERP, 베타, 페이드·구간 연수, 배당성향, "
    "재투자율, 터미널 성장률)에 민감하다. assumptions 에 쓴 값과 출처를 바꾸면 결과가 바뀐다.",
    "시가총액 = kis stock valuation 과 같은 식(기준 종가 × DART 보통주 발행주식총수, 우선주 제외).",
    "RIM: B0 은 DART 최신 지배기업지분(연결 우선). 1년차 ROE 가 fade_years 년에 걸쳐 자기자본비용으로 선형 수렴하고, "
    "그 뒤는 초과 ROE 가 정확히 0 이라고 가정한다(별도 터미널 값 없음). 장부가는 배당성향만큼만 유보해 성장한다.",
    "역DCF: EV = 시가총액 + DART 차입금(최신 보고 기준, 계정 합산 기준은 borrowings_basis) − 현금. 차입금·현금을 못 읽으면 "
    "EV·WACC 를 계산하지 않고 ev_reason 에 이유를 적는다(0 으로 메우지 않음). 매출은 TTM. "
    "재투자 = 매출증분 ÷ sales_to_capital(Damodaran 관행), horizon_years 년 뒤는 terminal_growth 로 영구성장한다고 "
    "가정한다.",
    "reverse_dcf.implied_revenue_growth 는 TTM 영업이익률을 그대로 horizon_years 동안 유지한다고 가정한 값이다 — "
    "업황 정점(또는 저점)의 TTM 마진이면 내재 성장률이 과장되게 낮아(또는 높아) 보일 수 있다. "
    "alternative_dart_3y_avg_margin 에 DART 3개년 평균 영업이익률로 다시 푼 값을 같이 낸다; 둘 다 '정답'이 아니라 "
    "마진 가정에 결과가 조건부라는 뜻이다.",
    "WACC 는 시가총액·차입금의 시장가치 가중. 세후 타인자본비용의 세율·ERP 는 둘 다 주어지지 않으면 Damodaran 한국 "
    "표(cluefin-feeds)에서 한 번 받는다 — erp 와 tax_rate 를 모두 주면 호출하지 않는다.",
    "ECOS 국고채(10년)·회사채(3년, AA-) 중 하나라도 최근 값이 없으면 자기자본비용·WACC 를 0% 로 채우지 않고 "
    "exit 4 로 멈춘다(BrokerUnavailable, retryable). --erp 없이 Damodaran 한국 ERP 조회가 실패해도 같은 exit 4 — "
    "둘 다 자격증명이 아니라 데이터 출처 문제라서다.",
    "no_solution(reason 있음)은 주어진 탐색 구간(ROE -50%~150%, 성장률 -50%~200%) 안에 해가 없다는 뜻이지 "
    "'불가능'이 아니다 — 가정을 좁히면 해가 생길 수 있다.",
)


def _fetch_latest_rate(ecos, item_code: str, end_date: str) -> tuple[float | None, str | None]:
    """Latest 817Y002(시장금리, 일별) value on or before end_date; (value_percent, as_of) or (None, None)."""
    start = (datetime.strptime(end_date, "%Y%m%d") - timedelta(days=14)).strftime("%Y%m%d")
    page = ecos.statistic_search.search(_RATE_STAT_CODE, "D", start, end_date, (item_code,))
    rows = sorted((page.rows or []), key=lambda row: row.time)
    if not rows:
        return None, None
    last = rows[-1]
    return to_number(last.data_value), last.time


def _fetch_damodaran_korea() -> dict | None:
    """Korea row of Damodaran's country risk premium table (ERP %, corporate tax rate %, page `updated`).

    Kept as its own function (rather than inlined) so unit tests can monkeypatch it and never touch the
    network; the handler calls it at most once, and only when erp or tax_rate is not already given.
    """
    from cluefin_feeds.damodaran import Client as DamodaranClient

    table = DamodaranClient().country_risk_premiums()
    row = table.get("Korea")
    if row is None or row.equity_risk_premium is None:
        return None
    return {
        "erp": float(row.equity_risk_premium),
        "tax_rate": float(row.corporate_tax_rate) if row.corporate_tax_rate is not None else None,
        "updated": table.updated.isoformat() if table.updated else None,
    }


def _payout_ratio(annual_years: list[dict]) -> tuple[float, str]:
    latest = annual_years[-1] if annual_years else None
    dividends = latest.get("dividends_paid") if latest else None
    net_income = latest.get("net_income_owners") if latest else None
    if dividends is not None and net_income is not None and net_income > 0:
        ratio = max(0.0, min(1.0, abs(dividends) / net_income)) * 100
        return ratio, "dart financial-summary 최신 FY 현금흐름표 배당금 지급 ÷ 지배주주순이익"
    return _DEFAULT_PAYOUT_RATIO, f"기본값 {_DEFAULT_PAYOUT_RATIO}% (DART 배당·순이익으로 계산할 수 없음)"


def _revenue_cagr(annual_years: list[dict]) -> float | None:
    if len(annual_years) < 2:
        return None
    first, last = annual_years[0], annual_years[-1]
    revenue_first, revenue_last = first.get("revenue"), last.get("revenue")
    if revenue_first is None or revenue_last is None or revenue_first <= 0:
        return None
    periods = len(annual_years) - 1
    return ((revenue_last / revenue_first) ** (1 / periods) - 1) * 100


def _avg_operating_margin(annual_years: list[dict]) -> float | None:
    """Simple mean of 영업이익 ÷ 매출 over the DART 3 FY rows (not TTM) — a less cyclical margin level."""
    margins = [
        year["operating_income"] / year["revenue"]
        for year in annual_years
        if year.get("operating_income") is not None and year.get("revenue")
    ]
    return mean(margins) if margins else None


def _kis_estimate_roe(kis, stock_code: str) -> list[dict]:
    estimate = kis.domestic_stock_info.get_estimated_earnings(stock_code)
    periods = [row.get("dt") for row in _estimate_rows(extract_output(estimate, "output4"))]
    table = _estimate_table(extract_output(estimate, "output3"), _ESTIMATE_DETAIL_ROWS, periods)
    roe_row = next((row for row in table if row["metric"] == "roe"), None)
    if roe_row is None:
        return []
    return [
        {"period": period, "estimate": str(period).endswith("E"), "roe": roe}
        for period, roe in roe_row["values"].items()
    ]


def _sensitivity_table(base_erp: float, base_risk_free: float, beta: float, build_row) -> list[dict]:
    """ERP ±1%p and a horizon/fade ±5 years, one row per delta combination (not a full cross-product)."""
    rows = []
    for erp_delta in (-1.0, 0.0, 1.0):
        for years_delta in (-5, 0, 5):
            if erp_delta != 0.0 and years_delta != 0:
                continue  # vary one factor at a time, keep the table small
            erp = base_erp + erp_delta
            coe = implied.cost_of_equity(base_risk_free / 100, beta, erp / 100)
            rows.append({"erp_delta": erp_delta, "years_delta": years_delta, **build_row(coe, years_delta)})
    return rows


@rpc_method(
    name="stock.implied_expectations",
    description=(
        "Reverse-engineer what today's market price assumes: RIM(잔여이익모델)의 내재 영구 ROE, 역DCF 의 내재 매출 "
        "성장률. 둘 다 DART 3개년 ROE·매출 성장률·TTM 영업이익률, 가능하면 KIS 추정 ROE 와 나란히 낸다. 숫자와 가정만 "
        "낸다 — 싸다/비싸다 라벨이나 추천은 없다. KIS 종가 + DART 재무제표(statements 모듈과 같은 규칙) + ECOS 국고채 "
        "10년·회사채 AA- 3년 + Damodaran 한국 ERP·법인세율(erp·tax_rate 를 모두 주면 생략)을 쓴다. 약 14회 호출."
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
                "description": "Reference date (YYYYMMDD): last close on or before it, reports received by it, "
                "latest rates on or before it. Default today (KST).",
            },
            "erp": {
                "type": "number",
                "description": "Equity risk premium override (%, e.g. 5.5). Default: Damodaran Korea equity risk "
                "premium (cluefin-feeds); source and the page's `updated` date are in the response.",
            },
            "beta": {
                "type": "number",
                "default": _DEFAULT_BETA,
                "description": f"Levered beta for CAPM cost of equity. Default {_DEFAULT_BETA} (no Damodaran "
                "industry-beta mapping in this phase).",
            },
            "fade_years": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30,
                "default": _DEFAULT_FADE_YEARS,
                "description": f"RIM: years over which excess ROE (ROE minus cost of equity) fades linearly to "
                f"zero. Default {_DEFAULT_FADE_YEARS}.",
            },
            "payout_ratio": {
                "type": "number",
                "minimum": 0,
                "maximum": 100,
                "description": "RIM: dividend payout ratio (%) used to grow book value each year. Default: "
                "latest FY DART dividends paid / net income attributable to owners, clipped to 0-100, or "
                f"{_DEFAULT_PAYOUT_RATIO} if that cannot be computed.",
            },
            "horizon_years": {
                "type": "integer",
                "minimum": 1,
                "maximum": 30,
                "default": _DEFAULT_HORIZON_YEARS,
                "description": f"Reverse DCF: explicit years of revenue growth solved for. Default "
                f"{_DEFAULT_HORIZON_YEARS}.",
            },
            "terminal_growth": {
                "type": "number",
                "default": _DEFAULT_TERMINAL_GROWTH,
                "description": f"Reverse DCF: perpetual revenue growth (%) after horizon_years. Default "
                f"{_DEFAULT_TERMINAL_GROWTH} (conservative, chosen independently of the risk-free rate).",
            },
            "tax_rate": {
                "type": "number",
                "description": "Tax rate (%) for after-tax cost of debt and reverse-DCF NOPAT. Default: Damodaran "
                f"Korea corporate tax rate, or {_DEFAULT_TAX_RATE} if that cannot be fetched.",
            },
            "sales_to_capital": {
                "type": "number",
                "exclusiveMinimum": 0,
                "default": _DEFAULT_SALES_TO_CAPITAL,
                "description": f"Reverse DCF: revenue generated per unit of invested capital (Damodaran "
                f"convention); reinvestment = revenue growth ÷ this. Default {_DEFAULT_SALES_TO_CAPITAL}.",
            },
        },
        "required": ["stock_code", "corp_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_implied_expectations(params: dict, session) -> dict:  # noqa: PLR0914
    stock_code = params["stock_code"]
    corp_code = params["corp_code"]
    as_of = params.get("as_of") or _kst_today()
    beta = float(params.get("beta", _DEFAULT_BETA))
    fade_years = int(params.get("fade_years", _DEFAULT_FADE_YEARS))
    horizon_years = int(params.get("horizon_years", _DEFAULT_HORIZON_YEARS))
    terminal_growth_pct = float(params.get("terminal_growth", _DEFAULT_TERMINAL_GROWTH))
    sales_to_capital = float(params.get("sales_to_capital", _DEFAULT_SALES_TO_CAPITAL))

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
    annual_reports = [r for r in reports if r.reprt_code == "11011"]
    annual_report = max(annual_reports, key=lambda r: r.year) if annual_reports else None
    annual_years = statements.annual(annual_report) if annual_report else []

    share_rows = dart_handlers.dart_rows(
        dart.periodic_report_key_information.get_total_number_of_shares(
            corp_code=corp_code, bsns_year=str(latest_report.year), reprt_code=latest_report.reprt_code
        )
    )
    shares = _common_shares(share_rows)
    issued = shares["issued"] if shares else None

    quarter_list = statements.quarters(reports)
    latest_figures = statements.latest(latest_report)
    eok = statements.EOK

    b0 = latest_figures["equity_owners"]
    borrowings = latest_figures["borrowings"]
    cash = latest_figures["cash"]
    ttm_revenue = statements.trailing(quarter_list, "revenue")
    ttm_operating_income = statements.trailing(quarter_list, "operating_income")

    market_cap = None if issued is None else close * issued
    ev_target = _enterprise_value(market_cap, borrowings, cash)
    operating_margin = None if not ttm_revenue or ttm_operating_income is None else ttm_operating_income / ttm_revenue

    payout_ratio_pct, payout_source = _payout_ratio(annual_years)
    if "payout_ratio" in params:
        payout_ratio_pct, payout_source = float(params["payout_ratio"]), "param"

    ecos = session.get_ecos()
    risk_free_pct, risk_free_as_of = _fetch_latest_rate(ecos, _KTB_10Y_ITEM, as_of)
    if risk_free_pct is None:
        raise CliError(
            f"ECOS returned no 국고채(10년) rate (817Y002/010210000) on or before {as_of}.",
            exit_code=EXIT_BROKER,
            error_type="BrokerUnavailable",
            retryable=True,
            data={"stat_code": _RATE_STAT_CODE, "item_code": _KTB_10Y_ITEM, "as_of": as_of},
            hint="Retry once; check with ecos series --stat-code 817Y002 --cycle D --item-codes 010210000.",
        )
    cost_of_debt_pct, cost_of_debt_as_of = _fetch_latest_rate(ecos, _CORP_AA_3Y_ITEM, as_of)
    if cost_of_debt_pct is None:
        raise CliError(
            f"ECOS returned no 회사채(3년, AA-) rate (817Y002/010300000) on or before {as_of}.",
            exit_code=EXIT_BROKER,
            error_type="BrokerUnavailable",
            retryable=True,
            data={"stat_code": _RATE_STAT_CODE, "item_code": _CORP_AA_3Y_ITEM, "as_of": as_of},
            hint="Retry once; check with ecos series --stat-code 817Y002 --cycle D --item-codes 010300000.",
        )

    erp_given = "erp" in params
    tax_given = "tax_rate" in params
    damodaran = None
    damodaran_error = None
    if not erp_given or not tax_given:
        try:
            damodaran = _fetch_damodaran_korea()
        except Exception as exc:  # noqa: BLE001 - network/parse failure, turned into a CLI error or fallback below
            damodaran_error = f"{type(exc).__name__}: {str(exc)[:200]}"

    if erp_given:
        erp_pct, erp_source, damodaran_updated = float(params["erp"]), "param", None
    elif damodaran is not None:
        erp_pct, erp_source = damodaran["erp"], "Damodaran Korea (cluefin-feeds)"
        damodaran_updated = damodaran["updated"]
    else:
        raise CliError(
            "Damodaran Korea ERP could not be fetched and --erp was not given.",
            exit_code=EXIT_BROKER,
            error_type="BrokerUnavailable",
            retryable=True,
            data={"reason": damodaran_error},
            hint="Pass --erp <percent> to override, or retry once network to pages.stern.nyu.edu is available.",
        )

    if tax_given:
        tax_rate_pct, tax_source = float(params["tax_rate"]), "param"
    elif damodaran is not None and damodaran.get("tax_rate") is not None:
        tax_rate_pct, tax_source = damodaran["tax_rate"], "Damodaran Korea (cluefin-feeds)"
    else:
        tax_rate_pct, tax_source = _DEFAULT_TAX_RATE, f"기본값 {_DEFAULT_TAX_RATE}% (Damodaran 을 못 받음)"

    risk_free = risk_free_pct / 100
    cost_of_debt = cost_of_debt_pct / 100
    tax_rate = tax_rate_pct / 100
    erp = erp_pct / 100
    terminal_growth = terminal_growth_pct / 100

    cost_of_equity = implied.cost_of_equity(risk_free, beta, erp)
    after_tax_cost_of_debt = implied.after_tax_cost_of_debt(cost_of_debt, tax_rate)
    market_cap_eok = None if market_cap is None else market_cap / eok
    borrowings_eok = None if borrowings is None else borrowings / eok
    wacc = (
        None
        if market_cap_eok is None or borrowings_eok is None
        else implied.wacc(market_cap_eok, borrowings_eok, cost_of_equity, after_tax_cost_of_debt)
    )

    rim_result = (
        implied.BisectionResult(None, "missing_book_equity_or_market_cap")
        if b0 is None or b0 <= 0 or market_cap_eok is None
        else implied.implied_roe(market_cap_eok, b0 / eok, cost_of_equity, fade_years, payout_ratio_pct / 100)
    )
    avg_operating_margin = _avg_operating_margin(annual_years)

    def _dcf_result(margin: float | None) -> implied.BisectionResult:
        if not ttm_revenue or margin is None or ev_target is None or wacc is None:
            return implied.BisectionResult(None, "missing_revenue_margin_ev_or_wacc")
        return implied.implied_growth(
            ev_target / eok, ttm_revenue / eok, margin, tax_rate, sales_to_capital, wacc, horizon_years, terminal_growth
        )

    dcf_result = _dcf_result(operating_margin)
    dcf_result_avg_margin = _dcf_result(avg_operating_margin)

    def rim_sensitivity_row(coe: float, years_delta: int) -> dict:
        years = max(1, fade_years + years_delta)
        result = (
            implied.BisectionResult(None, "missing_book_equity_or_market_cap")
            if b0 is None or b0 <= 0 or market_cap_eok is None
            else implied.implied_roe(market_cap_eok, b0 / eok, coe, years, payout_ratio_pct / 100)
        )
        return {"implied_roe": None if result.value is None else result.value * 100, "reason": result.reason}

    def dcf_sensitivity_row(coe: float, years_delta: int) -> dict:
        years = max(1, horizon_years + years_delta)
        row_after_tax_debt = implied.after_tax_cost_of_debt(cost_of_debt, tax_rate)
        row_wacc = (
            None
            if market_cap_eok is None or borrowings_eok is None
            else implied.wacc(market_cap_eok, borrowings_eok, coe, row_after_tax_debt)
        )
        result = (
            implied.BisectionResult(None, "missing_revenue_margin_ev_or_wacc")
            if not ttm_revenue or operating_margin is None or ev_target is None or row_wacc is None
            else implied.implied_growth(
                ev_target / eok,
                ttm_revenue / eok,
                operating_margin,
                tax_rate,
                sales_to_capital,
                row_wacc,
                years,
                terminal_growth,
            )
        )
        return {"implied_growth": None if result.value is None else result.value * 100, "reason": result.reason}

    roes = [year["roe"] for year in annual_years if year.get("roe") is not None]

    return {
        "stock_code": stock_code,
        "corp_code": corp_code,
        "as_of": as_of,
        "price": {"close": close, "date": last.timestamp[:8], "adjusted": False},
        "statement_basis": basis,
        "unit": "억원",
        "market_cap": market_cap_eok,
        "ev": None if ev_target is None else ev_target / eok,
        "ev_reason": _enterprise_value_reason(market_cap, borrowings, cash),
        "equity_owners": None if b0 is None else b0 / eok,
        "borrowings": borrowings_eok,
        "cash": None if cash is None else cash / eok,
        "ttm_revenue": None if ttm_revenue is None else ttm_revenue / eok,
        "ttm_operating_income": None if ttm_operating_income is None else ttm_operating_income / eok,
        "ttm_operating_margin": None if operating_margin is None else operating_margin * 100,
        "rim": {
            "implied_roe": None if rim_result.value is None else rim_result.value * 100,
            "reason": rim_result.reason,
        },
        "reverse_dcf": {
            "implied_revenue_growth": None if dcf_result.value is None else dcf_result.value * 100,
            "reason": dcf_result.reason,
            "margin_assumption": "ttm_operating_margin",
            "alternative_dart_3y_avg_margin": {
                "margin_assumption": "dart_3y_avg_operating_margin",
                "operating_margin": None if avg_operating_margin is None else avg_operating_margin * 100,
                "implied_revenue_growth": None
                if dcf_result_avg_margin.value is None
                else dcf_result_avg_margin.value * 100,
                "reason": dcf_result_avg_margin.reason,
            },
        },
        "comparison": {
            "dart_roe_latest_fy": annual_years[-1]["roe"] if annual_years else None,
            "dart_roe_3y_avg": mean(roes) if roes else None,
            "dart_revenue_cagr_3y": _revenue_cagr(annual_years),
            "ttm_operating_margin": None if operating_margin is None else operating_margin * 100,
            "dart_operating_margin_3y_avg": None if avg_operating_margin is None else avg_operating_margin * 100,
            "kis_estimate_roe": _kis_estimate_roe(kis, stock_code),
        },
        "sensitivity": {
            "rim_implied_roe": _sensitivity_table(erp_pct, risk_free_pct, beta, rim_sensitivity_row),
            "reverse_dcf_implied_growth": _sensitivity_table(erp_pct, risk_free_pct, beta, dcf_sensitivity_row),
        },
        "assumptions": {
            "beta": beta,
            "erp": {"value": erp_pct, "source": erp_source, "updated": damodaran_updated},
            "risk_free": {"value": risk_free_pct, "source": "ECOS 817Y002 국고채(10년)", "as_of": risk_free_as_of},
            "cost_of_debt": {
                "value": cost_of_debt_pct,
                "source": "ECOS 817Y002 회사채(3년, AA-)",
                "as_of": cost_of_debt_as_of,
            },
            "tax_rate": {"value": tax_rate_pct, "source": tax_source},
            "cost_of_equity": cost_of_equity * 100,
            "wacc": None if wacc is None else wacc * 100,
            "fade_years": fade_years,
            "payout_ratio": {"value": payout_ratio_pct, "source": payout_source},
            "horizon_years": horizon_years,
            "terminal_growth": terminal_growth_pct,
            "sales_to_capital": sales_to_capital,
        },
        "calls": 2 + dart_calls + 1 + 2,
        "notes": list(_IMPLIED_EXPECTATIONS_NOTES),
    }


# ---------------------------------------------------------------------------
# kis.stock_info.valuation_band — 5-year PER/PBR band from the local cache × per-year DART EPS/BPS
# ---------------------------------------------------------------------------

_BAND_DEFAULT_YEARS = 5
_BAND_MIN_YEARS = 2
_BAND_MAX_YEARS = 10

_VALUATION_BAND_NOTES = (
    "PER·PBR 시계열 = 그날 수정종가(로컬 `cache ohlcv` × adj_factor) ÷ 그날 이미 공시됐어야 하는 최신 사업연도 "
    "EPS·BPS(4월 1일부터 전년도, 그 전에는 전전년도 — 12월 결산 가정). current 와 같은 기준이라 현재 분위가 "
    "같은 잣대의 비교다. 결산월이 다른 종목은 기간이 어긋날 수 있다.",
    "EPS·BPS 는 cache financials(fnlttMultiAcnt, 지배/비지배 구분 없음) 대신 종목별 전체 재무제표를 "
    "연도마다 직접 불러 계산한다(지배주주순이익·지배기업지분 ÷ share_base.base_shares, 우선주 제외). "
    "base_shares 는 as_of 까지 공시된 가장 최근 정기보고서의 보통주 발행주식총수를 수정주가 기준으로 맞춘 값이고 "
    "모든 연도에 같이 쓴다 — 그 해 주식수로 나누면 무상증자·액면분할 뒤 다음 사업보고서까지 배수가 끊긴다"
    "(2026-11-08 194370). 유상증자·CB 전환으로 주식수가 실제로 늘어난 종목은 과거 배수가 조금 낮게 나온다. "
    "결정 2026-11-04 docs/plans/today-bundles-plan.md B-7, 2026-11-08 주식수 기준 변경.",
    "사업보고서가 늦어 아직 없는 연도는 빠진다 — 분기 실적을 연 환산하지 않는다.",
    "current 는 캐시의 가장 최근 종가 ÷ 계산 가능한 가장 최근 회계연도 EPS·BPS다 — kis stock valuation 의 "
    "TTM·최신 분기 분모와 다르다(연간 vs TTM). current_percentile 은 과거 분포 안에서 현재 값 이하인 표본의 "
    "비율(0~100)이다.",
    "가격은 로컬 cache(`cache load`)에서 읽는다 — 실시간 KIS 호출이 아니다. 캐시가 오래됐으면 band·current "
    "모두 그만큼 오래된 값이다.",
)


_PERIOD_END = {"11013": "03-31", "11012": "06-30", "11014": "09-30", "11011": "12-31"}


def _factor_on(priced: list[dict], day: str) -> float:
    """adj_factor of the last bar on or before `day` (ISO), or of the first bar when `day` precedes them all."""
    before = [bar for bar in priced if bar["date"] <= day]
    bar = before[-1] if before else priced[0]
    return bar["adj_factor"] or 1.0


def _share_count_as_of(dart, corp_code: str, as_of: str) -> tuple[float | None, dict | None, int]:
    """(issued common shares, report, calls) from the latest periodic report received by `as_of`.

    Tries this year's and last year's reports, newest period first; a report filed after `as_of` is skipped.
    """
    year = int(as_of[:4])
    calls = 0
    for bsns_year in (year, year - 1):
        for reprt_code in ("11011", "11014", "11012", "11013"):  # newest period first
            rows = dart_handlers.dart_rows(
                dart.periodic_report_key_information.get_total_number_of_shares(
                    corp_code=corp_code, bsns_year=str(bsns_year), reprt_code=reprt_code
                )
            )
            calls += 1
            rcept_no = str(rows[0].get("rcept_no") or "") if rows else ""
            if not rcept_no or rcept_no[:8] > as_of:
                continue
            shares = _common_shares(rows)
            report = {"bsns_year": str(bsns_year), "reprt_code": reprt_code, "rcept_no": rcept_no}
            return (shares["issued"] if shares else None), report, calls
    return None, None, calls


def _fetch_band_annual_reports(dart, corp_code: str, years: list[int], as_of: str) -> tuple[str | None, list, int]:
    """(basis, reports, calls): CFS across every year if any exists, else OFS across every year.

    Unlike `collect_reports` (which windows two years for the summary/valuation commands), this
    asks every year in the band at once so the whole series shares one statement basis.
    """
    keys = [(year, "11011") for year in years]
    calls = 0
    for basis in ("CFS", "OFS"):
        reports = dart_handlers.fetch_reports(dart, corp_code, keys, as_of, basis)
        calls += len(keys)
        if reports:
            return basis, reports, calls
    return None, [], calls


@rpc_method(
    name="stock.valuation_band",
    description=(
        "5-year PER/PBR band: each cached day's adjusted close (local `cache` DuckDB) over each fiscal "
        "year's EPS/BPS (DART full statements fetched per year rather than cache financials, which has no "
        "지배/비지배 split, divided by one common share count — the latest filed as of as_of, on the adjusted-price "
        "base — so bonus issues and splits do not break the band). Returns min/p25/median/p75/max of the daily multiple "
        "over the window plus the current multiple (latest cached close over the latest computable fiscal "
        "year's EPS/BPS) and its percentile within that history. Needs corp_code as well as stock_code, and a "
        "`cache load` already run. One DART call per fiscal year, doubled if only separate (OFS) statements "
        "exist, plus up to 8 for the share count; no live KIS call — prices come from the local cache."
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
                "description": "Reference date (YYYYMMDD): last cached close on or before it, reports received "
                "by it. Default today (KST).",
            },
            "years": {
                "type": "integer",
                "minimum": _BAND_MIN_YEARS,
                "maximum": _BAND_MAX_YEARS,
                "default": _BAND_DEFAULT_YEARS,
                "description": f"Band length in years of daily closes back from as_of. Default {_BAND_DEFAULT_YEARS}.",
            },
        },
        "required": ["stock_code", "corp_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_valuation_band(params: dict, session) -> dict:
    """Band from the local price cache, not a live KIS call; multiple math lives in `band.py`."""
    stock_code = params["stock_code"]
    corp_code = params["corp_code"]
    as_of = params.get("as_of") or _kst_today()
    years_n = int(params.get("years", _BAND_DEFAULT_YEARS))
    window_end = datetime.strptime(as_of, "%Y%m%d").date()
    try:
        window_start = window_end.replace(year=window_end.year - years_n)
    except ValueError:  # Feb 29
        window_start = window_end.replace(year=window_end.year - years_n, day=28)
    fiscal_years = list(
        range(valuation_band.trailing_fiscal_year(window_start), valuation_band.trailing_fiscal_year(window_end) + 1)
    )

    dart = session.get_dart()
    basis, reports, dart_calls = _fetch_band_annual_reports(dart, corp_code, fiscal_years, as_of)
    if not reports:
        raise CliError(
            f"No annual report (11011) of {corp_code} received by {as_of} for {fiscal_years[0]}-{fiscal_years[-1]}.",
            exit_code=EXIT_BROKER,
            error_type="NotFound",
            data={"corp_code": corp_code, "as_of": as_of, "calls": dart_calls},
            hint="Check the corp_code with dart company-overview; it must belong to the same company as stock_code.",
        )

    cache_conn = cache_store.open_store(read_only=True)
    try:
        bars_payload = read_ohlcv(cache_conn, stock_code, since=window_start, until=window_end, adjusted=True)
    finally:
        cache_conn.close()

    priced = [bar for bar in bars_payload["bars"] if bar["close"] is not None]
    bars = [(bar["date"], bar["close"]) for bar in priced]
    if not bars:
        raise CliError(
            f"No cached close for {stock_code} between {window_start:%Y%m%d} and {as_of}.",
            exit_code=EXIT_BROKER,
            error_type="NotFound",
            data={"stock_code": stock_code, "as_of": as_of},
            hint="Run `cache load` first, or check the code with `cache company --code`.",
        )
    # Adjusted prices sit on the share base after the latest corporate action in the cache. The share count is as
    # of the report's period end, so dividing by that day's factor puts it on the adjusted base — a bonus issue
    # between the period end and as_of is then still counted.
    issued, share_report, share_calls = _share_count_as_of(dart, corp_code, as_of)
    dart_calls += share_calls
    last_factor = priced[-1]["adj_factor"] or 1.0
    share_factor = (
        1.0
        if share_report is None
        else _factor_on(priced, f"{share_report['bsns_year']}-{_PERIOD_END[share_report['reprt_code']]}")
    )
    base_shares = None if issued is None else issued / share_factor

    eps_by_year: dict[int, float | None] = {}
    bps_by_year: dict[int, float | None] = {}
    years_detail = []
    for report in sorted(reports, key=lambda r: r.year):
        figures = statements.latest(report)
        eps, bps = valuation_band.eps_bps(figures["net_income_owners"], figures["equity_owners"], base_shares)
        eps_by_year[report.year] = eps
        bps_by_year[report.year] = bps
        years_detail.append(
            {
                "year": report.year,
                "net_income_owners": figures["net_income_owners"],
                "equity_owners": figures["equity_owners"],
                "eps": eps,
                "bps": bps,
            }
        )

    computable_years = [year for year in eps_by_year if eps_by_year[year] is not None or bps_by_year[year] is not None]
    latest_year = max(computable_years) if computable_years else None

    current_date, current_close = bars[-1]
    current_eps = eps_by_year.get(latest_year) if latest_year is not None else None
    current_bps = bps_by_year.get(latest_year) if latest_year is not None else None

    return {
        "stock_code": stock_code,
        "corp_code": corp_code,
        "as_of": as_of,
        "years": fiscal_years,
        "statement_basis": basis,
        "current": {
            "close": priced[-1]["close"] / last_factor,
            "date": current_date,
            "eps_bps_year": latest_year,
        },
        "share_base": {
            "issued_as_of": issued,
            "report": share_report,
            "adj_factor_at_period_end": share_factor,
            "base_shares": base_shares,
        },
        "per": valuation_band.band(bars, eps_by_year, current_close=current_close, current_per_share=current_eps),
        "pbr": valuation_band.band(bars, bps_by_year, current_close=current_close, current_per_share=current_bps),
        "years_detail": years_detail,
        "calls": dart_calls,
        "notes": list(_VALUATION_BAND_NOTES),
    }


# ---------------------------------------------------------------------------
# kis.stock_info.investor_metrics — FCF·오너 어닝스·EV/EBIT·PEG·주주수익률·Altman Z
# ---------------------------------------------------------------------------

_INVESTOR_METRICS_NOTES = (
    "계산값이다 — 추천·라벨(싸다/비싸다)을 내지 않는다. 시가총액 = kis stock valuation 과 같은 식(기준 "
    "종가 × DART 보통주 발행주식총수, 우선주 제외).",
    "fcf_yield·owner_earnings·shareholder_yield 는 최신 사업보고서(annual report)의 1개년(annual 의 "
    "마지막 해) 현금흐름표 기준이다 — 최신 분기가 그 이후면 그만큼 뒤처진다. statements.py 는 분기 "
    "현금흐름을 연환산하지 않는다(YTD 뿐). ev_ebit·earnings_yield·PEG 의 PER 은 직전 4개 분기 합산(TTM) "
    "지배주주순이익·영업이익을 쓴다 — kis stock valuation/implied-expectations 와 같은 관례.",
    "오너 어닝스 = 지배주주순이익 + 감가상각비 + 무형자산상각비 − 유형자산 취득 전액 − 운전자본 증가. "
    "감가상각비·무형자산상각비 중 하나라도 없으면 0 으로 메우지 않고 null + 이유를 낸다(investor_metrics.py).",
    "주주수익률 = (배당금 지급 + 자기주식 취득 − 자기주식 처분 − 주식 발행) ÷ 시가총액. proceeds_from_share_"
    "issuance(statements.py)는 실물로 확인됐다(2026-11-04, 대규모 유상증자가 있었던 종목 실호출). "
    "treasury_shares_disposed 는 아직 실물로 확인되지 않았다. 현금흐름표가 읽혔으면 없는 항목은 그 활동이 "
    "없었던 것으로 보고 0 으로 계산하며 assumed_zero 에 이름을 남긴다 — 값이 의심스러우면 assumed_zero 를 본다.",
    "PEG 의 성장률은 두 출처를 나란히 낸다: dart_eps_growth(최신 사업보고서 당기·전전기 지배주주순이익 ÷ "
    "그 사업연도 말 보통주 발행주식수로 구한 EPS 의 CAGR, DART share-count 호출 1회 추가)와 "
    "kis_eps_growth(KIS 종목추정실적 eps_growth_yoy, 가장 가까운 추정연도, 한국투자증권 한 곳의 추정). "
    "어느 쪽도 다른 쪽을 대신하지 않는다.",
    "Altman Z(시총 원형)는 quality.altman_z — quality.py 의 Z''(장부가) 계산 요소(x1~x3)를 재사용하고 "
    "x4(시가총액/부채)·x5(매출/자산)만 새로 낸다. 결측 성분은 missing 에 이유가 있다.",
)


@rpc_method(
    name="stock.investor_metrics",
    description=(
        "Value-investor quality/value metrics at a reference close: FCF yield, owner earnings (and its "
        "yield), EV/EBIT and earnings yield (Greenblatt magic-formula style), PEG from both a DART 3-year "
        "EPS CAGR and the KIS research estimate's EPS growth, shareholder yield (dividends + buybacks − "
        "disposals − issuance, cash-flow statement), and Altman Z (market-cap original, reusing dart "
        "financial-summary's quality.py for its components). Numbers and components only, no buy/sell "
        "label. Needs corp_code as well as stock_code. About 12 calls (1 KIS price, 8+2 DART, 1 KIS "
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
def handle_kis_investor_metrics(params: dict, session) -> dict:  # noqa: PLR0914
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
    annual_reports = [r for r in reports if r.reprt_code == "11011"]
    annual_report = max(annual_reports, key=lambda r: r.year) if annual_reports else None
    annual_years = statements.annual(annual_report) if annual_report else []

    share_rows = dart_handlers.dart_rows(
        dart.periodic_report_key_information.get_total_number_of_shares(
            corp_code=corp_code, bsns_year=str(latest_report.year), reprt_code=latest_report.reprt_code
        )
    )
    dart_calls += 1
    shares = _common_shares(share_rows)
    issued = shares["issued"] if shares else None

    quarter_list = statements.quarters(reports)
    latest_figures = statements.latest(latest_report)
    eok = statements.EOK

    market_cap = None if issued is None else close * issued
    borrowings = latest_figures["borrowings"]
    cash = latest_figures["cash"]
    ev = _enterprise_value(market_cap, borrowings, cash)

    ttm_net_income_owners = statements.trailing(quarter_list, "net_income_owners")
    ttm_operating_income = statements.trailing(quarter_list, "operating_income")
    per_ttm = _ratio_if_positive(market_cap, ttm_net_income_owners)

    latest_fy = annual_years[-1] if annual_years else None
    oldest_fy = annual_years[0] if annual_years else None
    previous_fy = annual_years[-2] if len(annual_years) >= 2 else None

    def _working_capital(year: dict | None) -> float | None:
        if year is None:
            return None
        ca, cl = year.get("current_assets"), year.get("current_liabilities")
        return None if ca is None or cl is None else ca - cl

    wc_now, wc_prev = _working_capital(latest_fy), _working_capital(previous_fy)
    working_capital_increase = None if wc_now is None or wc_prev is None else wc_now - wc_prev

    # Everything from here on is reported in 억원 (like market_cap/ev above) except EPS, which stays in 원
    # per share — `_to_eok` only touches the money-valued inputs the next few metrics take.
    def _to_eok(value: float | None) -> float | None:
        return None if value is None else value / eok

    free_cash_flow_eok = _to_eok(latest_fy.get("free_cash_flow")) if latest_fy else None
    market_cap_eok = _to_eok(market_cap)
    fcf_yield_result = investor_metrics.fcf_yield(free_cash_flow_eok, market_cap_eok)

    owner_earnings_result = investor_metrics.owner_earnings(
        _to_eok(latest_fy.get("net_income_owners")) if latest_fy else None,
        _to_eok(latest_fy.get("depreciation")) if latest_fy else None,
        _to_eok(latest_fy.get("amortization")) if latest_fy else None,
        _to_eok(latest_fy.get("capex")) if latest_fy else None,
        _to_eok(working_capital_increase),
    )
    owner_earnings_yield_result = investor_metrics.owner_earnings_yield(owner_earnings_result["value"], market_cap_eok)

    ev_ebit_result = investor_metrics.ev_ebit(_to_eok(ev), _to_eok(ttm_operating_income))
    earnings_yield_result = investor_metrics.earnings_yield(_to_eok(ttm_operating_income), _to_eok(ev))

    shareholder_yield_result = investor_metrics.shareholder_yield(
        _to_eok(latest_fy.get("dividends_paid")) if latest_fy else None,
        _to_eok(latest_fy.get("treasury_shares_acquired")) if latest_fy else None,
        _to_eok(latest_fy.get("treasury_shares_disposed")) if latest_fy else None,
        _to_eok(latest_fy.get("proceeds_from_share_issuance")) if latest_fy else None,
        market_cap_eok,
        cash_flow_statement_present=bool(latest_fy) and latest_fy.get("operating_cash_flow") is not None,
    )

    # Altman Z's x1-x5 are all ratios (dimensionless), so market_cap and the year's raw 원 figures only
    # need to share one scale, not specifically 억원 — raw 원 (statements.annual()'s native unit) is fine.
    altman_z_result = quality.altman_z(latest_fy, market_cap) if latest_fy else quality.altman_z({}, market_cap)

    # DART 3년 EPS CAGR: 최신 사업보고서의 당기(latest_fy)·전전기(oldest_fy) 지배주주순이익을 그 사업연도
    # 말 보통주 발행주식수로 나눈다. 최신 연도는 위에서 받은 issued 를 그대로 쓰고, 2개년 전은 그 해의
    # 사업보고서(reprt_code 11011)를 따로 한 번 더 부른다.
    dart_eps_cagr_result: dict
    if oldest_fy is None or latest_fy is None or issued is None:
        dart_eps_cagr_result = investor_metrics.eps_cagr(None, None, None)
    else:
        try:
            oldest_share_rows = dart_handlers.dart_rows(
                dart.periodic_report_key_information.get_total_number_of_shares(
                    corp_code=corp_code, bsns_year=str(oldest_fy["year"]), reprt_code="11011"
                )
            )
        except Exception as exc:  # noqa: BLE001 - turned into a null + reason, not a hard failure
            oldest_share_rows = []
            oldest_shares_error = f"{type(exc).__name__}: {str(exc)[:200]}"
        else:
            oldest_shares_error = None
        dart_calls += 1
        oldest_shares = _common_shares(oldest_share_rows)
        oldest_issued = oldest_shares["issued"] if oldest_shares else None
        eps_oldest = (
            None
            if oldest_issued is None or oldest_fy.get("net_income_owners") is None
            else oldest_fy["net_income_owners"] / oldest_issued
        )
        eps_latest = None if latest_fy.get("net_income_owners") is None else latest_fy["net_income_owners"] / issued
        years = latest_fy["year"] - oldest_fy["year"]
        dart_eps_cagr_result = investor_metrics.eps_cagr(eps_oldest, eps_latest, years)
        if dart_eps_cagr_result["value"] is None and oldest_issued is None:
            reason = oldest_shares_error or "DART 보통주 발행주식수를 그 사업연도(bsns_year) 사업보고서에서 찾지 못함"
            dart_eps_cagr_result = {**dart_eps_cagr_result, "reason": reason}

    estimate = kis.domestic_stock_info.get_estimated_earnings(stock_code)
    periods = [row.get("dt") for row in _estimate_rows(extract_output(estimate, "output4"))]
    estimate_table = _estimate_table(extract_output(estimate, "output3"), _ESTIMATE_DETAIL_ROWS, periods)
    growth_row = next((row for row in estimate_table if row["metric"] == "eps_growth_yoy"), None)
    kis_estimate_period = next((period for period in periods if str(period).endswith("E")), None)
    kis_eps_growth_pct = (
        growth_row["values"].get(kis_estimate_period)
        if growth_row is not None and kis_estimate_period is not None
        else None
    )

    peg_dart = investor_metrics.peg(per_ttm, dart_eps_cagr_result["value"], "dart_3y_eps_cagr")
    peg_kis = investor_metrics.peg(per_ttm, kis_eps_growth_pct, f"kis_estimated_eps_growth_yoy({kis_estimate_period})")

    return {
        "stock_code": stock_code,
        "corp_code": corp_code,
        "as_of": as_of,
        "price": {"close": close, "date": last.timestamp[:8], "adjusted": False},
        "shares": {**shares, "report": f"{latest_report.year}-{latest_report.reprt_code}"} if shares else None,
        "statement_basis": basis,
        "unit": "억원",
        "market_cap": None if market_cap is None else market_cap / eok,
        "ev": None if ev is None else ev / eok,
        "ev_reason": _enterprise_value_reason(market_cap, borrowings, cash),
        "per_ttm": per_ttm,
        "fcf_yield": fcf_yield_result,
        "owner_earnings": owner_earnings_result,
        "owner_earnings_yield": owner_earnings_yield_result,
        "ev_ebit": ev_ebit_result,
        "earnings_yield": earnings_yield_result,
        "peg": {"dart_3y_eps_cagr": peg_dart, "kis_estimated_eps_growth": peg_kis},
        "shareholder_yield": shareholder_yield_result,
        "altman_z": altman_z_result,
        "calls": 1 + dart_calls + 1,
        "notes": list(_INVESTOR_METRICS_NOTES),
    }


_ALL_HANDLERS = [
    handle_kis_product_basic_info,
    handle_kis_stock_basic_info,
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
    handle_kis_implied_expectations,
    handle_kis_stock_valuation_band,
    handle_kis_investor_metrics,
    handle_kis_stock_loanable_list,
    handle_kis_investment_opinion,
    handle_kis_investment_opinion_by_brokerage,
]


def register_kis_stock_info_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
