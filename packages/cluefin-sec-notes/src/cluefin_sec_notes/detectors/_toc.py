"""방식 1: 목차의 문서 안 링크(`<a href="#…">`)를 따라간다. Workiva·DFIN 공시 대부분이 이 형태다."""

from __future__ import annotations

from dataclasses import dataclass

from cluefin_sec_notes._blocks import Paragraph, Table
from cluefin_sec_notes._document import block_text
from cluefin_sec_notes._labels import match_title, normalize_title, parse_item_label, parse_part
from cluefin_sec_notes._model import INFO, TOC_NOT_FOUND, TOC_TARGET_MISSING, Candidate, Finding, ItemKey
from cluefin_sec_notes.detectors._base import Detection, DetectionContext

# 목차 항목 사이 거리(블록 수). 목차는 표 하나이거나 이어진 문단들이다.
_MAX_GAP = 6
# 이만큼 서로 다른 Item 링크가 모여야 목차로 본다.
_MIN_ITEMS = 3
# 앵커 블록이 그 Item 헤딩인지 확인하지 못한 후보. 정규식 탐지기(0.6)보다 낮다.
UNVERIFIED = "toc_anchor_unverified"
UNVERIFIED_CONFIDENCE = 0.5
# 링크가 페이지 머리를 가리킬 때 실제 Item 헤딩을 찾아 내려가는 최대 블록 수.
_MAX_REFINE = 40


@dataclass(frozen=True, slots=True)
class _Entry:
    """목차 행 하나: 어떤 Item(들)이 어느 앵커를 가리키는지."""

    block: int
    keys: tuple[ItemKey, ...]
    targets: tuple[str, ...]
    text: str


class TocAnchorDetector:
    name = "toc_anchor"
    confidence = 0.95

    def detect(self, context: DetectionContext) -> Detection:
        entries = self._entries(context)
        toc = _largest_cluster(entries)
        if len({key for entry in toc for key in entry.keys}) < _MIN_ITEMS:
            return Detection(findings=(Finding(TOC_NOT_FOUND, "Item 링크가 모인 목차가 없다", severity=INFO),))
        start, end = toc[0].block, toc[-1].block + 1
        context.excluded.append((start, end))

        candidates: list[Candidate] = []
        findings: list[Finding] = []
        anchors = context.document.anchors
        for entry in toc:
            blocks = [anchors[target] for target in entry.targets if target in anchors]
            if not blocks:
                findings.append(
                    Finding(
                        TOC_TARGET_MISSING,
                        f"목차 링크 대상이 없다: {', '.join(entry.targets)}",
                        key=entry.keys[0],
                        block=entry.block,
                        method=self.name,
                    )
                )
                continue
            block = min(blocks)
            if start <= block < end:  # 목차 안을 가리키는 링크(목차 맨 위로 등)
                continue
            for key in entry.keys:
                heading, verified = _heading_near(context, block, key)
                if not verified:
                    # 링크가 다른 Item 헤딩이나 본문 중간을 가리킨다(목차 작성 오류). 헤딩을 찾는 탐지기가 이기게 낮춘다.
                    evidence = f"목차: {entry.text} (앵커 블록이 이 Item 헤딩이 아니다)"
                    candidates.append(Candidate(key, heading, UNVERIFIED, UNVERIFIED_CONFIDENCE, evidence))
                    continue
                evidence = f"목차: {entry.text}" + ("" if heading == block else f" (앵커 블록 {block} → 헤딩)")
                candidates.append(Candidate(key, heading, self.name, self.confidence, evidence))
        return Detection(candidates=tuple(candidates), findings=tuple(findings))

    def _entries(self, context: DetectionContext) -> list[_Entry]:
        entries: list[_Entry] = []
        part: str | None = None
        for index, block in enumerate(context.document.blocks):
            for text, links in _rows(block):
                part = parse_part(text) or part
                targets = tuple(dict.fromkeys(link.target for link in links))
                if not targets:
                    continue
                keys = _keys(context, text, part)
                if keys:
                    entries.append(_Entry(index, keys, targets, text))
        return entries


