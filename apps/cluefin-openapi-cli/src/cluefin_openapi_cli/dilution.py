"""Pure normalization for `dart dilution-watch`: major-event rows -> common fields.

Each DART 주요사항보고서 endpoint names its money/share/price fields differently (see
`handlers/dart.py` `_MAJOR_EVENTS`). This module has no DART client dependency and does no I/O —
it only maps one already-fetched row (a dict with the endpoint's raw field names, as `dump_model`
produces) to a small common shape: `rcept_dt`, `kind`, `corp_name`, `amount_won`,
`conversion_price`, `refixing_floor`, `new_shares`, `pct_of_shares`.

Scope decided 2026-11-04 (docs/plans/bundle1-plan.md "B-11"): CB, BW, EB, rights offering, bonus
issue, rights-and-bonus issue, capital reduction, treasury stock acquisition/disposal (including
trust contract/termination). Treasury-stock *retirement* (소각) is not in 주요사항보고서 — it is a
periodic-report item (`dart report-item treasury-stock`) — so it is deliberately left out; see
`NOT_COVERED`.

`new_shares` carries sign: positive means shares added to the float (CB/BW/EB conversion, rights
and bonus issues, treasury disposal), negative means shares removed (capital reduction, treasury
acquisition). `pct_of_shares` is **not** computed here — it needs the issuer's outstanding share
count from `dart share-count`, which is the handler's job (`with_pct_of_shares`).
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass

# Kinds covered by `dart dilution-watch`, in the order rows are collected. These are the same
# slugs `_MAJOR_EVENTS` (handlers/dart.py) uses for `dart major-event --event`.
DILUTION_KINDS: tuple[str, ...] = (
    "convertible-bond",
    "bond-with-warrant",
    "exchangeable-bond",
    "rights-offering",
    "bonus-issue",
    "rights-and-bonus-issue",
    "capital-reduction",
    "treasury-stock-acquisition",
    "treasury-stock-disposal",
    "treasury-trust-contract",
    "treasury-trust-termination",
)

# Decided 2026-11-04: not fetched by dilution-watch, stated so callers don't read silence as "none".
NOT_COVERED: tuple[dict[str, str], ...] = (
    {
        "kind": "treasury-stock-retirement",
        "reason": (
            "자사주 소각은 주요사항보고서에 없고 정기보고서 report-item treasury-stock 에 있다. "
            "dart dilution-watch 는 이번 범위에 넣지 않는다."
        ),
    },
)


@dataclass(frozen=True, slots=True)
class DilutionRow:
    rcept_dt: str
    kind: str
    corp_name: str | None
    amount_won: float | None
    conversion_price: float | None
    refixing_floor: float | None
    new_shares: float | None
    pct_of_shares: float | None = None


def _num(value: object) -> float | None:
    """DART comma-string number ("1,234", "-", None, "") -> float, else None."""
    if value is None:
        return None
    cleaned = str(value).strip().replace(",", "")
    if cleaned in ("", "-"):
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _sum(*values: object) -> float | None:
    nums = [n for n in (_num(v) for v in values) if n is not None]
    return sum(nums) if nums else None


def _rcept_dt(row: dict) -> str:
    rcept_no = row.get("rcept_no") or ""
    return rcept_no[:8]


def normalize_row(kind: str, row: dict) -> DilutionRow:
    """Map one major-event row (dict, endpoint's own field names) to the common shape.

    `row` is one item of the `result.list` a `_MAJOR_EVENTS[kind]` call returns (after
    `dump_model`), e.g. a convertible-bond-issuance-decision row keyed by `bd_fta`/`cv_prc`/...
    """
    corp_name = row.get("corp_name")
    rcept_dt = _rcept_dt(row)

    if kind == "convertible-bond":
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=_num(row.get("bd_fta")),
            conversion_price=_num(row.get("cv_prc")),
            refixing_floor=_num(row.get("act_mktprcfl_cvprc_lwtrsprc")),
            new_shares=_num(row.get("cvisstk_cnt")),
        )
    if kind == "bond-with-warrant":
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=_num(row.get("bd_fta")),
            conversion_price=_num(row.get("ex_prc")),
            refixing_floor=_num(row.get("act_mktprcfl_cvprc_lwtrsprc")),
            new_shares=_num(row.get("nstk_isstk_cnt")),
        )
    if kind == "exchangeable-bond":
        # CorporateBondIssuanceDecisionItem (library name for 교환사채권) has no refixing field.
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=_num(row.get("bd_fta")),
            conversion_price=_num(row.get("ex_prc")),
            refixing_floor=None,
            new_shares=_num(row.get("extg_stkcnt")),
        )
    if kind == "rights-offering":
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=_sum(
                row.get("fdpp_fclt"),
                row.get("fdpp_bsninh"),
                row.get("fdpp_op"),
                row.get("fdpp_dtrp"),
                row.get("fdpp_ocsa"),
                row.get("fdpp_etc"),
            ),
            conversion_price=None,
            refixing_floor=None,
            new_shares=_num(row.get("nstk_ostk_cnt")),
        )
    if kind == "bonus-issue":
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=None,
            conversion_price=None,
            refixing_floor=None,
            new_shares=_num(row.get("nstk_ostk_cnt")),
        )
    if kind == "rights-and-bonus-issue":
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=_sum(
                row.get("piic_fdpp_fclt"),
                row.get("piic_fdpp_bsninh"),
                row.get("piic_fdpp_op"),
                row.get("piic_fdpp_dtrp"),
                row.get("piic_fdpp_ocsa"),
                row.get("piic_fdpp_etc"),
            ),
            conversion_price=None,
            refixing_floor=None,
            new_shares=_sum(row.get("piic_nstk_ostk_cnt"), row.get("fric_nstk_ostk_cnt")),
        )
    if kind == "capital-reduction":
        reduced = _num(row.get("crstk_ostk_cnt"))
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=None,
            conversion_price=None,
            refixing_floor=None,
            new_shares=-reduced if reduced is not None else None,
        )
    if kind == "treasury-stock-acquisition":
        acquired = _num(row.get("aqpln_stk_ostk"))
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=_num(row.get("aqpln_prc_ostk")),
            conversion_price=None,
            refixing_floor=None,
            new_shares=-acquired if acquired is not None else None,
        )
    if kind == "treasury-stock-disposal":
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=_num(row.get("dppln_prc_ostk")),
            conversion_price=None,
            refixing_floor=None,
            new_shares=_num(row.get("dppln_stk_ostk")),
        )
    if kind == "treasury-trust-contract":
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=_num(row.get("ctr_prc")),
            conversion_price=None,
            refixing_floor=None,
            new_shares=None,
        )
    if kind == "treasury-trust-termination":
        return DilutionRow(
            rcept_dt=rcept_dt,
            kind=kind,
            corp_name=corp_name,
            amount_won=_num(row.get("ctr_prc_atcc")),
            conversion_price=None,
            refixing_floor=None,
            new_shares=None,
        )
    raise ValueError(f"unsupported dilution kind: {kind}")


def with_pct_of_shares(row: DilutionRow, total_shares: float | None) -> DilutionRow:
    """Return a copy of `row` with `pct_of_shares` set against `total_shares`.

    `total_shares` is the issuer's outstanding common-share count from the periodic report
    closest to the end of the query window (`dart share-count`), per the 2026-11-04 decision.
    Left at `None` when either side is unknown (e.g. a treasury trust contract with no share
    count in the filing, or `share-count` returning no usable row).
    """
    if row.new_shares is None or not total_shares:
        return row
    return dataclasses.replace(row, pct_of_shares=row.new_shares / total_shares * 100)
