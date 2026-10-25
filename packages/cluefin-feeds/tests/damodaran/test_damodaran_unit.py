"""Damodaran: ctryprem.html 표, 업종 β xls, 종목 업종 행 파싱."""

import datetime as dt
from decimal import Decimal
from pathlib import Path

import pytest
import requests_mock

from cluefin_feeds import FeedParseError, HttpClient
from cluefin_feeds.damodaran import Client, CompanyIndustry
from cluefin_feeds.damodaran._parse import parse_companies, parse_country_risk_premiums, parse_industry_betas

FIXTURES = Path(__file__).parent / "fixtures"
BASE = "https://pages.stern.nyu.edu/~adamodar"


@pytest.fixture
def client() -> Client:
    return Client(HttpClient(max_retries=0, min_interval=0))


class TestCountryRiskPremiums:
    def test_korea_row(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(f"{BASE}/New_Home_Page/datafile/ctryprem.html", content=(FIXTURES / "ctryprem.html").read_bytes())
            table = client.country_risk_premiums()
        assert table.updated == dt.date(2026, 1, 5)
        korea = table.get("Korea")
        assert korea is not None
        assert (korea.moodys_rating, korea.country_risk_premium, korea.equity_risk_premium) == (
            "Aa2",
            Decimal("0.64"),
            Decimal("4.87"),
        )
        assert korea.corporate_tax_rate == Decimal("26.40")

    def test_na_becomes_none(self):
        table = parse_country_risk_premiums((FIXTURES / "ctryprem.html").read_text(encoding="latin-1"))
        north = table.get("Korea, D.P.R.")
        assert north.sovereign_cds is None
        assert north.cds_equity_risk_premium is None
        assert north.equity_risk_premium == Decimal("19.77")

    def test_columns_are_found_by_name_not_position(self):
        page = """<p>Last updated: July 1, 2026</p><table>
        <tr><td>Equity Risk Premium</td><td>Country</td><td>Country Risk Premium</td><td>Moody's rating</td>
            <td>Adj. Default Spread</td><td>Corporate Tax Rate</td><td>Sovereign CDS</td><td>ERP based on sovereign CDS</td></tr>
        <tr><td>5.00%</td><td>Korea</td><td>0.70%</td><td>Aa2</td><td>0.45%</td><td>26.40%</td><td>0.21%</td><td>4.60%</td></tr>
        </table>"""
        with pytest.raises(FeedParseError):  # 첫 열이 Country 가 아니면 표를 못 찾는다
            parse_country_risk_premiums(page)
        moved = page.replace(
            "<td>Equity Risk Premium</td><td>Country</td>", "<td>Country</td><td>Equity Risk Premium</td>"
        )
        moved = moved.replace("<td>5.00%</td><td>Korea</td>", "<td>Korea</td><td>5.00%</td>")
        korea = parse_country_risk_premiums(moved).get("Korea")
        assert (korea.equity_risk_premium, korea.country_risk_premium) == (Decimal("5.00"), Decimal("0.70"))
        assert parse_country_risk_premiums(moved).updated == dt.date(2026, 7, 1)

    def test_missing_column_is_named(self):
        page = "<table><tr><td>Country</td><td>Equity Risk Premium</td></tr><tr><td>Korea</td><td>4%</td></tr></table>"
        with pytest.raises(FeedParseError, match="moody"):
            parse_country_risk_premiums(page)


class TestIndustryBetas:
    def test_emerging_markets_xls(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(f"{BASE}/pc/datasets/betaemerg.xls", content=(FIXTURES / "betaemerg.xls").read_bytes())
            table = client.industry_betas("emerging")
        assert table.region == "Emerging Markets"
        assert table.updated == dt.date(2026, 1, 5)
        assert table.marginal_tax_rate == pytest.approx(0.2471)
        assert len(table.rows) == 96
        advertising = table.get("Advertising")
        assert advertising.number_of_firms == 184
        assert advertising.unlevered_beta_corrected_for_cash == pytest.approx(1.2809853688611113)
        assert advertising.unlevered_beta == pytest.approx(1.1632831718620542)
        assert set(advertising.unlevered_beta_by_year) == {2022, 2023, 2024, 2025}
        assert advertising.unlevered_beta_average is not None
        assert table.rows[-1].industry_name == "Total Market (without financials)"

    def test_unknown_region(self, client: Client):
        with pytest.raises(ValueError, match="region"):
            client.industry_betas("mars")  # type: ignore[arg-type]

    def test_not_an_xls(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(f"{BASE}/pc/datasets/betas.xls", content=b"<html>moved</html>")
            with pytest.raises(FeedParseError, match="xls"):
                client.industry_betas("us")

    def test_rows_stop_at_blank_and_header_is_required(self):
        header = ["Industry Name", "Number of firms", "Beta ", "D/E Ratio", "Effective Tax rate", "Unlevered beta"]
        header += ["Cash/Firm value", "Unlevered beta corrected for cash"]
        rows = [["Date updated:", 46027.0], header, ["Steel", 10.0, 1.1, 0.5, 0.2, 0.8, 0.05, 0.84], [""], ["Notes"]]
        table = parse_industry_betas(rows, lambda serial: dt.date(2026, 1, 5))
        assert [r.industry_name for r in table.rows] == ["Steel"]
        assert table.rows[0].hilo_risk is None  # 선택 열이 없어도 된다
        with pytest.raises(FeedParseError, match="Industry Name"):
            parse_industry_betas(rows[2:], lambda serial: dt.date(2026, 1, 5))


class TestCompanies:
    HEADER = [
        "Company Name",
        "Exchange:Ticker",
        "Industry Group",
        "Primary Sector",
        "SIC Code",
        "Country",
        "Broad Group",
        "Sub Group",
    ]

    def test_filter_and_krx_code(self):
        rows = [
            self.HEADER,
            ["Samsung Electronics Co., Ltd. (KOSE:A005930)", "KOSE:A005930", "Computers/Peripherals", "IT", "3674",
             "South Korea", "Emerging Markets", "Small Asia"],
            ["ADforus Co., Ltd. (KOSDAQ:A397810)", "KOSDAQ:A397810", "Advertising", "CS", 9995.0, "South Korea",
             "Emerging Markets", "Small Asia"],
            ["Coupang (NYSE:CPNG)", "NYSE:CPNG", "Retail (General)", "CD", "5961", "South Korea", "Emerging Markets",
             "Small Asia"],
            ["Apple Inc. (NasdaqGS:AAPL)", "NasdaqGS:AAPL", "Computers/Peripherals", "IT", "3571", "United States",
             "United States", "United States"],
        ]  # fmt: skip
        korea = parse_companies(rows, "South Korea")
        assert [c.krx_code for c in korea] == ["005930", "397810", None]
        assert korea[1].sic_code == "9995"
        assert len(parse_companies(rows, None)) == 4

    def test_konex_and_blank_ticker(self):
        konex = CompanyIndustry(company_name="X", exchange_ticker="XKON:A123456", industry_group="Software")
        blank = CompanyIndustry(company_name="Y", exchange_ticker="", industry_group="Software")
        assert (konex.krx_code, blank.krx_code) == ("123456", None)
