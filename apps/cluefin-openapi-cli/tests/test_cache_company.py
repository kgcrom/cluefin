"""`company` load: Kiwoom listing, KIS basic-info details, delisted codes from DART, survivorship."""

from __future__ import annotations

import json
from datetime import date
from types import SimpleNamespace

import pytest

from cluefin_openapi_cli.cache import cli as cache_cli
from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.company import fetch_listing, load_company
from cluefin_openapi_cli.cache.throttle import kis_call
from cluefin_openapi_cli.main import run_cli

TODAY = date(2026, 10, 19)
SINCE = date(2016, 1, 1)


def _listing_item(code, name, kind, state="증거금40%|담보대출|신용가능", up_name="전기전자"):
    return SimpleNamespace(
        code=code, name=name, marketName=kind, upName=up_name, listCount="0000005969782550", regDay="", state=state
    )


class FakeKiwoom:
    def __init__(self, markets: dict[str, list]):
        self.markets = markets
        self.calls: list[tuple[str, str]] = []
        self.stock_info = self

    def get_stock_info_summary(self, mrkt_tp, cont_yn="N", next_key=""):
        self.calls.append((mrkt_tp, cont_yn))
        pages = self.markets.get(mrkt_tp, [[]])
        page_index = int(next_key or 0)
        more = page_index + 1 < len(pages)
        return SimpleNamespace(
            body=SimpleNamespace(list=pages[page_index]),
            headers=SimpleNamespace(cont_yn="Y" if more else "N", next_key=str(page_index + 1) if more else ""),
        )


def _basic(mket_id_cd, *, abol="", scts="", kosdaq="", setl="12", name="회사", industry="제조업", group="ST"):
    return SimpleNamespace(
        mket_id_cd=mket_id_cd,
        scty_grp_id_cd=group,
        prdt_abrv_name=name,
        prdt_name=name,
        std_idst_clsf_cd_name=industry,
        setl_mmdd=setl,
        scts_mket_lstg_dt=scts,
        kosdaq_mket_lstg_dt=kosdaq,
        lstg_abol_dt=abol,
    )


class RateLimited(Exception):
    def __init__(self):
        super().__init__("Server error")
        self.response_data = {"rt_cd": "1", "msg_cd": "EGW00201", "msg1": "초당 거래건수를 초과하였습니다."}


class FakeKis:
    def __init__(self, infos: dict[str, SimpleNamespace], *, throttle_once: frozenset[str] = frozenset()):
        self.infos = infos
        self.throttle_once = set(throttle_once)
        self.calls: list[str] = []
        self.domestic_stock_info = self

    def get_stock_basic_info(self, prdt_type_cd, pdno):
        self.calls.append(pdno)
        if pdno in self.throttle_once:
            self.throttle_once.discard(pdno)
            raise RateLimited()
        if pdno not in self.infos:
            raise ValueError(f"KIS API Error [OPSQ0002]: no such code {pdno}")
        return SimpleNamespace(body=SimpleNamespace(output=self.infos[pdno]))


class FakeDart:
    def __init__(self, items: list[tuple[str, str, str]]):
        self.items = [SimpleNamespace(corp_code=c, stock_code=s, modify_date=m) for c, s, m in items]
        self.overview_calls: list[str] = []
        self.public_disclosure = self

    def corp_code(self):
        return SimpleNamespace(result=SimpleNamespace(list=self.items))

    def company_overview(self, corp_code):
        self.overview_calls.append(corp_code)
        return SimpleNamespace(acc_mt="12")


def _sources():
    kiwoom = FakeKiwoom(
        {
            "0": [
                [
                    _listing_item("005930", "삼성전자", "거래소"),
                    _listing_item("005935", "삼성전자우", "거래소"),
                    _listing_item("069500", "KODEX 200", "ETF", up_name=""),
                ]
            ],
            "10": [[_listing_item("035720", "카카오", "코스닥", state="관리종목|증거금100%|거래정지")]],
        }
    )
    kis = FakeKis(
        {
            "005930": _basic("STK", scts="19750611", setl="12", name="삼성전자"),
            "005935": _basic("STK", scts="19890825", setl="", name="삼성전자우"),
            "088260": _basic("STK", scts="20160101", abol="20200101", group="RT"),
            "035720": _basic("KSQ", kosdaq="20171110", setl="1231", name="카카오"),
            "117930": _basic("STK", scts="20091210", abol="20170307", name="한진해운", industry="해상 운송업"),
            "266170": _basic("KNX", kosdaq="20170609", setl="1231"),
            "037830": _basic("KSQ", kosdaq="20020205", abol="20100209"),
        },
        throttle_once=frozenset({"005930"}),
    )
    dart = FakeDart(
        [
            ("00126380", "005930", "20260101"),
            ("00258801", "035720", "20260101"),
            ("00111111", "117930", "20170401"),
            ("00222222", "266170", "20260101"),
            ("00333333", "037830", "20100301"),
            ("00444444", "088260", "20200201"),
            ("00999999", "   ", "20260101"),
        ]
    )
    return kiwoom, kis, dart


def _load(conn, kiwoom, kis, dart, today=TODAY):
    return load_company(conn, kiwoom=kiwoom, kis=kis, dart=dart, today=today, since=SINCE, sleep=lambda _s: None)


def _rows(conn):
    cols = "code, name, market, kind, corp_code, settle_month, listed_on, delisted_on, is_admin, is_halted, seen_on"
    return {
        row[0]: dict(zip(cols.split(", "), row, strict=False))
        for row in conn.execute(f"SELECT {cols} FROM company ORDER BY code").fetchall()
    }


