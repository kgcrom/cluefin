"""Standard annual accounts of one SEC filer out of XBRL companyfacts (`sec financial-summary`).

The accounts are `accounts/us_gaap.toml` (every filer) and `accounts/us_gaap_financial.toml` (banks, insurers,
brokers — added only when a `marker` account has a value, as in the DART tables). No network: the handler fetches
companyfacts and passes it in.

- Values are us-gaap USD facts from 10-K filings (amendments included) with ``fp == "FY"``: instants, or durations of
  350–380 days. A fiscal year is a period end that carries ``us-gaap:Assets``.
- The same period comes in several filings (its own 10-K, next year's comparative column, an amendment); the latest
  filed value wins, so restated figures replace the originals — the same rule as DART's JSON API.
- An account takes the first of its ids that has a value for that period end; `account_match` names it per account
  for the latest year (None when no id has a value).
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from cluefin_openapi_cli.accounts import Item, load_table

__all__ = ["COMMON_ITEMS", "FINANCIAL_ITEMS", "FINANCIAL_MARKERS", "fiscal_year_ends", "summarize"]


def _flat(name: str) -> dict[str, Item]:
    return {key: item for group in load_table(name).values() for key, item in group.items()}


COMMON_ITEMS = _flat("us_gaap")
FINANCIAL_ITEMS = _flat("us_gaap_financial")
FINANCIAL_MARKERS = frozenset(key for key, item in FINANCIAL_ITEMS.items() if item.marker)
if set(COMMON_ITEMS) & set(FINANCIAL_ITEMS):
    raise ValueError(f"us_gaap_financial.toml reuses common keys: {sorted(set(COMMON_ITEMS) & set(FINANCIAL_ITEMS))}")

_ANNUAL_DAYS = range(350, 381)
_MILLION = Decimal(1_000_000)
_ASSETS = "us-gaap_Assets"

# {account id: {period end: (filed, value)}}
Values = dict[str, dict[date, tuple[date, Decimal]]]


def _is_annual(fact: Any) -> bool:
    if not fact.form.startswith("10-K") or fact.fp != "FY":
        return False
    return fact.start is None or (fact.end - fact.start).days in _ANNUAL_DAYS


def annual_values(company_facts: Any) -> Values:
    """Latest-filed annual USD value per us-gaap concept and period end."""
    values: Values = {}
    for concept, concept_facts in (company_facts.facts or {}).get("us-gaap", {}).items():
        by_end: dict[date, tuple[date, Decimal]] = {}
        for fact in concept_facts.units.get("USD", []):
            if _is_annual(fact) and (fact.end not in by_end or fact.filed >= by_end[fact.end][0]):
                by_end[fact.end] = (fact.filed, Decimal(fact.val))
        if by_end:
            values[f"us-gaap_{concept}"] = by_end
    return values


def fiscal_year_ends(values: Values) -> list[date]:
    """Period ends carrying total assets, newest first."""
    return sorted(values.get(_ASSETS, {}), reverse=True)


def _pick(values: Values, items: dict[str, Item], end: date) -> tuple[dict[str, float | None], dict[str, str | None]]:
    figures: dict[str, float | None] = {}
    matched: dict[str, str | None] = {}
    for key, item in items.items():
        account_id = next((i for i in item.ids if end in values.get(i, {})), None)
        figures[key] = None if account_id is None else float(values[account_id][end][1] / _MILLION)
        matched[key] = None if account_id is None else account_id.removeprefix("us-gaap_")
    return figures, matched


def summarize(company_facts: Any, years: int) -> dict[str, Any] | None:
    """``{"years": [...newest first], "account_match": {...}}`` in USD millions, or None without a 10-K year."""
    values = annual_values(company_facts)
    ends = fiscal_year_ends(values)[:years]
    if not ends:
        return None
    common = [_pick(values, COMMON_ITEMS, end) for end in ends]
    financial = [_pick(values, FINANCIAL_ITEMS, end) for end in ends]
    has_financial = any(figures[key] is not None for figures, _ in financial for key in FINANCIAL_MARKERS)
    rows = []
    for end, (figures, _), (fin_figures, _) in zip(ends, common, financial, strict=True):
        rows.append({"period_end": end.isoformat(), **figures, **(fin_figures if has_financial else {})})
    match = {**common[0][1], **(financial[0][1] if has_financial else {})}
    return {"years": rows, "account_match": match}
