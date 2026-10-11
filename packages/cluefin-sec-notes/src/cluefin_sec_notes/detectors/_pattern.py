"""방식 4: 문단 맨 앞의 Item 표기("Item 1A. Risk Factors", "ITEM 7.")를 찾는다. 신뢰도가 가장 낮은 마지막 수단.

- 목차 구간(앞 탐지기가 `excluded`에 넣은 것)과 링크 없는 글자 목차(Item 표기가 연달아 붙은 블록 무리)는 뺀다.
- 앞 탐지기가 Item을 하나라도 찾았으면 **빈자리 채우기**만 한다. 못 찾은 Item마다, 카탈로그상 앞·뒤 Item 후보 사이에서
  첫 헤딩을 고른다(목차에 없던 1C, 참조 편입 한 줄짜리 Part III 등).
- 아무도 못 찾았으면 카탈로그 순서와 문서 순서가 함께 증가하는 가장 긴 후보 사슬을 고른다. 본문 중간의
  "Item 7 of this report…" 같은 문단이 끼어도 사슬에서 빠진다.
- 카탈로그에 없는 번호의 헤딩은 `unknown_item`으로 알린다(카탈로그에 더할 Item이 생겼다는 신호).
"""

from __future__ import annotations

from dataclasses import dataclass

from cluefin_sec_notes._blocks import Paragraph, Table
from cluefin_sec_notes._labels import normalize_title, parse_item_label, parse_part
from cluefin_sec_notes._model import UNKNOWN_ITEM, Candidate, Finding, ItemKey
from cluefin_sec_notes.detectors._base import Detection, DetectionContext

# 헤딩으로 볼 첫 줄 최대 길이. 이보다 길면 Item 표기 뒤가 카탈로그 제목으로 시작할 때만 헤딩이다
# ("Item 1A. Risk Factors. The following …"처럼 제목과 본문이 한 문단에 붙은 공시).
_MAX_HEADING = 200
# 헤딩을 담은 표로 볼 최대 행 수(글자 있는 행).
_MAX_HEADING_TABLE_ROWS = 3
# 링크 없는 글자 목차: Item 표기 블록이 이만큼 연달아(사이 블록 없이) 이어지면 목차다.
_MIN_TEXT_TOC_RUN = 4


@dataclass(frozen=True)
class _Heading:
    block: int
    part: str | None
    numbers: tuple[str, ...]
    text: str
    bold: bool


class PatternDetector:
    name = "pattern"
    confidence = 0.6

    def detect(self, context: DetectionContext) -> Detection:
        headings = [heading for heading in _headings(context) if not context.is_excluded(heading.block)]
        headings = _drop_text_toc(context, headings)
        candidates, unknown = self._candidates(context, headings)
        findings = tuple(
            Finding(UNKNOWN_ITEM, f"카탈로그에 없는 Item: {heading.text[:80]!r}", block=heading.block, method=self.name)
            for heading in unknown
        )
        if any(candidate.confidence > self.confidence for candidate in context.previous):
            chosen = _fill_gaps(context, candidates)
        else:
            chosen = _longest_chain(context, candidates)
        return Detection(candidates=tuple(chosen), findings=findings)

    def _candidates(
        self, context: DetectionContext, headings: list[_Heading]
    ) -> tuple[list[Candidate], list[_Heading]]:
        catalog = context.catalog
        candidates: list[Candidate] = []
        unknown: list[_Heading] = []
        for heading in headings:
            specs = [catalog.spec(heading.part, number) for number in heading.numbers]
            if not any(specs):
                unknown.append(heading)
                continue
            for spec in specs:
                if spec is not None:
                    key = ItemKey(spec.part, spec.number)
                    candidates.append(Candidate(key, heading.block, self.name, self.confidence, heading.text[:120]))
        return candidates, unknown


def _headings(context: DetectionContext) -> list[_Heading]:
    """Item 표기로 시작하는 블록. 표기에 Part가 없으면("Item 1.") 앞에 나온 Part 헤딩("PART II — OTHER
    INFORMATION")의 Part를 쓴다. 10-Q처럼 Part마다 번호가 다시 시작하는 서식은 이게 없으면 Part II Item 1이
    Part I Item 1로 잡힌다. 목차 구간의 Part 행은 따라가지 않는다."""
    catalog = context.catalog
    headings = []
    current_part: str | None = None
    for index, block in enumerate(context.document.blocks):
        lines, bold = _leading_lines(block)
        if not lines:
            continue
        part = parse_part(lines[0])
        if part is not None and not context.is_excluded(index):
            current_part = part
        label = parse_item_label(lines[0])
        line = lines[0]
        if label is None and part is not None and len(lines) > 1:
            # "PART I. FINANCIAL INFORMATION⏎ITEM 1. FINANCIAL STATEMENTS"처럼 Part와 Item이 한 블록에 줄로 나뉜 헤딩
            label, line = parse_item_label(lines[1]), lines[1]
        if label is None:
            continue
        label_part = label.part or current_part
        if len(line) > _MAX_HEADING and not _starts_with_title(catalog, label.rest, label.numbers, label_part):
            continue
        headings.append(_Heading(index, label_part, label.numbers, line, bold))
    return headings


