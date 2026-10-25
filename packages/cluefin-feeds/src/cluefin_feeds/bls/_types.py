from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, ConfigDict, Field


class BlsFootnote(BaseModel):
    model_config = ConfigDict(title="BLS 각주", extra="allow")

    code: str | None = Field(default=None, description="각주 코드 (X = 자료 없음 등)")
    text: str | None = Field(default=None, description="각주 내용")


class BlsObservation(BaseModel):
    """시계열 한 시점."""

    model_config = ConfigDict(title="BLS 시계열 값", populate_by_name=True, extra="allow")

    year: int = Field(description="연도")
    period: str = Field(description="M01~M12 월, M13 연평균(annual_average=True), Q01~Q05 분기, S01~S03 반기, A01 연")
    period_name: str | None = Field(default=None, alias="periodName", description="January … / Annual")
    raw_value: str = Field(alias="value", description='값 원문. 결측은 "-" (예: 2025-10 셧다운)')
    latest: str | None = Field(default=None, description='가장 최근 시점이면 "true"')
    footnotes: list[BlsFootnote] = Field(default_factory=list, description="각주 (빈 객체 {} 가 오는 것이 보통)")

    @property
    def value(self) -> Decimal | None:
        """값을 Decimal 로. 결측("-")이면 None."""
        try:
            return Decimal(self.raw_value)
        except InvalidOperation:
            return None

    @property
    def month(self) -> int | None:
        """월별 시점(M01~M12)이면 1~12, 아니면(M13 연평균 등) None."""
        if self.period.startswith("M") and self.period[1:].isdigit() and 1 <= int(self.period[1:]) <= 12:
            return int(self.period[1:])
        return None


class BlsSeries(BaseModel):
    model_config = ConfigDict(title="BLS 시계열", populate_by_name=True, extra="allow")

    series_id: str = Field(alias="seriesID", description="시계열 ID (예: CUUR0000SA0)")
    data: list[BlsObservation] = Field(default_factory=list, description="시점 오름차순. 없는 시리즈는 빈 목록")


class BlsResponse(BaseModel):
    """여러 요청(연도·시리즈 쪼개기)을 합친 결과."""

    model_config = ConfigDict(title="BLS 시계열 응답")

    series: list[BlsSeries] = Field(default_factory=list, description="요청한 순서대로")
    messages: list[str] = Field(
        default_factory=list,
        description='서버 안내 (예: "Invalid Series for Series X" — 없는 시리즈도 성공 상태로 온다)',
    )

    def get(self, series_id: str) -> BlsSeries | None:
        return self._by_id().get(series_id)

    def _by_id(self) -> dict[str, BlsSeries]:
        return {s.series_id: s for s in self.series}
