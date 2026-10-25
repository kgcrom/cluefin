from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, Field

from ._model import ECOS_ROW_CONFIG


class StatisticObservation(BaseModel):
    """StatisticSearch 한 행 — 통계표·항목·시점 하나의 값."""

    model_config = ECOS_ROW_CONFIG | {"title": "ECOS 통계 조회 행"}

    stat_code: str = Field(alias="STAT_CODE", description="통계표코드")
    stat_name: str = Field(alias="STAT_NAME", description="통계명")
    item_code1: str | None = Field(default=None, alias="ITEM_CODE1", description="통계항목코드1")
    item_name1: str | None = Field(default=None, alias="ITEM_NAME1", description="통계항목명1")
    item_code2: str | None = Field(default=None, alias="ITEM_CODE2", description="통계항목코드2")
    item_name2: str | None = Field(default=None, alias="ITEM_NAME2", description="통계항목명2")
    item_code3: str | None = Field(default=None, alias="ITEM_CODE3", description="통계항목코드3")
    item_name3: str | None = Field(default=None, alias="ITEM_NAME3", description="통계항목명3")
    item_code4: str | None = Field(default=None, alias="ITEM_CODE4", description="통계항목코드4")
    item_name4: str | None = Field(default=None, alias="ITEM_NAME4", description="통계항목명4")
    unit_name: str | None = Field(default=None, alias="UNIT_NAME", description="단위 (연%, 원, 2020=100 …)")
    weight: str | None = Field(default=None, alias="WGT", description="가중치")
    time: str = Field(alias="TIME", description="시점. 주기를 따른다: 2026, 2026Q3, 202609, 20261016 …")
    data_value: str | None = Field(default=None, alias="DATA_VALUE", description="값 원문. 휴일·미집계면 빈 문자열")

    @property
    def value(self) -> Decimal | None:
        """`data_value` 를 Decimal 로. 비었거나 숫자가 아니면 None."""
        if not self.data_value:
            return None
        try:
            return Decimal(self.data_value)
        except InvalidOperation:
            return None
