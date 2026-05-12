from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from cluefin_etf.providers._normalization import blank_to_none, parse_display_decimal, return_text
from cluefin_etf.providers._parsing import normalize_space, parse_date_text, parse_int_text


class TigerEtfListItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    name: str
    ksd_fund: str | None = None
    category: str | None = None
    categories: list[str] = Field(default_factory=list)
    pension_flags: list[str] = Field(default_factory=list)
    listing_date: date | None = None
    nav: Decimal | None = None
    aum: Decimal | None = None
    returns: dict[str, str | None] = Field(default_factory=dict)
    total_count: int | None = None

    @field_validator("code", "name", mode="before")
    @classmethod
    def _required_text(cls, value: object) -> object:
        value = blank_to_none(value)
        if isinstance(value, str):
            return normalize_space(value)
        return value

    @field_validator("ksd_fund", "category", mode="before")
    @classmethod
    def _optional_text(cls, value: object) -> object:
        return blank_to_none(value)

    @field_validator("listing_date", mode="before")
    @classmethod
    def _parse_date(cls, value: object) -> object:
        if isinstance(value, date):
            return value
        return parse_date_text(value)

    @field_validator("nav", "aum", mode="before")
    @classmethod
    def _parse_decimal(cls, value: object) -> object:
        return parse_display_decimal(value)

    @field_validator("total_count", mode="before")
    @classmethod
    def _parse_int(cls, value: object) -> object:
        return parse_int_text(blank_to_none(value))

    @field_validator("returns", mode="before")
    @classmethod
    def _normalize_returns(cls, value: object) -> object:
        if not isinstance(value, dict):
            return value
        return {str(key): return_text(item) for key, item in value.items()}


class TigerEtfDetailData(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    name: str
    category: str | None = None
    benchmark: str | None = None
    listing_date: date | None = None
    nav: Decimal | None = None
    aum: Decimal | None = None
    expense_ratio: Decimal | None = None
    as_of_date: date | None = None
    detail_url: str | None = None
    raw: dict[str, object] = Field(default_factory=dict)

    @field_validator("code", "name", mode="before")
    @classmethod
    def _required_text(cls, value: object) -> object:
        value = blank_to_none(value)
        if isinstance(value, str):
            return normalize_space(value)
        return value

    @field_validator("category", "benchmark", "detail_url", mode="before")
    @classmethod
    def _optional_text(cls, value: object) -> object:
        return blank_to_none(value)

    @field_validator("listing_date", "as_of_date", mode="before")
    @classmethod
    def _parse_date(cls, value: object) -> object:
        if isinstance(value, date):
            return value
        return parse_date_text(value)

    @field_validator("nav", "aum", "expense_ratio", mode="before")
    @classmethod
    def _parse_decimal(cls, value: object) -> object:
        return parse_display_decimal(value)


class TigerHoldingItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    rank: int | None = None
    code: str | None = None
    name: str | None = None
    quantity: Decimal | None = None
    valuation_amount: Decimal | None = None
    weight: Decimal | None = None
    as_of_date: date | None = None
    raw: dict[str, object] = Field(default_factory=dict)

    @field_validator("rank", mode="before")
    @classmethod
    def _parse_int(cls, value: object) -> object:
        return parse_int_text(blank_to_none(value))

    @field_validator("code", "name", mode="before")
    @classmethod
    def _optional_text(cls, value: object) -> object:
        return blank_to_none(value)

    @field_validator("quantity", "valuation_amount", "weight", mode="before")
    @classmethod
    def _parse_decimal(cls, value: object) -> object:
        return parse_display_decimal(value)
