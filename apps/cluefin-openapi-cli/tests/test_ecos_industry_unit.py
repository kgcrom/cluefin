from __future__ import annotations

import re
from datetime import date
from types import SimpleNamespace

import pytest
from cluefin_openapi.ecos import EcosPage, EcosQueryTimeoutError, StatisticObservation

from cluefin_openapi_cli import industry, macro
from cluefin_openapi_cli.errors import EXIT_BROKER, EXIT_CREDENTIALS, EXIT_USAGE, CliError
from cluefin_openapi_cli.handlers import ecos as handlers

_KSIC_CODES = {f"{n:02d}" for n in range(10, 34)}


def test_divisions_cover_every_ksic_manufacturing_code() -> None:
    assert {d.ksic for d in industry.DIVISIONS} == _KSIC_CODES
    assert len(industry.DIVISIONS) == 24
    # No duplicates, no accidental reuse of a production item across divisions.
    assert len({d.production_item for d in industry.DIVISIONS}) == 24


def test_division_codes_are_well_formed() -> None:
    for division in industry.DIVISIONS:
        assert re.fullmatch(r"I11AC[A-Z]", division.production_item), division
        if division.bsi_item is not None:
            assert re.fullmatch(r"C\d{4}", division.bsi_item), division
        for code in (division.export_price_item, division.ppi_item, division.export_value_item):
            if code is not None:
                assert re.fullmatch(r"[0-9]{3,6}AA", code), (division, code)
        # A division with no product name has no product-level codes either (division 18, printing).
        if division.product_name is None:
            assert division.export_price_item is None
            assert division.ppi_item is None
            assert division.export_value_item is None


def test_resolve_division_uses_the_first_two_digits() -> None:
    division = industry.resolve_division("26410")
    assert division is not None
    assert (division.ksic, division.bsi_item) == ("26", "C2600")
    assert industry.resolve_division("26") is division

    assert industry.resolve_division("09000") is None  # agriculture, not manufacturing
    assert industry.resolve_division("64") is None  # finance
    assert industry.resolve_division("5") is None  # too short to resolve


def test_series_specs_mark_divisions_with_no_mapped_product_as_none() -> None:
    printing = next(d for d in industry.DIVISIONS if d.ksic == "18")
    specs = dict((key, series) for key, _, _, series in industry.series_specs(printing))
    assert specs["export_price_yoy"] is None
    assert specs["ppi_yoy"] is None
    assert specs["export_value_yoy"] is None
    # Production/shipment/inventory and BSI are always mapped for a manufacturing division.
    assert specs["production_yoy"] is not None
    assert specs["bsi_outlook"] is not None


def _codes(series: macro.MacroSeries | None) -> tuple[str, ...]:
    assert series is not None
    return series.item_codes


def test_series_specs_item_code_group_order() -> None:
    electronics = next(d for d in industry.DIVISIONS if d.ksic == "26")
    specs = dict((key, series) for key, _, _, series in industry.series_specs(electronics))
    assert _codes(specs["bsi_outlook"]) == ("BA", "C2600")
    assert _codes(specs["bsi_actual"]) == ("AA", "C2600")
    assert _codes(specs["production_yoy"]) == ("I11ACQ", "1")
    assert _codes(specs["shipment_yoy"]) == ("I11ACQ", "3")
    assert _codes(specs["inventory_yoy"]) == ("I11ACQ", "5")
    assert _codes(specs["export_price_yoy"]) == ("30911AA", "W")
    assert _codes(specs["ppi_yoy"]) == ("30911AA",)
    assert _codes(specs["export_value_yoy"]) == ("30911AA",)


def _monthly(start_value: float, months: int = 25, step: float = 1.0) -> list[macro.Point]:
    """25 consecutive monthly points (chronological) so a year-over-year base exists for the latest 13."""
    points = []
    for m in range(months):
        year, month = divmod(2024 * 12 + m, 12)
        time = f"{year}{month + 1:02d}"
        points.append((time, start_value + step * m))
    return points


def test_inventory_cycle_reports_signs_and_difference_not_a_phase_name() -> None:
    electronics = next(d for d in industry.DIVISIONS if d.ksic == "26")

    def fetch(series: macro.MacroSeries) -> list[macro.Point]:
        if series.key == "shipment_yoy":
            return _monthly(100.0, step=1.0)  # rising level -> positive yoy
        if series.key == "inventory_yoy":
            return _monthly(200.0, step=-1.0)  # falling level -> negative yoy
        return _monthly(50.0)

    result = industry.industry_outlook(electronics, fetch, window_years=10)
    cycle = result["inventory_cycle"]
    assert cycle is not None
    assert cycle["shipments_up"] is True
    assert cycle["inventory_up"] is False
    for phase_word in ("회복", "확장", "수축"):
        assert phase_word not in cycle["name"]
    assert cycle["value"] == pytest.approx(cycle_shipment_minus_inventory(result))


