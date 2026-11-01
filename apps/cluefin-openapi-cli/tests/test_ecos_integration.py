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

from cluefin_openapi_cli import macro
from cluefin_openapi_cli.handlers.ecos import handle_macro_snapshot, handle_series

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
