"""`cache load --only theme`: Kiwoom theme snapshot under the last trading day."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.theme import load_theme

_FRIDAY, _SATURDAY = date(2026, 10, 23), date(2026, 10, 24)


def _group(code: str, name: str) -> SimpleNamespace:
    return SimpleNamespace(
        thema_grp_cd=code,
        thema_nm=name,
        stk_num="2",
        flu_rt="-1.50",
        dt_prft_rt="+12.30",
        rising_stk_num="1",
        fall_stk_num="1",
        main_stk="알파, 베타",
    )


def _member(code: str, ret: str) -> SimpleNamespace:
    return SimpleNamespace(stk_cd=code, stk_nm=f"종목{code}", flu_rt="+1.00", dt_prft_rt_n=ret)


class FakeKiwoom:
    def __init__(self, *, fail: str | None = None, ret: str = "+5.00") -> None:
        self.pages = [
            ([_group("101", "반도체"), _group("102", "2차전지")], "Y", "k1"),
            ([_group("103", "조선")], "N", ""),
        ]
        self.fail, self.ret = fail, ret
        self.keys: list[str] = []
        self.theme = self

    def get_theme_group(self, qry, date_tp, name, flu, stex, cont_yn="N", next_key=""):  # noqa: PLR0913
        self.keys.append(next_key)
        rows, cont, key = self.pages[len(self.keys) - 1]
        return SimpleNamespace(
            body=SimpleNamespace(thema_grp=rows), headers=SimpleNamespace(cont_yn=cont, next_key=key)
        )

    def get_theme_group_stocks(self, code, stex, date_tp):
        if code == self.fail:
            raise RuntimeError("boom")
        rows = [_member("000010", self.ret), _member(f"000{code[-1]}20", "-3.00")]
        return SimpleNamespace(body=SimpleNamespace(thema_comp_stk=rows))


class FakeKis:
    """Index bars: the last one on Friday, as on a weekend."""

    def __init__(self) -> None:
        self.domestic_issue_other = self

    def get_sector_period_quote(self, market, sector, start, end, period):  # noqa: PLR0913
        rows = [
            SimpleNamespace(
                stck_bsop_date=day,
                bstp_nmix_oprc="1",
                bstp_nmix_hgpr="1",
                bstp_nmix_lwpr="1",
                bstp_nmix_prpr="1",
                acml_vol="0",
                acml_tr_pbmn="0",
            )
            for day in ("20261023", "20261022")
            if start <= day <= end
        ]
        return SimpleNamespace(body=SimpleNamespace(output2=rows))


def _load(conn, kiwoom, *, today=_SATURDAY, last_day=_SATURDAY):
    return load_theme(conn, kiwoom=kiwoom, kis=FakeKis(), today=today, last_day=last_day)


def test_snapshot_pages_groups_and_stores_under_the_last_trading_day() -> None:
    conn = store.open_store(":memory:")
    kiwoom = FakeKiwoom()

    stats = _load(conn, kiwoom)

    assert kiwoom.keys == ["", "k1"]
    assert (stats.as_of, stats.themes, stats.members, stats.errors) == (_FRIDAY, 3, 6, [])
    theme = conn.execute("SELECT name, stock_count, period_return_pct, main_stocks FROM theme WHERE theme_code='101'")
    assert theme.fetchone() == ("반도체", 2, 12.3, "알파, 베타")
    member = conn.execute("SELECT period_return_pct FROM theme_member WHERE theme_code='101' AND code='000010'")
    assert member.fetchone() == (5.0,)


def test_one_failing_theme_does_not_stop_the_snapshot() -> None:
    conn = store.open_store(":memory:")

    stats = _load(conn, FakeKiwoom(fail="102"))

    assert stats.themes == 2
    assert stats.errors[0]["code"] == "102"


def test_rerun_on_the_same_day_replaces_the_snapshot() -> None:
    conn = store.open_store(":memory:")
    _load(conn, FakeKiwoom(ret="+5.00"))

    _load(conn, FakeKiwoom(ret="+9.00"))

    rows = conn.execute("SELECT period_return_pct FROM theme_member WHERE code='000010'").fetchall()
    assert rows == [(9.0,)] * 3
    assert conn.execute("SELECT count(*) FROM theme").fetchone() == (3,)


def test_weekday_before_the_close_is_skipped() -> None:
    conn = store.open_store(":memory:")
    kiwoom = FakeKiwoom()

    stats = _load(conn, kiwoom, today=date(2026, 10, 26), last_day=_SATURDAY)

    assert stats.skipped == "intraday"
    assert kiwoom.keys == []


def test_status_reports_snapshot_dates() -> None:
    conn = store.open_store(":memory:")
    _load(conn, FakeKiwoom())

    assert store.status(conn)["theme"] == {"snapshots": 1, "first_date": "2026-10-23", "last_date": "2026-10-23"}
