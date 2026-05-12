from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, TypeAdapter, field_validator


class KodexEtfListItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    fNm: str
    stkTicker: str
    fId: str | None = None
    typeLnm: str | None = None
    typeNm: str | None = None
    listD: str | None = None
    gijunYMD: str | None = None
    basp: Decimal | None = None
    nav: Decimal | None = None
    curp: Decimal | None = None
    risep: Decimal | None = None
    risepRt: Decimal | None = None
    basrp: Decimal | None = None
    basrpRt: Decimal | None = None
    yieldWeek: Decimal | None = None
    yieldMon1: Decimal | None = None
    yieldMon3: Decimal | None = None
    yieldMon6: Decimal | None = None
    yieldYear1: Decimal | None = None
    yieldYear3: Decimal | None = None
    yieldYear: Decimal | None = None
    yieldList: Decimal | None = None
    dcYn: str | None = None
    irpYn: str | None = None
    totalCnt: int | None = None

    @field_validator(
        "basp",
        "nav",
        "curp",
        "risep",
        "risepRt",
        "basrp",
        "basrpRt",
        "yieldWeek",
        "yieldMon1",
        "yieldMon3",
        "yieldMon6",
        "yieldYear1",
        "yieldYear3",
        "yieldYear",
        "yieldList",
        mode="before",
    )
    @classmethod
    def _empty_decimal_to_none(cls, value: object) -> object:
        if value == "":
            return None
        return value


KODEX_LIST_ADAPTER = TypeAdapter(list[KodexEtfListItem])
