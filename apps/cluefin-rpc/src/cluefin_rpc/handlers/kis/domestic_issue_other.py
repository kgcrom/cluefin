from __future__ import annotations

from typing import TYPE_CHECKING

from cluefin_rpc.handlers._base import extract_output, rpc_method

if TYPE_CHECKING:
    from cluefin_rpc.dispatcher import Dispatcher


# ---------------------------------------------------------------------------
# kis.issue_other.sector_current_index
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.sector_current_index",
    description="Get current sector index price.",
    parameters={
        "type": "object",
        "properties": {
            "market": {
                "type": "string",
                "description": "Market division code (U for sector). Default U.",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (0001:KOSPI, 1001:KOSDAQ, 2001:KOSPI200)",
            },
        },
        "required": ["sector_code"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_sector_current_index(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "U")
    response = kis.domestic_issue_other.get_sector_current_index(market, params["sector_code"])
    result = extract_output(response, "output")
    if result is None:
        return {"error": "No data returned"}
    return {**result}


# ---------------------------------------------------------------------------
# kis.issue_other.sector_daily_index
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.sector_daily_index",
    description="Get sector daily index history.",
    parameters={
        "type": "object",
        "properties": {
            "period": {
                "type": "string",
                "enum": ["D", "W", "M"],
                "description": "Period (D:daily, W:weekly, M:monthly). Default D.",
            },
            "market": {
                "type": "string",
                "description": "Market division code (U for sector). Default U.",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (0001:KOSPI, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
        },
        "required": ["sector_code", "start_date"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_sector_daily_index(params: dict, session) -> dict:
    kis = session.get_kis()
    period = params.get("period", "D")
    market = params.get("market", "U")
    response = kis.domestic_issue_other.get_sector_daily_index(
        period, market, params["sector_code"], params["start_date"]
    )
    return {
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# kis.issue_other.sector_time_index_second
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.sector_time_index_second",
    description="Get sector time index by second.",
    parameters={
        "type": "object",
        "properties": {
            "sector_code": {
                "type": "string",
                "description": "Sector code (0001:KRX, 1001:KOSDAQ, 2001:KOSPI200, 3003:KSQ150)",
            },
            "market": {
                "type": "string",
                "description": "Market division code (U for sector). Default U.",
            },
        },
        "required": ["sector_code"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_sector_time_index_second(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "U")
    response = kis.domestic_issue_other.get_sector_time_index_second(params["sector_code"], market)
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.issue_other.sector_time_index_minute
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.sector_time_index_minute",
    description="Get sector time index by minute.",
    parameters={
        "type": "object",
        "properties": {
            "hour": {
                "type": "string",
                "description": "Time interval in seconds (60:1min, 300:5min, 600:10min)",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (0001:KRX, 1001:KOSDAQ, 2001:KOSPI200, 3003:KSQ150)",
            },
            "market": {
                "type": "string",
                "description": "Market division code (U for sector). Default U.",
            },
        },
        "required": ["hour", "sector_code"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_sector_time_index_minute(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "U")
    response = kis.domestic_issue_other.get_sector_time_index_minute(params["hour"], params["sector_code"], market)
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.issue_other.sector_minute_inquiry
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.sector_minute_inquiry",
    description="Get sector minute chart data.",
    parameters={
        "type": "object",
        "properties": {
            "market": {
                "type": "string",
                "description": "Market division code (U for sector). Default U.",
            },
            "etc_cls_code": {
                "type": "string",
                "description": "Extra classification (0:default, 1:exclude after-hours). Default 0.",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (0001:all, 0002:large-cap)",
            },
            "hour": {
                "type": "string",
                "description": "Time interval (30, 60:1min, 600:10min, 3600:1hour)",
            },
            "pw_data_incu_yn": {
                "type": "string",
                "enum": ["Y", "N"],
                "description": "Include past data (Y:past, N:today only). Default N.",
            },
        },
        "required": ["sector_code", "hour"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_sector_minute_inquiry(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "U")
    etc_cls_code = params.get("etc_cls_code", "0")
    pw_data_incu_yn = params.get("pw_data_incu_yn", "N")
    response = kis.domestic_issue_other.get_sector_minute_inquiry(
        market, etc_cls_code, params["sector_code"], params["hour"], pw_data_incu_yn
    )
    return {
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# kis.issue_other.sector_period_quote
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.sector_period_quote",
    description="Get sector period quote (daily/weekly/monthly/yearly).",
    parameters={
        "type": "object",
        "properties": {
            "market": {
                "type": "string",
                "description": "Market division code (U for sector). Default U.",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (0001:all, 0002:large-cap)",
            },
            "start_date": {
                "type": "string",
                "description": "Start date (YYYYMMDD)",
            },
            "end_date": {
                "type": "string",
                "description": "End date (YYYYMMDD)",
            },
            "period": {
                "type": "string",
                "enum": ["D", "W", "M", "Y"],
                "description": "Period (D:daily, W:weekly, M:monthly, Y:yearly). Default D.",
            },
        },
        "required": ["sector_code", "start_date", "end_date"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_sector_period_quote(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "U")
    period = params.get("period", "D")
    response = kis.domestic_issue_other.get_sector_period_quote(
        market, params["sector_code"], params["start_date"], params["end_date"], period
    )
    return {
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# kis.issue_other.sector_all_quote_by_category
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.sector_all_quote_by_category",
    description="Get all sector quotes by category.",
    parameters={
        "type": "object",
        "properties": {
            "market": {
                "type": "string",
                "description": "Market division code (U for sector). Default U.",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (0001:KOSPI, 1001:KOSDAQ, 2001:KOSPI200)",
            },
            "cond_scr_div_code": {
                "type": "string",
                "description": "Screen division code (unique key: 20214). Default 20214.",
            },
            "mrkt_cls_code": {
                "type": "string",
                "description": "Market class code (K:KRX, Q:KOSDAQ, K2:KOSPI200)",
            },
            "blng_cls_code": {
                "type": "string",
                "description": "Category code (0:all sectors, 1:other, 2:capital/venture, 3:industry/general). Default 0.",
            },
        },
        "required": ["sector_code", "mrkt_cls_code"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_sector_all_quote_by_category(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "U")
    cond_scr_div_code = params.get("cond_scr_div_code", "20214")
    blng_cls_code = params.get("blng_cls_code", "0")
    response = kis.domestic_issue_other.get_sector_all_quote_by_category(
        market, params["sector_code"], cond_scr_div_code, params["mrkt_cls_code"], blng_cls_code
    )
    return {
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# kis.issue_other.expected_index_trend
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.expected_index_trend",
    description="Get expected settlement index trend.",
    parameters={
        "type": "object",
        "properties": {
            "mkop_cls_code": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Market operation code (1:pre-market, 2:post-market)",
            },
            "hour": {
                "type": "string",
                "description": "Time interval (10:10s, 30:30s, 60:1min, 600:10min)",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KOSPI, 1001:KOSDAQ, 2001:KOSPI200, 4001:KRX100)",
            },
            "market": {
                "type": "string",
                "description": "Market division code (U for sector). Default U.",
            },
        },
        "required": ["mkop_cls_code", "hour", "sector_code"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_expected_index_trend(params: dict, session) -> dict:
    kis = session.get_kis()
    market = params.get("market", "U")
    response = kis.domestic_issue_other.get_expected_index_trend(
        params["mkop_cls_code"], params["hour"], params["sector_code"], market
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.issue_other.expected_index_all
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.expected_index_all",
    description="Get all expected settlement indices.",
    parameters={
        "type": "object",
        "properties": {
            "mrkt_cls_code": {
                "type": "string",
                "description": "Market class code (0:all, K:KRX, Q:KOSDAQ). Default 0.",
            },
            "market": {
                "type": "string",
                "description": "Market division code (U for sector). Default U.",
            },
            "cond_scr_div_code": {
                "type": "string",
                "description": "Screen division code (unique key: 11175). Default 11175.",
            },
            "sector_code": {
                "type": "string",
                "description": "Sector code (0000:all, 0001:KRX, 1001:KOSDAQ, 2001:KOSPI200, 4001:KRX100)",
            },
            "mkop_cls_code": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Market operation code (1:pre-market, 2:post-market)",
            },
        },
        "required": ["sector_code", "mkop_cls_code"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_expected_index_all(params: dict, session) -> dict:
    kis = session.get_kis()
    mrkt_cls_code = params.get("mrkt_cls_code", "0")
    market = params.get("market", "U")
    cond_scr_div_code = params.get("cond_scr_div_code", "11175")
    response = kis.domestic_issue_other.get_expected_index_all(
        mrkt_cls_code, market, cond_scr_div_code, params["sector_code"], params["mkop_cls_code"]
    )
    return {
        "summary": extract_output(response, "output1"),
        "data": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# kis.issue_other.volatility_interruption_status
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.volatility_interruption_status",
    description="Get VI (Volatility Interruption) status.",
    parameters={
        "type": "object",
        "properties": {
            "div_cls_code": {
                "type": "string",
                "enum": ["0", "1", "2"],
                "description": "Direction (0:all, 1:up, 2:down). Default 0.",
            },
            "cond_scr_div_code": {
                "type": "string",
                "description": "Screen division code (unique key: 20139). Default 20139.",
            },
            "mrkt_cls_code": {
                "type": "string",
                "description": "Market class code (0:all, K:KRX, Q:KOSDAQ). Default 0.",
            },
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all)",
            },
            "rank_sort_cls_code": {
                "type": "string",
                "description": "Sort code (0:all, 1:static, 2:dynamic, 3:static&dynamic). Default 0.",
            },
            "start_date": {
                "type": "string",
                "description": "Business date (YYYYMMDD)",
            },
            "trgt_cls_code": {
                "type": "string",
                "description": "Target classification code. Default empty.",
            },
            "trgt_exls_cls_code": {
                "type": "string",
                "description": "Target exclusion code. Default empty.",
            },
        },
        "required": ["start_date"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_volatility_interruption_status(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_issue_other.get_volatility_interruption_status(
        params.get("div_cls_code", "0"),
        params.get("cond_scr_div_code", "20139"),
        params.get("mrkt_cls_code", "0"),
        params.get("stock_code", ""),
        params.get("rank_sort_cls_code", "0"),
        params["start_date"],
        params.get("trgt_cls_code", ""),
        params.get("trgt_exls_cls_code", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.issue_other.interest_rate_summary
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.interest_rate_summary",
    description="Get interest rate summary (domestic bonds/rates).",
    parameters={
        "type": "object",
        "properties": {
            "market": {
                "type": "string",
                "description": "Market division code (unique key: I). Default I.",
            },
            "cond_scr_div_code": {
                "type": "string",
                "description": "Screen division code (unique key: 20702). Default 20702.",
            },
            "div_cls_code": {
                "type": "string",
                "description": "Classification code (1:foreign interest rate indicators). Default 1.",
            },
            "div_cls_code1": {
                "type": "string",
                "description": "Sub classification code (blank for all). Default empty.",
            },
        },
        "required": [],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_interest_rate_summary(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_issue_other.get_interest_rate_summary(
        params.get("market", "I"),
        params.get("cond_scr_div_code", "20702"),
        params.get("div_cls_code", "1"),
        params.get("div_cls_code1", ""),
    )
    return {
        "domestic": extract_output(response, "output1"),
        "foreign": extract_output(response, "output2"),
    }


# ---------------------------------------------------------------------------
# kis.issue_other.market_announcement_schedule
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.market_announcement_schedule",
    description="Get market news and announcement titles.",
    parameters={
        "type": "object",
        "properties": {
            "news_ofer_entp_code": {
                "type": "string",
                "description": "News provider code. Default empty.",
            },
            "cond_mrkt_cls_code": {
                "type": "string",
                "description": "Market class code. Default empty.",
            },
            "stock_code": {
                "type": "string",
                "description": "Stock code (blank for all).",
            },
            "titl_cntt": {
                "type": "string",
                "description": "Title content filter. Default empty.",
            },
            "start_date": {
                "type": "string",
                "description": "Date filter (blank:current, format: 00YYYYMMDD). Default empty.",
            },
            "hour": {
                "type": "string",
                "description": "Time filter (blank:current, format: 0000HHMMSS). Default empty.",
            },
            "rank_sort_cls_code": {
                "type": "string",
                "description": "Sort classification code. Default empty.",
            },
            "input_srno": {
                "type": "string",
                "description": "Input serial number. Default empty.",
            },
        },
        "required": [],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_market_announcement_schedule(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_issue_other.get_market_announcement_schedule(
        params.get("news_ofer_entp_code", ""),
        params.get("cond_mrkt_cls_code", ""),
        params.get("stock_code", ""),
        params.get("titl_cntt", ""),
        params.get("start_date", ""),
        params.get("hour", ""),
        params.get("rank_sort_cls_code", ""),
        params.get("input_srno", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.issue_other.holiday_inquiry
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.holiday_inquiry",
    description="Get domestic market holiday schedule.",
    parameters={
        "type": "object",
        "properties": {
            "bass_dt": {
                "type": "string",
                "description": "Base date (YYYYMMDD)",
            },
            "ctx_area_nk": {
                "type": "string",
                "description": "Continuation key (blank for initial query). Default empty.",
            },
            "ctx_area_fk": {
                "type": "string",
                "description": "Continuation search condition (blank for initial query). Default empty.",
            },
        },
        "required": ["bass_dt"],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_holiday_inquiry(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_issue_other.get_holiday_inquiry(
        params["bass_dt"],
        params.get("ctx_area_nk", ""),
        params.get("ctx_area_fk", ""),
    )
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# kis.issue_other.futures_business_day_inquiry
# ---------------------------------------------------------------------------


@rpc_method(
    name="kis.issue_other.futures_business_day_inquiry",
    description="Get futures business day information.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
    returns={"type": "object"},
    category="kis.issue_other",
    broker="kis",
)
def handle_kis_futures_business_day_inquiry(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_issue_other.get_futures_business_day_inquiry()
    return {"data": extract_output(response, "output")}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kis_sector_current_index,
    handle_kis_sector_daily_index,
    handle_kis_sector_time_index_second,
    handle_kis_sector_time_index_minute,
    handle_kis_sector_minute_inquiry,
    handle_kis_sector_period_quote,
    handle_kis_sector_all_quote_by_category,
    handle_kis_expected_index_trend,
    handle_kis_expected_index_all,
    handle_kis_volatility_interruption_status,
    handle_kis_interest_rate_summary,
    handle_kis_market_announcement_schedule,
    handle_kis_holiday_inquiry,
    handle_kis_futures_business_day_inquiry,
]


def register_kis_issue_other_handlers(dispatcher: Dispatcher) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
