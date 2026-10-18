"""`company` table: listed stocks from Kiwoom, details and delisting dates from KIS, DART ids.

Survivorship is the point. A code that drops out of Kiwoom's list is never deleted; KIS
`basic-info` supplies its delisting date. Codes delisted before this cache existed come from
DART's corp-code index, which keeps `stock_code` after delisting, filtered through
`basic-info` because that index also holds KONEX listings (whose listing date sits in the
*KOSDAQ* field — `mket_id_cd` is what tells them apart).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any, Callable

import duckdb

from cluefin_openapi_cli.cache.throttle import kis_call

__all__ = [
    "BasicInfo",
    "ListedRow",
    "corp_code_for",
    "fetch_basic_info",
    "fetch_corp_codes",
    "fetch_listing",
    "load_company",
]

# (Kiwoom mrkt_tp, market label). Market 0 also carries ETF/ETN/REITs, filtered by kind.
_MARKETS: tuple[tuple[str, str], ...] = (("0", "KOSPI"), ("10", "KOSDAQ"))
_STOCK_KINDS = frozenset({"거래소", "코스닥"})
_MAX_PAGES = 20
_KIS_MARKETS = {"STK": ("KOSPI", "거래소"), "KSQ": ("KOSDAQ", "코스닥")}
# basic-info scty_grp_id_cd kept as stocks: 주권, 외국주권, 주식예탁증서. DART also lists REITs (RT),
# infrastructure funds (IF) and investment companies (MF), which Kiwoom files under other kinds.
_STOCK_GROUPS = frozenset({"ST", "FS", "DR"})


@dataclass(frozen=True, slots=True)
class ListedRow:
    code: str
    name: str
    market: str
    kind: str
    sector: str | None
    list_count: int | None
    is_admin: bool
    is_halted: bool


@dataclass(frozen=True, slots=True)
class BasicInfo:
    code: str
    name: str
    mket_id_cd: str
    scty_grp_id_cd: str
    industry: str | None
    settle_month: int | None
    listed_on: date | None
    delisted_on: date | None


@dataclass(slots=True)
class CompanyLoadStats:
    listed: int = 0
    details: int = 0
    vanished: int = 0
    delisted_found: int = 0
    probed: int = 0
    errors: list[dict[str, str]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "listed": self.listed,
            "details_refreshed": self.details,
            "vanished_from_listing": self.vanished,
            "delisted_added": self.delisted_found,
            "dart_candidates_probed": self.probed,
            "errors": len(self.errors),
            "error_samples": self.errors[:10],
        }


def _text(value: Any) -> str:
    return str(value or "").strip()


def _yyyymmdd(value: Any) -> date | None:
    text = _text(value)
    if len(text) != 8 or text == "00000000":
        return None
    try:
        return datetime.strptime(text, "%Y%m%d").date()
    except ValueError:
        return None


def _int_or_none(value: Any) -> int | None:
    text = _text(value).replace(",", "")
    return int(text) if text.isdigit() else None


def _settle_month(value: Any) -> int | None:
    # KIS sends '12' for some codes and '1231' for others.
    month = _int_or_none(_text(value)[:2])
    return month if month is not None and 1 <= month <= 12 else None


def fetch_listing(kiwoom: Any) -> list[ListedRow]:
    """Every listed stock (KOSPI 거래소 + KOSDAQ 코스닥), following continuation keys."""

    rows: list[ListedRow] = []
    for mrkt_tp, market in _MARKETS:
        cont_yn, next_key = "N", ""
        for _ in range(_MAX_PAGES):
            response = kiwoom.stock_info.get_stock_info_summary(mrkt_tp, cont_yn=cont_yn, next_key=next_key)
            rows.extend(row for row in (_listed_row(item, market) for item in response.body.list) if row)
            if response.headers.cont_yn != "Y" or not response.headers.next_key:
                break
            cont_yn, next_key = "Y", response.headers.next_key
    return rows


def _listed_row(item: Any, market: str) -> ListedRow | None:
    code, name, kind = _text(item.code), _text(item.name), _text(item.marketName)
    if not code or not name or kind not in _STOCK_KINDS:
        return None
    state = _text(item.state)
    return ListedRow(
        code=code,
        name=name,
        market=market,
        kind=kind,
        sector=_text(item.upName) or None,
        list_count=_int_or_none(item.listCount),
        is_admin="관리종목" in state,
        is_halted="거래정지" in state,
    )


def fetch_corp_codes(dart: Any) -> dict[str, str]:
    """`stock_code -> corp_code`; when a stock code was reused, the most recently modified wins."""

    best: dict[str, tuple[str, str]] = {}
    for item in dart.public_disclosure.corp_code().result.list:
        stock_code = _text(item.stock_code)
        if not stock_code:
            continue
        modified = _text(item.modify_date)
        if stock_code not in best or modified > best[stock_code][0]:
            best[stock_code] = (modified, _text(item.corp_code))
    return {code: corp for code, (_, corp) in best.items()}


def fetch_basic_info(kis: Any, code: str, *, sleep: Callable[[float], None] | None = None) -> BasicInfo:
    kwargs = {"sleep": sleep} if sleep is not None else {}
    output = kis_call(kis.domestic_stock_info.get_stock_basic_info, "300", code, **kwargs).body.output
    mket_id_cd = _text(output.mket_id_cd)
    # A KOSDAQ -> KOSPI move keeps the code and its history but gets a new KOSPI listing date
    # (035720: KOSPI 2017-07-10), so the earlier of the two dates is when trading began.
    dates = [d for d in (_yyyymmdd(output.scts_mket_lstg_dt), _yyyymmdd(output.kosdaq_mket_lstg_dt)) if d]
    listed_on = min(dates) if dates and mket_id_cd in _KIS_MARKETS else None
    return BasicInfo(
        code=code,
        name=_text(output.prdt_abrv_name) or _text(output.prdt_name),
        mket_id_cd=mket_id_cd,
        scty_grp_id_cd=_text(output.scty_grp_id_cd),
        industry=_text(output.std_idst_clsf_cd_name) or None,
        settle_month=_settle_month(output.setl_mmdd),
        listed_on=listed_on,
        delisted_on=_yyyymmdd(output.lstg_abol_dt),
    )


_UPSERT_LISTED = """
INSERT INTO company (code, name, market, kind, sector, list_count, is_admin, is_halted, seen_on, delisted_on)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
ON CONFLICT (code) DO UPDATE SET
  name = excluded.name, market = excluded.market, kind = excluded.kind, sector = excluded.sector,
  list_count = excluded.list_count, is_admin = excluded.is_admin, is_halted = excluded.is_halted,
  seen_on = excluded.seen_on, delisted_on = NULL
