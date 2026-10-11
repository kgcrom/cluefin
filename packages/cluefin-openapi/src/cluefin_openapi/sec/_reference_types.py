from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CompanyTicker(BaseModel):
    """`company_tickers.json` 한 행."""

    model_config = ConfigDict(title="SEC 티커-CIK 매핑", populate_by_name=True, extra="allow")

    cik: int = Field(alias="cik_str", description="CIK (앞자리 0 없는 정수)")
    ticker: str = Field(description="티커. 클래스 주식은 BRK-B처럼 하이픈을 쓴다")
    title: str = Field(description="회사명")


class CompanyTickerExchange(BaseModel):
    """`company_tickers_exchange.json` 한 행."""

    model_config = ConfigDict(title="SEC 티커-CIK-거래소 매핑", extra="allow")

    cik: int = Field(description="CIK (앞자리 0 없는 정수)")
    name: str = Field(description="회사명")
    ticker: str = Field(description="티커")
    exchange: Optional[str] = Field(default=None, description="거래소 (Nasdaq, NYSE, OTC, CBOE 등). 없으면 None")
