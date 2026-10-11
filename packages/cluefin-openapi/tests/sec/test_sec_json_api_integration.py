"""Live checks against www.sec.gov / data.sec.gov (read-only, no account involved)."""

from datetime import date
from decimal import Decimal

import pytest

from cluefin_openapi.sec import Client, FilingEntry, SecNotFoundError

from ._env import SEC_USER_AGENT, requires_user_agent

pytestmark = [pytest.mark.integration, requires_user_agent]

APPLE_CIK = 320193
# Apple FY2023 10-K (period 2022-09-25 ~ 2023-09-30): net sales $383,285M.
APPLE_FY2023_10K = "0000320193-23-000106"
APPLE_FY2023_REVENUE = Decimal("383285000000")


@pytest.fixture(scope="module")
def client() -> Client:
    return Client(user_agent=SEC_USER_AGENT or "")


def _declared_keys(model) -> set[str]:
    return {field.alias or name for name, field in model.model_fields.items()}


def test_ticker_to_cik(client: Client):
    tickers = client.reference.company_tickers()
    assert len(tickers) > 5000
    by_ticker = {row.ticker: row.cik for row in tickers}
    assert by_ticker["AAPL"] == APPLE_CIK
    assert by_ticker["BRK-B"] == 1067983


def test_company_tickers_exchange(client: Client):
    rows = client.reference.company_tickers_exchange()
    apple = next(row for row in rows if row.ticker == "AAPL")
    assert apple.cik == APPLE_CIK
    assert apple.exchange == "Nasdaq"


def test_submissions_rows_match_the_live_columns(client: Client):
    raw = client._get_json("https://data.sec.gov/submissions/CIK0000320193.json")
    live_columns = set(raw["filings"]["recent"])
    # A new or renamed column must be declared on FilingEntry, not left in model_extra.
    assert live_columns == _declared_keys(FilingEntry)

    company = client.submissions.submissions(APPLE_CIK)
    assert company.name == "Apple Inc."
    assert company.tickers[0] == "AAPL"
    assert company.fiscal_year_end == "0927" or company.fiscal_year_end == "0928"
    assert len(company.filings) == len(raw["filings"]["recent"]["accessionNumber"])
    assert company.filing_files, "Apple has more history than fits in `recent`"


def test_older_page_and_form_filter(client: Client):
    tenks = client.submissions.filings(APPLE_CIK, forms=["10-K"], include_older=True)
    fy2023 = next(entry for entry in tenks if entry.accession_number == APPLE_FY2023_10K)
    assert fy2023.report_date == date(2023, 9, 30)
    assert fy2023.primary_document == "aapl-20230930.htm"
    assert fy2023.is_inline_xbrl
    # Older pages reach back to the 1990s.
    assert min(entry.filing_date for entry in tenks) < date(2000, 1, 1)


def test_company_facts_revenue(client: Client):
    facts = client.xbrl.company_facts(APPLE_CIK)
    assert facts.entity_name == "Apple Inc."
    revenue = facts.concept("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax")
    assert revenue is not None
    row = next(
        v
        for v in revenue.units["USD"]
        if v.accn == APPLE_FY2023_10K and v.start == date(2022, 9, 25) and v.end == date(2023, 9, 30)
    )
    assert row.val == APPLE_FY2023_REVENUE
    assert row.form == "10-K"


def test_company_concept_revenue(client: Client):
    concept = client.xbrl.company_concept(APPLE_CIK, "us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax")
    values = {(v.accn, v.start, v.end): v.val for v in concept.units["USD"]}
    assert values[(APPLE_FY2023_10K, date(2022, 9, 25), date(2023, 9, 30))] == APPLE_FY2023_REVENUE


def test_company_concept_unknown_tag_is_not_found(client: Client):
    with pytest.raises(SecNotFoundError):
        client.xbrl.company_concept(APPLE_CIK, "us-gaap", "DefinitelyNotAConcept")


def test_frames_instant_assets(client: Client):
    frame = client.xbrl.frames("us-gaap", "Assets", "USD", "CY2023Q4I")
    assert frame.ccp == "CY2023Q4I"
    assert frame.pts == len(frame.data) > 1000
    assert all(row.start is None for row in frame.data)


def test_frames_per_share_unit(client: Client):
    frame = client.xbrl.frames("us-gaap", "EarningsPerShareDiluted", "USD/shares", "CY2023")
    assert frame.uom == "USD-per-shares" or frame.uom == "USD/shares"
    assert frame.pts > 100
