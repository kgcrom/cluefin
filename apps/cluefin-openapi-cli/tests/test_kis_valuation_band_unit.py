"""`kis stock valuation-band` — local cache daily closes × per-year DART EPS/BPS.

A fake DART answers one annual report (11011, CFS) and one share count per fiscal year; the
local cache is a real in-memory DuckDB (`cache.store.open_store(":memory:")`) seeded with a
handful of bars, so `cache_store.open_store` is monkeypatched to return it instead of opening
`~/.cache/cluefin/market.duckdb`. Numbers are chosen so every quantile can be hand-checked
(see `test_band_unit.py` for the same arithmetic in isolation).
"""

from __future__ import annotations

import pytest

from cluefin_openapi_cli.cache import store as cache_store
from cluefin_openapi_cli.errors import EXIT_BROKER, CliError
from cluefin_openapi_cli.handlers.kis import domestic_stock_info as handlers

EOK = 100_000_000


class _Row:
    def __init__(self, data: dict) -> None:
        self._data = data

    def model_dump(self) -> dict:
        return dict(self._data)


def _income(amount: float, rcept_no: str) -> dict:
    return {
        "sj_div": "CIS",
        "account_id": "ifrs-full_ProfitLossAttributableToOwnersOfParent",
        "thstrm_amount": str(amount),
        "rcept_no": rcept_no,
    }


def _equity(amount: float, rcept_no: str) -> dict:
    return {
        "sj_div": "BS",
        "account_id": "ifrs-full_EquityAttributableToOwnersOfParent",
        "thstrm_amount": str(amount),
        "rcept_no": rcept_no,
    }


SHARES = (
    {"se": "보통주", "istc_totqy": "1,000,000", "tesstk_co": "0", "distb_stock_co": "1,000,000"},
    {"se": "우선주", "istc_totqy": "10,000", "tesstk_co": "0", "distb_stock_co": "10,000"},
)


def _statements() -> dict:
    """FY2023: 지배주주순이익 100억, 지배지분 1,000억 → EPS 10,000/BPS 100,000 (shares 1,000,000).

    FY2024: 200억/1,500억 → EPS 20,000/BPS 150,000. Bars from 2024-04-01 use FY2023, from 2025-04-01 FY2024.
    """
    return {
        (2023, "11011", "CFS"): [
            _income(100 * EOK, "20240315000001"),
            _equity(1000 * EOK, "20240315000001"),
        ],
        (2024, "11011", "CFS"): [
            _income(200 * EOK, "20250315000001"),
            _equity(1500 * EOK, "20250315000001"),
        ],
    }


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


class _Session:
    def __init__(self, dart: _Dart) -> None:
        self.dart = dart

    def get_dart(self):
        return type(
            "Client",
            (),
            {"periodic_report_financial_statement": self.dart, "periodic_report_key_information": self.dart},
        )()


def _session(statements=None, shares=None) -> _Session:
    statements = _statements() if statements is None else statements
    shares = list(SHARES) if shares is None else shares
    return _Session(_Dart(statements, shares))


def _seed_cache(conn, code: str, bars: list[tuple[str, float]]) -> None:
    for day, close in bars:
        conn.execute(
            "INSERT INTO ohlcv (code, date, close) VALUES (?, ?, ?)",
            [code, day, close],
        )


BARS = [
    ("2024-06-01", 15000.0),
    ("2024-12-01", 20000.0),
    ("2025-06-01", 18000.0),
    ("2025-10-01", 22000.0),
]


@pytest.fixture
def cache_conn(monkeypatch):
    conn = cache_store.open_store(":memory:")
    _seed_cache(conn, "000001", BARS)
    monkeypatch.setattr(handlers.cache_store, "open_store", lambda *a, **k: conn)
    return conn


