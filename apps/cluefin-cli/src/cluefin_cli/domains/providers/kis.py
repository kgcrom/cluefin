"""KIS provider adapter."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from cluefin_cli.domains.models import FinancialMetric, NewsHeadline, StatementSnapshot
from cluefin_cli.domains.providers.base import BrokerProvider


class KisProvider(BrokerProvider):
    broker = "kis"

    def fetch_statement_snapshot(self, *, stock_code: str, div_cls_code: str = "0") -> StatementSnapshot:
        stock_info = self.client.domestic_stock_info
        metrics: list[FinancialMetric] = []
        for label, response in [
            ("balance_sheet", stock_info.get_balance_sheet(div_cls_code, "J", stock_code)),
            ("income_statement", stock_info.get_income_statement(div_cls_code, "J", stock_code)),
            ("financial_ratio", stock_info.get_financial_ratio(div_cls_code, "J", stock_code)),
        ]:
            metrics.extend(self._metrics_from_output(label, self._extract_output(response)))

        return StatementSnapshot(stock_code=stock_code.zfill(6), source="kis", metrics=metrics)

    def fetch_news(
        self, *, stock_code: str | None = None, days: int = 7, query: str | None = None
    ) -> list[NewsHeadline]:
        start = (date.today() - timedelta(days=days)).strftime("00%Y%m%d")
        response = self.client.domestic_issue_other.get_market_announcement_schedule(
            "",
            "",
            stock_code or "",
            query or "",
            start,
            "",
            "",
            "",
        )
        items = self._extract_output(response)
        return [
            NewsHeadline(
                source="kis",
                title=getattr(item, "hts_pbnt_titl_cntt", ""),
                published_at=self._published_at(item),
                stock_codes=[
                    code
                    for code in [
                        getattr(item, "iscd1", ""),
                        getattr(item, "iscd2", ""),
                        getattr(item, "iscd3", ""),
                        getattr(item, "iscd4", ""),
                        getattr(item, "iscd5", ""),
                    ]
                    if code
                ],
                provider=getattr(item, "dorg", None),
                raw_id=getattr(item, "cntt_usiq_srno", None),
            )
            for item in items
        ]

    @staticmethod
    def _extract_output(response: Any) -> list[Any]:
        output = getattr(getattr(response, "body", response), "output", [])
        if output is None:
            return []
        if isinstance(output, (list, tuple)):
            return list(output)
        return [output]

    @staticmethod
    def _metrics_from_output(section: str, items: list[Any]) -> list[FinancialMetric]:
        metrics: list[FinancialMetric] = []
        for item in items:
            data = item.model_dump() if hasattr(item, "model_dump") else getattr(item, "__dict__", {})
            for key, value in data.items():
                if value in {None, ""}:
                    continue
                metrics.append(FinancialMetric(name=f"{section}.{key}", value=value, source="kis"))
        return metrics

    @staticmethod
    def _published_at(item: Any) -> str | None:
        data_dt = getattr(item, "data_dt", None)
        data_tm = getattr(item, "data_tm", None)
        if data_dt and data_tm:
            return f"{data_dt}{data_tm}"
        return data_dt
