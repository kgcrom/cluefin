"""원문 XML을 문서 메타와 섹션 트리로 읽는다."""

from __future__ import annotations

import re
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING

from cluefin_dart_notes._blocks import Block, extract_blocks
from cluefin_dart_notes.repair import DartXmlRepairer, RepairResult

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element

PERIODIC_REPORT_CODES = frozenset({"11011", "11012", "11013", "11014"})
AUDIT_REPORT_CODES = frozenset({"00760", "00761"})

_SECTION_LEVELS = {"SECTION-1": 1, "SECTION-2": 2, "SECTION-3": 3}
_CORRECTION = "CORRECTION"
# 원문 파일 이름: <접수번호 14자리>.xml (본문) 또는 <접수번호>_<문서코드>.xml (첨부 감사보고서)
_FILE_NAME = re.compile(r"(\d{14})(?:_(\d{5}))?\.xml", re.IGNORECASE)


def normalize_text(text: str) -> str:
    """연속 공백을 한 칸으로 줄이고 앞뒤 공백을 지운다."""
    return " ".join(text.split())


def element_text(element: Element) -> str:
    return normalize_text("".join(element.itertext()))


@dataclass(frozen=True, eq=False)
class Section:
    """`SECTION-1/2/3` 하나(또는 정정신고 블록). 직속 `TITLE`에서 제목과 코드를 읽는다.

    Attributes:
        title: 제목 원문(공백만 정리). 예: "3. 연결재무제표 주석".
        title_en: `ENG` 속성. 2024년 이후 제출분에만 있다.
        assoc_code: `AASSOCNOTE` 섹션 코드(예: `D-0-3-3-0`). 장 제목에는 없는 경우가 많다.
            같은 코드가 문서 종류와 연도에 따라 다른 섹션을 가리키기도 한다(AGENTS.md 참고).
        toc_id: `ATOCID`. 2024년 이후 제출분에만 있다.
        level: `SECTION-n`의 n. 정정신고 블록은 1.
        is_correction: `[기재정정]` 보고서 맨 앞의 정정신고(`CORRECTION`) 블록인지.
    """

    title: str
    title_en: str | None
    assoc_code: str | None
    toc_id: str | None
    level: int
    is_correction: bool = False
    children: tuple[Section, ...] = field(default=(), repr=False)
    element: Element | None = field(default=None, repr=False)

    @cached_property
    def blocks(self) -> tuple[Block, ...]:
        """이 섹션 본문의 문단·소제목·표(문서 순서). 섹션 제목과 하위 섹션의 내용은 들어가지 않는다."""
        if self.element is None:
            return ()
        return tuple(extract_blocks(self.element))

    def iter(self) -> Iterator[Section]:
        """자기 자신과 모든 하위 섹션을 문서 순서로."""
        yield self
        for child in self.children:
            yield from child.iter()


@dataclass(frozen=True, eq=False)
class DartDocument:
    """원문 XML 하나(본문 또는 첨부 감사보고서).

    Attributes:
        document_name: `DOCUMENT-NAME` (예: "반기보고서", "연결감사보고서").
        document_code: `DOCUMENT-NAME`의 `ACODE`. 11011 사업 / 11012 반기 / 11013·11014 분기 / 00760 감사 / 00761 연결감사.
        company_name: `COMPANY-NAME`.
        corp_code: `COMPANY-NAME`의 `AREGCIK` (DART 고유번호 8자리).
        formula_version: `FORMULA-VERSION` (작성기 서식 버전).
        encoding: 원문 실제 인코딩(utf-8 또는 cp949).
        summary: `SUMMARY/EXTRACTION`의 `ACODE` → 값. 감사보고서에는 감사인·감사의견·자산총액 등이 있다.
        sections: 최상위 섹션들. 하위 섹션은 `Section.children`.
        rcept_no: 파일 이름에서 읽은 접수번호. 이름이 규칙과 다르면 None.
        repair: 원문 정리 기록.
    """

    document_name: str | None
    document_code: str | None
    company_name: str | None
    corp_code: str | None
    formula_version: str | None
    encoding: str
    summary: Mapping[str, str]
    sections: tuple[Section, ...] = field(repr=False)
    rcept_no: str | None = None
    repair: RepairResult | None = field(default=None, repr=False)
    root: Element | None = field(default=None, repr=False)

    @property
    def is_periodic_report(self) -> bool:
        return self.document_code in PERIODIC_REPORT_CODES

    @property
    def is_audit_report(self) -> bool:
        return self.document_code in AUDIT_REPORT_CODES

    def iter_sections(self) -> Iterator[Section]:
        """모든 섹션을 문서 순서(전위 순회)로."""
        for section in self.sections:
            yield from section.iter()


