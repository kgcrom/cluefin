"""Live check of `dart financial-as-filed` against DART (real .env key, two downloads).

Nodemason (01328170) FY2024: the original filing and its amendment report opposite-sign
consolidated operating income. The first run on a cold Arelle cache can take about a minute.
"""

from __future__ import annotations

import os
from pathlib import Path

import dotenv
import pytest
from cluefin_openapi import BrokerClientConfig, BrokerClientFactory

from cluefin_openapi_cli.handlers.dart import handle_financial_as_filed

CORP = "01328170"
ORIGINAL = "20250318001317"
AMENDED = "20250828000839"


class _Session:
    def __init__(self, dart) -> None:
        self._dart = dart

    def get_dart(self):
        return self._dart


@pytest.fixture(scope="module")
def session() -> _Session:
    dotenv.load_dotenv()
    if not os.getenv("DART_AUTH_KEY"):
        pytest.skip("DART_AUTH_KEY is not configured")
    return _Session(BrokerClientFactory(BrokerClientConfig.from_env()).create("dart"))


def _operating_income(session: _Session, rcept_no: str) -> str:
    result = handle_financial_as_filed(
        {"rcept_no": rcept_no, "reprt_code": "11011", "corp_code": CORP, "statements": "CIS", "fs_div": "CFS"},
        session,
    )
    assert result["entity_id"] == CORP and result["reporting_period_end"] == "2024-12-31"
    rows = [r for r in result["statements"]["CIS"]["consolidated"] if r["concept_qname"] == "dart:OperatingIncomeLoss"]
    # Current period sorts first.
    assert rows[0]["end_date"] == "2024-12-31"
    return rows[0]["value"]


@pytest.mark.integration
def test_original_and_amended_operating_income_have_opposite_signs(session: _Session) -> None:
    original = _operating_income(session, ORIGINAL)
    amended = _operating_income(session, AMENDED)

    assert original == "28915427"
    assert amended == "-190143795"
    assert not list(Path(".").glob("*.xbrl"))  # pass-through contract: nothing left behind
