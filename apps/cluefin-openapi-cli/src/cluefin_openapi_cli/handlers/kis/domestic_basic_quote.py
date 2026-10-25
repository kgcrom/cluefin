"""RPC handlers for KIS DomesticBasicQuote API (21 methods)."""

from __future__ import annotations

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from cluefin_openapi_cli import trend_setup
from cluefin_openapi_cli.cache.bars import fetch_index_bars
from cluefin_openapi_cli.errors import EXIT_BROKER, EXIT_USAGE, CliError
from cluefin_openapi_cli.handlers._base import DispatcherProtocol, extract_output, rpc_method
from cluefin_openapi_cli.indicators import MIN_CANDLES, analyze
from cluefin_openapi_cli.ohlcv import fetch_kis_daily_series

# ---------------------------------------------------------------------------
# Stock Current Price
# ---------------------------------------------------------------------------


def _delisted_on(kis, stock_code: str) -> str | None:
    """The delisting date from `basic-info` (KOSPI or KOSDAQ column), or None while listed."""
    info = kis.domestic_stock_info.get_stock_basic_info("300", stock_code)
    item = getattr(info.body, "output", None)
    for field in ("scts_mket_lstg_abol_dt", "kosdaq_mket_lstg_abol_dt"):
        value = str(getattr(item, field, "") or "").strip()
        if value and value != "00000000":
            return value
    return None


def _raise_if_delisted(kis, stock_code: str, cause: Exception) -> None:
    """A sparse current-price body is what KIS sends for a delisted code (117930, 2026-10-18). Say so."""
    delisted_on = _delisted_on(kis, stock_code)
    if delisted_on is None:
        return
    raise CliError(
        f"{stock_code} was delisted on {delisted_on}; it has no current price.",
        exit_code=EXIT_BROKER,
        error_type="Delisted",
        data={"stock_code": stock_code, "delisted_on": delisted_on},
        hint="Price history up to the delisting is still available from kis chart period; "
        "listing dates are in kis stock basic-info.",
    ) from cause


@rpc_method(
    name="stock.current_price",
    description="Get current stock price from KIS. Returns price, volume, market cap, PER, PBR.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_current_price(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    try:
        response = kis.domestic_basic_quote.get_stock_current_price(market, params["stock_code"])
    except Exception as exc:  # noqa: BLE001 - only a response-model failure is inspected; anything else re-raises
        if type(exc).__name__.endswith("ValidationError"):
            _raise_if_delisted(kis, params["stock_code"], exc)
        raise
    item = response.body.output
    if item is None:
        return {"stock_code": params["stock_code"], "error": "No data returned"}
    return {
        "stock_code": params["stock_code"],
        "current_price": int(item.stck_prpr),
        "change_rate": float(item.prdy_ctrt),
        "change_amount": int(item.prdy_vrss),
        "change_sign": item.prdy_vrss_sign,
        "volume": int(item.acml_vol),
        "trade_amount": int(item.acml_tr_pbmn),
        "open_price": int(item.stck_oprc),
        "high_price": int(item.stck_hgpr),
        "low_price": int(item.stck_lwpr),
        "upper_limit": int(item.stck_mxpr),
        "lower_limit": int(item.stck_llam),
        "base_price": int(item.stck_sdpr),
        "market_cap": int(item.hts_avls),
        "per": float(item.per) if item.per else None,
        "pbr": float(item.pbr) if item.pbr else None,
        "eps": float(item.eps) if item.eps else None,
        "bps": float(item.bps) if item.bps else None,
        "w52_high": int(item.w52_hgpr),
        "w52_low": int(item.w52_lwpr),
        "foreign_ratio": float(item.hts_frgn_ehrt),
        "foreign_net_buy": int(item.frgn_ntby_qty),
        "sector_name": item.bstp_kor_isnm,
    }


# ---------------------------------------------------------------------------
# Stock Current Price 2
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.current_price_extended",
    description="Get extended current stock price from KIS (includes warning flags, credit info, VI status).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_current_price_2(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price_2(market, params["stock_code"])
    result = extract_output(response, "output")
    if result is None:
        return {"stock_code": params["stock_code"], "error": "No data returned"}
    return {"stock_code": params["stock_code"], **result}


# ---------------------------------------------------------------------------
# Stock Conclusion (Trades)
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.conclusion",
    description="Get recent stock trade conclusions (tick-level execution data).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_conclusion(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price_conclusion(market, params["stock_code"])
    return {"stock_code": params["stock_code"], "data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# Stock Daily Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="chart.daily",
    description="Get daily stock price history from KIS.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code. Default J.",
            },
            "period": {
                "type": "string",
                "enum": ["D", "W", "M"],
                "description": "Period (D:daily, W:weekly, M:monthly). Default D.",
            },
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Adjusted price (0:unadjusted, 1:adjusted). Default 1.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="chart",
    broker="kis",
)
def handle_kis_stock_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    period = params.get("period", "D")
    adj = params.get("adj_price", "1")
    response = kis.domestic_basic_quote.get_stock_current_price_daily(market, params["stock_code"], period, adj)
    items = response.body.output or []
    return {
        "stock_code": params["stock_code"],
        "data": [
            {
                "date": item.stck_bsop_date,
                "open": int(item.stck_oprc),
                "high": int(item.stck_hgpr),
                "low": int(item.stck_lwpr),
                "close": int(item.stck_clpr),
                "volume": int(item.acml_vol),
                "change_rate": float(item.prdy_ctrt),
                "foreign_ratio": float(item.hts_frgn_ehrt),
            }
            for item in items
        ],
    }


