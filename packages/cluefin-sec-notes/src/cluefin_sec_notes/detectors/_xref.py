"""방식 2: "Form 10-K Cross-Reference Index"의 쪽 범위로 Item 구간을 정한다.

은행·대기업 일부는 10-K를 연차보고서 순서로 쓰고, 맨 앞이나 뒤의 색인 표에 Item마다 쪽 범위만 적는다
("1. | Business | 4–36, 121–127, 129" 또는 "Item 1. | Business | 4-7, 9-10, 71-73"). 본문에는 Item 헤딩이 없다.

- 제목에 "cross(-)reference index"가 있는 블록과 그 뒤에 이어진 표들만 색인으로 본다(일반 목차의 쪽 번호와 구별).
- Item 칸은 "Item 1." 또는 번호만("1."). 마지막 칸이 쪽 목록이 아니면 그 행은 건너뛴다.
- 쪽 범위를 `Page.label`로 블록 구간으로 옮겨 `Candidate.ranges`로 낸다. 공시가 직접 밝힌 구간이라 목차 앵커보다
  신뢰도가 높다.
- "Not Applicable"이나 각주만 있는 행(위임장 참조 편입)은 이 문서에 본문이 없다는 진술이라 `context.absent`에 넣는다.
- 색인 표는 `context.excluded`에 넣어 뒤 탐지기와 생략 판정이 "1." 행을 Item 표기로 보지 않게 한다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from cluefin_sec_notes._blocks import PageBreak, Paragraph, Table
from cluefin_sec_notes._labels import parse_item_label, parse_part
from cluefin_sec_notes._model import PAGE_REFERENCE_UNRESOLVED, Candidate, Finding, ItemKey
from cluefin_sec_notes._pages import PageIndex, PageList, parse_page_list
from cluefin_sec_notes.detectors._base import Detection, DetectionContext

_TITLE = re.compile(r"cross\W{0,3}reference\s+index", re.IGNORECASE)
_MAX_TITLE = 120
# 제목 블록과 첫 표 사이에 올 수 있는 블록 수(설명 문단, "Form 10-K" 같은 소제목).
_MAX_GAP = 6
_NUMBER_CELL = re.compile(r"^(\d{1,2}[A-D]?)\.?$", re.IGNORECASE)


@dataclass(frozen=True)
class _Row:
    key: ItemKey
    pages: PageList
    text: str


class CrossReferenceDetector:
    name = "cross_reference"
    confidence = 0.97

    def detect(self, context: DetectionContext) -> Detection:
        tables = _index_tables(context)
        if not tables:
            return Detection()
        context.excluded.append((tables[0], tables[-1] + 1))
        index = PageIndex(context.document.pages)
        candidates: list[Candidate] = []
        findings: list[Finding] = []
        for row in _index_rows(context, tables):
            if row.pages.not_applicable or not row.pages.spans:
                context.absent.setdefault(row.key, f"교차참조 색인: {row.text}")
                continue
            ranges, unresolved = index.ranges(row.pages.spans)
            if unresolved:
                findings.append(
                    Finding(
                        PAGE_REFERENCE_UNRESOLVED,
                        f"{row.key}: 교차참조 색인의 쪽 {', '.join(unresolved)}을 머리말·꼬리말 쪽 번호에서 찾지 못했다",
                        key=row.key,
                        block=tables[0],
                        method=self.name,
                    )
                )
            if ranges:
                evidence = f"교차참조 색인: {row.text}"
                candidates.append(Candidate(row.key, ranges[0][0], self.name, self.confidence, evidence, ranges))
        return Detection(candidates=tuple(candidates), findings=tuple(findings))


def _index_tables(context: DetectionContext) -> list[int]:
    """색인 제목 블록 뒤(제목이 표 첫 행이면 그 표부터)에 이어진 표들의 위치."""
    blocks = context.document.blocks
    for position, block in enumerate(blocks):
        if not _is_title(block):
            continue
        first = position if isinstance(block, Table) else _next_table(blocks, position)
        if first is None:
            continue
        tables = [first]
        for following in range(first + 1, len(blocks)):
            if isinstance(blocks[following], PageBreak):
                continue
            if not isinstance(blocks[following], Table):
                break
            tables.append(following)
        return tables
    return []


def _is_title(block) -> bool:
    if isinstance(block, Paragraph):
        text = block.text
    elif isinstance(block, Table) and block.rows:
        text = next((block.row_text(index) for index in range(len(block.rows)) if block.row_text(index)), "")
    else:
        return False
    return len(text) <= _MAX_TITLE and bool(_TITLE.search(text))


def _next_table(blocks, position: int) -> int | None:
    for following in range(position + 1, min(position + 1 + _MAX_GAP, len(blocks))):
        if isinstance(blocks[following], Table):
            return following
    return None


def _index_rows(context: DetectionContext, tables: list[int]) -> list[_Row]:
    catalog = context.catalog
    rows: list[_Row] = []
    part: str | None = None
    for position in tables:
        table = context.document.blocks[position]
        for row in table.rows:
            cells = [cell.text.strip() for cell in row if cell.text.strip()]
            if not cells:
                continue
            part = parse_part(cells[0]) or part
            numbers = _numbers(cells[0])
            pages = parse_page_list(cells[-1]) if len(cells) > 1 else None
            if not numbers or pages is None:
                continue
            text = " | ".join(" ".join(cell.split()) for cell in cells)
            for number in numbers:
                spec = catalog.spec(part, number)
                if spec is not None:
                    rows.append(_Row(ItemKey(spec.part, spec.number), pages, text))
    return rows


def _numbers(cell: str) -> tuple[str, ...]:
    label = parse_item_label(cell)
    if label is not None:
        return label.numbers
    match = _NUMBER_CELL.match(cell)
    return (match.group(1).upper(),) if match else ()