"""

_UPDATE_DETAILS = """
UPDATE company SET industry = ?, settle_month = ?, listed_on = coalesce(?, listed_on), updated_at = ?
WHERE code = ?
"""


def load_company(
    conn: duckdb.DuckDBPyConnection,
    *,
    kiwoom: Any,
    kis: Any,
    dart: Any,
    today: date,
    since: date,
    refresh_days: int = 7,
    progress: Callable[[str], None] = lambda _message: None,
    sleep: Callable[[float], None] | None = None,
) -> CompanyLoadStats:
    """Refresh `company` from the three sources, one call at a time."""

    stats = CompanyLoadStats()
    now = datetime.now()

    listing = fetch_listing(kiwoom)
    stats.listed = len(listing)
    conn.executemany(
        _UPSERT_LISTED,
        [(r.code, r.name, r.market, r.kind, r.sector, r.list_count, r.is_admin, r.is_halted, today) for r in listing],
    )
    progress(f"company: {len(listing)} listed stocks from Kiwoom")

    corp_codes = fetch_corp_codes(dart)
    _assign_corp_codes(conn, corp_codes)

    _refresh_details(conn, kis, stats, today=today, now=now, refresh_days=refresh_days, progress=progress, sleep=sleep)
    _mark_vanished(conn, kis, stats, today=today, now=now, sleep=sleep)
    _add_delisted_from_dart(conn, kis, stats, corp_codes, since=since, now=now, progress=progress, sleep=sleep)
    _fill_settle_month_from_dart(conn, dart, stats, now=now)
    return stats


def corp_code_for(code: str, corp_codes: dict[str, str]) -> str | None:
    """DART lists only common shares; a preferred share (`005935`) belongs to its common (`005930`)."""

    if code in corp_codes:
        return corp_codes[code]
    if code.endswith("0"):
        return None
    return corp_codes.get(code[:-1] + "0")


def _assign_corp_codes(conn: duckdb.DuckDBPyConnection, corp_codes: dict[str, str]) -> None:
    codes = [row[0] for row in conn.execute("SELECT code FROM company WHERE corp_code IS NULL").fetchall()]
    updates = [(corp, code) for code in codes if (corp := corp_code_for(code, corp_codes))]
    if updates:
        conn.executemany("UPDATE company SET corp_code = ? WHERE code = ?", updates)


def _fill_settle_month_from_dart(
    conn: duckdb.DuckDBPyConnection, dart: Any, stats: CompanyLoadStats, *, now: datetime
) -> None:
    """KIS leaves `setl_mmdd` blank for some new listings; DART's company overview has `acc_mt`."""

    rows = conn.execute(
        "SELECT code, corp_code FROM company WHERE settle_month IS NULL AND corp_code IS NOT NULL AND updated_at = ?",
        [now],
    ).fetchall()
    for code, corp_code in rows:
        try:
            month = _settle_month(dart.public_disclosure.company_overview(corp_code).acc_mt)
        except Exception as exc:  # noqa: BLE001 - optional enrichment
            stats.errors.append({"code": code, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
            continue
        if month is not None:
            conn.execute("UPDATE company SET settle_month = ? WHERE code = ?", [month, code])


def _refresh_details(
    conn: duckdb.DuckDBPyConnection,
    kis: Any,
    stats: CompanyLoadStats,
    *,
    today: date,
    now: datetime,
    refresh_days: int,
    progress: Callable[[str], None],
    sleep: Callable[[float], None] | None,
) -> None:
    stale_before = now - timedelta(days=refresh_days)
    codes = [
        row[0]
        for row in conn.execute(
            "SELECT code FROM company WHERE seen_on = ? AND (updated_at IS NULL OR updated_at < ?) ORDER BY code",
            [today, stale_before],
        ).fetchall()
    ]
    for index, code in enumerate(codes, 1):
        info = _probe(kis, code, stats, sleep)
        if info is not None:
            conn.execute(_UPDATE_DETAILS, [info.industry, info.settle_month, info.listed_on, now, code])
            stats.details += 1
        if index % 500 == 0:
            progress(f"company: basic-info {index}/{len(codes)}")


def _mark_vanished(
    conn: duckdb.DuckDBPyConnection,
    kis: Any,
    stats: CompanyLoadStats,
    *,
    today: date,
    now: datetime,
    sleep: Callable[[float], None] | None,
) -> None:
    """Codes seen in an earlier listing but not today's: fill `delisted_on` from basic-info."""

    codes = [
        row[0]
        for row in conn.execute(
            "SELECT code FROM company WHERE seen_on < ? AND delisted_on IS NULL ORDER BY code", [today]
        ).fetchall()
    ]
    stats.vanished = len(codes)
    for code in codes:
        info = _probe(kis, code, stats, sleep)
        if info is not None and info.delisted_on is not None:
            conn.execute(
                "UPDATE company SET delisted_on = ?, updated_at = ? WHERE code = ?", [info.delisted_on, now, code]
            )


def _add_delisted_from_dart(
    conn: duckdb.DuckDBPyConnection,
    kis: Any,
    stats: CompanyLoadStats,
    corp_codes: dict[str, str],
    *,
    since: date,
    now: datetime,
    progress: Callable[[str], None],
    sleep: Callable[[float], None] | None,
) -> None:
    known = {row[0] for row in conn.execute("SELECT code FROM company UNION SELECT code FROM probe_log").fetchall()}
    candidates = sorted(code for code in corp_codes if code not in known)
    progress(f"company: {len(candidates)} DART stock codes to check for delisting")
    for index, code in enumerate(candidates, 1):
        info = _probe(kis, code, stats, sleep)
        if info is None:
            continue
        stats.probed += 1
        conn.execute(
            "INSERT INTO probe_log VALUES (?, ?, ?, ?, ?) ON CONFLICT (code) DO UPDATE SET "
            "mket_id_cd = excluded.mket_id_cd, scty_grp_id_cd = excluded.scty_grp_id_cd, "
            "delisted_on = excluded.delisted_on, checked_at = excluded.checked_at",
            [code, info.mket_id_cd, info.scty_grp_id_cd, info.delisted_on, now],
        )
        if _is_delisted_stock(info, since):
            market, kind = _KIS_MARKETS[info.mket_id_cd]
            conn.execute(
                "INSERT INTO company (code, name, market, kind, industry, corp_code, settle_month, listed_on, "
                "delisted_on, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (code) DO NOTHING",
                [
                    code,
                    info.name,
                    market,
                    kind,
                    info.industry,
                    corp_code_for(code, corp_codes),
                    info.settle_month,
                    info.listed_on,
                    info.delisted_on,
                    now,
                ],
            )
            stats.delisted_found += 1
        if index % 200 == 0:
            progress(f"company: DART candidates {index}/{len(candidates)}, {stats.delisted_found} delisted kept")


def _is_delisted_stock(info: BasicInfo, since: date) -> bool:
    return (
        info.mket_id_cd in _KIS_MARKETS
        and info.scty_grp_id_cd in _STOCK_GROUPS
        and info.delisted_on is not None
        and info.delisted_on >= since
    )


def _probe(kis: Any, code: str, stats: CompanyLoadStats, sleep: Callable[[float], None] | None) -> BasicInfo | None:
    try:
        return fetch_basic_info(kis, code, sleep=sleep)
    except Exception as exc:  # noqa: BLE001 - one bad code must not stop a bulk load
        stats.errors.append({"code": code, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
        return None
