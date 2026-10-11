"""탐지기 규약. 새 탐지 방식은 `Detector`를 구현해 `DEFAULT_DETECTORS`에 넣으면 캐스케이드에 들어간다."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from cluefin_sec_notes._blocks import Paragraph, Table
from cluefin_sec_notes._catalog import FormCatalog
from cluefin_sec_notes._document import SecDocument
from cluefin_sec_notes._labels import parse_item_label, parse_part
from cluefin_sec_notes._model import Candidate, Finding, ItemKey

# 헤딩을 담은 표로 볼 최대 행 수(글자 있는 행). "Item 1." | "Business"처럼 표로 짠 헤딩.
MAX_HEADING_TABLE_ROWS = 3
# Item 표기 행이 이만큼 있는 표는 목차다. Part 헤딩 뒤 이만큼의 블록 안에서 찾는다.
_TOC_TABLE_ROWS = 3
_TOC_LOOKAHEAD = 3


@dataclass
class DetectionContext:
    """탐지기들이 공유하는 상태. 앞 탐지기가 알아낸 것을 뒤 탐지기가 쓴다.

    Attributes:
        excluded: Item 본문 탐색에서 뺄 블록 구간 `[start, end)`. 목차 탐지기가 목차 구간을 넣는다
            (목차 안의 "Item 1A. Risk Factors"를 본문 헤딩으로 잡지 않게).
        previous: 앞 탐지기들이 낸 후보. 신뢰도 낮은 탐지기는 이걸 보고 빈자리만 채운다.
        absent: 공시가 이 문서에 본문이 없다고 밝힌 Item → 근거(교차참조 색인의 "Not Applicable", 위임장 각주).
            못 찾아도 `missing_item`이 아니라 생략(`omitted`)으로 본다.
    """

    document: SecDocument
    catalog: FormCatalog
    excluded: list[tuple[int, int]] = field(default_factory=list)
    previous: list[Candidate] = field(default_factory=list)
    absent: dict[ItemKey, str] = field(default_factory=dict)
    _parts: tuple[int, list[str | None]] | None = field(default=None, repr=False)

    def is_excluded(self, block: int) -> bool:
        return any(start <= block < end for start, end in self.excluded)

    def part_at(self, block: int) -> str | None:
        """그 블록에 적용되는 Part: 앞에 나온(그 블록 포함) 마지막 Part 헤딩. 목차 구간의 Part 행은 보지 않는다.
        10-Q처럼 "Item 1."에 Part가 없는 서식에서 Item 키를 정한다."""
        if self._parts is None or self._parts[0] != len(self.excluded):
            current: str | None = None
            parts: list[str | None] = []
            blocks = self.document.blocks
            for index, each in enumerate(blocks):
                lines = leading_lines(each)[0]
                part = parse_part(lines[0]) if lines else None
                if part is not None and not self.is_excluded(index) and not _heads_toc_table(blocks, index):
                    current = part
                parts.append(current)
            self._parts = (len(self.excluded), parts)
        parts = self._parts[1]
        return parts[min(block, len(parts) - 1)] if parts else None


def _heads_toc_table(blocks, index: int) -> bool:
    """Part 헤딩 바로 뒤가 Item 표기 행이 여럿인 표(링크 없는 목차)다. 목차의 "PART II"가 본문 Part I Item들에
    붙지 않게 한다(본문에 Part I 헤딩 없이 "ITEM 1."부터 시작하는 2008년 10-Q)."""
    for following in range(index + 1, min(index + 1 + _TOC_LOOKAHEAD, len(blocks))):
        block = blocks[following]
        if isinstance(block, Table):
            labelled = sum(1 for row in range(len(block.rows)) if parse_item_label(block.row_text(row)) is not None)
            return labelled >= _TOC_TABLE_ROWS
        if isinstance(block, Paragraph) and block.text.strip():
            return False
    return False


def leading_lines(block) -> tuple[list[str], bool]:
    """헤딩을 읽을 블록 앞 두 줄(표는 글자 있는 앞 두 행)과 굵기. 행이 많은 표는 첫 행만 Item 표기일 때만 그 행을
    준다(8-K "Item 9.01 Financial Statements and Exhibits" 행 아래 전시물 목록이 붙은 표). 다른 행에도 Item 표기가
    있으면 목차라 빈 목록이다."""
    if isinstance(block, Paragraph):
        return block.text.split("\n")[:2], block.bold
    if isinstance(block, Table):
        filled = [index for index, row in enumerate(block.rows) if any(cell.text for cell in row)]
        if not filled:
            return [], False
        rows = [block.row_text(index) for index in filled]
        bold = all(cell.bold for cell in block.rows[filled[0]] if cell.text)
        if len(filled) <= MAX_HEADING_TABLE_ROWS:
            return rows[:2], bold
        if parse_item_label(rows[0]) is not None and not any(parse_item_label(row) for row in rows[1:]):
            return rows[:1], bold
    return [], False


@dataclass(frozen=True)
class Detection:
    candidates: tuple[Candidate, ...] = ()
    findings: tuple[Finding, ...] = ()


class Detector(Protocol):
    """Item 시작 위치 후보를 내는 방식 하나.

    `name`은 `Item.method`로 드러나고, `confidence`가 높은 탐지기의 후보부터 채택된다. 탐지기는 후보만 내고
    채택·충돌 판단은 하지 않는다(`extract_items`가 한다).
    """

    name: str
    confidence: float

    def detect(self, context: DetectionContext) -> Detection: ...
