"""XBRL financial statement fetcher using DART OpenAPI + cluefin-xbrl parser."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Literal

from cluefin_openapi.dart._client import Client as DartClient
from cluefin_openapi.dart._periodic_report_financial_statement import PeriodicReportFinancialStatement
from cluefin_openapi.dart._public_disclosure import PublicDisclosure
from cluefin_xbrl import ParsedFinancialStatements, extract_financial_statements, parse_xbrl_directory

from cluefin_cli.config.settings import settings

REPORT_CODE_MAP: dict[str, str] = {
    "annual": "11011",
    "half": "11012",
    "q1": "11013",
    "q3": "11014",
}

# Report name must contain the type keyword AND the period-end marker (YYYY.MM)
# to distinguish Q1 (03) from Q3 (09) quarterly reports.
REPORT_MATCH_RULES: dict[str, tuple[str, str]] = {
    "11011": ("사업보고서", ".12)"),
    "11012": ("반기보고서", ".06)"),
    "11013": ("분기보고서", ".03)"),
    "11014": ("분기보고서", ".09)"),
}


class XbrlStatementFetcher:
    """Downloads XBRL from DART and parses financial statements via cluefin-xbrl."""

    def __init__(self):
        if not settings.dart_auth_key:
            raise ValueError("DART_AUTH_KEY environment variable is required for XBRL analysis.")

        self._client = DartClient(auth_key=settings.dart_auth_key)
        self._public_disclosure = PublicDisclosure(self._client)
        self._financial_statement = PeriodicReportFinancialStatement(self._client)

    def fetch_statements(
        self,
        corp_code: str,
        rcept_no: str,
        reprt_code: Literal["11011", "11012", "11013", "11014"],
    ) -> ParsedFinancialStatements:
        """Download XBRL ZIP from DART, parse, and extract financial statements.

        Args:
            corp_code: DART corporate code (8 digits).
            rcept_no: 접수번호 (14 digits).
            reprt_code: Report code.

        Returns:
            ParsedFinancialStatements with structured data.
        """
        dest = Path(tempfile.mkdtemp(prefix="cluefin_xbrl_"))
        xbrl_dir = self._financial_statement.download_financial_statement_xbrl(
            rcept_no=rcept_no,
            reprt_code=reprt_code,
            destination=dest,
            overwrite=True,
        )
        doc = parse_xbrl_directory(xbrl_dir, include_taxonomy=True)
        return extract_financial_statements(doc)

    def find_rcept_no(
        self,
        corp_code: str,
        year: str,
        reprt_code: str,
    ) -> str | None:
        """Find the rcept_no for a given report by searching public disclosures.

        Args:
            corp_code: DART corporate code (8 digits).
            year: Business year (YYYY).
            reprt_code: Report code (e.g. "11011").

        Returns:
            The rcept_no if found, else None.
        """
        rule = REPORT_MATCH_RULES.get(reprt_code)
        if rule is None:
            return None

        report_keyword, period_marker = rule
        # Build the expected period marker with the year, e.g. "(2024.03)"
        year_period = f"({year}{period_marker}"

        bgn_de = f"{year}0101"
        # Search into the next year for annual reports filed after year-end
        end_de = f"{int(year) + 1}1231"

        result = self._public_disclosure.public_disclosure_search(
            corp_code=corp_code,
            bgn_de=bgn_de,
            end_de=end_de,
            pblntf_ty="A",
            last_reprt_at="Y",
        )

        if result.result.status != "000":
            return None

        for item in result.result.list or []:
            if report_keyword in item.report_nm and year_period in item.report_nm:
                return item.rcept_no

        return None
