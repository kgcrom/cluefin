"""본문이 같은 문서의 다른 쪽에 있다고만 적은 Item에 그 쪽 구간을 붙인다.

"Item 8. … See pages F-1 through F-30", 연차보고서형 "Item 7. … appears on pages 46–160"처럼 Item 자리에는 참조
문장만 있고 본문은 서명란 뒤 F-쪽이나 문서 앞쪽에 있는 공시가 있다. 머리말·꼬리말의 쪽 번호(`Page.label`)로 그
쪽들을 블록 구간으로 바꿔 `Item.ranges`에 더한다.

- 본문이 거의 참조 문장뿐인(`_REFERENCE_ONLY_MAX_CHARS` 이하) Item만 본다. 본문이 따로 있는 Item 끝의
  "Refer to … on pages 51–54 for information on occupancy expense"는 곁가지 참조다(골든 JPM Item 2).
- 이 문서를 가리키는 **첫 참조만** 따른다. 뒤 참조는 "read in conjunction with the Consolidated Financial
  Statements … on pages 165–314"처럼 다른 Item의 본문이다(골든 JPM Item 7).
- 위임장·주주 대상 연차보고서·Exhibit 13을 말하는 본문은 건드리지 않는다(내용이 다른 문서에 있다).
- 닫힌 범위("pages 55 through 119", "pages 133-142")만 따라간다. 쪽 하나("Management's report on page F-2",
  "see Market Risk Management on page 75")는 Item 내용 일부를 가리키는 곁가지라 붙이지 않는다(골든 9A·7A에서
  확인). 글자 없는 열린 참조("Note S beginning on page 96")는 끝을 모른다.
- 재무제표 Item(`ItemSpec.financial_statements`)은 본문 길이를 `REFERENCE_BODY_MAX_CHARS`까지 보고(F-쪽 색인 표가
  Item 자리에 있는 공시), 열린 참조("beginning on page F-1", "page II-24")와 "page F-1"을
  그 글자 쪽이 끊기지 않고 이어지는 데까지(다음 Item 헤딩이 먼저 오면 거기까지)로 읽고, 쪽 번호가 없어도
  ("appears following Item 15") F-쪽이 Item 뒤에 따로 있으면 F-쪽을 본문으로 본다.
- 문서 목록 Item(`ItemSpec.lists_documents`, 10-K Item 15)은 건드리지 않는다.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import replace

from cluefin_sec_notes._catalog import FormCatalog, ItemSpec
from cluefin_sec_notes._document import SecDocument
from cluefin_sec_notes._model import PAGE_REFERENCE_UNRESOLVED, Finding, Item
from cluefin_sec_notes._pages import (
    EXTERNAL_DOCUMENT,
    PageIndex,
    PageReference,
    find_page_references,
    merge_ranges,
)

REFERENCE_BODY_MAX_CHARS = 2500
_REFERENCE_ONLY_MAX_CHARS = 1000
_STATEMENT_PAGES = "F"
_LETTER_PREFIX = re.compile(r"^([A-Z]{1,3})-\d")


def item_body(item: Item) -> str:
    """헤딩 줄을 뺀 첫 구간 텍스트."""
    text = item.document.text(item.start, item.end)
    heading = item.heading
    return text[len(heading) :] if text.startswith(heading) else text


def resolve_page_references(
    document: SecDocument, catalog: FormCatalog, items: Sequence[Item]
) -> tuple[tuple[Item, ...], list[Finding]]:
    if not document.pages:
        return tuple(items), []
    index = PageIndex(document.pages)
    starts = sorted({item.start for item in items})
    resolved: list[Item] = []
    findings: list[Finding] = []
    for item in items:
        spec = catalog.spec(item.key.part, item.key.number)
        body = item_body(item)
        if spec is None or not _may_refer(spec, item, body):
            resolved.append(item)
            continue
        references = [reference for reference in find_page_references(body) if not reference.external][:1]
        ranges, unresolved = _resolve(index, references, starts, sections=spec.financial_statements)
        if not ranges and spec.financial_statements:
            section = index.lettered_section(_STATEMENT_PAGES)
            if section is not None and section[0] >= item.end:
                ranges = [section]
        added = _outside(ranges, (item.start, item.end))
        if added:
            resolved.append(
                replace(
                    item,
                    ranges=((item.start, item.end), *added),
                    incorporated_by_reference=False,
                )
            )
            continue
        resolved.append(item)
        if unresolved:
            findings.append(
                Finding(
                    PAGE_REFERENCE_UNRESOLVED,
                    f"{item.key}: 쪽 {', '.join(unresolved)}을 머리말·꼬리말 쪽 번호에서 찾지 못했다",
                    key=item.key,
                    block=item.start,
                )
            )
    return tuple(resolved), findings


def _may_refer(spec: ItemSpec, item: Item, body: str) -> bool:
    if spec.lists_documents or len(item.ranges) > 1 or EXTERNAL_DOCUMENT.search(body):
        return False
    return len(body) <= (REFERENCE_BODY_MAX_CHARS if spec.financial_statements else _REFERENCE_ONLY_MAX_CHARS)


def _resolve(
    index: PageIndex, references: list[PageReference], starts: list[int], *, sections: bool
) -> tuple[list[tuple[int, int]], list[str]]:
    """`sections`면 글자 쪽의 열린 참조·"X-1" 참조를 그 글자 쪽 구간으로 읽는다."""
    ranges: list[tuple[int, int]] = []
    unresolved: list[str] = []
    for reference in references:
        for first, last in reference.spans:
            prefix = _LETTER_PREFIX.match(first)
            if sections and prefix and (reference.open_ended or first == last == f"{prefix.group(1)}-1"):
                section = index.lettered_section(prefix.group(1), first)
                if section is None:
                    unresolved.append(first)
                else:
                    ranges.append(_until_next_item(section, starts))
            elif first != last:
                found, missing = index.ranges([(first, last)])
                ranges.extend(found)
                unresolved.extend(missing)
    return ranges, unresolved


def _until_next_item(section: tuple[int, int], starts: list[int]) -> tuple[int, int]:
    """다음 Item 헤딩 앞에서 끊는다. F-1쪽 맨 위가 다른 Item 헤딩("Item 15. Exhibits …")이면 그 블록은 건너뛴다."""
    start, end = section
    if start in starts:
        start += 1
    following = [item_start for item_start in starts if start < item_start < end]
    return (start, following[0]) if following else (start, end)


def _outside(ranges: list[tuple[int, int]], own: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    """합친 구간에서 Item 자기 구간과 겹치는 부분을 뺀 나머지."""
    pieces = []
    for start, end in merge_ranges(ranges):
        pieces.extend(piece for piece in ((start, min(end, own[0])), (max(start, own[1]), end)) if piece[0] < piece[1])
    return tuple(pieces)
