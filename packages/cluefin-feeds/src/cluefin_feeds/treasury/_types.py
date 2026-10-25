import datetime as dt
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ParYieldCurveRate(BaseModel):
    """Daily Treasury Par Yield Curve 한 영업일 (연 %).

    만기는 생긴 해부터만 온다 — 2개월 2018-10, 4개월 2022-10, 1.5개월 2025-02~. 없는 만기는 None.
    """

    model_config = ConfigDict(title="미 국채 명목 수익률 곡선", populate_by_name=True, extra="allow")

    id: int | None = Field(default=None, alias="Id", description="피드 내부 행 번호")
    date: dt.date = Field(alias="NEW_DATE", description="영업일")
    month_1: Decimal | None = Field(default=None, alias="BC_1MONTH", description="1개월")
    month_1_5: Decimal | None = Field(default=None, alias="BC_1_5MONTH", description="1.5개월 (6주)")
    month_2: Decimal | None = Field(default=None, alias="BC_2MONTH", description="2개월")
    month_3: Decimal | None = Field(default=None, alias="BC_3MONTH", description="3개월")
    month_4: Decimal | None = Field(default=None, alias="BC_4MONTH", description="4개월")
    month_6: Decimal | None = Field(default=None, alias="BC_6MONTH", description="6개월")
    year_1: Decimal | None = Field(default=None, alias="BC_1YEAR", description="1년")
    year_2: Decimal | None = Field(default=None, alias="BC_2YEAR", description="2년")
    year_3: Decimal | None = Field(default=None, alias="BC_3YEAR", description="3년")
    year_5: Decimal | None = Field(default=None, alias="BC_5YEAR", description="5년")
    year_7: Decimal | None = Field(default=None, alias="BC_7YEAR", description="7년")
    year_10: Decimal | None = Field(default=None, alias="BC_10YEAR", description="10년")
    year_20: Decimal | None = Field(default=None, alias="BC_20YEAR", description="20년")
    year_30: Decimal | None = Field(default=None, alias="BC_30YEAR", description="30년")
    year_30_display: Decimal | None = Field(
        default=None, alias="BC_30YEARDISPLAY", description="30년 (표시용; 30년물 발행 중단기에는 외삽값)"
    )
