"""Statements domain service."""

from __future__ import annotations

from datetime import date

from cluefin_cli.domains.models import StatementSnapshot
from cluefin_cli.domains.providers import DartProvider, KisProvider

REPORT_CODE_MAP = {
    "annual": "11011",
    "half": "11012",
    "q1": "11013",
    "q3": "11014",
}


def default_business_year() -> str:
    return str(date.today().year - 1)


class StatementsService:
    def __init__(self, dart_provider: DartProvider | None = None, kis_provider: KisProvider | None = None) -> None:
        self.dart_provider = dart_provider or DartProvider()
        self.kis_provider = kis_provider or KisProvider()

    def fetch(
        self,
        *,
        stock_code: str,
        source: str = "auto",
        year: str | None = None,
        report: str = "annual",
        include_xbrl: bool = False,
        statement_type: str | None = None,
    ) -> list[StatementSnapshot]:
        report_code = REPORT_CODE_MAP[report]
        business_year = year or default_business_year()
        snapshots: list[StatementSnapshot] = []

        if source in {"auto", "dart", "all"}:
            snapshots.append(
                self.dart_provider.fetch_statement_snapshot(
                    stock_code=stock_code,
                    business_year=business_year,
                    report_code=report_code,
                    include_xbrl=include_xbrl,
                    statement_type=statement_type,
                )
            )

        if source in {"kis", "all"}:
            div_cls_code = "0" if report == "annual" else "1"
            snapshots.append(
                self.kis_provider.fetch_statement_snapshot(stock_code=stock_code, div_cls_code=div_cls_code)
            )

        return snapshots
