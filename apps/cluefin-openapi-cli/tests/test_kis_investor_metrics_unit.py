"""`kis stock investor-metrics` — one fake session answering KIS (price, estimate) and DART (full
statements, two share-count calls: latest report and the oldest of the 3 DART fiscal years).

The metric math itself is covered with synthetic figures in test_investor_metrics_unit.py and
test_quality_unit.py (altman_z); this file drives the handler end to end so call counts and the
null-propagation wiring (missing D&A, missing share count) can be asserted on round numbers.
"""

from __future__ import annotations

import pytest

from cluefin_openapi_cli.errors import EXIT_BROKER, CliError
from cluefin_openapi_cli.handlers.kis import domestic_stock_info as handlers

EOK = 100_000_000  # 1억원 in 원, same convention as test_kis_opinion_valuation_unit.py


class _Row:
    def __init__(self, data: dict) -> None:
        self._data = data

    def model_dump(self) -> dict:
        return dict(self._data)


class _Dart:
    def __init__(self, statements: dict, shares_by_year: dict[str, list[dict]]) -> None:
        self._statements = statements
        self._shares_by_year = shares_by_year
        self.calls: list[tuple] = []

    def get_single_company_full_statements(self, corp_code, bsns_year, reprt_code, fs_div):
        self.calls.append(("statements", bsns_year, reprt_code, fs_div))
        rows = self._statements.get((int(bsns_year), reprt_code, fs_div), [])
        return type("R", (), {"result": type("E", (), {"status": "000", "list": [_Row(r) for r in rows]})()})()

    def get_total_number_of_shares(self, corp_code, bsns_year, reprt_code):
        self.calls.append(("shares", bsns_year, reprt_code))
        rows = self._shares_by_year.get(bsns_year, [])
        return type("R", (), {"result": type("E", (), {"status": "000", "list": [_Row(r) for r in rows]})()})()


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


def _row(account_id: str, sj_div: str, **amounts) -> dict:
    return {"sj_div": sj_div, "account_id": account_id, **amounts}


def _income(account_id: str, **amounts) -> dict:
    return _row(account_id, "CIS", **amounts)


def _bs(account_id: str, **amounts) -> dict:
    return _row(account_id, "BS", **amounts)


def _cf(account_id: str, **amounts) -> dict:
    return _row(account_id, "CF", **amounts)


def _borrowings_row(**amounts) -> dict:
    """`statements.borrowings` matches by `account_nm` label (regex), not `account_id`."""
    return {"sj_div": "BS", "account_nm": "단기차입금", **amounts}


def _won(eok_value: float) -> str:
    return str(int(eok_value * EOK))


def _quarter_rows(net_income_single, net_income_ytd, prior_single, prior_ytd) -> list[dict]:
    """One quarterly report's income rows — net income and operating income move together."""
    amounts = dict(
        thstrm_amount=_won(net_income_single),
        thstrm_add_amount=_won(net_income_ytd),
        frmtrm_q_amount=_won(prior_single),
        frmtrm_add_amount=_won(prior_ytd),
    )
    return [
        _income("ifrs-full_ProfitLossAttributableToOwnersOfParent", **amounts),
        _income("dart_OperatingIncomeLoss", **amounts),
        _income("ifrs-full_Revenue", **amounts),
        _bs("ifrs-full_CashAndCashEquivalents", thstrm_amount=_won(250)),
        _borrowings_row(thstrm_amount=_won(520)),
    ]


