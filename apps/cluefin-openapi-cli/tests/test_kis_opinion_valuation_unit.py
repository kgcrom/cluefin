"""`kis stock opinion-summary` and `kis stock valuation` — the two stock-info commands that compute.

Opinion cases follow cluefin-factory's `opinions()` behaviour (archived 2026-10-18). The valuation
handler is driven by one fake session that answers KIS (period quote, estimate) and DART (full
statements, share count) so the call count and every multiple can be asserted on round numbers.
"""

from __future__ import annotations

import pytest

from cluefin_openapi_cli import opinions
from cluefin_openapi_cli.errors import EXIT_BROKER, CliError
from cluefin_openapi_cli.handlers.kis import domestic_stock_info as handlers

# ---------------------------------------------------------------------------
# opinions.summarize
# ---------------------------------------------------------------------------


def _opinion(date, broker, target, rating="매수", previous="매수") -> dict:
    return {
        "stck_bsop_date": date,
        "mbcr_name": broker,
        "hts_goal_prc": target,
        "invt_opnn": rating,
        "rgbf_invt_opnn": previous,
    }


def test_summarize_keeps_each_brokers_latest_target_and_computes_statistics() -> None:
    rows = [
        _opinion("20260901", "A증권", "100,000"),
        _opinion("20260915", "A증권", "120,000", rating="매수", previous="중립"),
        _opinion("20260910", "B증권", "80,000", rating="중립"),
        _opinion("20260601", "C증권", "200,000"),  # before the window
        _opinion("20260920", "D증권", "0"),  # no target
    ]

    out = opinions.summarize(rows, since="20260720")

    assert out["count"] == 2
    assert [b["broker"] for b in out["brokers"]] == ["A증권", "B증권"]
    assert out["brokers"][0] == {
        "broker": "A증권",
        "date": "20260915",
        "rating": "매수",
        "previous_rating": "중립",
        "target": 120000,
    }
    assert out["mean"] == 100000
    assert out["median"] == 100000
    assert out["max"] == {"target": 120000, "broker": "A증권", "date": "20260915"}
    assert out["min"]["broker"] == "B증권"
    assert out["ratings"] == {"매수": 1, "중립": 1}


def test_summarize_with_nothing_in_the_window_is_empty_not_an_error() -> None:
    out = opinions.summarize([_opinion("20250101", "A증권", "100")], since="20260101")
    assert out["count"] == 0
    assert out["mean"] is None
    assert out["brokers"] == []
    assert opinions.summarize([{"value": "1"}], since="20260101")["count"] == 0


# ---------------------------------------------------------------------------
# fakes for the handlers
# ---------------------------------------------------------------------------


class _Row:
    def __init__(self, data: dict) -> None:
        self._data = data

    def model_dump(self) -> dict:
        return dict(self._data)


class _Dart:
    def __init__(self, statements: dict, shares: list[dict]) -> None:
        self._statements = statements
        self._shares = shares
        self.calls: list[tuple] = []

    def get_single_company_full_statements(self, corp_code, bsns_year, reprt_code, fs_div):
        self.calls.append(("statements", bsns_year, reprt_code, fs_div))
        rows = self._statements.get((int(bsns_year), reprt_code, fs_div), [])
        return type("R", (), {"result": type("E", (), {"status": "000", "list": [_Row(r) for r in rows]})()})()

    def get_total_number_of_shares(self, corp_code, bsns_year, reprt_code):
        self.calls.append(("shares", bsns_year, reprt_code))
        return type("R", (), {"result": type("E", (), {"status": "000", "list": [_Row(r) for r in self._shares]})()})()


class _Kis:
    def __init__(self, candles: list[dict], estimate: dict, opinion_rows: list[dict]) -> None:
        self._candles = candles
        self._estimate = estimate
        self._opinion_rows = opinion_rows
        self.calls: list[tuple] = []

    def get_stock_period_quote(self, market, code, start, end, period, adj):  # noqa: PLR0913
        self.calls.append(("period", start, end, adj))
        return type("Response", (), {"body": type("Body", (), {"output2": self._candles})()})()

    def get_estimated_earnings(self, stock_code):
        self.calls.append(("estimate", stock_code))
        body = type("Body", (), {k: [_Row(r) for r in v] for k, v in self._estimate.items()})()
        return type("Response", (), {"body": body})()

    def get_investment_opinion(self, market, scr, stock_code, start, end):
        self.calls.append(("opinion", start, end))
        body = type("Body", (), {"output": [_Row(r) for r in self._opinion_rows]})()
        return type("Response", (), {"body": body})()


class _Session:
    def __init__(self, kis: _Kis, dart: _Dart) -> None:
        self.kis = kis
        self.dart = dart

    def get_kis(self):
        return type("Client", (), {"domestic_basic_quote": self.kis, "domestic_stock_info": self.kis})()

    def get_dart(self):
        return type(
            "Client",
            (),
            {"periodic_report_financial_statement": self.dart, "periodic_report_key_information": self.dart},
        )()


def _candle(day: str, close: str) -> dict:
    return {
        "stck_bsop_date": day,
        "stck_oprc": close,
        "stck_hgpr": close,
        "stck_lwpr": close,
        "stck_clpr": close,
        "acml_vol": "10",
    }


def _income(**amounts) -> dict:
    return {"sj_div": "CIS", "account_id": "ifrs-full_ProfitLossAttributableToOwnersOfParent", **amounts}


def _revenue(**amounts) -> dict:
    return {"sj_div": "CIS", "account_id": "ifrs-full_Revenue", **amounts}


