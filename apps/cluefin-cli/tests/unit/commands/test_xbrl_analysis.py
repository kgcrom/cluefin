"""Tests for XBRL analysis command."""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

from click.testing import CliRunner
from cluefin_xbrl import (
    FinancialStatement,
    NoteLineItem,
    NoteSection,
    ParsedFinancialStatements,
    ParsedNotes,
    PeriodType,
    StatementLineItem,
    StatementType,
    XbrlDocument,
    XbrlPeriod,
)

from cluefin_cli.commands.xbrl_analysis import xbrl_analysis
from cluefin_cli.data.xbrl import XbrlBundle


def _make_bundle(
    statements: ParsedFinancialStatements,
    notes: ParsedNotes | None = None,
) -> XbrlBundle:
    """Wrap statements (and optional notes) into an XbrlBundle for the fetcher mock."""
    document = XbrlDocument(
        source_file="test.xbrl",
        facts=[],
        entity_id=statements.entity_id,
        reporting_period_end=None,
    )
    return XbrlBundle(
        document=document,
        statements=statements,
        notes=notes or ParsedNotes(source_file="test.xbrl", entity_id=statements.entity_id, notes={}),
    )


def _make_parsed_notes() -> ParsedNotes:
    """Build a ParsedNotes fixture with one consolidated and one separate note."""
    period = XbrlPeriod(period_type=PeriodType.INSTANT, instant="2024-12-31")

    cons = NoteSection(
        role_code="D810000",
        role_uri="http://example.com/role-D810000",
        title="일반사항",
        is_consolidated=True,
        line_items=[
            NoteLineItem(
                concept_local_name="EntityName",
                concept_qname="dart:EntityName",
                label_ko="회사명",
                text_value="삼성전자주식회사",
                period=period,
            ),
            NoteLineItem(
                concept_local_name="NumberOfEmployees",
                concept_qname="dart:NumberOfEmployees",
                label_ko="종업원수",
                value=Decimal("120000"),
                period=period,
                dimensions={"dart:SegmentAxis": "dart:DomesticMember"},
            ),
        ],
        periods=[period],
    )
    sep = NoteSection(
        role_code="D810005",
        role_uri="http://example.com/role-D810005",
        title="별도일반사항",
        is_consolidated=False,
        line_items=[
            NoteLineItem(
                concept_local_name="EntityName",
                concept_qname="dart:EntityName",
                label_ko="회사명",
                text_value="삼성전자별도",
                period=period,
            ),
        ],
        periods=[period],
    )
    return ParsedNotes(
        source_file="test.xbrl",
        entity_id="00126380",
        notes={"D810000": cons, "D810005": sep},
    )


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


def _make_parsed_with_separate() -> ParsedFinancialStatements:
    """ParsedFinancialStatements with both consolidated and separate BS."""
    period = XbrlPeriod(period_type=PeriodType.INSTANT, instant="2024-12-31")

    def _bs(label_ko: str, consolidated: bool) -> FinancialStatement:
        return FinancialStatement(
            statement_type=StatementType.BS,
            linkrole="http://example.com/BS",
            line_items=[
                StatementLineItem(
                    concept_local_name="Assets",
                    concept_qname="ifrs-full:Assets",
                    label_ko=label_ko,
                    label_en="Total Assets",
                    value=Decimal("100000000000"),
                    unit="KRW",
                    period=period,
                    depth=0,
                    order=1.0,
                    is_abstract=False,
                )
            ],
            periods=[period],
            is_consolidated=consolidated,
        )

    return ParsedFinancialStatements(
        source_file="test.xbrl",
        entity_id="00126380",
        statements={"BS": _bs("연결자산총계", True)},
        separate_statements={"BS": _bs("별도자산총계", False)},
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
        mock_xbrl.fetch.return_value = _make_bundle(_make_parsed_statements())
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024", "--report", "annual"])

        assert result.exit_code == 0
        assert "XBRL Analysis" in result.output
        assert "자산총계" in result.output
        assert "유동자산" in result.output

        mock_xbrl.find_rcept_no.assert_called_once_with("00126380", "2024", "11011")
        mock_xbrl.fetch.assert_called_once_with("00126380", "20240401000123", "11011")

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
        mock_xbrl.fetch.assert_not_called()

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_filter_statement_type(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        mock_xbrl.fetch.return_value = _make_bundle(_make_parsed_statements())
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
        mock_xbrl.fetch.return_value = _make_bundle(_make_parsed_statements())
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024", "--statement-type", "BS"])

        assert result.exit_code == 0
        assert "자산총계" in result.output

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_separate_flag_shows_separate(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        mock_xbrl.fetch.return_value = _make_bundle(_make_parsed_with_separate())
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024", "--separate"])

        assert result.exit_code == 0
        assert "별도자산총계" in result.output
        assert "연결자산총계" not in result.output

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_consolidated_is_default(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        mock_xbrl.fetch.return_value = _make_bundle(_make_parsed_with_separate())
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024"])

        assert result.exit_code == 0
        assert "연결자산총계" in result.output
        assert "별도자산총계" not in result.output

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_separate_flag_empty(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        # fixture has no separate_statements
        mock_xbrl.fetch.return_value = _make_bundle(_make_parsed_statements())
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024", "--separate"])

        assert result.exit_code == 0
        assert "No separate financial statements found" in result.output

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_shows_notes(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        mock_xbrl.fetch.return_value = _make_bundle(_make_parsed_statements(), _make_parsed_notes())
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(
            xbrl_analysis, ["005930", "--year", "2024", "--section", "notes"], env={"COLUMNS": "220"}
        )

        assert result.exit_code == 0
        assert "Disclosure Notes" in result.output
        assert "D810000" in result.output
        assert "종업원수" in result.output
        # consolidated note text shown, separate one not (default --consolidated)
        assert "별도일반사항" not in result.output

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_separate_notes(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        mock_xbrl.fetch.return_value = _make_bundle(_make_parsed_statements(), _make_parsed_notes())
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(
            xbrl_analysis, ["005930", "--year", "2024", "--separate", "--section", "notes"], env={"COLUMNS": "220"}
        )

        assert result.exit_code == 0
        assert "별도일반사항" in result.output
        assert "일반사항" in result.output

    @patch("cluefin_cli.commands.xbrl_analysis.XbrlStatementFetcher")
    @patch("cluefin_cli.commands.xbrl_analysis.DomesticFundamentalDataFetcher")
    def test_xbrl_analysis_overview_section(self, mock_fundamental_cls, mock_xbrl_cls):
        mock_fundamental = MagicMock()
        mock_fundamental.get_corp_code = AsyncMock(return_value="00126380")
        mock_fundamental_cls.return_value = mock_fundamental

        mock_xbrl = MagicMock()
        mock_xbrl.find_rcept_no.return_value = "20240401000123"
        mock_xbrl.fetch.return_value = _make_bundle(_make_parsed_statements(), _make_parsed_notes())
        mock_xbrl_cls.return_value = mock_xbrl

        runner = CliRunner()
        result = runner.invoke(xbrl_analysis, ["005930", "--year", "2024", "--section", "overview"])

        assert result.exit_code == 0
        assert "Document Overview" in result.output
        # section=overview must not render statement/notes details
        assert "자산총계" not in result.output


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
