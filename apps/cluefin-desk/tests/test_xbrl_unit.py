from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from cluefin_desk.data.xbrl import XbrlStatementFetcher


def _make_fetcher(disclosures, status="000"):
    with (
        patch("cluefin_desk.data.xbrl.PublicDisclosure") as public_cls,
        patch("cluefin_desk.data.xbrl.PeriodicReportFinancialStatement"),
    ):
        fetcher = XbrlStatementFetcher(MagicMock())
        public_cls.return_value.public_disclosure_search.return_value = SimpleNamespace(
            result=SimpleNamespace(status=status, list=disclosures)
        )
    return fetcher


def _filing(report_nm, rcept_no="20260310000123"):
    return SimpleNamespace(report_nm=report_nm, rcept_no=rcept_no)


class TestFindRceptNo:
    def test_matches_annual_report_by_keyword_and_period(self):
        fetcher = _make_fetcher(
            [
                _filing("분기보고서 (2025.09)", "1"),
                _filing("사업보고서 (2025.12)", "2"),
            ]
        )
        assert fetcher.find_rcept_no("00126380", "2025", "11011") == "2"

    def test_q1_and_q3_are_distinguished_by_period_marker(self):
        fetcher = _make_fetcher(
            [
                _filing("분기보고서 (2025.03)", "q1"),
                _filing("분기보고서 (2025.09)", "q3"),
            ]
        )
        assert fetcher.find_rcept_no("00126380", "2025", "11013") == "q1"
        assert fetcher.find_rcept_no("00126380", "2025", "11014") == "q3"

    def test_unknown_report_code_returns_none(self):
        fetcher = _make_fetcher([_filing("사업보고서 (2025.12)")])
        assert fetcher.find_rcept_no("00126380", "2025", "99999") is None

    def test_error_status_returns_none(self):
        fetcher = _make_fetcher([_filing("사업보고서 (2025.12)")], status="013")
        assert fetcher.find_rcept_no("00126380", "2025", "11011") is None

    def test_no_match_returns_none(self):
        fetcher = _make_fetcher([_filing("사업보고서 (2024.12)")])
        assert fetcher.find_rcept_no("00126380", "2025", "11011") is None
