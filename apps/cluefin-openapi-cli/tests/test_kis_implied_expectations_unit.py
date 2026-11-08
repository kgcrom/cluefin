"""`kis stock implied-expectations` — one fake session answering KIS, DART and ECOS.

The RIM/reverse-DCF math itself is covered hand-computed in test_implied_unit.py; this file
drives the handler end to end (call counts, assumption sourcing, error paths) with round
numbers so the result is easy to eyeball. Damodaran is never fetched over the network here —
either `--erp`/`--tax-rate` make it unnecessary, or `_fetch_damodaran_korea` is monkeypatched.
"""

from __future__ import annotations

import pytest

from cluefin_openapi_cli.errors import EXIT_BROKER, CliError
from cluefin_openapi_cli.handlers.kis import domestic_stock_info as handlers


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
    def __init__(self, candles: list[dict], estimate: dict) -> None:
        self._candles = candles
        self._estimate = estimate
        self.calls: list[tuple] = []

    def get_stock_period_quote(self, market, code, start, end, period, adj):  # noqa: PLR0913
        self.calls.append(("period", start, end, adj))
        return type("Response", (), {"body": type("Body", (), {"output2": self._candles})()})()

    def get_estimated_earnings(self, stock_code):
        self.calls.append(("estimate", stock_code))
        body = type("Body", (), {k: [_Row(r) for r in v] for k, v in self._estimate.items()})()
        return type("Response", (), {"body": body})()


class _EcosRow:
    def __init__(self, time: str, value: str) -> None:
        self.time = time
        self.data_value = value


class _StatisticSearch:
    def __init__(self, ecos: _Ecos) -> None:
        self._ecos = ecos

    def search(self, stat_code, cycle, start, end, item_codes):
        self._ecos.calls.append((stat_code, cycle, start, end, tuple(item_codes)))
        value = {"010210000": self._ecos._ktb_10y, "010300000": self._ecos._corp_aa_3y}.get(item_codes[0])
        rows = [] if value is None else [_EcosRow(end, value)]
        return type("Page", (), {"rows": rows})()


class _Ecos:
    def __init__(self, ktb_10y: str | None, corp_aa_3y: str | None) -> None:
        self._ktb_10y = ktb_10y
        self._corp_aa_3y = corp_aa_3y
        self.calls: list[tuple] = []
        self.statistic_search = _StatisticSearch(self)


class _Session:
    def __init__(self, kis: _Kis, dart: _Dart, ecos: _Ecos) -> None:
        self.kis = kis
        self.dart = dart
        self.ecos = ecos

    def get_kis(self):
        return type("Client", (), {"domestic_basic_quote": self.kis, "domestic_stock_info": self.kis})()

    def get_dart(self):
        return type(
            "Client",
            (),
            {"periodic_report_financial_statement": self.dart, "periodic_report_key_information": self.dart},
        )()

    def get_ecos(self):
        return self.ecos


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


def _operating_income(**amounts) -> dict:
    return {"sj_div": "CIS", "account_id": "dart_OperatingIncomeLoss", **amounts}


def _equity(**amounts) -> dict:
    return {"sj_div": "BS", "account_id": "ifrs-full_EquityAttributableToOwnersOfParent", **amounts}


def _borrowings(amount: str) -> dict:
    return {"sj_div": "BS", "account_nm": "단기차입금", "thstrm_amount": amount}


def _cash(amount: str) -> dict:
    return {"sj_div": "BS", "account_id": "ifrs-full_CashAndCashEquivalents", "thstrm_amount": amount}


def _dividends(amount: str) -> dict:
    return {
        "sj_div": "CF",
        "account_id": "ifrs-full_DividendsPaidClassifiedAsFinancingActivities",
        "thstrm_amount": amount,
    }


EOK = 100_000_000


def _statements() -> dict:
    """Owners' net income 100억/quarter (TTM 400억), opm 20%, equity 2,000억, borrowings 500억, cash 100억."""
    rcept = "20250815000001"

    def q(single, ytd):
        return [
            _income(thstrm_amount=str(single * EOK), thstrm_add_amount=str(ytd * EOK)),
            _revenue(thstrm_amount=str(single * 5 * EOK), thstrm_add_amount=str(ytd * 5 * EOK)),
            _operating_income(thstrm_amount=str(single * EOK), thstrm_add_amount=str(ytd * EOK)),
            _equity(thstrm_amount=str(2000 * EOK)),
            _borrowings(str(500 * EOK)),
            _cash(str(100 * EOK)),
            {"rcept_no": rcept},
        ]

    annual_rows = [
        _income(thstrm_amount=str(400 * EOK), frmtrm_amount=str(360 * EOK), bfefrmtrm_amount=str(320 * EOK)),
        _revenue(thstrm_amount=str(2000 * EOK), frmtrm_amount=str(1800 * EOK), bfefrmtrm_amount=str(1600 * EOK)),
        # Deliberately not 20% of revenue in every year (400/2000=20%, 270/1800=15%, 224/1600=14%) so the
        # DART 3y average operating margin (~16.3%) differs from the TTM margin (20%) used elsewhere.
        _operating_income(thstrm_amount=str(400 * EOK), frmtrm_amount=str(270 * EOK), bfefrmtrm_amount=str(224 * EOK)),
        _equity(thstrm_amount=str(2000 * EOK), frmtrm_amount=str(1900 * EOK), bfefrmtrm_amount=str(1800 * EOK)),
        _borrowings(str(500 * EOK)),
        _cash(str(100 * EOK)),
        _dividends(str(-120 * EOK)),
        {"rcept_no": "20260315000001"},
    ]

    return {
        (2025, "11013", "CFS"): q(100, 100),
        (2025, "11012", "CFS"): q(100, 200),
        (2025, "11014", "CFS"): q(100, 300),
        (2025, "11011", "CFS"): annual_rows,
        (2026, "11013", "CFS"): q(100, 100),
    }


