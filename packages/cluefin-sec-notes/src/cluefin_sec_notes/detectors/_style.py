"""방식 3: "Item" 표기 없이 제목만 있는 헤딩("CERTAIN RELATIONSHIPS AND RELATED TRANSACTIONS, AND DIRECTOR
INDEPENDENCE")을 스타일로 알아본다. 앞 탐지기들이 못 찾은 Item의 빈자리만 채운다.

- 앞 탐지기가 찾은 Item 헤딩 문단들의 스타일(굵기, 글자 크기) 최빈값을 이 문서의 Item 헤딩 스타일로 본다.
  참조할 헤딩이 없으면 아무것도 내지 않는다.
- 못 찾은 Item마다 카탈로그상 바로 앞 Item과 바로 뒤 Item 위치 사이에서, 그 스타일의 한 줄짜리 문단 중 제목이
  카탈로그 제목·별칭과 같은 첫 문단을 고른다. 앞 Item이 없으면 그 Part 헤딩부터 찾고, 그것도 없으면 찾지 않는다
  (표지·목차의 제목 줄을 피한다).
- 제목 비교는 단어 끝 s를 떼고 한다(공시가 "Related Transaction"처럼 단수로 쓴 경우). 같은 제목이라도 스타일이
  다르면(본문 속 굵지 않은 소제목) 받지 않는다.
- 신뢰도는 정규식(0.6)과 목차(0.95) 사이. 빈자리만 채우므로 다른 탐지기의 후보와 겨루지 않는다.
"""

from __future__ import annotations

from collections import Counter

from cluefin_sec_notes._blocks import Paragraph
from cluefin_sec_notes._labels import normalize_title, parse_item_label, parse_part
from cluefin_sec_notes._model import Candidate, ItemKey
from cluefin_sec_notes.detectors._base import Detection, DetectionContext

_MAX_TITLE_LINE = 150
# 앞 탐지기 후보 중 위치를 믿을 만한 것(검증 안 된 목차 링크 0.5는 뺀다).
_MIN_KNOWN_CONFIDENCE = 0.6


class HeadingStyleDetector:
    name = "heading_style"
    confidence = 0.7

    def detect(self, context: DetectionContext) -> Detection:
        known = _known_blocks(context)
        style = _heading_style(context, known)
        if style is None:
            return Detection()
        blocks = context.document.blocks
        candidates = []
        for position, spec in enumerate(context.catalog.items):
            key = ItemKey(spec.part, spec.number)
            if key in known or key in context.absent or not spec.applies_to(context.document.period_end):
                continue
            lower, upper = _neighbours(context, known, position)
            if lower is None:
                lower = _part_heading_before(context, spec.part, len(blocks) if upper is None else upper)
            if lower is None:
                continue
            titles = {_fold(title) for title in spec.titles}
            for index in range(lower + 1, len(blocks) if upper is None else upper):
                block = blocks[index]
                if context.is_excluded(index) or not _is_title_line(block, style, titles):
                    continue
                candidates.append(Candidate(key, index, self.name, self.confidence, f"제목 헤딩: {block.text[:120]}"))
                break
        return Detection(candidates=tuple(candidates))


def _known_blocks(context: DetectionContext) -> dict[ItemKey, int]:
    known: dict[ItemKey, int] = {}
    for candidate in context.previous:
        if candidate.confidence < _MIN_KNOWN_CONFIDENCE or candidate.ranges:
            continue
        known[candidate.key] = min(candidate.block, known.get(candidate.key, candidate.block))
    return known


def _heading_style(context: DetectionContext, known: dict[ItemKey, int]) -> tuple[bool, float | None] | None:
    styles = Counter(
        (block.bold, block.font_size)
        for block in (context.document.blocks[index] for index in set(known.values()))
        if isinstance(block, Paragraph)
    )
    return styles.most_common(1)[0][0] if styles else None


def _neighbours(context: DetectionContext, known: dict[ItemKey, int], position: int) -> tuple[int | None, int | None]:
    """카탈로그상 바로 앞 Item과 바로 뒤 Item의 블록 위치."""
    catalog = context.catalog
    before, after = [], []
    for key, block in known.items():
        index = catalog.index(key.part, key.number)
        if index is not None:
            (before if index < position else after).append((index, block))
    return (max(before)[1] if before else None, min(after)[1] if after else None)


def _part_heading_before(context: DetectionContext, part: str | None, before: int) -> int | None:
    """카탈로그상 앞 Item이 없을 때(Part I 첫 Item) 그 Part 헤딩("PART I. FINANCIAL INFORMATION")을 하한으로 쓴다."""
    if part is None:
        return None
    for index in range(before - 1, -1, -1):
        block = context.document.blocks[index]
        if isinstance(block, Paragraph) and not context.is_excluded(index) and parse_part(block.text) == part:
            return index
    return None


def _is_title_line(block, style: tuple[bool, float | None], titles: set[str]) -> bool:
    if not isinstance(block, Paragraph) or "\n" in block.text or len(block.text) > _MAX_TITLE_LINE:
        return False
    if (block.bold, block.font_size) != style or parse_item_label(block.text) is not None:
        return False
    return _fold(block.text) in titles


def _fold(title: str) -> str:
    """제목 비교용: `normalize_title` 뒤 단어 끝 s를 뗀다("transactions" = "transaction")."""
    return " ".join(
        word[:-1] if len(word) > 3 and word.endswith("s") else word for word in normalize_title(title).split()
    )
