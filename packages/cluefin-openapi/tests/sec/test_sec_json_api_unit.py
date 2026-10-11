"""Unit tests for the SEC JSON APIs: company tickers, submissions, XBRL facts/concept/frames.

Payloads are trimmed copies of real responses (same keys and value types).
"""

from datetime import date, datetime, timezone
from decimal import Decimal

import pytest
import requests_mock

from cluefin_openapi.sec import (
    Client,
    CompanyConcept,
    CompanyFacts,
    CompanySubmissions,
    FilingEntry,
    Frame,
    SecNotFoundError,
)

USER_AGENT = "Cluefin Test test@example.com"


@pytest.fixture
def client() -> Client:
    return Client(user_agent=USER_AGENT)


def _recent_columns(*rows: dict) -> dict:
    return {key: [row[key] for row in rows] for key in rows[0]}


TENK_ROW = {
    "accessionNumber": "0000320193-23-000106",
    "filingDate": "2023-11-03",
    "reportDate": "2023-09-30",
    "acceptanceDateTime": "2023-11-02T18:08:27.000Z",
    "act": "34",
    "form": "10-K",
    "fileNumber": "001-36743",
    "filmNumber": "231373899",
    "items": "",
    "core_type": "10-K",
    "size": 9472616,
    "isXBRL": 1,
    "isInlineXBRL": 1,
    "primaryDocument": "aapl-20230930.htm",
    "primaryDocDescription": "10-K",
}
FORM4_ROW = {
    **TENK_ROW,
    "accessionNumber": "0000320193-23-000110",
    "filingDate": "2023-11-20",
    "reportDate": "2023-11-16",
    "act": "",
    "form": "4",
    "fileNumber": "",
    "filmNumber": "",
    "core_type": "4",
    "size": 4800,
    "isXBRL": 0,
    "isInlineXBRL": 0,
    "primaryDocument": "xslF345X05/wk-form4_1700519405.xml",
    "primaryDocDescription": "FORM 4",
}
TENK_A_ROW = {**TENK_ROW, "accessionNumber": "0000320193-24-000001", "filingDate": "2024-01-10", "form": "10-K/A"}

SUBMISSIONS_PAYLOAD = {
    "cik": "320193",
    "entityType": "operating",
    "sic": "3571",
    "sicDescription": "Electronic Computers",
    "ownerOrg": "06 Technology",
    "insiderTransactionForOwnerExists": 0,
    "insiderTransactionForIssuerExists": 1,
    "name": "Apple Inc.",
    "tickers": ["AAPL"],
    "exchanges": ["Nasdaq"],
    "ein": "942404110",
    "lei": None,
    "description": "",
    "website": "",
    "investorWebsite": "",
    "category": "Large Accelerated Filer",
    "fiscalYearEnd": "0928",
    "stateOfIncorporation": "CA",
    "stateOfIncorporationDescription": "CA",
    "addresses": {"mailing": {"street1": "ONE APPLE PARK WAY", "city": "CUPERTINO"}},
    "phone": "(408) 996-1010",
    "flags": "",
    "formerNames": [
        {"name": "APPLE COMPUTER INC", "from": "1994-01-26T00:00:00.000Z", "to": "2007-01-04T00:00:00.000Z"}
    ],
    "filings": {
        "recent": _recent_columns(TENK_A_ROW, FORM4_ROW, TENK_ROW),
        "files": [
            {
                "name": "CIK0000320193-submissions-001.json",
                "filingCount": 1,
                "filingFrom": "1994-01-26",
                "filingTo": "2015-03-02",
            }
        ],
    },
}
OLD_PAGE_PAYLOAD = _recent_columns(
    {**TENK_ROW, "accessionNumber": "0001193125-14-383437", "filingDate": "2014-10-27", "reportDate": "2014-09-27"}
)


