"""KIS provider adapter."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from cluefin_cli.domains.models import (
    FinancialMetric,
    MarketRankItem,
    NewsHeadline,
    OhlcvPoint,
    OhlcvSeries,
    StatementSnapshot,
    TradingFlowSnapshot,
)
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

    def fetch_ohlcv(self, *, stock_code: str, interval: str = "daily", days: int = 300) -> OhlcvSeries:
        quote = self.client.domestic_basic_quote
        if interval == "minute":
            response = quote.get_stock_today_minute_chart("J", stock_code, "153000", "Y", "")
            items = getattr(response.body, "output2", [])
            points = [self._ohlcv_from_minute(item) for item in items]
        else:
            end_date = date.today()
            start_date = end_date - timedelta(days=days * 2)
            response = quote.get_stock_period_quote(
                "J",
                stock_code,
                start_date.strftime("%Y%m%d"),
                end_date.strftime("%Y%m%d"),
                "D",
                "0",
            )
            items = getattr(response.body, "output2", [])
            points = [self._ohlcv_from_daily(item) for item in items]

        points = sorted(points, key=lambda item: item.timestamp)[-days:]
        return OhlcvSeries(stock_code=stock_code.zfill(6), source="kis", interval=interval, points=points)

    def fetch_trading_flow(self, *, stock_code: str, start_date: str, end_date: str) -> TradingFlowSnapshot:
        response = self.client.domestic_market_analysis.get_investor_trading_trend_by_stock_daily(
            "J", stock_code, end_date
        )
        rows: list[dict[str, Any]] = []
        for item in getattr(response.body, "output2", []):
            row_date = getattr(item, "stck_bsop_date", "")
            if row_date and row_date < start_date:
                continue
            rows.append(
                {
                    "date": row_date,
                    "individual": self._to_float(getattr(item, "prsn_ntby_qty", None)),
                    "foreign": self._to_float(getattr(item, "frgn_ntby_qty", None)),
                    "institution": self._to_float(getattr(item, "orgn_ntby_qty", None)),
                    "securities": self._to_float(getattr(item, "scrt_ntby_qty", None)),
                    "investment_trust": self._to_float(getattr(item, "ivtr_ntby_qty", None)),
                    "private_fund": self._to_float(getattr(item, "pe_fund_ntby_vol", None)),
                    "bank": self._to_float(getattr(item, "bank_ntby_qty", None)),
                    "insurance": self._to_float(getattr(item, "insu_ntby_qty", None)),
                    "fund": self._to_float(getattr(item, "fund_ntby_qty", None)),
                    "other": self._to_float(getattr(item, "etc_ntby_qty", None)),
                }
            )
        rows = sorted(rows, key=lambda item: item["date"])
        return TradingFlowSnapshot(
            stock_code=stock_code.zfill(6),
            source="kis",
            start_date=start_date,
            end_date=end_date,
            rows=rows,
            totals=self._totals(rows),
        )

    def fetch_market_volume(self, *, limit: int = 20) -> list[MarketRankItem]:
        response = self.client.domestic_ranking_analysis.get_trading_volume_rank(
            "J",
            "20171",
            "0000",
            "0",
            "0",
            "111111111",
            "0000000000",
            "",
            "",
            "",
            "",
        )
        return [
            self._market_item(item, source="kis", category="volume", value_field="acml_vol")
            for item in getattr(response.body, "output", [])[:limit]
        ]

    def fetch_market_ranking(self, *, limit: int = 20) -> list[MarketRankItem]:
        response = self.client.domestic_ranking_analysis.get_stock_fluctuation_rank(
            "",
            "J",
            "20170",
            "0000",
            "0",
            "0",
            "0",
            "",
            "",
            "",
            "0",
            "0",
            "0",
            "",
        )
        return [
            self._market_item(item, source="kis", category="ranking", value_field="stck_prpr")
            for item in getattr(response.body, "output", [])[:limit]
        ]

    def fetch_market_sector(self, *, limit: int = 20) -> list[MarketRankItem]:
        response = self.client.domestic_issue_other.get_sector_all_quote_by_category("U", "0001", "20214", "K", "0")
        return [
            MarketRankItem(
                source="kis",
                category="sector",
                rank=index + 1,
                stock_code=getattr(item, "bstp_cls_code", None),
                stock_name=getattr(item, "hts_kor_isnm", None),
                value=getattr(item, "bstp_nmix_prpr", None),
                change_rate=getattr(item, "bstp_nmix_prdy_ctrt", None),
                raw=self._raw_dict(item),
            )
            for index, item in enumerate(getattr(response.body, "output2", [])[:limit])
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

    @classmethod
    def _ohlcv_from_daily(cls, item: Any) -> OhlcvPoint:
        return OhlcvPoint(
            timestamp=getattr(item, "stck_bsop_date", ""),
            open=cls._to_float(getattr(item, "stck_oprc", None)),
            high=cls._to_float(getattr(item, "stck_hgpr", None)),
            low=cls._to_float(getattr(item, "stck_lwpr", None)),
            close=cls._to_float(getattr(item, "stck_clpr", None)),
            volume=cls._to_float(getattr(item, "acml_vol", None)),
        )

    @classmethod
    def _ohlcv_from_minute(cls, item: Any) -> OhlcvPoint:
        return OhlcvPoint(
            timestamp=f"{getattr(item, 'stck_bsop_date', '')}{getattr(item, 'stck_cntg_hour', '')}",
            open=cls._to_float(getattr(item, "stck_oprc", None)),
            high=cls._to_float(getattr(item, "stck_hgpr", None)),
            low=cls._to_float(getattr(item, "stck_lwpr", None)),
            close=cls._to_float(getattr(item, "stck_prpr", None)),
            volume=cls._to_float(getattr(item, "cntg_vol", None)),
        )

    @staticmethod
    def _to_float(value: Any) -> float | None:
        if value in {None, ""}:
            return None
        try:
            return float(str(value).replace(",", "").strip())
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _totals(rows: list[dict[str, Any]]) -> dict[str, float]:
        totals: dict[str, float] = {}
        for row in rows:
            for key, value in row.items():
                if key == "date" or value is None:
                    continue
                totals[key] = totals.get(key, 0.0) + float(value)
        return totals

    @classmethod
    def _market_item(cls, item: Any, *, source: str, category: str, value_field: str) -> MarketRankItem:
        return MarketRankItem(
            source=source,
            category=category,
            rank=cls._to_int(getattr(item, "data_rank", None)),
            stock_code=getattr(item, "mksc_shrn_iscd", None) or getattr(item, "stck_shrn_iscd", None),
            stock_name=getattr(item, "hts_kor_isnm", None),
            value=getattr(item, value_field, None),
            change_rate=getattr(item, "prdy_ctrt", None),
            raw=cls._raw_dict(item),
        )

    @staticmethod
    def _to_int(value: Any) -> int | None:
        if value in {None, ""}:
            return None
        try:
            return int(str(value).replace(",", "").strip())
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _raw_dict(item: Any) -> dict[str, Any]:
        if hasattr(item, "model_dump"):
            return item.model_dump()
        return dict(getattr(item, "__dict__", {}))
