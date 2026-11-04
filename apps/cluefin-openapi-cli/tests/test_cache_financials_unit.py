"""`cache load --only financials`: DART `fnlttMultiAcnt`, batched 100 at a time, CFS over OFS."""

from __future__ import annotations

import json
from datetime import date, datetime
from types import SimpleNamespace

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.financials import (
    ANNUAL_REPORT_CODE,
    BATCH_SIZE,
    _fetch,
    default_years,
    load_financials,
)
from cluefin_openapi_cli.cache.read import read_financials
from cluefin_openapi_cli.main import run_cli


def _item(stock_code: str, account_nm: str, amount: str, *, fs_div: str = "CFS", currency: str = "KRW"):
    return SimpleNamespace(
        stock_code=stock_code, fs_div=fs_div, account_nm=account_nm, thstrm_amount=amount, currency=currency
    )


def _result(status: str, items: list | None, *, message: str = ""):
    return SimpleNamespace(result=SimpleNamespace(status=status, message=message, list=items))


class FakeDart:
    def __init__(self, by_year: dict[str, list]) -> None:
        self.by_year = by_year
        self.calls: list[tuple[tuple[str, ...], str]] = []
        self.periodic_report_financial_statement = self

    def get_multi_company_major_accounts(self, *, corp_code: str, bsns_year: str, reprt_code: str):
        assert reprt_code == ANNUAL_REPORT_CODE
        codes = tuple(corp_code.split(","))
        self.calls.append((codes, bsns_year))
        return self.by_year.get(bsns_year, _result("013", None))


def _conn_with_companies(pairs: list[tuple[str, str]]):
    conn = store.open_store(":memory:")
    conn.executemany(
        "INSERT INTO company (code, name, corp_code) VALUES (?, 'X', ?)",
        pairs,
    )
    return conn


def test_default_years_is_five_years_ending_last_year() -> None:
    assert default_years(date(2026, 11, 4)) == ("2021", "2022", "2023", "2024", "2025")


def test_loads_rows_and_marks_the_fetch_log() -> None:
    conn = _conn_with_companies([("005930", "00126380"), ("000660", "00164779")])
    dart = FakeDart(
        {
            "2025": _result(
                "000",
                [
                    _item("005930", "자본총계", "1000"),
                    _item("005930", "영업이익", "200"),
                    _item("000660", "자본총계", "500"),
                ],
            )
        }
    )

    stats = load_financials(conn, dart=dart, years=("2025",))

    assert stats.calls == 1
    assert stats.rows == 3
    assert stats.codes_ok == 2
    rows = conn.execute("SELECT code, account_nm, amount, basis FROM financials ORDER BY code, account_nm").fetchall()
    assert rows == [
        ("000660", "자본총계", 500.0, "CFS"),
        ("005930", "영업이익", 200.0, "CFS"),
        ("005930", "자본총계", 1000.0, "CFS"),
    ]
    log = conn.execute("SELECT code, status FROM financials_fetch_log ORDER BY code").fetchall()
    assert log == [("000660", "ok"), ("005930", "ok")]


def test_prefers_cfs_over_ofs_for_the_same_account() -> None:
    conn = _conn_with_companies([("005930", "00126380")])
    dart = FakeDart(
        {
            "2025": _result(
                "000",
                [
                    _item("005930", "자본총계", "999", fs_div="OFS"),
                    _item("005930", "자본총계", "1000", fs_div="CFS"),
                ],
            )
        }
    )

    load_financials(conn, dart=dart, years=("2025",))

    row = conn.execute("SELECT amount, basis FROM financials WHERE code = '005930'").fetchone()
    assert row == (1000.0, "CFS")


def test_company_with_no_filing_is_marked_empty_not_retried() -> None:
    conn = _conn_with_companies([("005930", "00126380"), ("000660", "00164779")])
    dart = FakeDart({"2025": _result("000", [_item("005930", "자본총계", "1000")])})

    stats = load_financials(conn, dart=dart, years=("2025",))

    assert stats.codes_ok == 1
    assert stats.codes_empty == 1
    log = dict(conn.execute("SELECT code, status FROM financials_fetch_log").fetchall())
    assert log == {"005930": "ok", "000660": "empty"}

    # A second run must not re-ask DART for either code.
    dart.calls.clear()
    stats2 = load_financials(conn, dart=dart, years=("2025",))
    assert dart.calls == []
    assert stats2.calls == 0
    assert stats2.codes_skipped == 2


