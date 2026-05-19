"""DART provider adapter."""

from __future__ import annotations

import tempfile
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from cluefin_openapi.dart._periodic_report_financial_statement import PeriodicReportFinancialStatement
from cluefin_xbrl import extract_financial_statements, parse_xbrl_directory

from cluefin_cli.domains.models import (
    DisclosureHeadline,
    DividendSnapshot,
    FinancialMetric,
    ShareholderSnapshot,
    StatementSnapshot,
)
from cluefin_cli.domains.providers.base import BrokerProvider


class DartProvider(BrokerProvider):
    broker = "dart"

    def resolve_corp_code(self, stock_code: str) -> str:
        response = self.client.public_disclosure.corp_code()
        items = getattr(response, "list", None) or getattr(getattr(response, "result", None), "list", None) or []
        normalized = stock_code.zfill(6)
        for item in items:
            if getattr(item, "stock_code", None) == normalized:
                return item.corp_code
        raise ValueError(f"No DART corp code found for stock code {normalized}.")

    def fetch_statement_snapshot(
        self,
        *,
        stock_code: str,
        business_year: str,
        report_code: str,
        include_xbrl: bool = False,
        statement_type: str | None = None,
    ) -> StatementSnapshot:
        corp_code = self.resolve_corp_code(stock_code)
        overview = self.client.public_disclosure.company_overview(corp_code)
        financial_statement = PeriodicReportFinancialStatement(self.client)
        key_information = self.client.periodic_report_key_information

        accounts_response = financial_statement.get_single_company_major_accounts(corp_code, business_year, report_code)
        indicators_response = financial_statement.get_single_company_major_indicators(
            corp_code=corp_code,
            bsns_year=business_year,
            reprt_code=report_code,
            idx_cl_code="M210000",
        )
        dividends_response = key_information.get_dividend_information(corp_code, business_year, report_code)
        shareholders_response = key_information.get_major_shareholder_status(corp_code, business_year, report_code)

        xbrl_statements: dict[str, Any] = {}
        if include_xbrl:
            xbrl_statements = self.fetch_xbrl_statements(
                corp_code=corp_code,
                business_year=business_year,
                report_code=report_code,
                statement_type=statement_type,
            )

        return StatementSnapshot(
            stock_code=stock_code.zfill(6),
            source="dart",
            corp_code=corp_code,
            company_name=getattr(overview, "corp_name", None),
            business_year=business_year,
            report_code=report_code,
            accounts=[
                FinancialMetric(
                    name=getattr(item, "account_nm", ""),
                    label=getattr(item, "account_nm", None),
                    value=getattr(item, "thstrm_amount", None),
                    unit=getattr(item, "currency", None),
                    period=getattr(item, "thstrm_nm", None),
                    source="dart",
                )
                for item in self._response_items(accounts_response)
            ],
            metrics=[
                FinancialMetric(
                    name=getattr(item, "idx_nm", ""),
                    value=getattr(item, "idx_val", None),
                    source="dart",
                )
                for item in self._response_items(indicators_response)
            ],
            dividends=[
                DividendSnapshot(
                    category=getattr(item, "se", ""),
                    current=getattr(item, "thstrm", None),
                    previous=getattr(item, "frmtrm", None),
                    two_years_ago=getattr(item, "lwfr", None),
                    stock_kind=getattr(item, "stock_knd", None),
                    source="dart",
                )
                for item in self._response_items(dividends_response)
            ],
            shareholders=[
                ShareholderSnapshot(
                    name=getattr(item, "nm", ""),
                    relation=getattr(item, "relate", None),
                    shares_current=getattr(item, "trmend_posesn_stock_co", None),
                    holding_ratio_current=getattr(item, "trmend_posesn_stock_qota_rt", None),
                    shares_previous=getattr(item, "bsis_posesn_stock_co", None),
                    holding_ratio_previous=getattr(item, "bsis_posesn_stock_qota_rt", None),
                    source="dart",
                )
                for item in self._response_items(shareholders_response)
            ],
            xbrl_statements=xbrl_statements,
        )

    def fetch_disclosures(
        self,
        *,
        stock_code: str | None = None,
        days: int = 7,
        query: str | None = None,
    ) -> list[DisclosureHeadline]:
        end = date.today()
        begin = end - timedelta(days=days)
        corp_code = self.resolve_corp_code(stock_code) if stock_code else None
        response = self.client.public_disclosure.public_disclosure_search(
            corp_code=corp_code,
            bgn_de=begin.strftime("%Y%m%d"),
            end_de=end.strftime("%Y%m%d"),
            last_reprt_at="N",
        )

        items = self._response_items(response)
        if query:
            items = [item for item in items if query in getattr(item, "report_nm", "")]

        return [
            DisclosureHeadline(
                source="dart",
                report_name=getattr(item, "report_nm", ""),
                rcept_no=getattr(item, "rcept_no", None),
                rcept_date=getattr(item, "rcept_dt", None),
                corp_code=getattr(item, "corp_code", None),
                corp_name=getattr(item, "corp_name", None),
                stock_code=getattr(item, "stock_code", None),
            )
            for item in items
        ]

    def fetch_xbrl_statements(
        self,
        *,
        corp_code: str,
        business_year: str,
        report_code: str,
        statement_type: str | None = None,
    ) -> dict[str, Any]:
        rcept_no = self.find_report_rcept_no(corp_code, business_year, report_code)
        if rcept_no is None:
            return {}

        dest = Path(tempfile.mkdtemp(prefix="cluefin_xbrl_"))
        xbrl_dir = PeriodicReportFinancialStatement(self.client).download_financial_statement_xbrl(
            rcept_no=rcept_no,
            reprt_code=report_code,
            destination=dest,
            overwrite=True,
        )
        parsed = extract_financial_statements(parse_xbrl_directory(xbrl_dir, include_taxonomy=True))
        statements = parsed.statements
        if statement_type:
            statements = {key: value for key, value in statements.items() if key == statement_type.upper()}
        return {key: value.model_dump() if hasattr(value, "model_dump") else value for key, value in statements.items()}

    def find_report_rcept_no(self, corp_code: str, business_year: str, report_code: str) -> str | None:
        markers = {
            "11011": ("사업보고서", ".12)"),
            "11012": ("반기보고서", ".06)"),
            "11013": ("분기보고서", ".03)"),
            "11014": ("분기보고서", ".09)"),
        }
        rule = markers.get(report_code)
        if rule is None:
            return None
        keyword, period_marker = rule
        response = self.client.public_disclosure.public_disclosure_search(
            corp_code=corp_code,
            bgn_de=f"{business_year}0101",
            end_de=f"{int(business_year) + 1}1231",
            pblntf_ty="A",
            last_reprt_at="Y",
        )
        year_period = f"({business_year}{period_marker}"
        for item in self._response_items(response):
            if keyword in getattr(item, "report_nm", "") and year_period in getattr(item, "report_nm", ""):
                return getattr(item, "rcept_no", None)
        return None

    @staticmethod
    def _response_items(response: Any) -> list[Any]:
        result = getattr(response, "result", response)
        return list(getattr(result, "list", None) or getattr(response, "list", None) or [])