def _equity(amount: str) -> dict:
    return {"sj_div": "BS", "account_id": "ifrs-full_EquityAttributableToOwnersOfParent", "thstrm_amount": amount}


def _statements() -> dict:
    """Owners' net income 100 every quarter (TTM 400), equity 2,000 at the latest period; all 억원 ×1e8 in 원."""
    eok = 100_000_000
    rcept = "20250815000001"

    def q(single, ytd, prior_single, prior_ytd):
        return [
            _income(
                thstrm_amount=str(single * eok),
                thstrm_add_amount=str(ytd * eok),
                frmtrm_q_amount=str(prior_single * eok),
                frmtrm_add_amount=str(prior_ytd * eok),
            ),
            _revenue(
                thstrm_amount=str(single * eok),
                thstrm_add_amount=str(ytd * eok),
                frmtrm_q_amount=str(prior_single * eok),
                frmtrm_add_amount=str(prior_ytd * eok),
            ),
            _equity(str(2000 * eok)),
            {"rcept_no": rcept},
        ]

    return {
        (2025, "11013", "CFS"): q(100, 100, 100, 100),
        (2025, "11012", "CFS"): q(100, 200, 100, 200),
        (2025, "11014", "CFS"): q(100, 300, 100, 300),
        (2025, "11011", "CFS"): [
            _income(thstrm_amount=str(400 * eok), frmtrm_amount=str(400 * eok), bfefrmtrm_amount=str(400 * eok)),
            _revenue(thstrm_amount=str(400 * eok), frmtrm_amount=str(400 * eok), bfefrmtrm_amount=str(400 * eok)),
            _equity(str(2000 * eok)),
            {"rcept_no": "20260315000001"},
        ],
        (2026, "11013", "CFS"): q(100, 100, 100, 100),
    }


SHARES = (
    {"se": "보통주", "istc_totqy": "1,000,000", "tesstk_co": "100,000", "distb_stock_co": "900,000"},
    {"se": "우선주", "istc_totqy": "50,000", "tesstk_co": "-", "distb_stock_co": "50,000"},
)

ESTIMATE = {
    "output4": [{"dt": "2025.12"}, {"dt": "2026.12E"}],
    # eps is the second detail row; ×10 on the wire → 40,000원 and 50,000원.
    "output3": [{"data1": "1", "data2": "1"}, {"data1": "400000", "data2": "500000"}],
}


def _session(candles=None, shares=None, estimate=None) -> _Session:
    """None means the standard fixture; pass [] to simulate an empty broker answer."""
    candles = [_candle("20261016", "40000"), _candle("20261017", "40000")] if candles is None else candles
    shares = list(SHARES) if shares is None else shares
    estimate = dict(ESTIMATE) if estimate is None else estimate
    return _Session(_Kis(candles, estimate, []), _Dart(_statements(), shares))


def test_valuation_computes_market_cap_per_and_pbr_from_the_three_sources() -> None:
    session = _session()

    out = handlers.handle_kis_stock_valuation(
        {"stock_code": "000001", "corp_code": "00000001", "as_of": "20261018"}, session
    )

    assert out["price"] == {"close": 40000.0, "date": "20261017", "adjusted": False}
    assert out["shares"] == {"issued": 1_000_000, "treasury": 100_000, "outstanding": 900_000, "report": "2026-11013"}
    assert out["market_cap"] == pytest.approx(400)  # 40,000 × 1,000,000 / 1e8 억원
    assert out["ttm_net_income_owners"] == pytest.approx(400)
    assert out["per_ttm"] == pytest.approx(1.0)
    assert out["pbr"] == pytest.approx(0.2)
    assert out["per_by_year"] == [
        {"period": "2025.12", "estimate": False, "eps": 40000.0, "per": pytest.approx(1.0)},
        {"period": "2026.12E", "estimate": True, "eps": 50000.0, "per": pytest.approx(0.8)},
    ]
    assert out["calls"] == 11
    assert session.dart.calls[-1] == ("shares", "2026", "11013")
    assert session.kis.calls[0][3] == "1"  # chart.period: "1" is the unadjusted price flag


def test_valuation_without_a_common_share_row_leaves_market_cap_null() -> None:
    out = handlers.handle_kis_stock_valuation(
        {"stock_code": "000001", "corp_code": "00000001", "as_of": "20261018"}, _session(shares=[])
    )
    assert out["shares"] is None
    assert out["market_cap"] is None
    assert out["per_ttm"] is None
    assert out["pbr"] is None
    assert out["per_by_year"][0]["per"] == pytest.approx(1.0)  # EPS-based PER needs no share count


def test_valuation_without_a_close_is_exit_4_before_any_dart_call() -> None:
    session = _session(candles=[])
    with pytest.raises(CliError) as info:
        handlers.handle_kis_stock_valuation(
            {"stock_code": "000001", "corp_code": "00000001", "as_of": "20261018"}, session
        )
    assert info.value.exit_code == EXIT_BROKER
    assert session.dart.calls == []


def test_opinion_summary_passes_the_window_with_the_kis_00_prefix() -> None:
    session = _session()
    session.kis._opinion_rows = [_opinion("20261001", "A증권", "50,000")]

    out = handlers.handle_kis_opinion_summary({"stock_code": "000001", "as_of": "20261018", "days": 30}, session)

    assert session.kis.calls == [("opinion", "0020260918", "0020261018")]
    assert out["since"] == "20260918"
    assert out["as_of"] == "20261018"
    assert out["count"] == 1
    assert out["brokers"][0]["target"] == 50000
