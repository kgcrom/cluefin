"""섹션 찾기."""

from __future__ import annotations

import re
from fnmatch import fnmatchcase

from cluefin_dart_notes._document import DartDocument, Section

# 제목 앞 번호: "III. ", "3. ", "7-1. ", "(첨부)" 는 번호가 아니라 제목의 일부로 둔다.
_TITLE_NUMBER = re.compile(r"^\s*(?:[IVX]+|\d+(?:-\d+)?)\.\s*")
_WHITESPACE = re.compile(r"\s+")


def title_key(title: str) -> str:
    """제목 비교용 키: 앞 번호와 모든 공백을 지운다. "3. 연결재무제표 주석" → "연결재무제표주석"."""
    return _WHITESPACE.sub("", _TITLE_NUMBER.sub("", title))


def find_sections(document: DartDocument, *, assoc_code: str | None = None, title: str | None = None) -> list[Section]:
    """조건에 맞는 섹션 전부(문서 순서).

    Args:
        assoc_code: 섹션 코드. `D-0-1-*` 같은 glob 패턴도 받는다.
        title: 제목. 앞 번호와 공백을 무시하고 같으면 맞는다("연결재무제표 주석"은 "3. 연결재무제표 주석"과 맞다).
    """
    if assoc_code is None and title is None:
        raise ValueError("assoc_code 와 title 중 하나는 있어야 합니다.")
    key = title_key(title) if title is not None else None
    return [
        section
        for section in document.iter_sections()
        if (assoc_code is None or (section.assoc_code is not None and fnmatchcase(section.assoc_code, assoc_code)))
        and (key is None or title_key(section.title) == key)
    ]


def find_section(document: DartDocument, *, assoc_code: str | None = None, title: str | None = None) -> Section | None:
    """조건에 맞는 첫 섹션. 없으면 None."""
    found = find_sections(document, assoc_code=assoc_code, title=title)
    return found[0] if found else None


def company_overview(document: DartDocument) -> Section | None:
    """정기보고서의 "I. 회사의 개요" 장. 장 자체에는 코드가 없어 하위 섹션 코드(`D-0-1-*`)로 찾는다."""
    if not document.is_periodic_report:
        return None
    return next(
        (
            section
            for section in document.sections
            if any(child.assoc_code and child.assoc_code.startswith("D-0-1-") for child in section.children)
        ),
        None,
    )


def business_description(document: DartDocument) -> Section | None:
    """정기보고서의 "II. 사업의 내용" 장(`D-0-2-0-0`). 하위 섹션(`L-0-2-*`)이 없는 문서도 있다.

    감사보고서에서는 같은 코드가 "외부감사 실시내용"이라 정기보고서가 아니면 None을 돌려준다.
    """
    if not document.is_periodic_report:
        return None
    return find_section(document, assoc_code="D-0-2-0-0")


def business_overviews(document: DartDocument) -> list[Section]:
    """정기보고서의 "사업의 개요" 섹션을 업종 템플릿마다 모두(문서 순서).

    여러 업종을 함께 하는 회사는 사업의 내용이 템플릿별로 따로 있다. 예: "(제조서비스업)사업의 개요"
    (`L-0-2-1-L1`)와 "(금융업)사업의 개요"(`L-0-2-1-L2`). `find_section`은 그중 첫 번째만 돌려준다.
    하위 섹션이 없는 오래된 공시는 "II. 사업의 내용" 장 하나를 돌려준다(장 본문에 개요가 바로 있다).
    정기보고서가 아니면 빈 목록이다.
    """
    business = business_description(document)
    if business is None:
        return []
    overviews = [
        section for section in business.iter() if section.assoc_code and section.assoc_code.startswith("L-0-2-1-")
    ]
    if overviews:
        return overviews
    return [] if business.children else [business]
