from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class KiwoomSearchVO(BaseModel):
    model_config = ConfigDict(extra="allow")

    pageNo: int = 1
    endPage: int | None = None

    @field_validator("endPage", mode="before")
    @classmethod
    def _empty_int_to_none(cls, value: object) -> object:
        if value == "":
            return None
        return value


class KiwoomEtfListItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    gcode: str
    goodsNm: str
    goodsTypeNm: str | None = None
    bsisIdex: str | None = None
    idexNm: str | None = None
    setdate: str | None = None
    standardprice: Decimal | None = None
    fundtotalamount: Decimal | None = None

    @field_validator("standardprice", "fundtotalamount", mode="before")
    @classmethod
    def _empty_decimal_to_none(cls, value: object) -> object:
        if value == "":
            return None
        return value


class KiwoomEtfListResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    totalCnt: int = 0
    searchVO: KiwoomSearchVO = Field(default_factory=KiwoomSearchVO)
    etfList: list[KiwoomEtfListItem] = Field(default_factory=list)
