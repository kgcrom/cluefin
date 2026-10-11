"""탐지기 후보를 모아 Item 구간을 정한다.

1. 탐지기를 순서대로 돌려 후보를 모은다(앞 탐지기가 `DetectionContext`에 남긴 것을 뒤 탐지기가 쓴다).
2. 신뢰도 높은 후보부터 채택한다. 후보는 자기보다 신뢰도가 높은 탐지기가 정한 Item 중 카탈로그상 바로 앞·뒤
   Item 사이에 있어야 한다. 아니면 버리고 `out_of_order`로 남긴다. 그래서 목차 앵커로 정한 경계를 정규식 후보가
   덮지 못하고, 목차에 없던 Item(1C 등)만 빈자리에 들어간다. 같은 신뢰도끼리는 순서를 따지지 않는다. 연차보고서
   형식 10-K는 Item이 카탈로그 순서와 다르게 놓이는 것이 정상이고(1B~5가 뒤쪽 "기타 정보"에), 그때는
   `non_sequential_layout`으로 알린다.
3. 채택한 시작 위치를 문서 순서로 늘어놓아 다음 Item 시작 직전까지를 구간으로 한다. 마지막 Item은 서명란
   ("SIGNATURES") 앞에서 끝난다.
4. 카탈로그상 있어야 하는데 못 찾은 Item을 `missing`과 `missing_item`으로 알린다.
"""

from __future__ import annotations

from collections.abc import Sequence

from cluefin_sec_notes._blocks import Paragraph
from cluefin_sec_notes._catalog import FormCatalog, catalog_for
from cluefin_sec_notes._document import SecDocument
from cluefin_sec_notes._labels import normalize_title, parse_item_label
from cluefin_sec_notes._model import (
    CONFLICTING_CANDIDATE,
    EMPTY_ITEM,
    INFO,
    MISSING_ITEM,
    NON_SEQUENTIAL_LAYOUT,
    OUT_OF_ORDER,
    Candidate,
    Finding,
    Item,
    ItemExtraction,
    ItemKey,
)
from cluefin_sec_notes.detectors import DEFAULT_DETECTORS, DetectionContext, Detector

_SIGNATURES = "signatures"
# 제목 자리에 이것만 있으면 빈 Item이 아니라 "해당 없음"을 적은 것이다(Item 6 "[Reserved]" 등).
_PLACEHOLDERS = frozenset({"reserved", "removed and reserved", "none", "not applicable"})


def extract_items(
    document: SecDocument,
    *,
    detectors: Sequence[Detector] = DEFAULT_DETECTORS,
    catalog: FormCatalog | None = None,
) -> ItemExtraction:
    """공시 주 문서에서 Item 구간을 찾는다.

    Args:
        document: `load_filing`/`parse_filing` 결과.
        detectors: 탐지기 목록. 기본값은 목차 앵커 → 정규식 캐스케이드.
        catalog: Item 카탈로그. 없으면 `document.form`으로 고른다.

    Raises:
        ValueError: 서식을 모르거나 지원하지 않는다.
    """
    catalog = catalog or catalog_for(document.form)
    if catalog is None:
        raise ValueError(f"지원하지 않는 서식입니다: {document.form!r} (load_filing(form=…)으로 알려 줄 수 있다)")
    context = DetectionContext(document=document, catalog=catalog)
    candidates: list[Candidate] = []
    findings: list[Finding] = []
    for detector in detectors:
        detection = detector.detect(context)
        candidates.extend(detection.candidates)
        findings.extend(detection.findings)

    accepted, resolve_findings = _resolve(candidates, catalog)
    findings.extend(resolve_findings)
    findings.extend(_non_sequential(accepted, catalog))
    items = _build_items(document, catalog, accepted)
    findings.extend(_empty_items(document, catalog, items))
    missing = _missing(document, catalog, accepted)
    findings.extend(
        Finding(MISSING_ITEM, f"{key}을 찾지 못했다", key=key) for key in missing if not _is_amendment(document)
    )
    return ItemExtraction(
        document=document,
        catalog=catalog.name,
        items=items,
        missing=missing,
        findings=tuple(findings),
        candidates=tuple(candidates),
    )


def _resolve(candidates: list[Candidate], catalog: FormCatalog) -> tuple[dict[ItemKey, Candidate], list[Finding]]:
    accepted: dict[ItemKey, Candidate] = {}
    findings: list[Finding] = []
    # 신뢰도 높은 순, 같으면 문서 앞쪽 먼저. sorted는 안정 정렬이라 탐지기 순서도 유지된다.
    for candidate in sorted(candidates, key=lambda candidate: (-candidate.confidence, candidate.block)):
        current = accepted.get(candidate.key)
        if current is not None:
            if current.block != candidate.block and current.method != candidate.method:
                findings.append(
                    Finding(
                        CONFLICTING_CANDIDATE,
                        f"{candidate.key}: {current.method}는 블록 {current.block}, {candidate.method}는 블록 {candidate.block}",
                        severity=INFO,
                        key=candidate.key,
                        block=candidate.block,
                        method=candidate.method,
                    )
                )
            continue
        conflict = _order_conflict(candidate, accepted, catalog)
        if conflict is not None:
            findings.append(
                Finding(
                    OUT_OF_ORDER,
                    f"{candidate.key}(블록 {candidate.block})가 {conflict.key}(블록 {conflict.block})와 순서가 어긋난다",
                    key=candidate.key,
                    block=candidate.block,
                    method=candidate.method,
                )
            )
            continue
        accepted[candidate.key] = candidate
    return accepted, findings


