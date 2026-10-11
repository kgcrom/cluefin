"""Financial statements from a real SEC filing (Apple FY2023 10-K, inline XBRL).

Downloads the filing with cluefin-openapi, then parses it here. Arelle fetches the US-GAAP/DEI taxonomies
on first run (cached afterwards), so this needs network and SEC_USER_AGENT ("Name email") in the
repo-root .env.test:
    uv run pytest packages/cluefin-xbrl/tests/test_sec_statements_integration.py -m integration
"""

import os
from datetime import date
from decimal import Decimal
from pathlib import Path

import dotenv
import pytest

from cluefin_xbrl import extract_financial_statements, parse_xbrl_directory

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / ".env.test")
_USER_AGENT = os.getenv("SEC_USER_AGENT")

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not _USER_AGENT, reason="SEC_USER_AGENT 미설정 (.env.test)"),
]

APPLE_CIK = 320193
APPLE_FY2023_10K = "0000320193-23-000106"
FY2023 = (date(2022, 9, 25), date(2023, 9, 30))


@pytest.fixture(scope="module")
def statements(tmp_path_factory):
    sec = pytest.importorskip("cluefin_openapi.sec")
    folder = tmp_path_factory.mktemp("aapl-fy2023")
    client = sec.Client(user_agent=_USER_AGENT)
    try:
        client.archives.download_xbrl_files(APPLE_CIK, APPLE_FY2023_10K, destination=folder)
    finally:
        client.close()

    doc = parse_xbrl_directory(folder, include_taxonomy=True, http_user_agent=_USER_AGENT)
    return doc, extract_financial_statements(doc)


def _value(statement, concept, *, period=None, instant=None, dimensions=None):
    matches = [
        item.value
        for item in statement.line_items
        if item.concept_local_name == concept
        and not item.is_abstract
        and item.dimensions == (dimensions or {})
        and (period is None or (item.period.start_date, item.period.end_date) == period)
        and (instant is None or item.period.instant == instant)
    ]
    # Exactly one row: inline XBRL repeats facts, and the extractor must collapse the copies.
    assert len(matches) == 1, f"{concept}: {matches}"
    return matches[0]


def test_document_metadata(statements):
    doc, _ = statements
    assert doc.source_file.endswith("aapl-20230930_htm.xml")
    assert doc.reporting_period_end == date(2023, 9, 30)
    assert doc.entity_id == "0000320193"


def test_five_consolidated_statements(statements):
    _, result = statements
    assert set(result.statements) == {"IS", "CIS", "BS", "SCE", "CF"}
    assert result.separate_statements == {}
    assert result.statements["BS"].linkrole.endswith("CONSOLIDATEDBALANCESHEETS")


def test_income_statement_numbers(statements):
    _, result = statements
    income = result.statements["IS"]
    revenue = "RevenueFromContractWithCustomerExcludingAssessedTax"
    assert _value(income, revenue, period=FY2023) == Decimal("383285000000")
    # Product and Service [Axis] is drawn on the face of Apple's income statement.
    assert _value(
        income, revenue, period=FY2023, dimensions={"srt:ProductOrServiceAxis": "us-gaap:ProductMember"}
    ) == Decimal("298085000000")
    assert _value(income, "NetIncomeLoss", period=FY2023) == Decimal("96995000000")


def test_balance_sheet_numbers(statements):
    _, result = statements
    balance = result.statements["BS"]
    assert _value(balance, "Assets", instant=date(2023, 9, 30)) == Decimal("352583000000")
    assert _value(balance, "Assets", instant=date(2022, 9, 24)) == Decimal("352755000000")


def test_cash_flow_numbers(statements):
    _, result = statements
    cash_flow = result.statements["CF"]
    assert _value(cash_flow, "NetCashProvidedByUsedInOperatingActivities", period=FY2023) == Decimal("110543000000")


def test_equity_statement_keeps_component_axis(statements):
    _, result = statements
    equity = result.statements["SCE"]
    axes = {axis for item in equity.line_items for axis in item.dimensions}
    assert "us-gaap:StatementEquityComponentsAxis" in axes