SHARES = ({"se": "보통주", "istc_totqy": "1,000,000", "tesstk_co": "-", "distb_stock_co": "1,000,000"},)

ESTIMATE = {
    "output4": [{"dt": "2025.12"}, {"dt": "2026.12E"}],
    # roe is the 6th detail row (index 5); ×10 on the wire.
    "output3": [
        {"data1": "1", "data2": "1"},
        {"data1": "1", "data2": "1"},
        {"data1": "1", "data2": "1"},
        {"data1": "1", "data2": "1"},
        {"data1": "1", "data2": "1"},
        {"data1": "150", "data2": "160"},
    ],
}


def _session(
    *,
    ktb_10y: str | None = "3.0",
    corp_aa_3y: str | None = "4.0",
    candles=None,
    estimate=None,
    shares=None,
) -> _Session:
    candles = [_candle("20261017", "120000")] if candles is None else candles
    estimate = dict(ESTIMATE) if estimate is None else estimate
    shares = list(SHARES) if shares is None else shares
    return _Session(_Kis(candles, estimate), _Dart(_statements(), shares), _Ecos(ktb_10y, corp_aa_3y))


def _base_params(**overrides) -> dict:
    params = {
        "stock_code": "000001",
        "corp_code": "00000001",
        "as_of": "20261018",
        "erp": 6.0,
        "tax_rate": 22.0,
    }
    params.update(overrides)
    return params


def test_implied_expectations_computes_rim_and_reverse_dcf_without_damodaran() -> None:
    session = _session()

    out = handlers.handle_kis_implied_expectations(_base_params(), session)

    assert out["market_cap"] == pytest.approx(1200)  # 120,000 x 1,000,000 / 1e8
    assert out["equity_owners"] == pytest.approx(2000)
    assert out["borrowings"] == pytest.approx(500)
    assert out["cash"] == pytest.approx(100)
    assert out["ev"] == pytest.approx(1200 + 500 - 100)
    assert out["ttm_revenue"] == pytest.approx(2000)
    assert out["ttm_operating_margin"] == pytest.approx(20.0)

    assert out["rim"]["reason"] is None
    assert out["rim"]["implied_roe"] is not None
    assert out["reverse_dcf"]["reason"] is None
    assert out["reverse_dcf"]["implied_revenue_growth"] is not None
    assert out["reverse_dcf"]["margin_assumption"] == "ttm_operating_margin"

    alternative = out["reverse_dcf"]["alternative_dart_3y_avg_margin"]
    assert alternative["margin_assumption"] == "dart_3y_avg_operating_margin"
    assert alternative["operating_margin"] == pytest.approx((20.0 + 15.0 + 14.0) / 3)
    assert alternative["reason"] is None
    assert alternative["implied_revenue_growth"] is not None
    # A lower average margin than the TTM one implies a higher revenue growth is needed to hit the same EV.
    assert alternative["implied_revenue_growth"] > out["reverse_dcf"]["implied_revenue_growth"]

    assert out["assumptions"]["erp"] == {"value": 6.0, "source": "param", "updated": None}
    assert out["assumptions"]["tax_rate"] == {"value": 22.0, "source": "param"}
    assert out["assumptions"]["risk_free"]["value"] == pytest.approx(3.0)
    assert out["assumptions"]["cost_of_debt"]["value"] == pytest.approx(4.0)

    assert out["comparison"]["dart_roe_latest_fy"] is not None
    assert out["comparison"]["dart_revenue_cagr_3y"] is not None
    assert out["comparison"]["dart_operating_margin_3y_avg"] == pytest.approx((20.0 + 15.0 + 14.0) / 3)
    assert out["comparison"]["kis_estimate_roe"] == [
        {"period": "2025.12", "estimate": False, "roe": 15.0},
        {"period": "2026.12E", "estimate": True, "roe": 16.0},
    ]

    # 2 KIS (price, estimate) + dart_calls (quarters window + extra annual) + 1 share + 2 ECOS
    assert session.kis.calls[0][0] == "period"
    assert ("estimate", "000001") in session.kis.calls
    assert session.dart.calls[-1][0] == "shares"
    assert {call[0] for call in session.ecos.calls} == {"817Y002"}


