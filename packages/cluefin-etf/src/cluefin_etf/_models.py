from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ProviderName(str, Enum):
    KODEX = "kodex"
    TIGER = "tiger"
    RISE = "rise"
    ACE = "ace"
    SOL = "sol"
    KIWOOM = "kiwoom"

    @classmethod
    def _missing_(cls, value: object) -> "ProviderName | None":
        if isinstance(value, str):
            normalized = value.lower()
            for member in cls:
                if member.value == normalized:
                    return member
        return None


class ProviderInfo(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: ProviderName
    display_name: str
    homepage_url: str | None = None


class EtfSummary(BaseModel):
    model_config = ConfigDict(frozen=True)

    provider: ProviderName
    code: str
    name: str
    isin: str | None = None
    category: str | None = None
    benchmark: str | None = None
    listing_date: date | None = None
    nav: Decimal | None = None
    aum: Decimal | None = None
    expense_ratio: Decimal | None = None
    as_of_date: date | None = None
    detail_url: str | None = None
    holdings_url: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class EtfDetail(BaseModel):
    model_config = ConfigDict(frozen=True)

    provider: ProviderName
    code: str
    name: str | None = None
    isin: str | None = None
    category: str | None = None
    benchmark: str | None = None
    listing_date: date | None = None
    nav: Decimal | None = None
    aum: Decimal | None = None
    expense_ratio: Decimal | None = None
    as_of_date: date | None = None
    detail_url: str | None = None
    holdings_url: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class FetchMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)

    provider: ProviderName
    url: str
    strategy: Literal["http", "playwright"]
    status_code: int | None = None
    final_url: str | None = None
    content_type: str | None = None
    elapsed_ms: float | None = None
    fallback_reason: str | None = None


class FetchResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    html: str
    metadata: FetchMetadata
