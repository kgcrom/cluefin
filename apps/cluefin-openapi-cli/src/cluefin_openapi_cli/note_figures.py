"""Standard note figures (depreciation, amortisation, interest, taxes paid) out of a parsed DART XBRL document.

The accounts are `accounts/notes.toml`: XBRL concepts, read from the filing's facts whichever role they sit in (a note
roll-forward or the cash-flow statement). A figure is a fact with no dimension other than the consolidated/separate
axis, whose period ends on the report's period end; the longest such period wins, so a quarterly report gives the
year-to-date figure. A fact without the consolidation axis counts for either basis (filers with one set of
statements). The first id of an account that has a fact wins. Values stay exact ``str(Decimal)`` as filed, sign
included.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date
from typing import Any

from cluefin_openapi_cli.accounts import load_table

__all__ = ["NOTE_ITEMS", "note_figures"]

NOTE_ITEMS = load_table("notes")["notes"]

_CONSOLIDATION_AXIS = "ConsolidatedAndSeparateFinancialStatementsAxis"
_MEMBER_BASIS = {"ConsolidatedMember": "consolidated", "SeparateMember": "separate"}


def _local(name: str) -> str:
    for sep in ("#", ":", "/"):
        name = name.rsplit(sep, 1)[-1]
    return name


def _fact_id(fact: Any) -> str:
    """``ifrs-full:Revenue`` → ``ifrs-full_Revenue``, the id form the account tables use."""
    return fact.concept_qname.replace(":", "_", 1)


def _basis(fact: Any) -> str | None:
    """``consolidated``/``separate``, ``both`` without the axis, None when another axis makes it a breakdown."""
    basis = "both"
    for axis, member in fact.dimensions.items():
        if _local(axis) != _CONSOLIDATION_AXIS:
            return None
        basis = _MEMBER_BASIS.get(_local(member), "other")
    return None if basis == "other" else basis


def _span(fact: Any, period_end: date) -> int | None:
    """Days covered by a duration fact ending on ``period_end``; None for anything else."""
    period = fact.period
    if fact.numeric_value is None or period is None or period.start_date is None or period.end_date != period_end:
        return None
    return (period.end_date - period.start_date).days


def note_figures(facts: Iterable[Any], period_end: date | None, bases: list[str]) -> dict[str, dict[str, str | None]]:
    """``{basis: {account: value or None}}`` for the requested bases (``consolidated``/``separate``)."""
    best: dict[tuple[str, str], tuple[int, str]] = {}
    wanted = {account_id for item in NOTE_ITEMS.values() for account_id in item.ids}
    for fact in facts:
        account_id = _fact_id(fact)
        if period_end is None or account_id not in wanted:
            continue
        span, basis = _span(fact, period_end), _basis(fact)
        if span is None or basis is None:
            continue
        for name in bases if basis == "both" else [basis]:
            key = (name, account_id)
            if key not in best or span > best[key][0]:
                best[key] = (span, str(fact.numeric_value))
    return {
        name: {
            key: next((best[(name, i)][1] for i in item.ids if (name, i) in best), None)
            for key, item in NOTE_ITEMS.items()
        }
        for name in bases
    }
