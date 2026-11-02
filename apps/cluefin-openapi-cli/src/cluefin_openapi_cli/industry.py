"""`ecos industry-outlook`: one manufacturing division's leading indicators, each against its own history.

Covers KSIC manufacturing divisions C10-C33 (24 divisions). The division table below is hand-authored and was
checked against the live ECOS API on 2026-11-03 (`docs/plans/forward-outlook-plan.md` F-a):

- Business survey index (BSI), outlook and actual: 512Y008/512Y007, Group1 indicator code (BA/AA) x Group2
  industry code (Cxxxx, `ecos items --stat-code 512Y008`). The two tables' group order is the same, but it is
  the *opposite* of `901Y032` below — Group1 is the indicator there, Group2 the industry. Division 12 (담배)
  and 33 (기타 제품) share the one BSI industry code C3300 ("기타제품, 담배"); there is no separate C1200.
- Production/shipment/inventory: 901Y032, Group1 industry code (I11ACx) x Group2 indicator (1 production,
  3 shipment, 5 inventory — 원지수/raw index, not seasonally adjusted, so the same basis is used for the
  inventory-cycle YoY comparison and for the indicator rows). The letter suffix does **not** follow KSIC order
  past I11ACR: I11ACV is 기타 운송장비 (KSIC 31), then I11ACS/T/U are 28/29/30, then I11ACW/X are 32/33 — this
  table maps by item name, not by assuming the letters are sequential. Divisions 18 (인쇄), 21 (의료용 물질 및
  의약품) and 31 (기타 운송장비) have production and shipment data but no inventory index (checked live
  2026-11-03: blank rows for item 5 over a 5-year window) — their `inventory_yoy` and `inventory_cycle` land
  in `missing`/`None`, not a stale code.
- Product price/value: 402Y014 수출물가(export price, Group1 commodity x Group2 currency basis — "W" 원화기준
  is used here to stay in KRW like the PPI and production/shipment/inventory legs), 404Y014 생산자물가(PPI,
  single group), 403Y001 수출금액지수(export value index, single group). All three tables share one commodity
  code set; a division with no product-level code in a table (checked live, not guessed) is recorded as `None`
  there rather than substituted with a loosely related one. Division 18 (인쇄 및 기록매체 복제업) has no code in
  any of the three — printing has no standalone commodity price series. Division 11 (음료) and 16 (목재) have a
  PPI code but no export code (not an export product in this classification). Division 31 (기타 운송장비, where
  조선/shipbuilding sits) has a PPI code but no export price/value code either — ships are not priced as a
  standard commodity in this series, a real gap for a shipbuilding-heavy company.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from cluefin_openapi.ecos import EcosAPIError, EcosAuthenticationError, EcosRateLimitError

from cluefin_openapi_cli import macro

__all__ = ["Division", "DIVISIONS", "resolve_division", "series_specs", "industry_outlook"]


@dataclass(frozen=True, slots=True)
class Division:
    ksic: str  # KSIC manufacturing division, two digits, "10".."33".
    name: str
    production_item: str  # 901Y032 Group1 (industry) item code, I11ACx.
    bsi_item: str | None  # 512Y007/512Y008 Group2 (industry) item code, Cxxxx.
    product_name: str | None  # Representative product (for export_price/ppi/export_value), or None.
    export_price_item: str | None  # 402Y014 Group1 (commodity) item code.
    ppi_item: str | None  # 404Y014 item code.
    export_value_item: str | None  # 403Y001 item code.


DIVISIONS: tuple[Division, ...] = (
    Division("10", "식료품 제조업", "I11ACA", "C1000", "식료품", "3011AA", "3011AA", "3011AA"),
    Division("11", "음료 제조업", "I11ACB", "C1100", "음료품", None, "3012AA", None),
    Division("12", "담배 제조업", "I11ACC", "C3300", "담배", "3013AA", "3013AA", "3013AA"),
    Division("13", "섬유제품 제조업(의복 제외)", "I11ACD", "C1300", "직물제품", "30213AA", "30213AA", "30213AA"),
    Division(
        "14", "의복, 의복액세서리 및 모피제품 제조업", "I11ACE", "C1400", "의복제품", "30214AA", "30214AA", "30214AA"
    ),
    Division("15", "가죽, 가방 및 신발 제조업", "I11ACF", "C1500", "가죽제품", "30221AA", "30221AA", "30221AA"),
    Division("16", "목재 및 나무제품 제조업(가구 제외)", "I11ACG", "C1600", "목재 및 목제품", None, "3031AA", None),
    Division(
        "17", "펄프, 종이 및 종이제품 제조업", "I11ACH", "C1700", "펄프 및 종이제품", "3032AA", "3032AA", "3032AA"
    ),
    Division("18", "인쇄 및 기록매체 복제업", "I11ACI", "C1800", None, None, None, None),
    Division(
        "19", "코크스, 연탄 및 석유정제품 제조업", "I11ACJ", "C1900", "석탄 및 석유제품", "3041AA", "3041AA", "3041AA"
    ),
    Division(
        "20",
        "화학물질 및 화학제품 제조업(의약품 제외)",
        "I11ACK",
        "C2000",
        "합성수지 및 합성고무",
        "3052AA",
        "3052AA",
        "3052AA",
    ),
    Division("21", "의료용 물질 및 의약품 제조업", "I11ACL", "C2100", "의약품", "3054AA", "3054AA", "3054AA"),
    Division("22", "고무제품 및 플라스틱제품 제조업", "I11ACM", "C2200", "고무제품", "3058AA", "3058AA", "3058AA"),
    Division("23", "비금속 광물제품 제조업", "I11ACN", "C2300", "시멘트", "30622AA", "30622AA", "30622AA"),
    Division("24", "1차 금속 제조업", "I11ACO", "C2400", "철강 1차제품", "3071AA", "3071AA", "3071AA"),
    Division(
        "25", "금속가공제품 제조업(기계 및 가구 제외)", "I11ACP", "C2500", "금속가공제품", "3081AA", "3081AA", "3081AA"
    ),
    Division(
        "26",
        "전자부품, 컴퓨터, 영상, 음향 및 통신장비 제조업",
        "I11ACQ",
        "C2600",
        "반도체",
        "30911AA",
        "30911AA",
        "30911AA",
    ),
    Division("27", "의료, 정밀, 광학기기 및 시계 제조업", "I11ACR", "C2700", "정밀기기", "3096AA", "3096AA", "3096AA"),
    Division("28", "전기장비 제조업", "I11ACS", "C2800", "전기장비", "3101AA", "3101AA", "3101AA"),
    Division("29", "기타 기계 및 장비 제조업", "I11ACT", "C2900", "기계 및 장비", "311AA", "311AA", "311AA"),
    Division("30", "자동차 및 트레일러 제조업", "I11ACU", "C3000", "자동차 및 부품", "3121AA", "3121AA", "3121AA"),
    Division("31", "기타 운송장비 제조업", "I11ACV", "C3100", "기타 운송장비", None, "3122AA", None),
    Division("32", "가구 제조업", "I11ACW", "C3200", "가구", "31311AA", "31311AA", "31311AA"),
    Division("33", "기타 제품 제조업", "I11ACX", "C3300", "기타 제조업 제품", "31312AA", "31312AA", "31312AA"),
)

_BY_KSIC: dict[str, Division] = {division.ksic: division for division in DIVISIONS}


def resolve_division(induty_code: str) -> Division | None:
    """DART `induty_code` (2-5 digits) -> its manufacturing division, or None (non-manufacturing/unknown)."""
    return _BY_KSIC.get(induty_code[:2])


def _series(key: str, name: str, group: str, stat_code: str, item_codes: tuple[str, ...]) -> macro.MacroSeries:
    return macro.MacroSeries(key, name, group, stat_code, "M", item_codes, "%", "yoy")


def series_specs(division: Division) -> tuple[tuple[str, str, str, macro.MacroSeries | None], ...]:
    """(key, name, group, series-or-None) for every indicator this division can show."""

    product = division.product_name
    specs: list[tuple[str, str, str, macro.MacroSeries | None]] = [
        (
            "bsi_outlook",
            f"{division.name} 업황전망BSI",
            "sentiment",
            macro.MacroSeries(
                "bsi_outlook",
                f"{division.name} 업황전망BSI",
                "sentiment",
                "512Y008",
                "M",
                ("BA", division.bsi_item),
                "지수",
            )
            if division.bsi_item
            else None,
        ),
        (
            "bsi_actual",
            f"{division.name} 업황실적BSI",
            "sentiment",
            macro.MacroSeries(
                "bsi_actual",
                f"{division.name} 업황실적BSI",
                "sentiment",
                "512Y007",
                "M",
                ("AA", division.bsi_item),
                "지수",
            )
            if division.bsi_item
            else None,
        ),
        (
            "production_yoy",
            f"{division.name} 생산지수(원지수, 전년동월비)",
            "production",
            _series(
                "production_yoy",
                f"{division.name} 생산지수(원지수, 전년동월비)",
                "production",
                "901Y032",
                (division.production_item, "1"),
            ),
        ),  # fmt: skip
        (
            "shipment_yoy",
            f"{division.name} 출하지수(원지수, 전년동월비)",
            "production",
            _series(
                "shipment_yoy",
                f"{division.name} 출하지수(원지수, 전년동월비)",
                "production",
                "901Y032",
                (division.production_item, "3"),
            ),
        ),  # fmt: skip
        (
            "inventory_yoy",
            f"{division.name} 재고지수(원지수, 전년동월비)",
            "production",
            _series(
                "inventory_yoy",
                f"{division.name} 재고지수(원지수, 전년동월비)",
                "production",
                "901Y032",
                (division.production_item, "5"),
            ),
        ),  # fmt: skip
        (
            "export_price_yoy",
            f"{product} 수출물가(원화기준, 전년동월비)" if product else "",
            "price",
            _series(
                "export_price_yoy",
                f"{product} 수출물가(원화기준, 전년동월비)",
                "price",
                "402Y014",
                (division.export_price_item, "W"),
            )
            if division.export_price_item
            else None,
        ),  # fmt: skip
        (
            "ppi_yoy",
            f"{product} 생산자물가(전년동월비)" if product else "",
            "price",
            _series("ppi_yoy", f"{product} 생산자물가(전년동월비)", "price", "404Y014", (division.ppi_item,))
            if division.ppi_item
            else None,
        ),  # fmt: skip
        (
            "export_value_yoy",
            f"{product} 수출금액지수(전년동월비)" if product else "",
            "trade",
            _series(
                "export_value_yoy",
                f"{product} 수출금액지수(전년동월비)",
                "trade",
                "403Y001",
                (division.export_value_item,),
            )
            if division.export_value_item
            else None,
        ),  # fmt: skip
    ]
    return tuple(specs)


def _inventory_cycle(points: dict[str, list[macro.Point]], *, window_years: int) -> dict[str, Any] | None:
    """shipment YoY - inventory YoY (both 원지수/raw index). Signs only, no phase name."""
    if "shipment_yoy" not in points or "inventory_yoy" not in points:
        return None
    diff = macro.align(points["shipment_yoy"], points["inventory_yoy"])
    summary = macro.summarize(diff, window_years=window_years)
    if summary is None:
        return None
    by_shipment = dict(points["shipment_yoy"])
    by_inventory = dict(points["inventory_yoy"])
    as_of = summary["as_of"]
    return {
        "name": "재고순환(출하지수 전년비 - 재고지수 전년비, 원지수)",
        "formula": "shipment_yoy - inventory_yoy",
        "shipments_up": by_shipment[as_of] > 0,
        "inventory_up": by_inventory[as_of] > 0,
        **summary,
    }


def industry_outlook(
    division: Division,
    fetch: Callable[[macro.MacroSeries], Sequence[macro.Point]],
    *,
    window_years: int,
) -> dict[str, Any]:
    """Run every mapped series through `fetch` (which may raise) and summarize. Failures land in `missing`."""
    points: dict[str, list[macro.Point]] = {}
    indicators = []
    missing = []
    for key, name, group, series in series_specs(division):
        if series is None:
            missing.append({"key": key, "error": "no mapped item for this division (see industry.DIVISIONS)"})
            continue
        try:
            raw = fetch(series)
        except (EcosAuthenticationError, EcosRateLimitError):
            raise
        except EcosAPIError as exc:
            missing.append({"key": key, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
            continue
        if len({time for time, _ in raw}) != len(raw):
            missing.append({"key": key, "error": "several rows per period; item_codes do not pin one series"})
            continue
        values = macro.year_over_year(raw) if series.transform == "yoy" else list(raw)
        summary = macro.summarize(values, window_years=window_years, cycle=series.cycle)
        if summary is None:
            missing.append({"key": key, "error": "no data in the window"})
            continue
        points[key] = values
        indicators.append(
            {
                "key": key,
                "name": name,
                "group": group,
                "unit": series.unit,
                "transform": series.transform,
                "source": {"stat_code": series.stat_code, "cycle": series.cycle, "item_codes": list(series.item_codes)},
                **summary,
            }
        )
    inventory_cycle = _inventory_cycle(points, window_years=window_years)
    return {"indicators": indicators, "inventory_cycle": inventory_cycle, "missing": missing}