def cycle_shipment_minus_inventory(result: dict) -> float:
    by_key = {row["key"]: row["value"] for row in result["indicators"]}
    return by_key["shipment_yoy"] - by_key["inventory_yoy"]


def test_industry_outlook_records_a_failed_or_ambiguous_series_and_keeps_going() -> None:
    printing = next(d for d in industry.DIVISIONS if d.ksic == "18")

    def fetch(series: macro.MacroSeries) -> list[macro.Point]:
        if series.key == "bsi_outlook":
            raise EcosQueryTimeoutError("60초", code="ERROR-400")
        if series.key == "production_yoy":
            return [("202609", 100.0), ("202609", 90.0)]
        return _monthly(10.0)

    result = industry.industry_outlook(printing, fetch, window_years=10)
    missing = {row["key"]: row["error"] for row in result["missing"]}
    assert "bsi_outlook" in missing
    assert "EcosQueryTimeoutError" in missing["bsi_outlook"]
    assert "several rows" in missing["production_yoy"]
    for key in ("export_price_yoy", "ppi_yoy", "export_value_yoy"):
        assert "no mapped item" in missing[key]
    # shipment/inventory still came through, so the inventory cycle can still be computed.
    assert result["inventory_cycle"] is not None


class _Session:
    def __init__(self, *, sample: bool = False) -> None:
        self.calls: list[tuple] = []

        def search(stat_code, cycle, start, end, item_codes):
            self.calls.append((stat_code, cycle, start, end, item_codes))
            rows = [
                {"STAT_CODE": stat_code, "STAT_NAME": "x", "TIME": time, "DATA_VALUE": str(value)}
                for time, value in _monthly(100.0)
            ]
            return EcosPage[StatisticObservation].model_validate({"list_total_count": len(rows), "row": rows})

        self._client = SimpleNamespace(is_sample=sample, statistic_search=SimpleNamespace(search=search))

    def get_ecos(self):
        return self._client


def test_handler_calls_every_mapped_series_once(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(handlers, "_today", lambda: date(2026, 11, 1))
    session = _Session()

    result = handlers.handle_industry_outlook({"induty_code": "26410"}, session)

    assert len(session.calls) == 8  # bsi x2, production/shipment/inventory x3, product price x3
    assert result["industry"] == {
        "ksic": "26",
        "name": "전자부품, 컴퓨터, 영상, 음향 및 통신장비 제조업",
        "product": "반도체",
        "codes": {
            "bsi": "C2600",
            "production_shipment_inventory": "I11ACQ",
            "export_price": "30911AA",
            "ppi": "30911AA",
            "export_value": "30911AA",
        },
    }
    assert result["missing"] == []
    assert result["window_years"] == 10
    assert any("no phase" in note or "phase" in note for note in result["notes"])


def test_handler_refuses_the_sample_key() -> None:
    session = _Session(sample=True)
    with pytest.raises(CliError) as caught:
        handlers.handle_industry_outlook({"induty_code": "26410"}, session)
    assert caught.value.exit_code == EXIT_CREDENTIALS
    assert session.calls == []


def test_handler_rejects_a_non_manufacturing_induty_code() -> None:
    session = _Session()
    with pytest.raises(CliError) as caught:
        handlers.handle_industry_outlook({"induty_code": "64110"}, session)
    assert caught.value.exit_code == EXIT_USAGE
    assert caught.value.error_type == "UnsupportedIndustry"
    assert session.calls == []


def test_handler_fails_when_nothing_came_back(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(handlers, "_today", lambda: date(2026, 11, 1))

    class _EmptySession:
        def __init__(self) -> None:
            self.calls: list[tuple] = []

        def get_ecos(self):
            def search(stat_code, cycle, start, end, item_codes):
                self.calls.append((stat_code, cycle, start, end, item_codes))
                return EcosPage[StatisticObservation].model_validate({"list_total_count": 0, "row": []})

            return SimpleNamespace(is_sample=False, statistic_search=SimpleNamespace(search=search))

    session = _EmptySession()
    with pytest.raises(CliError) as caught:
        handlers.handle_industry_outlook({"induty_code": "26410"}, session)
    assert caught.value.exit_code == EXIT_BROKER
    assert len(caught.value.data["missing"]) == 8