def test_batches_at_one_hundred_codes() -> None:
    pairs = [(f"{i:06d}", f"c{i:08d}") for i in range(BATCH_SIZE + 1)]
    conn = _conn_with_companies(pairs)
    dart = FakeDart({"2025": _result("013", None)})

    load_financials(conn, dart=dart, years=("2025",))

    assert [len(call[0]) for call in dart.calls] == [BATCH_SIZE, 1]


def test_daily_quota_stops_the_load_without_raising() -> None:
    conn = _conn_with_companies([("005930", "00126380")])
    dart = FakeDart({"2025": _result("020", None, message="사용한도 초과")})

    stats = load_financials(conn, dart=dart, years=("2025", "2026"))

    assert stats.errors
    assert conn.execute("SELECT count(*) FROM financials_fetch_log").fetchone()[0] == 0


def test_reruns_skip_the_second_year_too() -> None:
    conn = _conn_with_companies([("005930", "00126380")])
    dart = FakeDart(
        {
            "2024": _result("000", [_item("005930", "자본총계", "900")]),
            "2025": _result("000", [_item("005930", "자본총계", "1000")]),
        }
    )

    load_financials(conn, dart=dart, years=("2024", "2025"))

    assert dart.calls == [(("00126380",), "2024"), (("00126380",), "2025")]
    assert conn.execute("SELECT count(*) FROM financials WHERE code = '005930'").fetchone()[0] == 2


def test_company_limit_exceeded_splits_the_batch_in_half() -> None:
    """Defensive: `BATCH_SIZE` already caps at 100, but 021 (>100) must not be fatal."""

    class SplittingDart:
        def __init__(self) -> None:
            self.calls: list[tuple[str, ...]] = []
            self.periodic_report_financial_statement = self

        def get_multi_company_major_accounts(self, *, corp_code: str, bsns_year: str, reprt_code: str):
            codes = tuple(corp_code.split(","))
            self.calls.append(codes)
            if len(codes) > 1:
                return _result("021", None)
            return _result("000", [_item(codes[0], "자본총계", f"{int(codes[0]) * 10}")])

    dart = SplittingDart()
    outcome = _fetch(dart, ["1", "2", "3", "4"], "2025")

    assert {item.stock_code for item in outcome.items} == {"1", "2", "3", "4"}
    assert not outcome.failed_corp_codes
    assert outcome.calls == len(dart.calls) == 7  # 1 (4-way) + 2 (2-way) + 4 (singles)


def test_fetch_deduplicates_corp_codes_before_calling() -> None:
    """A preferred share remaps to its common share's corp_code — the batch must not repeat it."""

    class RecordingDart:
        def __init__(self) -> None:
            self.calls: list[tuple[str, ...]] = []
            self.periodic_report_financial_statement = self

        def get_multi_company_major_accounts(self, *, corp_code: str, bsns_year: str, reprt_code: str):
            codes = tuple(corp_code.split(","))
            self.calls.append(codes)
            return _result("000", [_item(codes[0], "자본총계", "1")])

    dart = RecordingDart()
    outcome = _fetch(dart, ["A", "B", "A"], "2025")

    assert dart.calls == [("A", "B")]
    assert outcome.calls == 1


def test_one_bad_corp_code_is_isolated_and_the_rest_still_succeed() -> None:
    """A record that always fails validation must not sink the other 99 in its batch."""

    class FlakyDart:
        def __init__(self) -> None:
            self.calls: list[tuple[str, ...]] = []
            self.periodic_report_financial_statement = self

        def get_multi_company_major_accounts(self, *, corp_code: str, bsns_year: str, reprt_code: str):
            codes = tuple(corp_code.split(","))
            self.calls.append(codes)
            if "BAD0000" in codes:
                raise ValueError("boom: this corp_code always fails")
            return _result("000", [_item(c, "자본총계", "1") for c in codes])

    dart = FlakyDart()
    good_codes = [f"G{i:06d}" for i in range(7)]
    all_codes = [*good_codes[:3], "BAD0000", *good_codes[3:]]

    outcome = _fetch(dart, all_codes, "2025")

    assert outcome.failed_corp_codes == ("BAD0000",)
    assert "boom" in outcome.error_samples[0]
    assert {item.stock_code for item in outcome.items} == set(good_codes)


def test_quota_hit_while_narrowing_stops_without_finishing_the_batch() -> None:
    class QuotaMidwayDart:
        def __init__(self) -> None:
            self.periodic_report_financial_statement = self

        def get_multi_company_major_accounts(self, *, corp_code: str, bsns_year: str, reprt_code: str):
            codes = tuple(corp_code.split(","))
            if len(codes) > 1:
                return _result("021", None)
            if codes[0] == "1":
                from cluefin_openapi_cli.errors import DartQuotaExceededAPIError

                raise DartQuotaExceededAPIError("한도 초과")
            return _result("000", [_item(codes[0], "자본총계", "1")])

    dart = QuotaMidwayDart()
    outcome = _fetch(dart, ["1", "2", "3", "4"], "2025")

    assert outcome.quota_exhausted is True


