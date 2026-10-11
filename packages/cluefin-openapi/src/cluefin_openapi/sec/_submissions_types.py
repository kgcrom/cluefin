from datetime import date, datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FilingEntry(BaseModel):
    """제출 이력 한 건. SEC는 열 단위 배열로 주므로 `Filings`가 행으로 바꿔 만든다."""

    model_config = ConfigDict(title="SEC 제출 이력 항목", populate_by_name=True, extra="allow")

    accession_number: str = Field(alias="accessionNumber", description="접수번호 (0000320193-23-000106)")
    filing_date: date = Field(alias="filingDate", description="제출일")
    report_date: Optional[date] = Field(default=None, alias="reportDate", description="보고 기준일. 없으면 None")
    acceptance_date_time: Optional[datetime] = Field(
        default=None, alias="acceptanceDateTime", description="EDGAR 접수 시각 (UTC)"
    )
    act: Optional[str] = Field(default=None, description="근거 법령 (33, 34 등)")
    form: str = Field(description="서식 (10-K, 10-Q, 8-K, 4 ...)")
    file_number: Optional[str] = Field(default=None, alias="fileNumber", description="SEC 파일 번호")
    film_number: Optional[str] = Field(default=None, alias="filmNumber", description="필름 번호")
    items: Optional[str] = Field(default=None, description="8-K 항목 번호 (쉼표 구분, 예: 2.02,9.01)")
    core_type: Optional[str] = Field(default=None, description="SEC 내부 서식 분류")
    size: Optional[int] = Field(default=None, description="제출물 전체 크기(바이트)")
    is_xbrl: bool = Field(default=False, alias="isXBRL", description="XBRL 포함 여부")
    is_inline_xbrl: bool = Field(default=False, alias="isInlineXBRL", description="인라인 XBRL 여부")
    is_xbrl_numeric: Optional[bool] = Field(
        default=None,
        alias="isXBRLNumeric",
        description="SEC 문서에 없는 열. 최근 제출분에만 0/1이 있고 이전 제출분은 null (2026-10 실측). 이름상 숫자 XBRL 값 포함 여부",
    )
    primary_document: Optional[str] = Field(default=None, alias="primaryDocument", description="주 문서 파일명")
    primary_doc_description: Optional[str] = Field(
        default=None, alias="primaryDocDescription", description="주 문서 설명"
    )

    @model_validator(mode="before")
    @classmethod
    def _blank_to_none(cls, data: Any) -> Any:
        """SEC는 값이 없는 칸을 빈 문자열로 준다 (reportDate, act, items ...)."""
        if isinstance(data, dict):
            return {key: (None if value == "" else value) for key, value in data.items()}
        return data


class SubmissionsFile(BaseModel):
    """`filings.files` 항목 — `recent`에 못 담은 오래된 제출 이력 페이지."""

    model_config = ConfigDict(title="SEC 제출 이력 추가 페이지", populate_by_name=True, extra="allow")

    name: str = Field(description="페이지 파일명 (CIK0000320193-submissions-001.json)")
    filing_count: int = Field(alias="filingCount", description="페이지에 든 제출 건수")
    filing_from: date = Field(alias="filingFrom", description="가장 이른 제출일")
    filing_to: date = Field(alias="filingTo", description="가장 늦은 제출일")


class FormerName(BaseModel):
    model_config = ConfigDict(title="SEC 이전 회사명", populate_by_name=True, extra="allow")

    name: str = Field(description="이전 회사명")
    date_from: Optional[datetime] = Field(default=None, alias="from", description="사용 시작")
    date_to: Optional[datetime] = Field(default=None, alias="to", description="사용 종료")


class CompanySubmissions(BaseModel):
    """`data.sec.gov/submissions/CIK##########.json` — 회사 정보와 최근 제출 이력.

    `filings`는 최근 1,000건 또는 1년치 중 많은 쪽이다. 그보다 오래된 이력은 `filing_files`의
    페이지를 `Submissions.submissions_page()`로 따로 받는다.
    """

    model_config = ConfigDict(title="SEC 회사 제출 이력", populate_by_name=True, extra="allow")

    cik: str = Field(description="CIK (앞자리 0 없는 문자열)")
    entity_type: Optional[str] = Field(default=None, alias="entityType", description="operating, other ...")
    sic: Optional[str] = Field(default=None, description="표준산업분류(SIC) 코드")
    sic_description: Optional[str] = Field(default=None, alias="sicDescription", description="SIC 설명")
    name: str = Field(description="회사명")
    tickers: List[str] = Field(default_factory=list, description="티커")
    exchanges: List[Optional[str]] = Field(default_factory=list, description="거래소 (tickers와 같은 순서)")
    ein: Optional[str] = Field(default=None, description="고용주 식별번호")
    lei: Optional[str] = Field(default=None, description="LEI")
    category: Optional[str] = Field(default=None, description="제출자 구분 (Large Accelerated Filer 등)")
    fiscal_year_end: Optional[str] = Field(default=None, alias="fiscalYearEnd", description="회계연도 말 (MMDD)")
    state_of_incorporation: Optional[str] = Field(default=None, alias="stateOfIncorporation", description="설립 주")
    former_names: List[FormerName] = Field(default_factory=list, alias="formerNames", description="이전 회사명")
    filings: List[FilingEntry] = Field(default_factory=list, description="최근 제출 이력 (최신순)")
    filing_files: List[SubmissionsFile] = Field(default_factory=list, description="오래된 제출 이력 페이지")

    @model_validator(mode="before")
    @classmethod
    def _unpack_filings(cls, data: Any) -> Any:
        """`filings: {recent: {열: [...]}, files: [...]}`를 행 목록과 페이지 목록으로 편다."""
        if not isinstance(data, dict) or not isinstance(data.get("filings"), dict):
            return data
        unpacked = dict(data)
        raw = unpacked.pop("filings")
        unpacked["filings"] = columns_to_rows(raw.get("recent") or {})
        unpacked["filing_files"] = raw.get("files") or []
        return unpacked


def columns_to_rows(columns: dict) -> List[dict]:
    """열 이름 → 값 배열 형태를 행(dict) 목록으로 바꾼다. 열 길이가 다르면 ValueError."""
    if not columns:
        return []
    names = list(columns)
    lengths = {len(values) for values in columns.values()}
    if len(lengths) != 1:
        raise ValueError(
            f"제출 이력 열 길이가 서로 다릅니다: {dict(zip(names, map(len, columns.values()), strict=False))}"
        )
    return [dict(zip(names, row, strict=True)) for row in zip(*columns.values(), strict=True)]
