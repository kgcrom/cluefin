"""Tests for XBRL analysis command."""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

from click.testing import CliRunner
from cluefin_xbrl import (
    FinancialStatement,
    ParsedFinancialStatements,
    PeriodType,
    StatementLineItem,
    StatementType,
    XbrlPeriod,
)

from cluefin_cli.commands.xbrl_analysis import xbrl_analysis


def _make_parsed_statements() -> ParsedFinancialStatements:
    """Build a minimal ParsedFinancialStatements fixture."""
    period = XbrlPeriod(
        period_type=PeriodType.INSTANT,
        instant="2024-12-31",
    )
    bs = FinancialStatement(
        statement_type=StatementType.BS,
        linkrole="http://example.com/BS",
        line_items=[
            StatementLineItem(
                concept_local_name="Assets",
                concept_qname="ifrs-full:Assets",
                label_ko="자산총계",
                label_en="Total Assets",
                value=Decimal("100000000000"),
                unit="KRW",
                period=period,
                depth=0,
                order=1.0,
                is_abstract=False,
            ),
            StatementLineItem(
                concept_local_name="CurrentAssets",
                concept_qname="ifrs-full:CurrentAssets",
                label_ko="유동자산",
                label_en="Current Assets",
                value=Decimal("50000000000"),
                unit="KRW",
                period=period,
                depth=1,
                order=2.0,
                is_abstract=False,
            ),
        ],
        periods=[period],
    )
    return ParsedFinancialStatements(
        source_file="test.xbrl",
        entity_id="00126380",
        statements={"BS": bs},
    )


class TestXbrlAnalysisCommand:
    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_success(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        mock_xbrl.fetch_statements.return_value = _make_parsed_statements()
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024", "--report", "annual"])

        assert result.exit_code == 0
        assert "XBRL Analysis" in result.output
        assert "자산총계" in result.output
        assert "유동자산" in result.output

        mock_xbrl.find_rcept_no.assert_called_once_with("00126380", "2024", "11011")
        mock_xbrl.fetch_statements.assert_called_once_with("00126380", "20240401000123", "11011")

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_no_report_found(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = None
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024"])

        assert result.exit_code == 0
        assert "No report filing found" in result.output
        mock_xbrl.fetch_statements.assert_not_called()

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_filter_statement_type(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        mock_xbrl.fetch_statements.return_value = _make_parsed_statements()
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        # Filter for IS which doesn't exist in our fixture
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024", "--statement-type", "IS"])

        assert result.exit_code == 0
        assert "not found" in result.output

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_filter_bs(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        mock_xbrl.fetch_statements.return_value = _make_parsed_statements()
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024", "--statement-type", "BS"])

        assert result.exit_code == 0
        assert "자산총계" in result.output


class TestXbrlStatementFetcher:
    @patch("cluefin_cli.data.xbrl.settings")
    @patch("cluefin_cli.data.xbrl.PublicDisclosure")
    @patch("cluefin_cli.data.xbrl.PeriodicReportFinancialStatement")
    @patch("cluefin_cli.data.xbrl.DartClient")
    def test_find_rcept_no_annual(self, mock_client_cls, mock_fs_cls, mock_pd_cls, mock_settings):
        from cluefin_cli.data.xbrl import XbrlStatementFetcher

        mock_settings.dart_auth_key = "test_key"

        mock_pd = MagicMock()
        mock_search_result = MagicMock()
        mock_search_result.result.status = "000"
        mock_item = MagicMock()
        mock_item.report_nm = "[기재정정]사업보고서 (2024.12)"
        mock_item.rcept_no = "20250401000123"
        mock_search_result.result.list = [mock_item]
        mock_pd.public_disclosure_search.return_value = mock_search_result
        mock_pd_cls.return_value = mock_pd

        fetcher = XbrlStatementFetcher()
        rcept_no = fetcher.find_rcept_no("00126380", "2024", "11011")

        assert rcept_no == "20250401000123"

    @patch("cluefin_cli.data.xbrl.settings")
    @patch("cluefin_cli.data.xbrl.PublicDisclosure")
    @patch("cluefin_cli.data.xbrl.PeriodicReportFinancialStatement")
    @patch("cluefin_cli.data.xbrl.DartClient")
    def test_find_rcept_no_q1_skips_q3(self, mock_client_cls, mock_fs_cls, mock_pd_cls, mock_settings):
        from cluefin_cli.data.xbrl import XbrlStatementFetcher

        mock_settings.dart_auth_key = "test_key"

        mock_pd = MagicMock()
        mock_search_result = MagicMock()
        mock_search_result.result.status = "000"
        # Q3 report comes first in results (reverse chronological)
        q3_item = MagicMock()
        q3_item.report_nm = "분기보고서 (2024.09)"
        q3_item.rcept_no = "20241114002642"
        q1_item = MagicMock()
        q1_item.report_nm = "분기보고서 (2024.03)"
        q1_item.rcept_no = "20240516001421"
        mock_search_result.result.list = [q3_item, q1_item]
        mock_pd.public_disclosure_search.return_value = mock_search_result
        mock_pd_cls.return_value = mock_pd

        fetcher = XbrlStatementFetcher()
        rcept_no = fetcher.find_rcept_no("00126380", "2024", "11013")

        # Should pick Q1 (2024.03), not Q3 (2024.09)
        assert rcept_no == "20240516001421"

    @patch("cluefin_cli.data.xbrl.settings")
    @patch("cluefin_cli.data.xbrl.PublicDisclosure")
    @patch("cluefin_cli.data.xbrl.PeriodicReportFinancialStatement")
    @patch("cluefin_cli.data.xbrl.DartClient")
    def test_find_rcept_no_not_found(self, mock_client_cls, mock_fs_cls, mock_pd_cls, mock_settings):
        from cluefin_cli.data.xbrl import XbrlStatementFetcher

        mock_settings.dart_auth_key = "test_key"

        mock_pd = MagicMock()
        mock_search_result = MagicMock()
        mock_search_result.result.status = "000"
        mock_search_result.result.list = []
        mock_pd.public_disclosure_search.return_value = mock_search_result
        mock_pd_cls.return_value = mock_pd

        fetcher = XbrlStatementFetcher()
        rcept_no = fetcher.find_rcept_no("00126380", "2024", "11011")

        assert rcept_no is None
