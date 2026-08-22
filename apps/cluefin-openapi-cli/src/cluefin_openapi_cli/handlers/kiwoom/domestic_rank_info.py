"""RPC handlers for Kiwoom DomesticRankInfo API (21 methods)."""

from __future__ import annotations

from cluefin_openapi_cli.handlers._base import DispatcherProtocol, extract_body, rpc_method

# ---------------------------------------------------------------------------
# Top Remaining Order Quantity
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.remaining_order",
    description="Get top stocks by remaining order quantity ranking.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {"type": "string", "enum": ["001", "101"], "description": "Market (001:KOSPI, 101:KOSDAQ)"},
            "sort_tp": {
                "type": "string",
                "enum": ["1", "2", "3", "4"],
                "description": "Sort (1:net buy qty, 2:net sell qty, 3:buy ratio, 4:sell ratio)",
            },
            "trde_qty_tp": {
                "type": "string",
                "enum": ["0000", "0010", "0050", "00100"],
                "description": "Volume filter. Default 0000.",
            },
            "stk_cnd": {
                "type": "string",
                "enum": ["0", "1", "5", "6", "7", "8", "9"],
                "description": "Stock condition. Default 0.",
            },
            "crd_cnd": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4", "9"],
                "description": "Credit condition. Default 0.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "sort_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_remaining_order_qty(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_remaining_order_quantity(
        mrkt_tp=params["market_type"],
        sort_tp=params["sort_tp"],
        trde_qty_tp=params.get("trde_qty_tp", "0000"),
        stk_cnd=params.get("stk_cnd", "0"),
        crd_cnd=params.get("crd_cnd", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Rapidly Increasing Remaining Order Quantity
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.increasing_order",
    description="Get stocks with rapidly increasing remaining order quantity.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {"type": "string", "enum": ["001", "101"], "description": "Market (001:KOSPI, 101:KOSDAQ)"},
            "trde_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Trade type (1:buy remaining, 2:sell remaining)",
            },
            "sort_tp": {"type": "string", "enum": ["1", "2"], "description": "Sort (1:surge qty, 2:surge rate)"},
            "tm_tp": {"type": "string", "description": "Time period (minutes)"},
            "trde_qty_tp": {
                "type": "string",
                "enum": ["1", "5", "10", "50", "100"],
                "description": "Volume filter. Default 1.",
            },
            "stk_cnd": {
                "type": "string",
                "enum": ["0", "1", "5", "6", "7", "8", "9"],
                "description": "Stock condition. Default 0.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "trde_tp", "sort_tp", "tm_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_increasing_remaining_order(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_rapidly_increasing_remaining_order_quantity(
        mrkt_tp=params["market_type"],
        trde_tp=params["trde_tp"],
        sort_tp=params["sort_tp"],
        tm_tp=params["tm_tp"],
        trde_qty_tp=params.get("trde_qty_tp", "1"),
        stk_cnd=params.get("stk_cnd", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Rapidly Increasing Total Sell Orders
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.increasing_sell",
    description="Get stocks with rapidly increasing total sell orders.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {"type": "string", "enum": ["001", "101"], "description": "Market (001:KOSPI, 101:KOSDAQ)"},
            "rt_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Ratio type (1:buy/sell ratio, 2:sell/buy ratio)",
            },
            "tm_tp": {"type": "string", "enum": ["1", "2"], "description": "Time type (1:minutes, 2:prev day)"},
            "trde_qty_tp": {
                "type": "string",
                "enum": ["5", "10", "50", "100"],
                "description": "Volume filter. Default 5.",
            },
            "stk_cnd": {
                "type": "string",
                "enum": ["0", "1", "5", "6", "7", "8", "9"],
                "description": "Stock condition. Default 0.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "rt_tp", "tm_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_increasing_total_sell(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_rapidly_increasing_total_sell_orders(
        mrkt_tp=params["market_type"],
        rt_tp=params["rt_tp"],
        tm_tp=params["tm_tp"],
        trde_qty_tp=params.get("trde_qty_tp", "5"),
        stk_cnd=params.get("stk_cnd", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Rapidly Increasing Trading Volume
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.increasing_volume",
    description="Get stocks with rapidly increasing trading volume.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "sort_tp": {
                "type": "string",
                "enum": ["1", "2", "3", "4"],
                "description": "Sort (1:surge qty, 2:surge rate, 3:decline qty, 4:decline rate)",
            },
            "tm_tp": {"type": "string", "enum": ["1", "2"], "description": "Time type (1:minutes, 2:prev day)"},
            "trde_qty_tp": {
                "type": "string",
                "enum": ["5", "10", "50", "100", "200", "300", "500", "1000"],
                "description": "Volume filter. Default 5.",
            },
            "stk_cnd": {
                "type": "string",
                "description": "Stock condition code. Default 0.",
            },
            "pric_tp": {
                "type": "string",
                "enum": ["0", "2", "5", "6", "8", "9"],
                "description": "Price filter. Default 0.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "tm": {"type": "string", "description": "Time value (minutes or days). Default empty."},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "sort_tp", "tm_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_increasing_volume(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_rapidly_increasing_trading_volume(
        mrkt_tp=params["market_type"],
        sort_tp=params["sort_tp"],
        tm_tp=params["tm_tp"],
        trde_qty_tp=params.get("trde_qty_tp", "5"),
        stk_cnd=params.get("stk_cnd", "0"),
        pric_tp=params.get("pric_tp", "0"),
        stex_tp=params.get("exchange_type", "1"),
        tm=params.get("tm", ""),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Percentage Change From Previous Day
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.fluctuation",
    description="Get top stocks by percentage change from previous day.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "sort_tp": {
                "type": "string",
                "enum": ["1", "2", "3", "4", "5"],
                "description": "Sort (1:gain rate, 2:gain amount, 3:loss rate, 4:loss amount, 5:flat)",
            },
            "trde_qty_cnd": {
                "type": "string",
                "enum": ["0000", "0010", "0050", "0100", "0150", "0200", "0300", "0500", "1000"],
                "description": "Volume filter in shares (0000:all, 0010:10k+, 0050:50k+, 0100:100k+, "
                "0150:150k+, 0200:200k+, 0300:300k+, 0500:500k+, 1000:1M+). Default 0000.",
            },
            "stk_cnd": {
                "type": "string",
                "enum": ["0", "1", "4", "3", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16"],
                "description": "Stock condition (0:all, 1:excl-managed, 4:excl-managed+preferred, "
                "3:excl-preferred, 5:excl-margin100, 6:margin100-only, 7:margin40-only, 8:margin30-only, "
                "9:margin20-only, 11:excl-liquidation, 12:margin50-only, 13:margin60-only, 14:excl-ETF, "
                "15:excl-SPAC, 16:excl-ETF+ETN). Default 0.",
            },
            "crd_cnd": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4", "9"],
                "description": "Credit condition (0:all, 1:margin-loan-A, 2:margin-loan-B, 3:margin-loan-C, "
                "4:margin-loan-D, 9:margin-loan-all). Default 0.",
            },
            "updown_incls": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Include upper/lower limit (0:no, 1:yes). Default 0.",
            },
            "pric_cnd": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4", "5", "8", "10"],
                "description": "Price filter in KRW (0:all, 1:<1k, 2:1k-2k, 3:2k-5k, 4:5k-10k, 5:10k+, "
                "8:1k+, 10:<10k). Default 0.",
            },
            "trde_prica_cnd": {
                "type": "string",
                "enum": ["0", "3", "5", "10", "30", "50", "100", "300", "500", "1000", "3000", "5000"],
                "description": "Trade amount filter in KRW 10-millions (0:all, 3:30M+, 5:50M+, 10:100M+, "
                "30:300M+, 50:500M+, 100:1B+, 300:3B+, 500:5B+, 1000:10B+, 3000:30B+, 5000:50B+). Default 0.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "sort_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_pct_change_from_prev(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_percentage_change_from_previous_day(
        mrkt_tp=params["market_type"],
        sort_tp=params["sort_tp"],
        trde_qty_cnd=params.get("trde_qty_cnd", "0000"),
        stk_cnd=params.get("stk_cnd", "0"),
        crd_cnd=params.get("crd_cnd", "0"),
        updown_incls=params.get("updown_incls", "0"),
        pric_cnd=params.get("pric_cnd", "0"),
        trde_prica_cnd=params.get("trde_prica_cnd", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Expected Conclusion Percentage Change
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.expected_conclusion",
    description="Get top stocks by expected conclusion percentage change.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "sort_tp": {
                "type": "string",
                "enum": ["1", "2", "3", "4", "5", "6", "7", "8"],
                "description": "Sort (1:gain-rate, 2:gain-amount, 3:flat, 4:loss-rate, 5:loss-amount, "
                "6:conclusion-volume, 7:upper-limit, 8:lower-limit). Default 1.",
            },
            "trde_qty_cnd": {
                "type": "string",
                "enum": ["0", "1", "3", "5", "10", "50", "100"],
                "description": "Volume filter in 1000 shares (0:all, 1:1k+, 3:3k+, 5:5k+, 10:10k+, "
                "50:50k+, 100:100k+). Default 0.",
            },
            "stk_cnd": {
                "type": "string",
                "enum": ["0", "1", "3", "4", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16"],
                "description": "Stock condition (0:all, 1:excl-managed, 3:excl-preferred, "
                "4:excl-managed+preferred, 5:excl-margin100, 6:margin100-only, 7:margin40-only, "
                "8:margin30-only, 9:margin20-only, 11:excl-liquidation, 12:margin50-only, 13:margin60-only, "
                "14:excl-ETF, 15:excl-SPAC, 16:excl-ETF+ETN). Default 0.",
            },
            "crd_cnd": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4", "8", "9"],
                "description": "Credit condition (0:all, 1:margin-loan-A, 2:margin-loan-B, 3:margin-loan-C, "
                "4:margin-loan-D, 8:stock-loan, 9:margin-loan-all). Default 0.",
            },
            "pric_cnd": {
                "type": "string",
                "enum": ["0", "1", "2", "3", "4", "5", "8", "10"],
                "description": "Price filter in KRW (0:all, 1:<1k, 2:1k-2k, 3:2k-5k, 4:5k-10k, 5:10k+, "
                "8:1k+, 10:<10k). Default 0.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_expected_conclusion_pct_change(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_expected_conclusion_percentage_change(
        mrkt_tp=params["market_type"],
        sort_tp=params.get("sort_tp", "1"),
        trde_qty_cnd=params.get("trde_qty_cnd", "0"),
        stk_cnd=params.get("stk_cnd", "0"),
        crd_cnd=params.get("crd_cnd", "0"),
        pric_cnd=params.get("pric_cnd", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Previous Day Trading Volume
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.prev_day_volume",
    description="Get top stocks by previous day trading volume.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "qry_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Query type (1:volume top100, 2:trade amount top100)",
            },
            "rank_strt": {"type": "string", "description": "Rank start (0-100)"},
            "rank_end": {"type": "string", "description": "Rank end (0-100)"},
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "qry_tp", "rank_strt", "rank_end"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_prev_day_volume(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_previous_day_trading_volume(
        mrkt_tp=params["market_type"],
        qry_tp=params["qry_tp"],
        rank_strt=params["rank_strt"],
        rank_end=params["rank_end"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Transaction Value
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.transaction_value",
    description="Get top stocks by transaction value.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "mang_stk_incls": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Include admin stocks (0:exclude, 1:include). Default 0.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Exchange (1:KRX, 2:NXT). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_transaction_value(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_transaction_value(
        mrkt_tp=params["market_type"],
        mang_stk_incls=params.get("mang_stk_incls", "0"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Foreigner Period Trading
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.foreigner_period",
    description="Get top stocks by foreigner period trading.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "trde_tp": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Trade type (1:net sell, 2:net buy, 3:net trade)",
            },
            "dt": {
                "type": "string",
                "enum": ["0", "1", "5", "10", "20", "60"],
                "description": "Period (0:today, 1:prev day, 5/10/20/60 days)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "trde_tp", "dt"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_foreigner_period_trading(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_foreigner_period_trading(
        mrkt_tp=params["market_type"],
        trde_tp=params["trde_tp"],
        dt=params["dt"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Consecutive Net Buy/Sell by Foreigners
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.consecutive_foreign",
    description="Get top stocks by consecutive net buy/sell by foreigners.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "trde_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Trade type (1:consecutive net sell, 2:consecutive net buy)",
            },
            "base_dt_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Base date (0:today, 1:prev day)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "trde_tp", "base_dt_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_consecutive_net_buy_sell_foreigners(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_consecutive_net_buy_sell_by_foreigners(
        mrkt_tp=params["market_type"],
        trde_tp=params["trde_tp"],
        base_dt_tp=params["base_dt_tp"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Limit Exhaustion Rate (Foreigner)
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.foreign_limit",
    description="Get top stocks by foreigner ownership limit exhaustion rate.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "dt": {
                "type": "string",
                "enum": ["0", "1", "5", "10", "20", "60"],
                "description": "Period (0:today, 1:prev day, 5/10/20/60 days)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "dt"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_limit_exhaustion_rate_foreigner(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_limit_exhaustion_rate_foreigner(
        mrkt_tp=params["market_type"],
        dt=params["dt"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Foreign Account Group Trading
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.foreign_account",
    description="Get top stocks by foreign account group trading.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "dt": {
                "type": "string",
                "enum": ["0", "1", "5", "10", "20", "60"],
                "description": "Period (0:today, 1:prev day, 5/10/20/60 days)",
            },
            "trde_tp": {
                "type": "string",
                "enum": ["1", "2", "3", "4"],
                "description": "Trade type (1:net buy, 2:net sell, 3:buy, 4:sell)",
            },
            "sort_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Sort (1:amount, 2:quantity)",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "dt", "trde_tp", "sort_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_foreign_account_group_trading(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_foreign_account_group_trading(
        mrkt_tp=params["market_type"],
        dt=params["dt"],
        trde_tp=params["trde_tp"],
        sort_tp=params["sort_tp"],
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Stock Specific Securities Firm Ranking
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.securities_firm_by_stock",
    description="Get securities firm ranking for a specific stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "qry_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Query type (1:net sell rank, 2:net buy rank)",
            },
            "dt": {
                "type": "string",
                "enum": ["1", "4", "9", "19", "39", "59", "119"],
                "description": "Period (1:prev, 4:5d, 9:10d, 19:20d, 39:40d, 59:60d, 119:120d). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "start_date", "end_date", "qry_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_securities_firm_by_stock(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_stock_specific_securities_firm_ranking(
        stk_cd=params["stock_code"],
        strt_dt=params["start_date"],
        end_dt=params["end_date"],
        qry_tp=params["qry_tp"],
        dt=params.get("dt", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Securities Firm Trading
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.securities_firm",
    description="Get top stocks traded by a specific securities firm.",
    parameters={
        "type": "object",
        "properties": {
            "member_company_code": {"type": "string", "description": "3-digit member company code"},
            "trde_qty_tp": {"type": "string", "description": "Volume filter. Default 0."},
            "trde_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Trade type (1:net buy, 2:net sell)",
            },
            "dt": {
                "type": "string",
                "enum": ["1", "5", "10", "60"],
                "description": "Period (1:prev, 5:5d, 10:10d, 60:60d). Default 1.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["member_company_code", "trde_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_securities_firm_trading(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_securities_firm_trading(
        mmcm_cd=params["member_company_code"],
        trde_qty_tp=params.get("trde_qty_tp", "0"),
        trde_tp=params["trde_tp"],
        dt=params.get("dt", "1"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Current Day Major Traders
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.major_traders",
    description="Get current day major traders (top trading firms) for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_current_day_major_traders(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_current_day_major_traders(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Net Buy Trader Ranking
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.net_buy_trader",
    description="Get net buy trader ranking for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "qry_dt_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Query period type (0:by period, 1:by start/end date)",
            },
            "pot_tp": {
                "type": "string",
                "enum": ["0", "1"],
                "description": "Point of time (0:today, 1:prev day)",
            },
            "dt": {
                "type": "string",
                "enum": ["5", "10", "20", "40", "60", "120"],
                "description": "Period (5/10/20/40/60/120 days)",
            },
            "sort_base": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Sort base (1:by close price, 2:by date)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code", "start_date", "end_date", "qry_dt_tp", "pot_tp", "dt", "sort_base"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_net_buy_trader(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_net_buy_trader_ranking(
        stk_cd=params["stock_code"],
        strt_dt=params["start_date"],
        end_dt=params["end_date"],
        qry_dt_tp=params["qry_dt_tp"],
        pot_tp=params["pot_tp"],
        dt=params["dt"],
        sort_base=params["sort_base"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Current Day Deviation Sources
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.deviation_sources",
    description="Get top current day deviation sources for a stock.",
    parameters={
        "type": "object",
        "properties": {
            "stock_code": {"type": "string", "description": "Stock code (e.g. KRX:039490, NXT:039490_NX)"},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["stock_code"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_current_day_deviation_sources(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_current_day_deviation_sources(
        stk_cd=params["stock_code"],
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Same Net Buy/Sell Ranking
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.same_net_buy_sell",
    description="Get same net buy/sell ranking across dates.",
    parameters={
        "type": "object",
        "properties": {
            "start_date": {"type": "string", "description": "Start date (YYYYMMDD)"},
            "end_date": {"type": "string", "description": "End date (YYYYMMDD)"},
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "trde_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Trade type (1:net buy, 2:net sell)",
            },
            "sort_cnd": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Sort condition (1:quantity, 2:amount)",
            },
            "unit_tp": {
                "type": "string",
                "enum": ["1", "1000"],
                "description": "Unit (1:share, 1000:thousand shares). Default 1.",
            },
            "exchange_type": {
                "type": "string",
                "enum": ["1", "2", "3"],
                "description": "Exchange (1:KRX, 2:NXT, 3:Combined). Default 1.",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["start_date", "end_date", "market_type", "trde_tp", "sort_cnd"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_same_net_buy_sell(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_same_net_buy_sell_ranking(
        strt_dt=params["start_date"],
        end_dt=params["end_date"],
        mrkt_tp=params["market_type"],
        trde_tp=params["trde_tp"],
        sort_cnd=params["sort_cnd"],
        unit_tp=params.get("unit_tp", "1"),
        stex_tp=params.get("exchange_type", "1"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Top Intraday Trading by Investor
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.intraday_investor",
    description="Get top intraday trading stocks by investor type.",
    parameters={
        "type": "object",
        "properties": {
            "trde_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Trade type (1:net buy, 2:net sell)",
            },
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "orgn_tp": {
                "type": "string",
                "enum": [
                    "9000",
                    "9100",
                    "1000",
                    "3000",
                    "5000",
                    "4000",
                    "2000",
                    "6000",
                    "7000",
                    "7100",
                    "9999",
                ],
                "description": "Investor type (9000:foreigner, 9100:foreign-firm, 1000:financial-investment, "
                "3000:investment-trust, 5000:other-financial, 4000:bank, 2000:insurance, "
                "6000:pension-fund, 7000:government, 7100:other-corporation, 9999:institution-total)",
            },
            "amt_qty_tp": {
                "type": "string",
                "enum": ["1", "2"],
                "description": "Rank by amount or quantity (1:amount, 2:quantity)",
            },
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["trde_tp", "market_type", "orgn_tp"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_intraday_trading_by_investor(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_top_intraday_trading_by_investor(
        trde_tp=params["trde_tp"],
        mrkt_tp=params["market_type"],
        orgn_tp=params["orgn_tp"],
        amt_qty_tp=params.get("amt_qty_tp"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# After Hours Single Price Change Rate Ranking
# ---------------------------------------------------------------------------


@rpc_method(
    name="ranking.after_hours",
    description="Get after-hours single price change rate ranking.",
    parameters={
        "type": "object",
        "properties": {
            "market_type": {
                "type": "string",
                "enum": ["000", "001", "101"],
                "description": "Market (000:all, 001:KOSPI, 101:KOSDAQ)",
            },
            "sort_base": {
                "type": "string",
                "enum": ["1", "2", "3", "4", "5"],
                "description": "Sort (1:gain rate, 2:gain amount, 3:loss rate, 4:loss amount, 5:flat)",
            },
            "stk_cnd": {"type": "string", "description": "Stock condition. Default 0."},
            "trde_qty_cnd": {"type": "string", "description": "Volume condition. Default 0."},
            "crd_cnd": {"type": "string", "description": "Credit condition. Default 0."},
            "trde_prica": {"type": "string", "description": "Trade amount filter. Default 0."},
            "cont_yn": {"type": "string", "enum": ["Y", "N"], "description": "Continuation flag. Default N."},
            "next_key": {"type": "string", "description": "Continuation key. Default empty."},
        },
        "required": ["market_type", "sort_base"],
    },
    returns={"type": "object"},
    category="ranking",
    broker="kiwoom",
)
def handle_kiwoom_after_hours_single_price_change(params: dict, session) -> dict:
    kiwoom = session.get_kiwoom()
    response = kiwoom.rank_info.get_after_hours_single_price_change_rate_ranking(
        mrkt_tp=params["market_type"],
        sort_base=params["sort_base"],
        stk_cnd=params.get("stk_cnd", "0"),
        trde_qty_cnd=params.get("trde_qty_cnd", "0"),
        crd_cnd=params.get("crd_cnd", "0"),
        trde_prica=params.get("trde_prica", "0"),
        cont_yn=params.get("cont_yn", "N"),
        next_key=params.get("next_key", ""),
    )
    return extract_body(response)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

_ALL_HANDLERS = [
    handle_kiwoom_remaining_order_qty,
    handle_kiwoom_increasing_remaining_order,
    handle_kiwoom_increasing_total_sell,
    handle_kiwoom_increasing_volume,
    handle_kiwoom_pct_change_from_prev,
    handle_kiwoom_expected_conclusion_pct_change,
    handle_kiwoom_prev_day_volume,
    handle_kiwoom_transaction_value,
    handle_kiwoom_foreigner_period_trading,
    handle_kiwoom_consecutive_net_buy_sell_foreigners,
    handle_kiwoom_limit_exhaustion_rate_foreigner,
    handle_kiwoom_foreign_account_group_trading,
    handle_kiwoom_securities_firm_by_stock,
    handle_kiwoom_securities_firm_trading,
    handle_kiwoom_current_day_major_traders,
    handle_kiwoom_net_buy_trader,
    handle_kiwoom_current_day_deviation_sources,
    handle_kiwoom_same_net_buy_sell,
    handle_kiwoom_intraday_trading_by_investor,
    handle_kiwoom_after_hours_single_price_change,
]


def register_kiwoom_rank_info_handlers(dispatcher: DispatcherProtocol) -> None:
    for handler in _ALL_HANDLERS:
        schema = handler._rpc_schema
        dispatcher.register(schema.name, handler, schema)
