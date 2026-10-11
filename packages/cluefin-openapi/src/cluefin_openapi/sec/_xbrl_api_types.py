from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class FactValue(BaseModel):
    """회사 하나의 XBRL 값 하나 (companyfacts / companyconcept 공통).

    같은 기간 값이 여러 공시(원공시·다음 해 비교 표시·정정)에 거듭 실리므로 `accn`·`filed`가 다른 행이
    여러 개일 수 있다. `frame`은 SEC가 그 기간의 대표 값으로 고른 행에만 붙는다.
    """

    model_config = ConfigDict(title="SEC XBRL 값", extra="allow")

    start: Optional[date] = Field(default=None, description="기간 시작일. 시점 값(재무상태표 등)은 None")
    end: date = Field(description="기간 종료일 또는 시점")
    val: Decimal = Field(description="값")
    accn: str = Field(description="이 값을 실은 공시의 접수번호")
    fy: Optional[int] = Field(default=None, description="공시의 회계연도 (값의 기간이 아니라 공시 기준)")
    fp: Optional[str] = Field(default=None, description="공시의 회계기간 (FY, Q1, Q2, Q3)")
    form: str = Field(description="공시 서식 (10-K, 10-Q ...)")
    filed: date = Field(description="공시 제출일")
    frame: Optional[str] = Field(default=None, description="SEC 대표 기간 (CY2023, CY2023Q4I ...)")


class ConceptFacts(BaseModel):
    """개념 하나의 값들, 단위별로 묶음."""

    model_config = ConfigDict(title="SEC XBRL 개념", extra="allow")

    label: Optional[str] = Field(default=None, description="개념 이름")
    description: Optional[str] = Field(default=None, description="개념 설명")
    units: Dict[str, List[FactValue]] = Field(
        default_factory=dict, description="단위(USD, shares, USD/shares ...) → 값"
    )


class CompanyFacts(BaseModel):
    """`api/xbrl/companyfacts/CIK##########.json` — 회사의 모든 XBRL 값.

    `facts`는 택소노미(us-gaap, dei, ifrs-full, srt ...) → 개념 이름 → 값 구조다.
    """

    model_config = ConfigDict(title="SEC 회사 XBRL 전체", populate_by_name=True, extra="allow")

    cik: int = Field(description="CIK")
    entity_name: str = Field(alias="entityName", description="회사명")
    facts: Dict[str, Dict[str, ConceptFacts]] = Field(default_factory=dict, description="택소노미 → 개념 → 값")

    def concept(self, taxonomy: str, tag: str) -> Optional[ConceptFacts]:
        """택소노미와 개념 이름으로 값을 찾는다. 없으면 None."""
        return self.facts.get(taxonomy, {}).get(tag)


class CompanyConcept(BaseModel):
    """`api/xbrl/companyconcept/CIK##########/{taxonomy}/{tag}.json` — 회사 하나, 개념 하나."""

    model_config = ConfigDict(title="SEC 회사 XBRL 개념", populate_by_name=True, extra="allow")

    cik: int = Field(description="CIK")
    taxonomy: str = Field(description="택소노미 (us-gaap, dei ...)")
    tag: str = Field(description="개념 이름")
    label: Optional[str] = Field(default=None, description="개념 이름")
    description: Optional[str] = Field(default=None, description="개념 설명")
    entity_name: str = Field(alias="entityName", description="회사명")
    units: Dict[str, List[FactValue]] = Field(default_factory=dict, description="단위 → 값")


class FrameValue(BaseModel):
    """frames 응답의 회사 한 곳 값."""

    model_config = ConfigDict(title="SEC XBRL frame 값", populate_by_name=True, extra="allow")

    accn: str = Field(description="값을 실은 공시의 접수번호")
    cik: int = Field(description="CIK")
    entity_name: str = Field(alias="entityName", description="회사명")
    loc: Optional[str] = Field(default=None, description="소재지 (US-CA 등)")
    start: Optional[date] = Field(default=None, description="기간 시작일. 시점 frame이면 None")
    end: date = Field(description="기간 종료일 또는 시점")
    val: Decimal = Field(description="값")


class Frame(BaseModel):
    """`api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json` — 개념 하나, 기간 하나, 모든 회사."""

    model_config = ConfigDict(title="SEC XBRL frame", extra="allow")

    taxonomy: str = Field(description="택소노미")
    tag: str = Field(description="개념 이름")
    ccp: str = Field(description="달력 기간 (CY2023, CY2023Q4I ...)")
    uom: str = Field(description="단위")
    label: Optional[str] = Field(default=None, description="개념 이름")
    description: Optional[str] = Field(default=None, description="개념 설명")
    pts: int = Field(description="회사 수")
    data: List[FrameValue] = Field(default_factory=list, description="회사별 값")
