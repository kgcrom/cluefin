"""Collect one company's recent major-event disclosures (주요사항보고서) for the
financial-analysis screen's "주요사항" tab.

This calls `cluefin_openapi.dart`'s `MajorMattersReport` client directly
instead of reusing cluefin-openapi-cli's `dart.dilution_watch`/`dart.major_event`
handlers (2026-11-04 decision) — desk's dependency on that CLI (added for the
watchlist's trend-setup group column, see `data/trend_groups.py`) is for its cache
module only, not its DART handlers. The slug -> client-method mapping below mirrors
`apps/cluefin-openapi-cli/src/cluefin_openapi_cli/handlers/dart.py`'s `_MAJOR_EVENTS`
table, the source of truth for which library method actually serves which DART
endpoint. Only the event kinds the B-14 plan decided on are covered here: CB/BW/EB
issuance, rights offering, bonus issue, rights-and-bonus issue, capital reduction,
treasury stock acquisition/disposal (trust included), plus
default/business-suspension/rehabilitation-filing/dissolution.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from cluefin_desk.clock import today_kst

logger = logging.getLogger(__name__)

# DART serves 주요사항보고서 data from 2015-01-01 on.
_MIN_DATE = "20150101"
_WINDOW_DAYS = 365
_NO_DATA_STATUS = "013"

_DART_FILING_URL = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"


@dataclass(frozen=True, slots=True)
class MajorEventRow:
    """One normalized major-event report row, ready to render in a table."""

    rcept_dt: str  # YYYYMMDD, taken from rcept_no's leading 8 digits (items carry no rcept_dt field)
    kind: str  # Korean report name
    summary: str  # one line, amount/shares/reason depending on kind
    rcept_no: str
    link: str


def _clean(value: Any) -> str:
    text = str(value).strip() if value is not None else ""
    return text if text and text != "-" else "-"


def _summary_bond(item: Any) -> str:
    return f"권면(전자등록)총액 {_clean(getattr(item, 'bd_fta', None))}원"


def _summary_rights_offering(item: Any) -> str:
    return f"신주(보통주) {_clean(getattr(item, 'nstk_ostk_cnt', None))}주"


def _summary_bonus_issue(item: Any) -> str:
    return f"무상증자 신주(보통주) {_clean(getattr(item, 'nstk_ostk_cnt', None))}주"


def _summary_rights_and_bonus(item: Any) -> str:
    rights = _clean(getattr(item, "piic_nstk_ostk_cnt", None))
    bonus = _clean(getattr(item, "fric_nstk_ostk_cnt", None))
    return f"유상(보통주) {rights}주 / 무상(보통주) {bonus}주"


def _summary_capital_reduction(item: Any) -> str:
    shares = _clean(getattr(item, "crstk_ostk_cnt", None))
    ratio = _clean(getattr(item, "cr_rt_ostk", None))
    return f"감자(보통주) {shares}주, 비율 {ratio}%"


def _summary_treasury_acquisition(item: Any) -> str:
    return f"취득예정금액 {_clean(getattr(item, 'aqpln_prc_ostk', None))}원"


def _summary_treasury_disposal(item: Any) -> str:
    return f"처분예정금액 {_clean(getattr(item, 'dppln_prc_ostk', None))}원"


def _summary_treasury_trust_contract(item: Any) -> str:
    return f"신탁계약금액 {_clean(getattr(item, 'ctr_prc', None))}원"


def _summary_treasury_trust_termination(item: Any) -> str:
    return f"신탁계약금액(해지 전) {_clean(getattr(item, 'ctr_prc_bfcc', None))}원"


def _summary_default(item: Any) -> str:
    amount = _clean(getattr(item, "df_amt", None))
    bank = _clean(getattr(item, "df_bnk", None))
    return f"부도금액 {amount}원 ({bank})"


def _summary_business_suspension(item: Any) -> str:
    return f"영업정지금액 {_clean(getattr(item, 'bsnsp_amt', None))}원"


def _summary_rehabilitation(item: Any) -> str:
    return f"신청사유 {_clean(getattr(item, 'rq_rs', None))}"


def _summary_dissolution(item: Any) -> str:
    return f"해산사유 {_clean(getattr(item, 'ds_rs', None))}"


@dataclass(frozen=True, slots=True)
class _EventType:
    label: str  # Korean report name
    call: Callable[[Any, str, str, str], Any]
    summarize: Callable[[Any], str]


def _event(label: str, method: Callable[[Any], Callable[..., Any]], summarize: Callable[[Any], str]) -> _EventType:
    def call(dart_client: Any, corp_code: str, bgn_de: str, end_de: str) -> Any:
        return method(dart_client.major_matters_report)(corp_code=corp_code, bgn_de=bgn_de, end_de=end_de)

    return _EventType(label, call, summarize)


# slug -> event type. A subset of cluefin-openapi-cli's `_MAJOR_EVENTS` table
# (dilution/shareholder-return + distress kinds only — B-14 decision 2026-11-04).
# Follow that table's method choice, not the library's naming, when adding a slug.
MAJOR_EVENT_TYPES: dict[str, _EventType] = {
    "convertible-bond": _event("전환사채권 발행결정", lambda c: c.convertible_bond_issuance_decision, _summary_bond),
    "bond-with-warrant": _event(
        "신주인수권부사채권 발행결정", lambda c: c.new_stock_warrant_bond_issuance_decision, _summary_bond
    ),
    "exchangeable-bond": _event("교환사채권 발행결정", lambda c: c.exchangeable_bond_issuance_decision, _summary_bond),
    "rights-offering": _event("유상증자 결정", lambda c: c.paid_in_capital_increase_decision, _summary_rights_offering),
    "bonus-issue": _event("무상증자 결정", lambda c: c.free_capital_increase_decision, _summary_bonus_issue),
    "rights-and-bonus-issue": _event(
        "유무상증자 결정", lambda c: c.paid_in_and_free_capital_increase_decision, _summary_rights_and_bonus
    ),
    "capital-reduction": _event("감자 결정", lambda c: c.capital_reduction_decision, _summary_capital_reduction),
    "treasury-stock-acquisition": _event(
        "자기주식 취득 결정", lambda c: c.treasury_stock_acquisition_decision, _summary_treasury_acquisition
    ),
    "treasury-stock-disposal": _event(
        "자기주식 처분 결정", lambda c: c.treasury_stock_disposal_decision, _summary_treasury_disposal
    ),
    "treasury-trust-contract": _event(
        "자기주식취득 신탁계약 체결 결정",
        lambda c: c.treasury_stock_trust_contract_decision,
        _summary_treasury_trust_contract,
    ),
    "treasury-trust-termination": _event(
        "자기주식취득 신탁계약 해지 결정",
        lambda c: c.treasury_stock_trust_contract_termination_decision,
        _summary_treasury_trust_termination,
    ),
    "default": _event("부도발생", lambda c: c.default_occurrence, _summary_default),
    "business-suspension": _event("영업정지", lambda c: c.business_suspension, _summary_business_suspension),
    "rehabilitation-filing": _event(
        "회생절차 개시신청", lambda c: c.corporate_rehabilitation_proceedings, _summary_rehabilitation
    ),
    "dissolution": _event("해산사유 발생", lambda c: c.dissolution_occurrence, _summary_dissolution),
}


def _event_window(end: date | None, days: int) -> tuple[str, str]:
    end_date = end or today_kst()
    begin_date = end_date - timedelta(days=days)
    bgn_de = begin_date.strftime("%Y%m%d")
    if bgn_de < _MIN_DATE:
        bgn_de = _MIN_DATE
    return bgn_de, end_date.strftime("%Y%m%d")


def _dart_filing_link(rcept_no: str) -> str:
    return _DART_FILING_URL.format(rcept_no=rcept_no)


def collect_major_events(
    dart_client: Any,
    corp_code: str,
    *,
    end: date | None = None,
    days: int = _WINDOW_DAYS,
) -> tuple[list[MajorEventRow], dict[str, str]]:
    """Fetch every event type in `MAJOR_EVENT_TYPES` for one company over the last
    `days` days (default 365; the window floors at DART's 2015-01-01 data start) and
    normalize the rows: receipt date, kind, a one-line summary and a DART filing link.

    One event type's call failing does not stop the others — its error message is
    returned in the second element, keyed by slug, so a caller can show it without
    losing the rows the other calls returned. Status 013 ("no such report in the
    range") is not an error and is skipped silently, same as `dart major-event`.

    Rows are sorted by receipt date, newest first.
    """
    bgn_de, end_de = _event_window(end, days)
    rows: list[MajorEventRow] = []
    errors: dict[str, str] = {}

    for slug, event_type in MAJOR_EVENT_TYPES.items():
        try:
            response = event_type.call(dart_client, corp_code, bgn_de, end_de)
        except Exception as e:  # one broken endpoint must not blank the whole tab
            logger.error(f"Failed to fetch {slug} major events for {corp_code}: {e}")
            errors[slug] = str(e)
            continue

        result = getattr(response, "result", None)
        if getattr(result, "status", None) == _NO_DATA_STATUS:
            continue

        for item in getattr(result, "list", None) or []:
            rcept_no = getattr(item, "rcept_no", None) or ""
            rows.append(
                MajorEventRow(
                    rcept_dt=rcept_no[:8],
                    kind=event_type.label,
                    summary=event_type.summarize(item),
                    rcept_no=rcept_no,
                    link=_dart_filing_link(rcept_no),
                )
            )

    rows.sort(key=lambda row: row.rcept_dt, reverse=True)
    return rows, errors