def _order_conflict(candidate: Candidate, accepted: dict[ItemKey, Candidate], catalog: FormCatalog) -> Candidate | None:
    """신뢰도가 더 높은 채택 Item 중 카탈로그상 바로 앞·뒤 Item과 위치가 어긋나면 그 Item."""
    position = _catalog_index(catalog, candidate.key)
    stronger = [other for other in accepted.values() if other.confidence > candidate.confidence]
    before = [other for other in stronger if _catalog_index(catalog, other.key) < position]
    after = [other for other in stronger if _catalog_index(catalog, other.key) > position]
    previous = max(before, key=lambda other: _catalog_index(catalog, other.key), default=None)
    following = min(after, key=lambda other: _catalog_index(catalog, other.key), default=None)
    if previous is not None and previous.block > candidate.block:
        return previous
    if following is not None and following.block < candidate.block:
        return following
    return None


def _non_sequential(accepted: dict[ItemKey, Candidate], catalog: FormCatalog) -> list[Finding]:
    ordered = sorted(accepted.values(), key=lambda candidate: _catalog_index(catalog, candidate.key))
    for previous, current in zip(ordered, ordered[1:], strict=False):
        if current.block < previous.block:
            return [
                Finding(
                    NON_SEQUENTIAL_LAYOUT,
                    f"{current.key}(블록 {current.block})가 {previous.key}(블록 {previous.block})보다 앞에 있다. "
                    "Item이 카탈로그 순서대로 놓이지 않은 공시라 구간이 다른 Item 중간에서 끊겼을 수 있다",
                    key=current.key,
                    block=current.block,
                )
            ]
    return []


def _catalog_index(catalog: FormCatalog, key: ItemKey) -> int:
    index = catalog.index(key.part, key.number)
    return len(catalog.items) if index is None else index


def _build_items(document: SecDocument, catalog: FormCatalog, accepted: dict[ItemKey, Candidate]) -> tuple[Item, ...]:
    ordered = sorted(accepted.values(), key=lambda candidate: (candidate.block, _catalog_index(catalog, candidate.key)))
    starts = sorted({candidate.block for candidate in ordered})
    last_start = starts[-1] if starts else 0
    end_of_items = _signatures(document, last_start)
    items = []
    for candidate in ordered:
        later = [start for start in starts if start > candidate.block]
        end = later[0] if later else end_of_items
        spec = catalog.spec(candidate.key.part, candidate.key.number)
        shared = tuple(other.key for other in ordered if other.block == candidate.block and other.key != candidate.key)
        items.append(
            Item(
                key=candidate.key,
                title=spec.title if spec else "",
                start=candidate.block,
                end=end,
                method=candidate.method,
                confidence=candidate.confidence,
                document=document,
                evidence=candidate.evidence,
                shared_with=shared,
            )
        )
    return tuple(items)


def _signatures(document: SecDocument, after: int) -> int:
    """마지막 Item 뒤의 서명란 헤딩 위치. 없으면 문서 끝."""
    for index in range(after + 1, len(document.blocks)):
        block = document.blocks[index]
        if isinstance(block, Paragraph) and normalize_title(block.text) == _SIGNATURES:
            return index
    return len(document.blocks)


def _empty_items(document: SecDocument, catalog: FormCatalog, items: tuple[Item, ...]) -> list[Finding]:
    """제목 블록 하나뿐이고 그 블록에도 제목 말고는 아무것도 없는 Item. "[Reserved]", "None"은 내용으로 본다."""
    findings = []
    for item in items:
        spec = catalog.spec(item.key.part, item.key.number)
        if item.end - item.start > 1 or item.shared_with or spec is None or spec.may_be_incorporated:
            continue
        label = parse_item_label(item.heading)
        rest = normalize_title(label.rest if label else item.heading)
        titles = {normalize_title(title) for title in spec.titles}
        if (not rest or rest in titles) and rest not in _PLACEHOLDERS:
            findings.append(Finding(EMPTY_ITEM, f"{item.key} 본문이 없다", key=item.key, block=item.start))
    return findings


def _missing(document: SecDocument, catalog: FormCatalog, accepted: dict[ItemKey, Candidate]) -> tuple[ItemKey, ...]:
    return tuple(
        ItemKey(spec.part, spec.number)
        for spec in catalog.items
        if not spec.optional
        and spec.applies_to(document.period_end)
        and ItemKey(spec.part, spec.number) not in accepted
    )


def _is_amendment(document: SecDocument) -> bool:
    return bool(document.form and document.form.endswith("/A"))