def _statements_fixture() -> dict:
    """FY2023/2024/2025 from one 11011 report (annual window year=2026), plus TTM quarters to 2026Q1."""
    rcept = "20260315000001"
    annual_row = [
        _income(
            "ifrs-full_ProfitLossAttributableToOwnersOfParent",
            bfefrmtrm_amount=_won(300),
            frmtrm_amount=_won(350),
            thstrm_amount=_won(400),
        ),
        _income("dart_OperatingIncomeLoss", thstrm_amount=_won(400)),
        _income("ifrs-full_Revenue", thstrm_amount=_won(400)),
        _bs("ifrs-full_Assets", thstrm_amount=_won(6000)),
        _bs("ifrs-full_Liabilities", thstrm_amount=_won(2700)),
        _bs("ifrs-full_RetainedEarnings", thstrm_amount=_won(1500)),
        _bs(
            "ifrs-full_CurrentAssets",
            bfefrmtrm_amount=_won(2000),
            frmtrm_amount=_won(2200),
            thstrm_amount=_won(2500),
        ),
        _bs(
            "ifrs-full_CurrentLiabilities",
            bfefrmtrm_amount=_won(1000),
            frmtrm_amount=_won(1100),
            thstrm_amount=_won(1200),
        ),
        _cf("ifrs-full_CashFlowsFromUsedInOperatingActivities", thstrm_amount=_won(150)),
        _cf("ifrs-full_PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities", thstrm_amount=_won(60)),
        _cf("ifrs-full_DepreciationExpense", thstrm_amount=_won(40)),
        _cf("ifrs-full_AmortisationExpense", thstrm_amount=_won(5)),
        _cf("ifrs-full_DividendsPaidClassifiedAsFinancingActivities", thstrm_amount=_won(-50)),
        _cf("dart_AcquisitionOfTreasuryShares", thstrm_amount=_won(-30)),
        _cf("ifrs-full_ProceedsFromSaleOrDisposalOfEntitysSharesHeld", thstrm_amount=_won(10)),
        _cf("ifrs-full_ProceedsFromIssuingShares", thstrm_amount=_won(5)),
        {"rcept_no": rcept},
    ]
    return {
        (2025, "11013", "CFS"): _quarter_rows(100, 100, 100, 100) + [{"rcept_no": "20250515000001"}],
        (2025, "11012", "CFS"): _quarter_rows(100, 200, 100, 200) + [{"rcept_no": "20250815000001"}],
        (2025, "11014", "CFS"): _quarter_rows(100, 300, 100, 300) + [{"rcept_no": "20251115000001"}],
        (2025, "11011", "CFS"): annual_row,
        (2026, "11013", "CFS"): _quarter_rows(100, 100, 100, 100) + [{"rcept_no": "20260515000001"}],
    }


LATEST_SHARES = ({"se": "보통주", "istc_totqy": "1,000,000", "tesstk_co": "-", "distb_stock_co": "1,000,000"},)
OLDEST_SHARES = ({"se": "보통주", "istc_totqy": "800,000", "tesstk_co": "-", "distb_stock_co": "800,000"},)

ESTIMATE = {
    "output4": [{"dt": "2025.12"}, {"dt": "2026.12E"}],
    # layout order: ebitda, eps, eps_growth_yoy, ... — only the first three rows are supplied.
    "output3": [
        {"data1": "1", "data2": "1"},
        {"data1": "1", "data2": "1"},
        {"data1": "150", "data2": "200"},  # eps_growth_yoy ×10 on the wire: 15.0% / 20.0%
    ],
}


def _session(candles=None, shares_by_year=None, statements=None, estimate=None) -> _Session:
    candles = [_candle("20261016", "100000"), _candle("20261017", "100000")] if candles is None else candles
    shares_by_year = (
        {"2026": list(LATEST_SHARES), "2023": list(OLDEST_SHARES)} if shares_by_year is None else shares_by_year
    )
    statements = _statements_fixture() if statements is None else statements
    estimate = dict(ESTIMATE) if estimate is None else estimate
    return _Session(_Kis(candles, estimate), _Dart(statements, shares_by_year))


def _call(session=None, **params) -> dict:
    session = session or _session()
    return handlers.handle_kis_investor_metrics(
        {"stock_code": "000001", "corp_code": "00000001", "as_of": "20261018", **params}, session
    )


