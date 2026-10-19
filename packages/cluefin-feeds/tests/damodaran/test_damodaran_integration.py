"""Live checks against pages.stern.nyu.edu (read-only; indname.xls 는 약 22MB)."""

import pytest

from cluefin_feeds.damodaran import Client

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def client() -> Client:
    return Client()


def test_country_risk_premiums(client: Client):
    table = client.country_risk_premiums()
    assert len(table.rows) > 150
    korea = table.get("Korea")
    assert korea is not None and korea.equity_risk_premium is not None
    assert 3 < korea.equity_risk_premium < 10
    assert table.updated is not None


def test_emerging_industry_betas(client: Client):
    table = client.industry_betas("emerging")
    assert table.region == "Emerging Markets"
    assert len(table.rows) > 90
    assert all(row.unlevered_beta_corrected_for_cash is not None for row in table.rows)


def test_korean_companies_match_beta_industries(client: Client):
    companies = client.companies("South Korea")
    assert len(companies) > 2000
    samsung = next(c for c in companies if c.krx_code == "005930")
    industries = {row.industry_name for row in client.industry_betas("emerging").rows}
    assert samsung.industry_group in industries
    unmatched = {c.industry_group for c in companies} - industries
    assert not unmatched, f"업종 β 표에 없는 업종: {unmatched}"