def _leading_lines(block) -> tuple[list[str], bool]:
    """블록 앞 두 줄(표는 글자 있는 앞 두 행)과 굵기."""
    if isinstance(block, Paragraph):
        return block.text.split("\n")[:2], block.bold
    if isinstance(block, Table):
        row = _first_filled_row(block)
        if row is None:
            return [], False
        rows = [block.row_text(index) for index in range(row, len(block.rows)) if block.row_text(index)]
        return rows[:2], all(cell.bold for cell in block.rows[row] if cell.text)
    return [], False


def _first_filled_row(table: Table) -> int | None:
    """표로 짠 헤딩("Item 1." | "Business")의 글자 있는 첫 행. 행이 많은 데이터 표는 헤딩이 아니다."""
    filled = [index for index, row in enumerate(table.rows) if any(cell.text for cell in row)]
    return filled[0] if filled and len(filled) <= _MAX_HEADING_TABLE_ROWS else None


def _starts_with_title(catalog, rest: str, numbers: tuple[str, ...], part: str | None) -> bool:
    normalized = normalize_title(rest)
    for number in numbers:
        spec = catalog.spec(part, number)
        if spec and any(normalized.startswith(normalize_title(title)) for title in spec.titles):
            return True
    return False


def _drop_text_toc(context: DetectionContext, headings: list[_Heading]) -> list[_Heading]:
    """사이 블록 없이 연달아 붙은 Item 표기 무리(링크 없는 목차)를 뺀다. 카탈로그 순서가 되돌아가면 무리가 끝난다
    (목차 바로 뒤에 본문 "Item 1."이 붙어 와도 본문 헤딩은 남는다)."""
    runs: list[list[_Heading]] = []
    for heading in headings:
        if (
            runs
            and heading.block - runs[-1][-1].block <= 1
            and _heading_position(context, heading) > _heading_position(context, runs[-1][-1])
        ):
            runs[-1].append(heading)
        else:
            runs.append([heading])
    return [heading for run in runs if len(run) < _MIN_TEXT_TOC_RUN for heading in run]


def _heading_position(context: DetectionContext, heading: _Heading) -> int:
    positions = [context.catalog.index(heading.part, number) for number in heading.numbers]
    return min((position for position in positions if position is not None), default=-1)


def _position(context: DetectionContext, key: ItemKey) -> int:
    index = context.catalog.index(key.part, key.number)
    return len(context.catalog.items) if index is None else index


def _fill_gaps(context: DetectionContext, candidates: list[Candidate]) -> list[Candidate]:
    """앞 탐지기가 못 찾은 Item마다, 카탈로그상 바로 앞·뒤 Item의 위치 사이에 있는 첫 후보."""
    known: dict[ItemKey, int] = {}
    for candidate in context.previous:
        if candidate.confidence <= PatternDetector.confidence:  # 검증 안 된 목차 링크 등은 빈자리로 본다
            continue
        if candidate.ranges:  # 교차참조 색인처럼 구간이 정해진 Item은 문서 순서의 기준이 아니다
            continue
        known[candidate.key] = min(candidate.block, known.get(candidate.key, candidate.block))
    chosen = []
    for key in dict.fromkeys(candidate.key for candidate in candidates):
        if key in known:
            continue
        lower, upper = _neighbours(context, known, _position(context, key))
        chosen.extend(
            next(
                (
                    [candidate]
                    for candidate in candidates
                    if candidate.key == key
                    and (lower is None or candidate.block >= lower)
                    and (upper is None or candidate.block <= upper)
                ),
                [],
            )
        )
    return chosen


def _neighbours(context: DetectionContext, known: dict[ItemKey, int], position: int) -> tuple[int | None, int | None]:
    """카탈로그상 바로 앞 Item과 바로 뒤 Item의 블록 위치."""
    before = [(_position(context, key), block) for key, block in known.items() if _position(context, key) < position]
    after = [(_position(context, key), block) for key, block in known.items() if _position(context, key) > position]
    return (max(before)[1] if before else None, min(after)[1] if after else None)


def _longest_chain(context: DetectionContext, candidates: list[Candidate]) -> list[Candidate]:
    """문서 순서와 카탈로그 순서가 함께 증가하는 가장 긴 헤딩 사슬. 같은 길이면 앞쪽 것.

    한 블록의 후보(결합 헤딩 "Items 1 and 2")는 한 마디로 묶고 그중 가장 앞 Item의 카탈로그 위치로 순서를 본다.
    그래야 "Items 1 and 2" 다음의 "Item 1A"가 사슬에 들어간다.
    """
    nodes: dict[int, list[Candidate]] = {}
    for candidate in candidates:
        nodes.setdefault(candidate.block, []).append(candidate)
    blocks = sorted(nodes)
    positions = [min(_position(context, candidate.key) for candidate in nodes[block]) for block in blocks]
    best = [1] * len(blocks)
    previous = [-1] * len(blocks)
    for current in range(len(blocks)):
        for earlier in range(current):
            if positions[earlier] < positions[current] and best[earlier] + 1 > best[current]:
                best[current] = best[earlier] + 1
                previous[current] = earlier
    if not blocks:
        return []
    end = max(range(len(blocks)), key=lambda index: (best[index], -index))
    chain: list[Candidate] = []
    while end != -1:
        chain = nodes[blocks[end]] + chain
        end = previous[end]
    return chain