def load_document(path: Path | str, *, repairer: DartXmlRepairer | None = None) -> DartDocument:
    """원문 XML 파일을 읽는다. 파일 이름(`<rcept_no>.xml`, `<rcept_no>_00760.xml`)에서 접수번호와 문서코드를 보강한다."""
    path = Path(path)
    return parse_document(path.read_bytes(), file_name=path.name, repairer=repairer)


def parse_document(
    raw: bytes, *, file_name: str | None = None, repairer: DartXmlRepairer | None = None
) -> DartDocument:
    """원문 바이트를 읽는다. `file_name`을 주면 접수번호와 (없을 때) 문서코드를 이름에서 보강한다."""
    root, result = (repairer or DartXmlRepairer()).parse(raw)
    name_match = _FILE_NAME.fullmatch(file_name) if file_name else None

    header = _header(root)
    document_name = header.find("DOCUMENT-NAME")
    company = header.find("COMPANY-NAME")
    formula = header.find("FORMULA-VERSION")
    document_code = _attribute(document_name, "ACODE")
    if document_code is None and name_match:
        document_code = name_match.group(2)

    return DartDocument(
        document_name=_text(document_name),
        document_code=document_code,
        company_name=_text(company),
        corp_code=_attribute(company, "AREGCIK"),
        formula_version=_text(formula),
        encoding=result.encoding,
        summary=MappingProxyType(_summary(root)),
        sections=tuple(_collect_sections(root)),
        rcept_no=name_match.group(1) if name_match else None,
        repair=result,
        root=root,
    )


def _header(root: Element) -> Element:
    # 2022년 이후 제출분은 루트 바로 아래, 그 전은 DOCUMENT-HEADER 안에 메타 태그가 있다.
    header = root.find("DOCUMENT-HEADER")
    return header if header is not None else root


def _text(element: Element | None) -> str | None:
    if element is None:
        return None
    return element_text(element) or None


def _attribute(element: Element | None, name: str) -> str | None:
    if element is None:
        return None
    return element.get(name) or None


def _summary(root: Element) -> dict[str, str]:
    entries = []
    for extraction in root.iterfind(".//SUMMARY/EXTRACTION"):
        code = extraction.get("ACODE")
        if code:
            entries.append((code, element_text(extraction)))
    return dict(entries)


def _collect_sections(element: Element) -> list[Section]:
    sections: list[Section] = []
    for child in element:
        level = _SECTION_LEVELS.get(child.tag)
        if level is not None:
            sections.append(_section(child, level, is_correction=False))
        elif child.tag == _CORRECTION:
            sections.append(_section(child, 1, is_correction=True))
        else:
            # LIBRARY·TABLE-GROUP 같은 묶음 태그는 투명하게 통과한다.
            sections.extend(_collect_sections(child))
    return sections


def _section(element: Element, level: int, *, is_correction: bool) -> Section:
    title = next((child for child in element if child.tag == "TITLE"), None)
    return Section(
        title=element_text(title) if title is not None else "",
        title_en=_attribute(title, "ENG"),
        assoc_code=_attribute(title, "AASSOCNOTE"),
        toc_id=_attribute(title, "ATOCID"),
        level=level,
        is_correction=is_correction,
        children=tuple(_collect_sections(element)),
        element=element,
    )
