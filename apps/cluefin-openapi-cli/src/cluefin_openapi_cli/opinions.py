"""Broker opinion rows (`kis stock investment-opinion`) → each broker's latest target and summary statistics.

Ported from cluefin-factory ``scripts/company/market.mjs`` ``opinions()`` (archived 2026-10-18).
"""

from __future__ import annotations

from statistics import mean, median
from typing import Any

from cluefin_openapi_cli.statements import won


def _digits(value: Any) -> str:
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def summarize(rows: list[dict[str, Any]], since: str) -> dict[str, Any]:
    """Each broker's latest target in the window (newest first) with mean/median/max/min and a rating count.

    Rows without a date, with a date before `since`, or without a positive target are ignored.
    """
    latest_by_broker: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        day = _digits(row.get("stck_bsop_date"))
        target = won(row.get("hts_goal_prc"))
        if not day or day < since or not target or target <= 0:
            continue
        broker = str(row.get("mbcr_name") or "").strip()
        if not broker:
            continue
        seen = latest_by_broker.get(broker)
        if seen is None or seen["date"] < day:
            latest_by_broker[broker] = {
                "broker": broker,
                "date": day,
                "rating": row.get("invt_opnn") or None,
                "previous_rating": row.get("rgbf_invt_opnn") or None,
                "target": target,
            }

    brokers = sorted(latest_by_broker.values(), key=lambda b: b["date"], reverse=True)
    if not brokers:
        return {
            "since": since,
            "count": 0,
            "mean": None,
            "median": None,
            "max": None,
            "min": None,
            "ratings": {},
            "brokers": [],
        }

    targets = [b["target"] for b in brokers]
    top = max(brokers, key=lambda b: b["target"])
    bottom = min(brokers, key=lambda b: b["target"])
    ratings: dict[str, int] = {}
    for b in brokers:
        key = str(b["rating"] or "").strip().upper() or "(없음)"
        ratings[key] = ratings.get(key, 0) + 1
    return {
        "since": since,
        "count": len(brokers),
        "mean": mean(targets),
        "median": median(targets),
        "max": {"target": top["target"], "broker": top["broker"], "date": top["date"]},
        "min": {"target": bottom["target"], "broker": bottom["broker"], "date": bottom["date"]},
        "ratings": ratings,
        "brokers": brokers,
    }
