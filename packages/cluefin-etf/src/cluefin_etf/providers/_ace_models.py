from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from cluefin_etf.providers._normalization import blank_to_none
from cluefin_etf.providers._parsing import parse_compact_date, parse_decimal_text, parse_int_text


class AceEtfListItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    fund_code: str
    name: str
    category: str | None = None
    pension_flags: list[str] = Field(default_factory=list)
    raw: dict[str, object] = Field(default_factory=dict)

    @field_validator("fund_code", "name", mode="before")
    @classmethod
    def _required_text(cls, value: object) -> object:
        value = blank_to_none(value)
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("category", mode="before")
    @classmethod
    def _optional_text(cls, value: object) -> object:
        return blank_to_none(value)


class AceDetailPayload(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    fundCd: str
    fundNm: str
    stockCd: str | None = None
    fundWhlNm: str | None = None
    stdDt: date | None = None
    stpr: Decimal | None = None
    nastAmt: Decimal | None = None
    lstdDt: date | None = None
    badge: dict[str, object] = Field(default_factory=dict)
    summaryContent: str | None = None

    @field_validator("fundCd", "fundNm", mode="before")
    @classmethod
    def _required_text(cls, value: object) -> object:
        value = blank_to_none(value)
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("stockCd", "fundWhlNm", "summaryContent", mode="before")
    @classmethod
    def _optional_text(cls, value: object) -> object:
        return blank_to_none(value)

    @field_validator("stdDt", "lstdDt", mode="before")
    @classmethod
    def _parse_date(cls, value: object) -> object:
        if isinstance(value, date):
            return value
        return parse_compact_date(value)

    @field_validator("stpr", "nastAmt", mode="before")
    @classmethod
    def _parse_decimal(cls, value: object) -> object:
        return _parse_decimal(value)

    @field_validator("badge", mode="before")
    @classmethod
    def _badge_dict(cls, value: object) -> object:
        return value if isinstance(value, dict) else {}


class AcePdfHoldingItem(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    rank: int | None = None
    jm_KSC_CD: str | None = None
    sec_NM: str | None = None
    cu_ITEM_CNT: Decimal | None = None
    val_AM: Decimal | None = None
    wg: Decimal | None = None
    std_DT: date | None = None

    @field_validator("rank", mode="before")
    @classmethod
    def _parse_int(cls, value: object) -> object:
        return parse_int_text(blank_to_none(value))

    @field_validator("jm_KSC_CD", "sec_NM", mode="before")
    @classmethod
    def _optional_text(cls, value: object) -> object:
        return blank_to_none(value)

    @field_validator("cu_ITEM_CNT", "val_AM", "wg", mode="before")
    @classmethod
    def _parse_decimal(cls, value: object) -> object:
        return _parse_decimal(value)

    @field_validator("std_DT", mode="before")
    @classmethod
    def _parse_date(cls, value: object) -> object:
        if isinstance(value, date):
            return value
        return parse_compact_date(value)


class AceHoldingsPayload(BaseModel):
    model_config = ConfigDict(extra="allow", frozen=True)

    pdfList: list[AcePdfHoldingItem]


def _parse_decimal(value: object) -> Decimal | None:
    value = blank_to_none(value)
    if value is None or isinstance(value, Decimal):
        return value
    return parse_decimal_text(str(value))