def test_first_load_keeps_stocks_and_backfills_delisted() -> None:
    conn = store.open_store(":memory:")
    kiwoom, kis, dart = _sources()

    stats = _load(conn, kiwoom, kis, dart)
    rows = _rows(conn)

    assert set(rows) == {"005930", "005935", "035720", "117930"}  # ETF, KONEX, REIT, pre-2016 left out
    assert rows["005930"]["settle_month"] == 12 and rows["005930"]["listed_on"] == date(1975, 6, 11)
    assert rows["005930"]["corp_code"] == "00126380" and rows["005930"]["delisted_on"] is None
    assert rows["035720"]["settle_month"] == 12  # '1231' normalised
    assert rows["005935"]["corp_code"] == "00126380"  # preferred share -> its common's DART id
    assert rows["005935"]["settle_month"] == 12 and dart.overview_calls == ["00126380"]  # blank in KIS, DART fills
    assert rows["035720"]["is_admin"] is True and rows["035720"]["is_halted"] is True
    assert rows["117930"]["delisted_on"] == date(2017, 3, 7) and rows["117930"]["seen_on"] is None
    assert rows["117930"]["market"] == "KOSPI" and rows["117930"]["corp_code"] == "00111111"
    probed = {row[0]: row[1] for row in conn.execute("SELECT code, mket_id_cd FROM probe_log").fetchall()}
    assert probed == {"117930": "STK", "266170": "KNX", "037830": "KSQ", "088260": "STK"}
    assert stats.as_dict()["errors"] == 0 and stats.delisted_found == 1


def test_second_load_marks_vanished_code_and_skips_fresh_details() -> None:
    conn = store.open_store(":memory:")
    kiwoom, kis, dart = _sources()
    _load(conn, kiwoom, kis, dart)
    kiwoom.markets["10"] = [[]]
    kis.infos["035720"] = _basic("KSQ", kosdaq="20171110", abol="20261020")
    kis.calls.clear()

    stats = _load(conn, kiwoom, kis, dart, today=date(2026, 10, 21))

    assert _rows(conn)["035720"]["delisted_on"] == date(2026, 10, 20)
    assert kis.calls == ["035720"]  # details are fresh, DART candidates already probed
    assert stats.vanished == 1


def test_relisted_code_clears_delisted_on() -> None:
    conn = store.open_store(":memory:")
    kiwoom, kis, dart = _sources()
    _load(conn, kiwoom, kis, dart)
    kiwoom.markets["0"][0].append(_listing_item("117930", "한진해운", "거래소"))

    _load(conn, kiwoom, kis, dart, today=date(2026, 10, 20))

    assert _rows(conn)["117930"]["delisted_on"] is None


def test_listing_follows_continuation_pages() -> None:
    kiwoom = FakeKiwoom({"0": [[_listing_item("005930", "A", "거래소")], [_listing_item("000660", "B", "거래소")]]})

    rows = fetch_listing(kiwoom)

    assert [row.code for row in rows] == ["005930", "000660"]
    assert kiwoom.calls == [("0", "N"), ("0", "Y"), ("10", "N")]


def test_kis_call_retries_only_rate_limit() -> None:
    pauses: list[float] = []
    attempts = iter([RateLimited(), RateLimited(), "ok"])

    def flaky():
        value = next(attempts)
        if isinstance(value, Exception):
            raise value
        return value

    assert kis_call(flaky, sleep=pauses.append) == "ok"
    assert pauses == [0.1, 0.1]
    session_full = iter([ValueError("KIS API Error [OPSQ1002]: SESSION FULL (rt_cd=9)"), "ok"])

    def busy():
        value = next(session_full)
        if isinstance(value, Exception):
            raise value
        return value

    pauses.clear()
    assert kis_call(busy, sleep=pauses.append) == "ok"
    assert pauses == [1.0]
    with pytest.raises(ValueError):
        kis_call(lambda: (_ for _ in ()).throw(ValueError("boom")), sleep=pauses.append)


def test_basic_info_error_is_counted_not_fatal() -> None:
    conn = store.open_store(":memory:")
    kiwoom, kis, dart = _sources()
    del kis.infos["266170"]

    stats = _load(conn, kiwoom, kis, dart)

    assert stats.as_dict()["errors"] == 1
    assert "266170" not in {row[0] for row in conn.execute("SELECT code FROM probe_log").fetchall()}


@pytest.fixture
def cache_dir(tmp_path, monkeypatch):
    monkeypatch.setenv(store.CACHE_DIR_ENV, str(tmp_path))
    return tmp_path


def test_cache_load_company_command(cache_dir, monkeypatch) -> None:
    kiwoom, kis, dart = _sources()
    clients = {"kiwoom": kiwoom, "kis": kis, "dart": dart}
    monkeypatch.setattr(cache_cli, "_client_factory", lambda: SimpleNamespace(create=clients.__getitem__))
    monkeypatch.setattr("cluefin_openapi_cli.cache.throttle.time.sleep", lambda _s: None)

    result = run_cli(["cache", "load", "--only", "company", "--json"])

    assert result.exit_code == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["parts"]["company"]["listed"] == 3
    assert payload["parts"]["company"]["delisted_added"] == 1
    assert kis.max_retries == 0
    status = json.loads(run_cli(["cache", "status", "--json"]).stdout)
    assert status["company"] == {"listed": 3, "delisted": 1}
    assert "company" in status["last_load"]


def test_cache_load_rejects_unknown_part(cache_dir) -> None:
    result = run_cli(["cache", "load", "--only", "minutes", "--json"])

    assert result.exit_code == 2
    assert json.loads(result.stdout)["error"]["data"]["parts"] == ["company"]


def test_cache_load_rejects_bad_since(cache_dir) -> None:
    assert run_cli(["cache", "load", "--since", "2016-01-01", "--json"]).exit_code == 2
