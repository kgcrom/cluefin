"""Domain DTOs used by cluefin-cli services."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FinancialMetric:
    name: str
    label: str | None = None
    value: str | int | float | None = None
    unit: str | None = None
    period: str | None = None
    source: str | None = None


@dataclass(slots=True)
class DividendSnapshot:
    category: str
    current: str | None = None
    previous: str | None = None
    two_years_ago: str | None = None
    stock_kind: str | None = None
    source: str | None = None


@dataclass(slots=True)
class ShareholderSnapshot:
    name: str
    relation: str | None = None
    shares_current: str | None = None
    holding_ratio_current: str | None = None
    shares_previous: str | None = None
    holding_ratio_previous: str | None = None
    source: str | None = None


@dataclass(slots=True)
class StatementSnapshot:
    stock_code: str
    source: str
    corp_code: str | None = None
    company_name: str | None = None
    business_year: str | None = None
    report_code: str | None = None
    accounts: list[FinancialMetric] = field(default_factory=list)
    metrics: list[FinancialMetric] = field(default_factory=list)
    dividends: list[DividendSnapshot] = field(default_factory=list)
    shareholders: list[ShareholderSnapshot] = field(default_factory=list)
    xbrl_statements: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class OhlcvPoint:
    timestamp: str
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None
    volume: float | None = None


@dataclass(slots=True)
class IndicatorSnapshot:
    name: str
    values: list[float | None] = field(default_factory=list)
    latest: float | None = None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class OhlcvSeries:
    stock_code: str
    source: str
    interval: str
    points: list[OhlcvPoint] = field(default_factory=list)
    indicators: list[IndicatorSnapshot] = field(default_factory=list)


@dataclass(slots=True)
class NewsHeadline:
    source: str
    title: str
    published_at: str | None = None
    stock_codes: list[str] = field(default_factory=list)
    provider: str | None = None
    raw_id: str | None = None


@dataclass(slots=True)
class DisclosureHeadline:
    source: str
    report_name: str
    rcept_no: str | None = None
    rcept_date: str | None = None
    corp_code: str | None = None
    corp_name: str | None = None
    stock_code: str | None = None


@dataclass(slots=True)
class TradingFlowSnapshot:
    stock_code: str
    source: str
    start_date: str
    end_date: str
    rows: list[dict[str, Any]] = field(default_factory=list)
    totals: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MarketRankItem:
    source: str
    category: str
    rank: int | None = None
    stock_code: str | None = None
    stock_name: str | None = None
    value: str | int | float | None = None
    change_rate: str | int | float | None = None
    raw: dict[str, Any] = field(default_factory=dict)