# ---------------------------------------------------------------------------
# Stock Asking Price / Expected Conclusion
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.order_book",
    description="Get order book (bid/ask prices) and expected conclusion data for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_asking_expected(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price_asking_expected_conclusion(market, params["stock_code"])
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# Stock Period Quote
# ---------------------------------------------------------------------------


@rpc_method(
    name="chart.period",
    description="Get stock price for a specific date range (daily/weekly/monthly/yearly candles).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "period": {
                "type": "string",
                "enum": ["D", "W", "M", "Y"],
                "description": "Period (D:daily, W:weekly, M:monthly, Y:yearly). Default D.",
            },
            "adj_price": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Price adjustment (0:adjusted, 1:original). Default 0.",
            },
        },
        "required": ["stock_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="chart",
    broker="kis",
)
def handle_kis_stock_period_quote(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    period = params.get("period", "D")
    adj = params.get("adj_price", "0")
    response = kis.domestic_basic_quote.get_stock_period_quote(
        market, params["stock_code"], params["start_date"], params["end_date"], period, adj
    )
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# Stock Today Minute Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="chart.minute",
    description="Get intraday minute-level chart data for a stock (today only).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
            "hour": {"type": "string", "description": "Query start time (HHMMSS)"},
            "include_volume": {
                "type": "string",
                "enum": ["N", "Y"],
                "description": "Include volume data (N/Y). Default N.",
            },
            "etc_cls_code": {"type": "string", "description": "Additional classification code. Default empty."},
        },
        "required": ["stock_code", "hour"],
    },
    returns={"type": "object"},
    category="chart",
    broker="kis",
)
def handle_kis_stock_today_minute(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    include_volume = params.get("include_volume", "N")
    etc_cls_code = params.get("etc_cls_code", "")
    response = kis.domestic_basic_quote.get_stock_today_minute_chart(
        market, params["stock_code"], params["hour"], include_volume, etc_cls_code
    )
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# Stock Daily Minute Chart
# ---------------------------------------------------------------------------


@rpc_method(
    name="chart.daily_minute",
    description="Get minute-level chart data for a stock across multiple days.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
            "hour": {"type": "string", "description": "Query start time (HHMMSS)"},
            "date": {"type": "string", "description": "Query start date (YYYYMMDD)"},
            "include_history": {
                "type": "string",
                "enum": ["N", "Y"],
                "description": "Include historical data (N/Y). Default N.",
            },
            "include_fake_tick": {
                "type": "string",
                "enum": ["", "N", "Y"],
                "description": "Include fake tick data (empty/N/Y). Default empty.",
            },
        },
        "required": ["stock_code", "hour", "date"],
    },
    returns={"type": "object"},
    category="chart",
    broker="kis",
)
def handle_kis_stock_daily_minute(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    include_history = params.get("include_history", "N")
    include_fake_tick = params.get("include_fake_tick", "")
    response = kis.domestic_basic_quote.get_stock_daily_minute_chart(
        market, params["stock_code"], params["hour"], params["date"], include_history, include_fake_tick
    )
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# Stock Time Conclusion (Intraday Trades by Time)
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.time_conclusion",
    description="Get intraday trade conclusions grouped by time for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
            "hour": {"type": "string", "description": "Query start time (HHMMSS)"},
        },
        "required": ["stock_code", "hour"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_time_conclusion(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price_time_item_conclusion(
        market, params["stock_code"], params["hour"]
    )
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# Stock Overtime Daily Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.overtime_daily",
    description="Get after-hours daily price history for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_overtime_daily_price(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price_daily_overtime_price(market, params["stock_code"])
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# Stock Overtime Conclusion
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.overtime_conclusion",
    description="Get after-hours trade conclusions for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_overtime_conclusion(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price_overtime_conclusion(market, params["stock_code"])
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# Stock Overtime Asking Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.overtime_order_book",
    description="Get after-hours order book (bid/ask prices) for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_overtime_asking_price(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_stock_overtime_asking_price(params["stock_code"])
    result = extract_output(response, "output")
    if result is None:
        return {"stock_code": params["stock_code"], "error": "No data returned"}
    return {"stock_code": params["stock_code"], **result}


# ---------------------------------------------------------------------------
# Stock Closing Expected Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="stock.closing_expected",
    description="Get expected closing prices at market close (ranked list of stocks).",
    parameters={
        "type": "object",
        "properties": {
            "sort_code": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4"],
                "description": (
                    "Rank sort code: 0=all, 1=upper-limit expected, 2=lower-limit expected, "
                    "3=top gainers vs previous, 4=top losers vs previous."
                ),
            },
            "sector_code": {
                "type": "string",
                "enum": ["0000", "0001", "1001", "2001", "4001"],
                "description": "Sector: 0000=all, 0001=KRX, 1001=KOSDAQ, 2001=KOSPI200, 4001=KRX100.",
            },
            "classification": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Classification: 0=all, 1=closing-range extension only.",
            },
        },
        "required": ["sort_code", "sector_code", "classification"],
    },
    returns={"type": "object"},
    category="stock",
    broker="kis",
)
def handle_kis_stock_closing_expected_price(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_stock_closing_expected_price(
        params["sort_code"], params["sector_code"], params["classification"]
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# ETF/ETN Current Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="etf.current_price",
    description="Get current price and NAV data for an ETF or ETN.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF/ETN 6-digit code", "pattern": "^[0-9]{6}$"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="etf",
    broker="kis",
)
def handle_kis_etf_etn_current_price(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_etfetn_current_price(params["stock_code"])
    result = extract_output(response, "output")
    if result is None:
        return {"stock_code": params["stock_code"], "error": "No data returned"}
    return {"stock_code": params["stock_code"], **result}


# ---------------------------------------------------------------------------
# ETF Component Stock Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="etf.component_stocks",
    description="Get component stock prices and weights for an ETF.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF 6-digit code", "pattern": "^[0-9]{6}$"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="etf",
    broker="kis",
)
def handle_kis_etf_component_stock_price(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_etf_component_stock_price(params["stock_code"])
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# ETF NAV Comparison Trend (by Stock)
# ---------------------------------------------------------------------------


@rpc_method(
    name="etf.nav_trend",
    description="Get ETF NAV comparison trend data (price vs NAV for a single ETF).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF 6-digit code", "pattern": "^[0-9]{6}$"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="etf",
    broker="kis",
)
def handle_kis_etf_nav_comparison_trend(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_etf_nav_comparison_trend(params["stock_code"])
    return {
        "stock_code": params["stock_code"],
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# ETF NAV Comparison Daily Trend
# ---------------------------------------------------------------------------


@rpc_method(
    name="etf.daily",
    description="Get daily ETF NAV comparison trend for a date range.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF 6-digit code", "pattern": "^[0-9]{6}$"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
        },
        "required": ["stock_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="etf",
    broker="kis",
)
def handle_kis_etf_nav_comparison_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_etf_nav_comparison_daily_trend(
        params["stock_code"], params["start_date"], params["end_date"]
    )
    return {"stock_code": params["stock_code"], "data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# Technical Analysis
# ---------------------------------------------------------------------------

_TECHNICAL_DEFAULT_COUNT = 120
_TECHNICAL_MAX_COUNT = 600


@rpc_method(
    name="chart.technical",
    description=(
        "Compute technical indicators and signal readings for a stock from daily OHLCV. "
        "Returns final indicator values and rule votes only, not the candle series."
    ),
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
            "count": {
                "type": "integer",
                "minimum": MIN_CANDLES,
                "maximum": _TECHNICAL_MAX_COUNT,
                "description": (
                    f"Daily candles to analyze. Default {_TECHNICAL_DEFAULT_COUNT}, minimum {MIN_CANDLES} "
                    "(the SMA(60) warm-up). More candles cost more broker calls, not more output."
                ),
            },
            "end_date": {
                "type": "string",
                "description": "Analyze as of this date (YYYYMMDD). Default today.",
                "pattern": "^[0-9]{8}$",
            },
            "adjusted": {
                "type": "boolean",
                "description": "Use adjusted prices (default true). False returns original prices.",
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="chart",
    broker="kis",
)
def handle_kis_chart_technical(params: dict, session) -> dict:
    """Fetch daily candles and return indicator readings rather than the candles.

    This is the one command in the registry that computes instead of passing a client
    response through. That is the entire point: a caller asking "what is RSI doing"
    otherwise has to pull several hundred OHLCV rows through its own context to find
    out. Everything here beyond the fetch lives in `ohlcv` and `indicators`.
    """

    kis = session.get_kis()
    count = int(params.get("count", _TECHNICAL_DEFAULT_COUNT))
    series = fetch_kis_daily_series(
        kis,
        params["stock_code"],
        count=count,
        market=params.get("market", "J"),
        end_date=params.get("end_date"),
        adjusted=params.get("adjusted", True),
    )

    if len(series) < MIN_CANDLES:
        raise CliError(
            f"Only {len(series)} daily candles available for {params['stock_code']}; "
            f"indicators need at least {MIN_CANDLES}.",
            exit_code=EXIT_BROKER,
            error_type="InsufficientHistory",
            data={"stock_code": params["stock_code"], "candles": len(series), "required": MIN_CANDLES},
            hint=(
                "The code may be newly listed, suspended, or wrong. Check `kis stock basic-info`, "
                "or widen the window with an earlier --end-date."
            ),
        )

    return analyze(series)


# ---------------------------------------------------------------------------
# Trend setup
# ---------------------------------------------------------------------------

# 260 bars leave room above trend_setup.MIN_CANDLES (251); one more covers a dropped intraday bar.
_TREND_CANDLES = 260
# Calendar days of index history to cover 251 index closes (~245 sessions a year).
_INDEX_LOOKBACK_DAYS = 420
# KRX closes at 15:30; before 15:40 today's bar is still moving.
_SESSION_FINAL = time(15, 40)
_KST = ZoneInfo("Asia/Seoul")
_BENCHMARKS = {"STK": ("0001", "KOSPI"), "KSQ": ("1001", "KOSDAQ")}
_BENCHMARK_MARKETS = {code: market for code, market in _BENCHMARKS.values()}


def _now() -> datetime:
    """KST wall clock; tests replace this function."""

    return datetime.now(_KST).replace(tzinfo=None)


def _resolve_benchmark(kis, stock_code: str, caveats: list[str]) -> str:
    """0001 for a KOSPI stock, 1001 for KOSDAQ, from `basic-info` (one call)."""

    output = getattr(kis.domestic_stock_info.get_stock_basic_info("300", stock_code).body, "output", None)
    if output is None:
        raise CliError(
            f"basic-info returned no body for {stock_code}.",
            exit_code=EXIT_BROKER,
            error_type="ResponseParseError",
            hint="Check the stock code with `kis stock basic-info`.",
        )
    market = str(getattr(output, "mket_id_cd", "") or "").strip()
    if market not in _BENCHMARKS:
        raise CliError(
            f"{stock_code} trades on `{market or 'unknown'}`, not KOSPI (STK) or KOSDAQ (KSQ).",
            exit_code=EXIT_USAGE,
            error_type="ValidationError",
            data={"stock_code": stock_code, "mket_id_cd": market},
            hint="Pass --benchmark 0001 (KOSPI) or 1001 (KOSDAQ).",
        )
    group = str(getattr(output, "scty_grp_id_cd", "") or "").strip()
    if group != "ST":
        caveats.append(f"보통주가 아니다(scty_grp_id_cd={group}) — 백테스트 유니버스는 보통주만이었다.")
    return _BENCHMARKS[market][0]


def _insufficient(stock_code: str, exc: trend_setup.InsufficientHistory) -> CliError:
    return CliError(
        f"Only {exc.count} daily bars for the {exc.which} of {stock_code}; trend-setup needs {trend_setup.MIN_CANDLES}.",
        exit_code=EXIT_BROKER,
        error_type="InsufficientHistory",
        data={"stock_code": stock_code, "series": exc.which, "candles": exc.count, "required": trend_setup.MIN_CANDLES},
        hint=(
            "A listing younger than ~260 sessions is outside the backtest. Check `kis stock basic-info`, "
            "or the code may be suspended or wrong."
        ),
    )


@rpc_method(
    name="chart.trend_setup",
    description=(
        "Trend-following breakout setup for one stock from about 260 adjusted daily bars and its market index: "
        "Minervini trend template with moving average stack, 52-week high gap, fractal pivot and base "
        "contraction (VCP), relative strength vs. KOSPI/KOSDAQ, watchlist setup group 1/2/3, and pivot "
        "alert/stop levels. Returns the readings and one alert/watch/exclude action, not the candles."
    ),
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
            "market": {
                "type": "string",
                "enum": ["J", "NX", "UN"],
                "description": "Market code (J:KRX, NX:NXT, UN:Combined). Default J.",
            },
            "benchmark": {
                "type": "string",
                "enum": ["auto", "0001", "1001"],
                "description": (
                    "Index for relative strength: 0001 KOSPI, 1001 KOSDAQ (not KOSPI200). "
                    "Default auto: from basic-info (one more call)."
                ),
            },
            "end_date": {
                "type": "string",
                "description": "Judge as of this date (YYYYMMDD), to replay a past day. Default today.",
                "pattern": "^[0-9]{8}$",
            },
            "include_today": {
                "type": "boolean",
                "description": (
                    "Keep today's unfinished bar before 15:40 KST (default false: judge on the last closed day, "
                    "as the backtest did)."
                ),
            },
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="chart",
    broker="kis",
)
def handle_kis_chart_trend_setup(params: dict, session) -> dict:
    """Fetch ~260 adjusted bars and the index, return the setup reading rather than the candles.

    The rules are the backtest's (`trend_setup.py`); this handler only does I/O, the
    intraday-bar decision and error mapping. About 10 calls: basic-info (auto benchmark),
    ~3 stock windows and ~6 index windows (50 rows each).
    """

    kis = session.get_kis()
    stock_code = params["stock_code"]
    caveats: list[str] = []
    if not stock_code.endswith("0"):
        caveats.append("우선주로 보인다(코드 끝자리 0 아님) — 백테스트 유니버스는 보통주만이었다.")
    benchmark = params.get("benchmark", "auto")
    if benchmark == "auto":
        benchmark = _resolve_benchmark(kis, stock_code, caveats)

    end_date = params.get("end_date")
    series = fetch_kis_daily_series(
        kis, stock_code, count=_TREND_CANDLES + 1, market=params.get("market", "J"), end_date=end_date, adjusted=True
    )
    prices = trend_setup.PriceArrays.from_series(series)
    dropped = None
    now = _now()
    intraday = (
        not end_date and len(prices) > 0 and prices.dates[-1] == now.strftime("%Y%m%d") and now.time() < _SESSION_FINAL
    )
    if intraday and params.get("include_today", False):
        caveats.append("장중 미완성 캔들 포함 — 백테스트 조건(마지막 완료 거래일)과 다르다.")
    elif intraday:
        dropped = prices.dates[-1]
        prices = prices.window(stop=-1)
    prices = prices.window(start=-_TREND_CANDLES)
    if len(prices) < trend_setup.MIN_CANDLES:
        raise _insufficient(stock_code, trend_setup.InsufficientHistory("stock", len(prices)))

    as_of = datetime.strptime(prices.dates[-1], "%Y%m%d").date()
    bars = fetch_index_bars(kis, benchmark, as_of - timedelta(days=_INDEX_LOOKBACK_DAYS), as_of)
    index = trend_setup.IndexCloses.from_pairs((bar.date, bar.close) for bar in bars)
    try:
        reading = trend_setup.analyze(prices, index)
    except trend_setup.InsufficientHistory as exc:
        raise _insufficient(stock_code, exc) from exc
    except trend_setup.IndexDateMismatch as exc:
        raise CliError(
            f"Index {benchmark} has no close on {exc.as_of}, the stock's last bar.",
            exit_code=EXIT_BROKER,
            error_type="IndexDateMismatch",
            data={"stock_code": stock_code, "benchmark": benchmark, "as_of": exc.as_of},
            hint="Pass an earlier --end-date, or leave include_today false during the session.",
        ) from exc
    return {
        "stock_code": stock_code,
        "benchmark": benchmark,
        "market": _BENCHMARK_MARKETS[benchmark],
        "as_of": reading.pop("as_of"),
        "dropped_intraday_candle": dropped,
        "adjusted": True,
        **reading,
        "caveats": [*reading["caveats"], *caveats],
    }


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kis_stock_current_price,
    handle_kis_stock_current_price_2,
    handle_kis_stock_conclusion,
    handle_kis_stock_daily,
    handle_kis_stock_asking_expected,
    handle_kis_stock_period_quote,
    handle_kis_stock_today_minute,
    handle_kis_stock_daily_minute,
    handle_kis_stock_time_conclusion,
    handle_kis_stock_overtime_daily_price,
    handle_kis_stock_overtime_conclusion,
    handle_kis_stock_overtime_asking_price,
    handle_kis_stock_closing_expected_price,
    handle_kis_etf_etn_current_price,
    handle_kis_etf_component_stock_price,
    handle_kis_etf_nav_comparison_trend,
    handle_kis_etf_nav_comparison_daily,
    handle_kis_chart_technical,
    handle_kis_chart_trend_setup,
]


def register_kis_basic_quote_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