def _rows(block):
    """(행 텍스트, 그 행의 링크). 표는 행마다, 문단은 통째로."""
    if isinstance(block, Paragraph):
        return [(block.text, block.links)]
    if isinstance(block, Table):
        return [
            (block.row_text(index), [link for cell in row for link in cell.links])
            for index, row in enumerate(block.rows)
        ]
    return []


def _keys(context: DetectionContext, text: str, part: str | None) -> tuple[ItemKey, ...]:
    catalog = context.catalog
    label = parse_item_label(text)
    if label is not None:
        label_part = label.part or part
        keys = []
        for number in label.numbers:
            spec = catalog.resolve(label_part, number)
            if spec is not None:
                keys.append(ItemKey(spec.part, spec.number))
        return tuple(keys)
    spec = match_title(catalog, text, part)
    return (ItemKey(spec.part, spec.number),) if spec else ()


def _heading_near(context: DetectionContext, block: int, key: ItemKey) -> tuple[int, bool]:
    """`(Item 시작 블록, 헤딩으로 확인했는지)`.

    앵커 블록이 이 Item의 헤딩이 아니면 뒤로 내려가며 이 Item 번호로 시작하는 블록을 찾는다. 목차 링크가 헤딩이 아니라
    페이지 맨 위(머리말 앞)를 가리키는 공시가 있고, 한 페이지에 Item이 여럿이면(Item 9·9A·9B·9C) 링크 여러 개가 같은
    블록을 가리킨다. 카탈로그상 더 뒤 Item의 헤딩을 지나치면 멈춘다. 못 찾으면 앵커 블록 그대로, 확인 안 됨.
    """
    document, catalog = context.document, context.catalog
    position = catalog.index(key.part, key.number)
    first = block
    # 빈 칸만 있는 표(Workiva 쪽 머리 자리)는 건너뛰고 확인한다.
    while first + 1 < len(document.blocks) and not block_text(document.blocks[first]).strip():
        first += 1
    if first < len(document.blocks) and _is_heading_of(context, first, key):
        return block, True
    for index in range(first, min(first + _MAX_REFINE, len(document.blocks))):
        for text, _ in _rows(document.blocks[index]):
            label = parse_item_label(text)
            if label is None:
                continue
            if _labels_key(context, label, index, key):
                return index, True
            later = [catalog.index(label.part or key.part, number) for number in label.numbers]
            if position is not None and any(other is not None and other > position for other in later):
                return block, False
    return block, False


def _labels_key(context: DetectionContext, label, index: int, key: ItemKey) -> bool:
    """Item 표기가 이 Item이다. Part마다 번호가 다시 시작하는 서식은 Part도 맞아야 한다(Part I Item 4 링크가
    Part II "Item 4." 헤딩을 가리키는 작성 오류)."""
    if key.number not in label.numbers:
        return False
    return not context.catalog.part_scoped or (label.part or context.part_at(index)) == key.part


def _is_heading_of(context: DetectionContext, index: int, key: ItemKey) -> bool:
    """블록이 이 Item 표기나 이 Item 제목으로 시작한다("RISK FACTORS. The following …"처럼 본문이 붙어도)."""
    spec = context.catalog.spec(key.part, key.number)
    titles = [normalize_title(title) for title in spec.titles] if spec else []
    for text, _ in _rows(context.document.blocks[index]):
        label = parse_item_label(text)
        if label is not None and _labels_key(context, label, index, key):
            return True
        normalized = normalize_title(text)
        if any(normalized == title or normalized.startswith(title + " ") for title in titles):
            return True
    return False


def _largest_cluster(entries: list[_Entry]) -> list[_Entry]:
    """블록 거리로 이어진 목차 항목 무리 중 서로 다른 Item이 가장 많은 것."""
    clusters: list[list[_Entry]] = []
    for entry in entries:
        if clusters and entry.block - clusters[-1][-1].block <= _MAX_GAP:
            clusters[-1].append(entry)
        else:
            clusters.append([entry])
    if not clusters:
        return []
    return max(clusters, key=lambda cluster: len({key for entry in cluster for key in entry.keys}))