def test_implied_expectations_sensitivity_varies_one_factor_at_a_time() -> None:
    out = handlers.handle_kis_implied_expectations(_base_params(), _session())

    roe_rows = out["sensitivity"]["rim_implied_roe"]
    growth_rows = out["sensitivity"]["reverse_dcf_implied_growth"]
    assert len(roe_rows) == 5  # erp -1/0/+1 at years_delta 0, plus years -5/+5 at erp_delta 0
    assert {(row["erp_delta"], row["years_delta"]) for row in roe_rows} == {
        (-1.0, 0),
        (0.0, 0),
        (1.0, 0),
        (0.0, -5),
        (0.0, 5),
    }
    assert len(growth_rows) == 5


def test_implied_expectations_uses_damodaran_only_when_erp_or_tax_rate_is_missing(monkeypatch) -> None:
    calls = []

    def fake_damodaran():
        calls.append(1)
        return {"erp": 5.5, "tax_rate": 23.0, "updated": "2026-01-15"}

    monkeypatch.setattr(handlers, "_fetch_damodaran_korea", fake_damodaran)

    handlers.handle_kis_implied_expectations(_base_params(), _session())
    # erp/tax_rate both given: no damodaran fetch
    assert calls == []

    out = handlers.handle_kis_implied_expectations({k: v for k, v in _base_params().items() if k != "erp"}, _session())
    assert calls == [1]
    assert out["assumptions"]["erp"] == {
        "value": 5.5,
        "source": "Damodaran Korea (cluefin-feeds)",
        "updated": "2026-01-15",
    }


def test_implied_expectations_without_erp_and_failing_damodaran_is_exit_4(monkeypatch) -> None:
    def failing_damodaran():
        raise RuntimeError("network down")

    monkeypatch.setattr(handlers, "_fetch_damodaran_korea", failing_damodaran)

    params = {k: v for k, v in _base_params().items() if k != "erp"}
    with pytest.raises(CliError) as info:
        handlers.handle_kis_implied_expectations(params, _session())

    # A fetch failure is a broker/network problem, not a credentials problem.
    assert info.value.exit_code == EXIT_BROKER
    assert info.value.error_type == "BrokerUnavailable"
    assert info.value.retryable is True
    assert "erp" in (info.value.hint or "")


def test_implied_expectations_missing_risk_free_rate_is_exit_4() -> None:
    session = _session(ktb_10y=None)
    with pytest.raises(CliError) as info:
        handlers.handle_kis_implied_expectations(_base_params(), session)

    assert info.value.exit_code == EXIT_BROKER
    assert info.value.error_type == "BrokerUnavailable"
    assert info.value.retryable is True
    # ECOS was tried before falling over to Damodaran/the rest of the computation.
    assert ("817Y002", "D", "20261004", "20261018", ("010210000",)) in session.ecos.calls


def test_implied_expectations_missing_cost_of_debt_rate_is_exit_4() -> None:
    session = _session(corp_aa_3y=None)
    with pytest.raises(CliError) as info:
        handlers.handle_kis_implied_expectations(_base_params(), session)

    assert info.value.exit_code == EXIT_BROKER
    assert info.value.error_type == "BrokerUnavailable"


def test_implied_expectations_without_a_close_is_exit_4_before_any_dart_call() -> None:
    session = _session(candles=[])
    with pytest.raises(CliError) as info:
        handlers.handle_kis_implied_expectations(_base_params(), session)
    assert info.value.exit_code == EXIT_BROKER
    assert session.dart.calls == []


def test_implied_expectations_without_borrowings_leaves_ev_and_reverse_dcf_empty() -> None:
    statements = {
        key: [row for row in rows if row.get("account_nm") != "단기차입금"] for key, rows in _statements().items()
    }
    session = _Session(
        _Kis([_candle("20261017", "120000")], dict(ESTIMATE)), _Dart(statements, list(SHARES)), _Ecos("3.0", "4.0")
    )

    out = handlers.handle_kis_implied_expectations(_base_params(), session)

    assert out["borrowings"] is None
    assert out["ev"] is None  # not 1200 + 0 - 100
    assert "borrowings" in out["ev_reason"]
    assert out["reverse_dcf"]["reason"] == "missing_revenue_margin_ev_or_wacc"
    assert out["rim"]["implied_roe"] is not None  # RIM needs no debt


def test_implied_expectations_without_shares_has_no_rim_or_reverse_dcf_solution() -> None:
    out = handlers.handle_kis_implied_expectations(_base_params(), _session(shares=[]))
    assert out["market_cap"] is None
    assert out["rim"]["implied_roe"] is None
    assert out["rim"]["reason"] == "missing_book_equity_or_market_cap"
    assert out["reverse_dcf"]["reason"] == "missing_revenue_margin_ev_or_wacc"
