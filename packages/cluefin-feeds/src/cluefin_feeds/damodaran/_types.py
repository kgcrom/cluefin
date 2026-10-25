import datetime as dt
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

KRX_EXCHANGES = ("KOSE", "KOSDAQ", "XKON")


class CountryRiskPremium(BaseModel):
    """ctryprem.html 한 행. 비율은 % 단위 값(0.64 = 0.64%), "NA" 는 None."""

    model_config = ConfigDict(title="Damodaran 국가 위험 프리미엄")

    country: str = Field(description="국가 (예: Korea)")
    moodys_rating: str | None = Field(default=None, description="Moody's 국가 신용등급")
    default_spread: Decimal | None = Field(default=None, description="조정 부도 스프레드 (%)")
    country_risk_premium: Decimal | None = Field(default=None, description="국가 위험 프리미엄 CRP (%)")
    equity_risk_premium: Decimal | None = Field(default=None, description="총 ERP = 성숙시장 ERP + CRP (%)")
    corporate_tax_rate: Decimal | None = Field(default=None, description="법인세 한계세율 (%)")
    sovereign_cds: Decimal | None = Field(default=None, description="국가 CDS 스프레드 (%)")
    cds_equity_risk_premium: Decimal | None = Field(default=None, description="CDS 기반 ERP (%)")


class CountryRiskPremiumTable(BaseModel):
    model_config = ConfigDict(title="Damodaran 국가 위험 프리미엄 표")

    updated: dt.date | None = Field(default=None, description='페이지의 "Last updated" 날짜 (매년 1월·7월쯤)')
    rows: list[CountryRiskPremium] = Field(default_factory=list)

    def get(self, country: str) -> CountryRiskPremium | None:
        """국가 이름이 정확히 같은 행. 한국은 "Korea" (북한은 "Korea, D.P.R.")."""
        return next((row for row in self.rows if row.country == country), None)


class IndustryBeta(BaseModel):
    """업종 β 표(`beta*.xls` "Industry Averages") 한 행."""

    model_config = ConfigDict(title="Damodaran 업종 베타")

    industry_name: str = Field(description="업종 (Damodaran 분류, indname.xls 의 Industry Group 과 같은 이름)")
    number_of_firms: int = Field(description="기업 수")
    beta: float | None = Field(default=None, description="레버드 β (평균)")
    de_ratio: float | None = Field(default=None, description="D/E (시가 기준)")
    effective_tax_rate: float | None = Field(default=None, description="유효세율")
    unlevered_beta: float | None = Field(default=None, description="언레버드 β")
    cash_firm_value: float | None = Field(default=None, description="현금 / 기업가치")
    unlevered_beta_corrected_for_cash: float | None = Field(
        default=None, description="현금 보정 언레버드 β — 영업자산 β, 사업 하나의 β 로 쓰는 값"
    )
    hilo_risk: float | None = Field(default=None, description="HiLo Risk")
    std_equity: float | None = Field(default=None, description="주가 표준편차")
    std_operating_income: float | None = Field(default=None, description="영업이익 표준편차 (최근 10년)")
    unlevered_beta_by_year: dict[int, float] = Field(
        default_factory=dict, description="연도별 현금 보정 언레버드 β (표에 있는 해만)"
    )
    unlevered_beta_average: float | None = Field(default=None, description='"Average: 2021-26" 같은 기간 평균')


class IndustryBetaTable(BaseModel):
    model_config = ConfigDict(title="Damodaran 업종 베타 표")

    region: str = Field(description='표의 지역 이름 (예: "Emerging Markets", "US companies")')
    updated: dt.date | None = Field(default=None, description="Date updated (매년 1월)")
    marginal_tax_rate: float | None = Field(default=None, description="언레버에 쓴 한계세율")
    rows: list[IndustryBeta] = Field(default_factory=list, description='업종들, 끝에 "Total Market" 행 포함')

    def get(self, industry_name: str) -> IndustryBeta | None:
        return next((row for row in self.rows if row.industry_name == industry_name), None)


class CompanyIndustry(BaseModel):
    """indname.xls 한 행 — 종목의 Damodaran 업종."""

    model_config = ConfigDict(title="Damodaran 종목 업종 분류")

    company_name: str = Field(description='회사명 (예: "Samsung Electronics Co., Ltd. (KOSE:A005930)")')
    exchange_ticker: str = Field(
        description="거래소:티커 (예: KOSE:A005930, KOSDAQ:A397810, XKON = 코넥스). 비어 있기도 하다"
    )
    industry_group: str = Field(description="업종 — 업종 β 표의 industry_name 과 맞춘다")
    primary_sector: str | None = Field(default=None, description="대분류 섹터")
    sic_code: str | None = Field(default=None, description="SIC 코드")
    country: str | None = Field(default=None, description='국가 (한국은 "South Korea")')
    broad_group: str | None = Field(default=None, description='지역 대분류 (한국은 "Emerging Markets")')
    sub_group: str | None = Field(default=None, description='지역 소분류 (한국은 "Small Asia")')

    @property
    def krx_code(self) -> str | None:
        """국내 상장 종목이면 6자리 단축코드(005930), 아니면 None."""
        exchange, _, symbol = self.exchange_ticker.partition(":")
        if exchange in KRX_EXCHANGES and symbol.startswith("A") and len(symbol) == 7:
            return symbol[1:]
        return None