def test_load_financials_marks_the_isolated_bad_code_as_error_and_keeps_the_rest() -> None:
    conn = _conn_with_companies([("005930", "00126380"), ("000660", "00164779"), ("005380", "00164742")])
    stock_code_of = {"00126380": "005930", "00164779": "000660", "00164742": "005380"}

    class FlakyDart:
        def __init__(self) -> None:
            self.periodic_report_financial_statement = self

        def get_multi_company_major_accounts(self, *, corp_code: str, bsns_year: str, reprt_code: str):
            codes = tuple(corp_code.split(","))
            if "00164742" in codes:
                raise ValueError("boom")
            return _result("000", [_item(stock_code_of[c], "자본총계", "1") for c in codes])

    stats = load_financials(conn, dart=FlakyDart(), years=("2025",))

    assert stats.failed_codes == 1
    log = dict(conn.execute("SELECT code, status FROM financials_fetch_log").fetchall())
    assert log == {"005930": "ok", "000660": "ok", "005380": "error"}
    assert conn.execute("SELECT count(*) FROM financials WHERE code = '005380'").fetchone()[0] == 0

    # The `error` pair is retried on the next run; `ok` pairs are not.
    stats2 = load_financials(conn, dart=FlakyDart(), years=("2025",))
    assert stats2.codes_skipped == 2
    assert stats2.failed_codes == 1


def test_loaded_at_is_recorded() -> None:
    conn = _conn_with_companies([("005930", "00126380")])
    dart = FakeDart({"2025": _result("000", [_item("005930", "자본총계", "1000")])})

    load_financials(conn, dart=dart, years=("2025",))

    loaded_at = conn.execute("SELECT loaded_at FROM financials").fetchone()[0]
    assert isinstance(loaded_at, datetime)


def test_read_financials_groups_by_year_newest_first() -> None:
    conn = store.open_store(":memory:")
    conn.executemany(
        "INSERT INTO financials (code, year, reprt_code, basis, account_nm, amount, currency, loaded_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("005930", "2024", "11011", "CFS", "자본총계", 1000.0, "KRW", datetime(2026, 1, 1)),
            ("005930", "2024", "11011", "CFS", "영업이익", 200.0, "KRW", datetime(2026, 1, 1)),
            ("005930", "2025", "11011", "CFS", "자본총계", 1100.0, "KRW", datetime(2026, 1, 1)),
        ],
    )

    payload = read_financials(conn, "005930")

    assert payload["count"] == 2
    assert [row["year"] for row in payload["years"]] == ["2025", "2024"]
    assert payload["years"][1]["accounts"] == {"자본총계": 1000.0, "영업이익": 200.0}
    assert payload["years"][1]["basis"] == "CFS"
    assert payload["notes"]


def test_read_financials_year_range_filters() -> None:
    conn = store.open_store(":memory:")
    conn.executemany(
        "INSERT INTO financials (code, year, reprt_code, basis, account_nm, amount, currency, loaded_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("005930", "2021", "11011", "CFS", "자본총계", 1.0, "KRW", datetime(2026, 1, 1)),
            ("005930", "2023", "11011", "CFS", "자본총계", 2.0, "KRW", datetime(2026, 1, 1)),
            ("005930", "2025", "11011", "CFS", "자본총계", 3.0, "KRW", datetime(2026, 1, 1)),
        ],
    )

    payload = read_financials(conn, "005930", since_year="2022", until_year="2024")

    assert [row["year"] for row in payload["years"]] == ["2023"]


def test_cli_cache_financials_reads_from_the_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    conn = store.open_store()
    conn.execute(
        "INSERT INTO financials (code, year, reprt_code, basis, account_nm, amount, currency, loaded_at) "
        "VALUES ('005930', '2025', '11011', 'CFS', '자본총계', 1000.0, 'KRW', ?)",
        [datetime(2026, 1, 1)],
    )
    conn.close()

    result = run_cli(["cache", "financials", "--code", "005930", "--json"])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["years"][0]["accounts"]["자본총계"] == 1000.0


def test_cli_cache_financials_requires_code(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    store.open_store().close()

    result = run_cli(["cache", "financials", "--json"])

    assert result.exit_code == 2