class TestReference:
    def test_company_tickers(self, client: Client):
        payload = {
            "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."},
            "1": {"cik_str": 1067983, "ticker": "BRK-B", "title": "BERKSHIRE HATHAWAY INC"},
        }
        with requests_mock.Mocker() as m:
            m.get("https://www.sec.gov/files/company_tickers.json", json=payload)
            rows = client.reference.company_tickers()
        assert [(row.cik, row.ticker, row.title) for row in rows] == [
            (320193, "AAPL", "Apple Inc."),
            (1067983, "BRK-B", "BERKSHIRE HATHAWAY INC"),
        ]

    @pytest.mark.parametrize(
        "ticker, expected", [("aapl", 320193), ("BRK.B", 1067983), ("brk-b", 1067983), ("ZZZZ", None)]
    )
    def test_ticker_to_cik(self, client: Client, ticker, expected):
        payload = {
            "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."},
            "1": {"cik_str": 1067983, "ticker": "BRK-B", "title": "BERKSHIRE HATHAWAY INC"},
        }
        with requests_mock.Mocker() as m:
            m.get("https://www.sec.gov/files/company_tickers.json", json=payload)
            assert client.reference.ticker_to_cik(ticker) == expected

    def test_company_tickers_exchange(self, client: Client):
        payload = {
            "fields": ["cik", "name", "ticker", "exchange"],
            "data": [[320193, "Apple Inc.", "AAPL", "Nasdaq"], [1001, "Delisted Co", "DLST", None]],
        }
        with requests_mock.Mocker() as m:
            m.get("https://www.sec.gov/files/company_tickers_exchange.json", json=payload)
            rows = client.reference.company_tickers_exchange()
        assert rows[0].exchange == "Nasdaq"
        assert rows[1].exchange is None

    def test_company_tickers_rejects_non_object(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get("https://www.sec.gov/files/company_tickers.json", json=[])
            with pytest.raises(TypeError):
                client.reference.company_tickers()


class TestSubmissions:
    def test_submissions_unpacks_columnar_filings(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get("https://data.sec.gov/submissions/CIK0000320193.json", json=SUBMISSIONS_PAYLOAD)
            company = client.submissions.submissions(320193)

        assert isinstance(company, CompanySubmissions)
        assert company.name == "Apple Inc."
        assert company.fiscal_year_end == "0928"
        assert company.former_names[0].name == "APPLE COMPUTER INC"
        assert [f.form for f in company.filings] == ["10-K/A", "4", "10-K"]
        assert company.filing_files[0].filing_to == date(2015, 3, 2)

        tenk = company.filings[2]
        assert tenk.accession_number == "0000320193-23-000106"
        assert tenk.report_date == date(2023, 9, 30)
        assert tenk.acceptance_date_time == datetime(2023, 11, 2, 18, 8, 27, tzinfo=timezone.utc)
        assert tenk.is_xbrl is True and tenk.is_inline_xbrl is True
        assert tenk.items is None  # "" becomes None
        assert tenk.primary_document == "aapl-20230930.htm"

        form4 = company.filings[1]
        assert form4.act is None and form4.file_number is None
        assert form4.is_xbrl is False

    def test_mismatched_column_lengths_fail_loudly(self, client: Client):
        broken = {**SUBMISSIONS_PAYLOAD, "filings": {"recent": {"form": ["10-K", "4"], "accessionNumber": ["x"]}}}
        with requests_mock.Mocker() as m:
            m.get("https://data.sec.gov/submissions/CIK0000320193.json", json=broken)
            with pytest.raises(ValueError, match="열 길이"):
                client.submissions.submissions(320193)

    def test_filings_filters_forms_with_amendments(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get("https://data.sec.gov/submissions/CIK0000320193.json", json=SUBMISSIONS_PAYLOAD)
            assert [f.form for f in client.submissions.filings(320193, forms=["10-k"])] == ["10-K/A", "10-K"]
            assert [f.form for f in client.submissions.filings(320193, forms=["10-K"], include_amendments=False)] == [
                "10-K"
            ]
            assert len(client.submissions.filings(320193)) == 3
            assert m.call_count == 3

    def test_filings_include_older_pages_sorted_newest_first(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get("https://data.sec.gov/submissions/CIK0000320193.json", json=SUBMISSIONS_PAYLOAD)
            m.get("https://data.sec.gov/submissions/CIK0000320193-submissions-001.json", json=OLD_PAGE_PAYLOAD)
            entries = client.submissions.filings(320193, forms=["10-K"], include_older=True)
        assert [e.filing_date.year for e in entries] == [2024, 2023, 2014]

    def test_submissions_page(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get("https://data.sec.gov/submissions/CIK0000320193-submissions-001.json", json=OLD_PAGE_PAYLOAD)
            rows = client.submissions.submissions_page("CIK0000320193-submissions-001.json")
        assert len(rows) == 1 and isinstance(rows[0], FilingEntry)

    @pytest.mark.parametrize(
        "name", ["../submissions/CIK0000320193.json", "CIK0000320193.json", "x-submissions-001.json"]
    )
    def test_submissions_page_rejects_other_names(self, client: Client, name):
        with pytest.raises(ValueError, match="페이지"):
            client.submissions.submissions_page(name)


FACT_ROWS = [
    {
        "start": "2022-09-25",
        "end": "2023-09-30",
        "val": 383285000000,
        "accn": "0000320193-23-000106",
        "fy": 2023,
        "fp": "FY",
        "form": "10-K",
        "filed": "2023-11-03",
        "frame": "CY2023",
    },
    {
        "start": "2022-09-25",
        "end": "2023-09-30",
        "val": 383285000000,
        "accn": "0000320193-24-000123",
        "fy": 2024,
        "fp": "FY",
        "form": "10-K",
        "filed": "2024-11-01",
    },
]


class TestXbrlApi:
    def test_company_facts(self, client: Client):
        payload = {
            "cik": 320193,
            "entityName": "Apple Inc.",
            "facts": {
                "dei": {
                    "EntityCommonStockSharesOutstanding": {
                        "label": "Entity Common Stock, Shares Outstanding",
                        "description": "...",
                        "units": {
                            "shares": [
                                {
                                    "end": "2023-10-20",
                                    "val": 15550061000,
                                    "accn": "0000320193-23-000106",
                                    "fy": 2023,
                                    "fp": "FY",
                                    "form": "10-K",
                                    "filed": "2023-11-03",
                                    "frame": "CY2023Q3I",
                                }
                            ]
                        },
                    }
                },
                "us-gaap": {
                    "Revenues": {"label": "Revenues", "description": "...", "units": {"USD": FACT_ROWS}},
                    "EarningsPerShareDiluted": {
                        "label": "EPS",
                        "description": "...",
                        "units": {"USD/shares": [{**FACT_ROWS[0], "val": 6.13}]},
                    },
                },
            },
        }
        with requests_mock.Mocker() as m:
            m.get("https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json", json=payload)
            facts = client.xbrl.company_facts("0000320193")

        assert isinstance(facts, CompanyFacts)
        assert facts.entity_name == "Apple Inc."
        revenues = facts.concept("us-gaap", "Revenues")
        assert revenues is not None
        first, restated = revenues.units["USD"]
        assert first.val == Decimal("383285000000")
        assert first.start == date(2022, 9, 25) and first.end == date(2023, 9, 30)
        assert first.frame == "CY2023" and restated.frame is None
        assert facts.concept("us-gaap", "EarningsPerShareDiluted").units["USD/shares"][0].val == Decimal("6.13")
        shares = facts.concept("dei", "EntityCommonStockSharesOutstanding").units["shares"][0]
        assert shares.start is None
        assert facts.concept("us-gaap", "Missing") is None
        assert facts.concept("ifrs-full", "Revenue") is None

    def test_company_concept(self, client: Client):
        payload = {
            "cik": 320193,
            "taxonomy": "us-gaap",
            "tag": "Revenues",
            "label": "Revenues",
            "description": "...",
            "entityName": "Apple Inc.",
            "units": {"USD": FACT_ROWS},
        }
        url = "https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/Revenues.json"
        with requests_mock.Mocker() as m:
            m.get(url, json=payload)
            concept = client.xbrl.company_concept(320193, "us-gaap", "Revenues")
        assert isinstance(concept, CompanyConcept)
        assert len(concept.units["USD"]) == 2

    def test_company_concept_missing_raises_not_found(self, client: Client):
        url = "https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/NotAConcept.json"
        with requests_mock.Mocker() as m:
            m.get(url, status_code=404)
            with pytest.raises(SecNotFoundError):
                client.xbrl.company_concept(320193, "us-gaap", "NotAConcept")

    def test_frames_converts_unit_and_parses(self, client: Client):
        payload = {
            "taxonomy": "us-gaap",
            "tag": "EarningsPerShareDiluted",
            "ccp": "CY2023",
            "uom": "USD/shares",
            "label": "EPS",
            "description": "...",
            "pts": 2,
            "data": [
                {
                    "accn": "0000320193-23-000106",
                    "cik": 320193,
                    "entityName": "Apple Inc.",
                    "loc": "US-CA",
                    "start": "2022-09-25",
                    "end": "2023-09-30",
                    "val": 6.13,
                },
                {
                    "accn": "0000789019-23-014423",
                    "cik": 789019,
                    "entityName": "MICROSOFT CORPORATION",
                    "loc": "US-WA",
                    "start": "2022-07-01",
                    "end": "2023-06-30",
                    "val": 9.68,
                },
            ],
        }
        url = "https://data.sec.gov/api/xbrl/frames/us-gaap/EarningsPerShareDiluted/USD-per-shares/CY2023.json"
        with requests_mock.Mocker() as m:
            m.get(url, json=payload)
            frame = client.xbrl.frames("us-gaap", "EarningsPerShareDiluted", "USD/shares", "CY2023")
        assert isinstance(frame, Frame)
        assert frame.pts == 2
        assert [row.val for row in frame.data] == [Decimal("6.13"), Decimal("9.68")]

    @pytest.mark.parametrize("period", ["2023", "CY23", "CY2023Q5", "CY2023I", "FY2023", "CY2023Q1i"])
    def test_frames_rejects_bad_period(self, client: Client, period):
        with pytest.raises(ValueError, match="기간"):
            client.xbrl.frames("us-gaap", "Revenues", "USD", period)

    def test_bad_tag_never_reaches_the_network(self, client: Client):
        with requests_mock.Mocker() as m:
            with pytest.raises(ValueError):
                client.xbrl.company_concept(320193, "us-gaap", "../../submissions/CIK0000320193")
            assert m.call_count == 0
