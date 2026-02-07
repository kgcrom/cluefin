"""Integration with cluefin-openapi DART client for download + parse workflow."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from cluefin_xbrl._types import ParsedFinancialStatements, XbrlDocument
from cluefin_xbrl.parser import parse_xbrl_directory
from cluefin_xbrl.statements import extract_financial_statements

if TYPE_CHECKING:
    from cluefin_openapi.dart._periodic_report_financial_statement import PeriodicReportFinancialStatement


def download_and_parse_xbrl(
    dart_financial_statement: PeriodicReportFinancialStatement,
    rcept_no: str,
    reprt_code: Literal["11011", "11012", "11013", "11014"],
    *,
    destination: Path | str | None = None,
    include_taxonomy: bool = True,
) -> XbrlDocument:
    """Download XBRL from DART and parse it.

    Args:
        dart_financial_statement: DART PeriodicReportFinancialStatement instance.
        rcept_no: 접수번호 (14자리).
        reprt_code: 보고서코드.
        destination: 다운로드 경로. None이면 임시 디렉토리 사용.
        include_taxonomy: taxonomy 추출 여부.

    Returns:
        Parsed XbrlDocument.
    """
    dest = _resolve_destination(destination)
    xbrl_dir = dart_financial_statement.download_financial_statement_xbrl(
        rcept_no=rcept_no,
        reprt_code=reprt_code,
        destination=dest,
        overwrite=True,
    )
    return parse_xbrl_directory(xbrl_dir, include_taxonomy=include_taxonomy)


def download_and_extract_statements(
    dart_financial_statement: PeriodicReportFinancialStatement,
    rcept_no: str,
    reprt_code: Literal["11011", "11012", "11013", "11014"],
    *,
    destination: Path | str | None = None,
) -> ParsedFinancialStatements:
    """Download XBRL from DART, parse, and extract financial statements.

    Args:
        dart_financial_statement: DART PeriodicReportFinancialStatement instance.
        rcept_no: 접수번호 (14자리).
        reprt_code: 보고서코드.
        destination: 다운로드 경로. None이면 임시 디렉토리 사용.

    Returns:
        ParsedFinancialStatements with structured data.
    """
    doc = download_and_parse_xbrl(
        dart_financial_statement,
        rcept_no,
        reprt_code,
        destination=destination,
        include_taxonomy=True,
    )
    return extract_financial_statements(doc)


def _resolve_destination(destination: Path | str | None) -> Path:
    """Resolve download destination, creating temp dir if needed."""
    if destination is None:
        return Path(tempfile.mkdtemp(prefix="cluefin_xbrl_"))
    return Path(destination)