def test_investor_metrics_computes_every_block_from_the_three_sources() -> None:
    session = _session()

    out = _call(session)

    assert out["market_cap"] == pytest.approx(1000.0)  # 100,000 × 1,000,000 / 1e8
    assert out["ev"] == pytest.approx(1000.0 + 520.0 - 250.0)
    assert out["per_ttm"] == pytest.approx(2.5)  # 1000 / 400 (TTM net income owners)

    assert out["fcf_yield"]["value"] == pytest.approx(9.0)  # (150-60)/1000 * 100
    assert out["fcf_yield"]["reason"] is None

    owner_earnings = 400.0 + 40.0 + 5.0 - 60.0 - (1300.0 - 1100.0)  # 185
    assert out["owner_earnings"]["value"] == pytest.approx(owner_earnings)
    assert out["owner_earnings_yield"]["value"] == pytest.approx(owner_earnings / 1000.0 * 100)

    assert out["ev_ebit"]["value"] == pytest.approx(out["ev"] / 400.0)  # TTM operating income 400
    assert out["earnings_yield"]["value"] == pytest.approx(400.0 / out["ev"] * 100)

    assert out["shareholder_yield"]["value"] == pytest.approx((50.0 + 30.0 - 10.0 - 5.0) / 1000.0 * 100)

    assert out["altman_z"]["value"] is not None
    assert out["altman_z"]["missing"] == []

    dart_peg = out["peg"]["dart_3y_eps_cagr"]
    assert dart_peg["growth_pct"] == pytest.approx(((40000.0 / 37500.0) ** 0.5 - 1) * 100)
    assert dart_peg["value"] == pytest.approx(2.5 / dart_peg["growth_pct"])

    kis_peg = out["peg"]["kis_estimated_eps_growth"]
    assert kis_peg["growth_pct"] == pytest.approx(20.0)
    assert kis_peg["value"] == pytest.approx(2.5 / 20.0)

    assert ("shares", "2026", "11013") in session.dart.calls
    assert ("shares", "2023", "11011") in session.dart.calls
    assert out["calls"] == 12


def test_investor_metrics_without_borrowings_has_no_ev_ebit() -> None:
    statements = {
        key: [row for row in rows if row.get("account_nm") != "단기차입금"]
        for key, rows in _statements_fixture().items()
    }
    out = _call(_session(statements=statements))
    assert out["ev"] is None  # not market cap − cash
    assert "borrowings" in out["ev_reason"]
    assert out["ev_ebit"]["value"] is None
    assert out["earnings_yield"]["value"] is None


def test_investor_metrics_owner_earnings_is_null_when_depreciation_is_missing() -> None:
    statements = _statements_fixture()
    annual_rows = statements[(2025, "11011", "CFS")]
    statements[(2025, "11011", "CFS")] = [
        row for row in annual_rows if row.get("account_id") != "ifrs-full_DepreciationExpense"
    ]

    out = _call(_session(statements=statements))

    assert out["owner_earnings"]["value"] is None
    assert "감가상각" in out["owner_earnings"]["reason"]
    # FCF yield is unaffected — it does not depend on D&A.
    assert out["fcf_yield"]["value"] == pytest.approx(9.0)


def test_investor_metrics_dart_peg_growth_is_null_when_oldest_share_count_is_missing() -> None:
    out = _call(_session(shares_by_year={"2026": list(LATEST_SHARES), "2023": []}))

    assert out["peg"]["dart_3y_eps_cagr"]["value"] is None
    assert out["peg"]["dart_3y_eps_cagr"]["reason"]
    # KIS-sourced PEG is independent of the DART share-count lookup.
    assert out["peg"]["kis_estimated_eps_growth"]["value"] == pytest.approx(2.5 / 20.0)


def test_investor_metrics_without_a_close_is_exit_4_before_any_dart_call() -> None:
    session = _session(candles=[])
    with pytest.raises(CliError) as info:
        _call(session)
    assert info.value.exit_code == EXIT_BROKER
    assert session.dart.calls == []


def test_investor_metrics_without_a_periodic_report_is_exit_4() -> None:
    session = _session(statements={})
    with pytest.raises(CliError) as info:
        _call(session)
    assert info.value.exit_code == EXIT_BROKER


def test_common_shares_accepts_the_long_common_stock_label() -> None:
    from cluefin_openapi_cli.handlers.kis.domestic_stock_info import _common_shares

    rows = [
        {"se": "보통주식\n(의결권 있는주식)", "istc_totqy": "1,000", "tesstk_co": "0", "distb_stock_co": "1,000"},
        {"se": "우선주식", "istc_totqy": "10", "tesstk_co": "0", "distb_stock_co": "10"},
    ]
    assert _common_shares(rows)["issued"] == 1000
