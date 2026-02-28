"""RPC handlers for KIS DomesticBasicQuote API (21 methods)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_output, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# Stock Current Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.basic_quote.stock_current_price",
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
    category="kis.basic_quote",
    broker="kis",
)
def handle_kis_stock_current_price(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price(market, params["stock_code"])
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
    name="kis.basic_quote.stock_current_price_2",
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
    category="kis.basic_quote",
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
    name="kis.basic_quote.stock_conclusion",
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
    category="kis.basic_quote",
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
    name="kis.basic_quote.stock_daily",
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
    category="kis.basic_quote",
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
    name="kis.basic_quote.stock_asking_expected",
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
    category="kis.basic_quote",
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
# Stock Investor
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.basic_quote.stock_investor",
    description="Get investor trading data (individual, foreign, institutional) for a stock.",
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
    category="kis.basic_quote",
    broker="kis",
)
def handle_kis_stock_investor(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price_investor(market, params["stock_code"])
    return {"stock_code": params["stock_code"], "data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# Stock Member (Brokerage Firm Trading)
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.basic_quote.stock_member",
    description="Get top brokerage firm (member) trading data for a stock.",
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
    category="kis.basic_quote",
    broker="kis",
)
def handle_kis_stock_member(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_current_price_member(market, params["stock_code"])
    return {"stock_code": params["stock_code"], "data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# Stock Period Quote
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.basic_quote.stock_period_quote",
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
    category="kis.basic_quote",
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
    name="kis.basic_quote.stock_today_minute",
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
    category="kis.basic_quote",
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
    name="kis.basic_quote.stock_daily_minute",
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
    category="kis.basic_quote",
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
    name="kis.basic_quote.stock_time_conclusion",
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
    category="kis.basic_quote",
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
    name="kis.basic_quote.stock_overtime_daily_price",
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
    category="kis.basic_quote",
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
    name="kis.basic_quote.stock_overtime_conclusion",
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
    category="kis.basic_quote",
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
# Stock Overtime Current Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.basic_quote.stock_overtime_current_price",
    description="Get after-hours current price for a stock.",
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
    category="kis.basic_quote",
    broker="kis",
)
def handle_kis_stock_overtime_current_price(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "J")
    response = kis.domestic_basic_quote.get_stock_overtime_current_price(market, params["stock_code"])
    result = extract_output(response, "output")
    if result is None:
        return {"stock_code": params["stock_code"], "error": "No data returned"}
    return {"stock_code": params["stock_code"], **result}


# ---------------------------------------------------------------------------
# Stock Overtime Asking Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.basic_quote.stock_overtime_asking_price",
    description="Get after-hours order book (bid/ask prices) for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "6-digit stock code", "pattern": "^[0-9]{6}$"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.basic_quote",
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
    name="kis.basic_quote.stock_closing_expected_price",
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
    category="kis.basic_quote",
    broker="kis",
)
def handle_kis_stock_closing_expected_price(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_stock_closing_expected_price(
        params["sort_code"], params["sector_code"], params["classification"]
    )
    return {"data": extract_output(response, "output1")}


# ---------------------------------------------------------------------------
# ETF/ETN Current Price
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.basic_quote.etf_etn_current_price",
    description="Get current price and NAV data for an ETF or ETN.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF/ETN 6-digit code", "pattern": "^[0-9]{6}$"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.basic_quote",
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
    name="kis.basic_quote.etf_component_stock_price",
    description="Get component stock prices and weights for an ETF.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF 6-digit code", "pattern": "^[0-9]{6}$"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.basic_quote",
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
    name="kis.basic_quote.etf_nav_comparison_trend",
    description="Get ETF NAV comparison trend data (price vs NAV for a single ETF).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF 6-digit code", "pattern": "^[0-9]{6}$"},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="kis.basic_quote",
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
    name="kis.basic_quote.etf_nav_comparison_daily",
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
    category="kis.basic_quote",
    broker="kis",
)
def handle_kis_etf_nav_comparison_daily(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_etf_nav_comparison_daily_trend(
        params["stock_code"], params["start_date"], params["end_date"]
    )
    return {"stock_code": params["stock_code"], "data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# ETF NAV Comparison Time Trend (Minute)
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.basic_quote.etf_nav_comparison_time",
    description="Get minute-level ETF NAV comparison trend (1min=60, 3min=180, etc.).",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "ETF 6-digit code", "pattern": "^[0-9]{6}$"},
            "hour_cls_code": {
                "type": "string",
                "description": "Time interval in seconds (60=1min, 180=3min, 300=5min, etc.).",
            },
        },
        "required": ["stock_code", "hour_cls_code"],
    },
    returns={"type": "object"},
    category="kis.basic_quote",
    broker="kis",
)
def handle_kis_etf_nav_comparison_time(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_etf_nav_comparison_time_trend(params["hour_cls_code"], params["stock_code"])
    return {"stock_code": params["stock_code"], "data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kis_stock_current_price,
    handle_kis_stock_current_price_2,
    handle_kis_stock_conclusion,
    handle_kis_stock_daily,
    handle_kis_stock_asking_expected,
    handle_kis_stock_investor,
    handle_kis_stock_member,
    handle_kis_stock_period_quote,
    handle_kis_stock_today_minute,
    handle_kis_stock_daily_minute,
    handle_kis_stock_time_conclusion,
    handle_kis_stock_overtime_daily_price,
    handle_kis_stock_overtime_conclusion,
    handle_kis_stock_overtime_current_price,
    handle_kis_stock_overtime_asking_price,
    handle_kis_stock_closing_expected_price,
    handle_kis_etf_etn_current_price,
    handle_kis_etf_component_stock_price,
    handle_kis_etf_nav_comparison_trend,
    handle_kis_etf_nav_comparison_daily,
    handle_kis_etf_nav_comparison_time,
]


def register_kis_basic_quote_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
