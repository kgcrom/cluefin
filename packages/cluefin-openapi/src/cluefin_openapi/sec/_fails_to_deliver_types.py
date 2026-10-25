from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FailsToDeliverFile(BaseModel):
    """Fails-to-Deliver 파일 하나. 한 달을 앞(a)·뒤(b) 반월로 나눠 낸다."""

    model_config = ConfigDict(title="SEC Fails-to-Deliver 파일", extra="allow")

    name: str = Field(description="파일명에서 확장자를 뗀 이름 (cnsfails202609a)")
    year: int = Field(description="연도")
    month: int = Field(description="월")
    half: str = Field(description="a: 1–15일 결제분, b: 16일–말일 결제분")
    path: str = Field(description="www.sec.gov 아래 zip 경로. 시기마다 폴더가 다르다")


class FailToDeliver(BaseModel):
    """결제일 하루, 종목 하나의 누적 결제 불이행 수량."""

    model_config = ConfigDict(title="SEC Fails-to-Deliver 행", extra="allow")

    settlement_date: date = Field(description="결제일")
    cusip: str = Field(description="CUSIP (9자리)")
    symbol: str | None = Field(default=None, description="티커. 없으면 None")
    quantity: int = Field(description="결제 불이행 수량 (주)")
    description: str | None = Field(default=None, description="종목 설명")
    price: Decimal | None = Field(default=None, description="전일 종가. 없으면(원문 '.') None")
