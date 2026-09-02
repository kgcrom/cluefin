"""XBRL financial statement fetcher using DART OpenAPI + cluefin-xbrl parser.

Ported from cluefin-cli's data/xbrl.py, adapted for desk: the fetcher takes the
app-lifetime DART client instead of building its own from settings.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from cluefin_openapi.dart._client import Client as DartClient
from cluefin_openapi.dart._periodic_report_financial_statement import PeriodicReportFinancialStatement
from cluefin_openapi.dart._public_disclosure import PublicDisclosure
from cluefin_xbrl import (
    ParsedFinancialStatements,
    ParsedNotes,
    XbrlDocument,
    extract_financial_statements,
    extract_notes,
    parse_xbrl_directory,
)


@dataclass
class XbrlBundle:
    """All data parseable from a single XBRL filing."""

    document: XbrlDocument
    statements: ParsedFinancialStatements
    notes: ParsedNotes


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

    def __init__(self, dart_client: DartClient):
        self._public_disclosure = PublicDisclosure(dart_client)
        self._financial_statement = PeriodicReportFinancialStatement(dart_client)

    def fetch(
        self,
        rcept_no: str,
        reprt_code: Literal["11011", "11012", "11013", "11014"],
    ) -> XbrlBundle:
        """Download the XBRL ZIP from DART, parse it, and extract everything."""
        dest = Path(tempfile.mkdtemp(prefix="cluefin_xbrl_"))
        xbrl_dir = self._financial_statement.download_financial_statement_xbrl(
            rcept_no=rcept_no,
            reprt_code=reprt_code,
            destination=dest,
            overwrite=True,
        )
        doc = parse_xbrl_directory(xbrl_dir, include_taxonomy=True)
        statements = extract_financial_statements(doc)
        notes = extract_notes(doc)
        return XbrlBundle(document=doc, statements=statements, notes=notes)

    def find_rcept_no(self, corp_code: str, year: str, reprt_code: str) -> str | None:
        """Find the rcept_no for a given report by searching public disclosures."""
        rule = REPORT_MATCH_RULES.get(reprt_code)
        if rule is None:
            return None

        report_keyword, period_marker = rule
        year_period = f"({year}{period_marker}"

        result = self._public_disclosure.public_disclosure_search(
            corp_code=corp_code,
            bgn_de=f"{year}0101",
            # Search into the next year for annual reports filed after year-end
            end_de=f"{int(year) + 1}1231",
            pblntf_ty="A",
            last_reprt_at="Y",
        )

        if result.result.status != "000":
            return None

        for item in result.result.list or []:
            if report_keyword in item.report_nm and year_period in item.report_nm:
                return item.rcept_no

        return None