def test_valuation_band_computes_quantiles_and_current_percentile(cache_conn) -> None:
    session = _session()

    out = handlers.handle_kis_stock_valuation_band(
        {"stock_code": "000001", "corp_code": "00000001", "as_of": "20260331", "years": 2}, session
    )

    # window 2024-03-31..2026-03-31 → trailing fiscal years 2022..2024 (FY2022 has no report here)
    assert out["years"] == [2022, 2023, 2024]
    assert out["statement_basis"] == "CFS"
    assert out["current"] == {"close": 22000.0, "date": "2025-10-01", "eps_bps_year": 2024}

    per = out["per"]
    assert per["n"] == 4
    assert per["quantiles"] == {"min": 0.9, "p25": 1.05, "median": 1.3, "p75": 1.625, "max": 2.0}
    assert per["current"] == pytest.approx(1.1)
    assert per["current_percentile"] == pytest.approx(50.0)

    pbr = out["pbr"]
    assert pbr["n"] == 4
    assert pbr["quantiles"] == {"min": 0.12, "p25": 0.14, "median": 0.1483, "p75": 0.1625, "max": 0.2}
    assert pbr["current"] == pytest.approx(0.1467, rel=1e-3)
    assert pbr["current_percentile"] == pytest.approx(50.0)

    assert out["calls"] == 5  # 3 statements (CFS) + 2 share-count (only years with a report)
    assert session.dart.calls == [
        ("statements", "2022", "11011", "CFS"),
        ("statements", "2023", "11011", "CFS"),
        ("statements", "2024", "11011", "CFS"),
        ("shares", "2023", "11011"),
        ("shares", "2024", "11011"),
    ]


def test_valuation_band_falls_back_to_ofs_when_cfs_is_empty(cache_conn) -> None:
    ofs_statements = {(year, "11011", "OFS"): rows for (year, _code, _fs), rows in _statements().items()}
    session = _session(statements=ofs_statements)

    out = handlers.handle_kis_stock_valuation_band(
        {"stock_code": "000001", "corp_code": "00000001", "as_of": "20260331", "years": 2}, session
    )

    assert out["statement_basis"] == "OFS"
    assert out["calls"] == 3 + 3 + 2  # CFS attempt (3, empty) + OFS attempt (3) + share-count (2)


def test_valuation_band_without_any_annual_report_is_exit_4(cache_conn) -> None:
    session = _session(statements={})

    with pytest.raises(CliError) as info:
        handlers.handle_kis_stock_valuation_band(
            {"stock_code": "000001", "corp_code": "00000001", "as_of": "20260331", "years": 2}, session
        )

    assert info.value.exit_code == EXIT_BROKER
    assert all(call[0] != "shares" for call in session.dart.calls)


def test_valuation_band_without_cached_bars_is_exit_4(monkeypatch) -> None:
    conn = cache_store.open_store(":memory:")  # empty: no ohlcv rows for this code
    monkeypatch.setattr(handlers.cache_store, "open_store", lambda *a, **k: conn)
    session = _session()

    with pytest.raises(CliError) as info:
        handlers.handle_kis_stock_valuation_band(
            {"stock_code": "000001", "corp_code": "00000001", "as_of": "20260331", "years": 2}, session
        )

    assert info.value.exit_code == EXIT_BROKER


def test_valuation_band_drops_a_year_whose_shares_are_missing(cache_conn) -> None:
    session = _session(shares=[])

    out = handlers.handle_kis_stock_valuation_band(
        {"stock_code": "000001", "corp_code": "00000001", "as_of": "20260331", "years": 2}, session
    )

    assert out["years_detail"] == [
        {
            "year": 2023,
            "net_income_owners": pytest.approx(100 * EOK),
            "equity_owners": pytest.approx(1000 * EOK),
            "shares": None,
            "eps": None,
            "bps": None,
        },
        {
            "year": 2024,
            "net_income_owners": pytest.approx(200 * EOK),
            "equity_owners": pytest.approx(1500 * EOK),
            "shares": None,
            "eps": None,
            "bps": None,
        },
    ]
    assert out["current"]["eps_bps_year"] is None
    assert out["per"]["n"] == 0
    assert out["per"]["current"] is None


def test_valuation_band_never_pairs_a_bar_with_a_report_not_yet_due(cache_conn) -> None:
    """A 2025-03 bar must use FY2023, not FY2024 (whose report is due 2025-03-31)."""
    cache_conn.execute("INSERT INTO ohlcv (code, date, close) VALUES ('000001', '2025-03-01', 30000.0)")
    session = _session()

    out = handlers.handle_kis_stock_valuation_band(
        {"stock_code": "000001", "corp_code": "00000001", "as_of": "20260331", "years": 2}, session
    )

    assert out["per"]["n"] == 5
    assert out["per"]["quantiles"]["max"] == pytest.approx(3.0)  # 30,000 / FY2023 EPS 10,000
