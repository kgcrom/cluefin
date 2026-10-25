from datetime import date, datetime
from pathlib import Path
from typing import Any, NamedTuple

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FilingIndexItem(BaseModel):
    """공시 폴더 안의 파일 하나 (`index.json`의 `directory.item[]`)."""

    model_config = ConfigDict(title="SEC 공시 폴더 항목", populate_by_name=True, extra="allow")

    name: str = Field(description="파일명")
    type: str | None = Field(default=None, description="EDGAR 디렉터리 목록의 아이콘 종류 (text.gif, folder.gif)")
    size: int | None = Field(default=None, description="크기(바이트). 하위 폴더는 None")
    last_modified: datetime | None = Field(default=None, alias="last-modified", description="수정 시각")

    @field_validator("size", mode="before")
    @classmethod
    def _blank_size(cls, value: Any) -> Any:
        """SEC는 크기를 문자열로 주고, 폴더는 빈 문자열로 준다."""
        return None if value == "" else value


class FilingIndex(BaseModel):
    """공시 폴더 목록 (`Archives/edgar/data/{cik}/{접수번호}/index.json`)."""

    model_config = ConfigDict(title="SEC 공시 폴더", populate_by_name=True, extra="allow")

    name: str = Field(description="폴더 경로 (/Archives/edgar/data/320193/000032019323000106)")
    parent_dir: str | None = Field(default=None, alias="parent-dir", description="상위 폴더 경로")
    items: list[FilingIndexItem] = Field(default_factory=list, alias="item", description="파일 목록")


class FilingDocument(BaseModel):
    """공시 상세 페이지(`-index.html`)의 문서 한 행."""

    model_config = ConfigDict(title="SEC 공시 문서", populate_by_name=True, extra="allow")

    sequence: int | None = Field(default=None, description="문서 순번. 전체 제출 텍스트 파일(.txt)은 None")
    description: str | None = Field(default=None, description="설명 (EX-99.1 EARNINGS RELEASE 등)")
    name: str = Field(
        description="폴더 안 경로. 보통 파일명이고, Form 4 렌더링은 `xslF345X06/form4.xml`처럼 하위 폴더가 붙는다"
    )
    type: str | None = Field(
        default=None, description="문서 종류 (10-K, EX-99.1, EX-101.SCH, GRAPHIC ...). 없으면 None"
    )
    size: int | None = Field(default=None, description="크기(바이트). XSL 렌더링 행은 None")
    data_file: bool = Field(default=False, description="'Data Files' 표(XBRL 등)의 행인지")


class FilingParty(BaseModel):
    """공시 상세 페이지의 제출자·발행사 한 명."""

    model_config = ConfigDict(title="SEC 공시 당사자", populate_by_name=True, extra="allow")

    cik: int = Field(description="CIK (앞자리 0 없는 정수)")
    name: str = Field(description="이름")
    role: str | None = Field(default=None, description="역할 (Filer, Issuer, Reporting, Subject, Filed by ...)")


class FilingDetail(BaseModel):
    """공시 상세 페이지 (`Archives/edgar/data/{cik}/{접수번호}/{접수번호}-index.html`).

    `index.json`에는 없는 문서 종류(EX-99.1 등)와 제출 당사자의 CIK가 있다. 폴더는 아무 CIK 경로로도 열리므로
    (다른 회사 CIK + 접수번호도 200, 2026-10 실측) 그 공시가 어느 회사 것인지는 `parties`로 확인한다.
    """

    model_config = ConfigDict(title="SEC 공시 상세", populate_by_name=True, extra="allow")

    accession_number: str = Field(description="접수번호 (0000320193-23-000106)")
    form: str = Field(description="서식 (10-K, 8-K, 4 ...)")
    filing_date: date | None = Field(default=None, description="제출일")
    period_of_report: date | None = Field(default=None, description="보고 기준일. 없으면 None")
    items: list[str] = Field(default_factory=list, description="8-K 항목 (`Item 2.02: Results of Operations ...`)")
    documents: list[FilingDocument] = Field(default_factory=list, description="문서 (페이지 순서)")
    parties: list[FilingParty] = Field(default_factory=list, description="제출자·발행사·보고자")

    @property
    def ciks(self) -> list[int]:
        """당사자 CIK (페이지 순서, 중복 없음)."""
        return list(dict.fromkeys(party.cik for party in self.parties))


class Form13FFiles(NamedTuple):
    """13F 공시에서 받은 파일. `cluefin_sec_notes.ownership.load_13f`가 그대로 읽는다."""

    cover: Path
    """표지 `primary_doc.xml`"""
    information_table: Path | None
    """보유 목록 XML. 통지(13F-NT)는 None"""
