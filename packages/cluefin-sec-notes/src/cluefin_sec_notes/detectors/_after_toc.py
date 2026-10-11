"""방식 5: 헤딩 없이 목차 바로 뒤에서 시작하는 재무제표 Item.

10-Q 상당수가 목차("PART I – FINANCIAL INFORMATION | Item 1. Financial Statements | … | Item 6. Exhibits") 다음 쪽에
"Item 1." 헤딩 없이 재무상태표부터 싣는다. Item 1 표기는 목차에만 있어서 다른 탐지기는 찾지 못한다.

- 재무제표 Item(`ItemSpec.financial_statements`)을 앞 탐지기가 못 찾았고, 카탈로그상 다음 Item 위치는 알 때만 본다.
- 다음 Item 앞의 마지막 목차(목차 탐지기가 뺀 구간, 또는 Item 표기 행이 여럿인 표) 바로 뒤 블록을 시작으로 본다.
- 그 사이에 이미 찾은 다른 Item이 있거나(10-K Item 8) 표가 하나도 없으면 내지 않는다.
- 신뢰도가 가장 낮다(다른 어떤 탐지기의 후보와도 겨루지 않는다).
"""

from __future__ import annotations

from cluefin_sec_notes._blocks import PageBreak, Table
from cluefin_sec_notes._document import block_text
from cluefin_sec_notes._labels import parse_item_label
from cluefin_sec_notes._model import Candidate, ItemKey
from cluefin_sec_notes.detectors._base import Detection, DetectionContext

_MIN_KNOWN_CONFIDENCE = 0.5
_TOC_TABLE_ROWS = 3


class StatementsAfterTocDetector:
    name = "statements_after_toc"
    confidence = 0.45

    def detect(self, context: DetectionContext) -> Detection:
        catalog = context.catalog
        known: dict[ItemKey, int] = {}
        for candidate in context.previous:
            if candidate.confidence >= _MIN_KNOWN_CONFIDENCE and not candidate.ranges:
                known[candidate.key] = min(candidate.block, known.get(candidate.key, candidate.block))
        candidates = []
        for position, spec in enumerate(catalog.items):
            key = ItemKey(spec.part, spec.number)
            if not spec.financial_statements or key in known or position + 1 >= len(catalog.items):
                continue
            following = catalog.items[position + 1]
            upper = known.get(ItemKey(following.part, following.number))
            if upper is None:
                continue
            start = _after_last_toc(context, upper)
            if start is None or any(start <= block < upper for block in known.values()):
                continue  # 사이에 다른 Item이 있으면 목차 바로 뒤가 이 Item이 아니다(10-K Item 8)
            if not any(isinstance(block, Table) for block in context.document.blocks[start:upper]):
                continue
            evidence = f"목차 뒤 헤딩 없는 재무제표: {block_text(context.document.blocks[start])[:80]}"
            candidates.append(Candidate(key, start, self.name, self.confidence, evidence))
        return Detection(candidates=tuple(candidates))


def _after_last_toc(context: DetectionContext, upper: int) -> int | None:
    """`upper` 앞 마지막 목차의 바로 뒤, 글자가 있는 첫 블록."""
    toc_end = max((end for _, end in context.excluded if end <= upper), default=None)
    for index in range(upper - 1, (toc_end or 0) - 1, -1):
        if _is_toc_table(context.document.blocks[index]):
            toc_end = index + 1
            break
    if toc_end is None:
        return None
    for index in range(toc_end, upper):
        block = context.document.blocks[index]
        if not isinstance(block, PageBreak) and block_text(block).strip():
            return index
    return None


def _is_toc_table(block) -> bool:
    if not isinstance(block, Table):
        return False
    labelled = sum(1 for row in range(len(block.rows)) if parse_item_label(block.row_text(row)) is not None)
    return labelled >= _TOC_TABLE_ROWS
