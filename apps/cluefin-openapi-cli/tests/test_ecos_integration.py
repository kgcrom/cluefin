"""Live check of `ecos macro-snapshot` against ecos.bok.or.kr (read-only, ECOS_AUTH_KEY from .env.test).

About 15 series calls. It guards the series table in `macro.py`: a code ECOS retires or a table that grows a second
item group shows up here as a `missing` entry.
"""

from __future__ import annotations

import os
from pathlib import Path

import dotenv
import pytest
from cluefin_openapi import BrokerClientConfig, BrokerClientFactory

from cluefin_openapi_cli import industry, macro
from cluefin_openapi_cli.handlers.ecos import handle_industry_outlook, handle_macro_snapshot, handle_series

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / ".env.test")
ECOS_AUTH_KEY = os.getenv("ECOS_AUTH_KEY")

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not ECOS_AUTH_KEY, reason="ECOS_AUTH_KEY is not set (.env.test)"),
]


class _Session:
    def __init__(self) -> None:
        # Not BrokerClientConfig.from_env(): it merges the cwd's .env (production) into the config.
        self._ecos = BrokerClientFactory(BrokerClientConfig(ecos_auth_key=ECOS_AUTH_KEY)).create("ecos")

    def get_ecos(self):
        return self._ecos


def test_macro_snapshot_reads_every_series() -> None:
    result = handle_macro_snapshot({"window_years": 5}, _Session())

    assert result["missing"] == []
    assert [row["key"] for row in result["indicators"]] == [series.key for series in macro.SERIES]
    assert [row["key"] for row in result["derived"]] == [spec.key for spec in macro.DERIVED]
    for row in result["indicators"]:
        assert 0 <= row["percentile"] <= 100, row["key"]
        assert row["min"] <= row["value"] <= row["max"], row["key"]


def test_series_reads_a_short_daily_range() -> None:
    result = handle_series(
        {"stat_code": "817Y002", "cycle": "D", "start_date": "20261001", "end_date": "20261031",
         "item_codes": "010200000"},
        _Session(),
    )  # fmt: skip

    assert result["unit"] == "연%"
    assert result["total"] > 15
    assert all(row["item_code1"] == "010200000" for row in result["data"])


def test_industry_outlook_reads_one_division_end_to_end() -> None:
    result = handle_industry_outlook({"induty_code": "26410", "window_years": 5}, _Session())

    assert result["missing"] == []
    assert result["industry"]["ksic"] == "26"
    keys = {row["key"] for row in result["indicators"]}
    assert keys == {
        "bsi_outlook",
        "bsi_actual",
        "production_yoy",
        "shipment_yoy",
        "inventory_yoy",
        "export_price_yoy",
        "ppi_yoy",
        "export_value_yoy",
    }
    assert result["inventory_cycle"] is not None
    for row in result["indicators"]:
        assert 0 <= row["percentile"] <= 100, row["key"]
        assert row["min"] <= row["value"] <= row["max"], row["key"]


#: Real data gaps checked live (2026-11-03), not stale codes: 인쇄(18), 의료용 물질 및 의약품(21), 기타 운송장비(31)
#: all have production and shipment data in 901Y032 but no 재고(inventory) index for the division (blank rows).
_KNOWN_GAPS = {("18", "inventory_yoy"), ("21", "inventory_yoy"), ("31", "inventory_yoy")}


@pytest.mark.slow
def test_industry_outlook_reads_every_division_table_entry() -> None:
    """Every one of the 24 divisions' *mapped* items returns data — guards `industry.DIVISIONS` itself.

    A division legitimately missing a product-level code (e.g. no export price for 음료/목재/기타운송장비, see
    `industry.py`'s module docstring) still shows up in `missing` with "no mapped item" — that is not a stale
    code, so it is excluded here on purpose, along with `_KNOWN_GAPS`.
    """
    for division in industry.DIVISIONS:
        induty_code = f"{division.ksic}00"
        result = handle_industry_outlook({"induty_code": induty_code, "window_years": 5}, _Session())
        broken = [
            row
            for row in result["missing"]
            if "no mapped item" not in row["error"] and (division.ksic, row["key"]) not in _KNOWN_GAPS
        ]
        assert broken == [], (division.ksic, broken)
