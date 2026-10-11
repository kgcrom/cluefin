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

import re
from collections.abc import Sequence
from dataclasses import replace

from cluefin_sec_notes._blocks import Paragraph, Table
from cluefin_sec_notes._catalog import FormCatalog, catalog_for
from cluefin_sec_notes._document import SecDocument, block_text
from cluefin_sec_notes._labels import normalize_title, parse_item_label, parse_part
from cluefin_sec_notes._model import (
    CONFLICTING_CANDIDATE,
    EMPTY_ITEM,
    INFO,
    MISSING_ITEM,
    NON_SEQUENTIAL_LAYOUT,
    OMITTED_ITEM,
    OUT_OF_ORDER,
    Candidate,
    Finding,
    Item,
    ItemExtraction,
    ItemKey,
)
from cluefin_sec_notes._references import REFERENCE_BODY_MAX_CHARS, item_body, resolve_page_references
from cluefin_sec_notes.detectors import DEFAULT_DETECTORS, DetectionContext, Detector

_SIGNATURES = frozenset({"signatures", "signature"})  # 8-K는 단수가 흔하다
# 참조 편입 문구. 본문이 `REFERENCE_BODY_MAX_CHARS` 이하이고 문구가 있으면 Item 내용이 다른 문서(위임장,
# Exhibit 13 연차보고서 등)에 있다는 뜻이다. 같은 문서의 쪽을 가리키면 `resolve_page_references`가 그 쪽을 붙이고
# 참조 편입 표시를 거둔다.
_INCORPORATION = re.compile(
    r"incorporated\s+(?:\w+\s+){0,3}?by\s+reference"
    r"|will\s+be\s+(?:included|set\s+forth|contained|presented)\s+in\s+.{0,120}?proxy\s+statement"
    r"|(?:is|are)\s+(?:included|set\s+forth|contained)\s+(?:in|under)\s+.{0,160}?"
    r"(?:proxy\s+statement|annual\s+report\s+to\s+(?:share|stock)holders)"
    r"|can\s+be\s+found\s+(?:in|under)\s+.{0,160}?(?:proxy\s+statement|annual\s+report\s+to\s+(?:share|stock)holders)",
    re.IGNORECASE | re.DOTALL,
)
# 참조 편입 문구 바로 앞(글자 수)에 이 부정어가 있으면 편입이 아니다.
_NEGATION = re.compile(r"\bnot\b|\bnor\b", re.IGNORECASE)
_NEGATION_WINDOW = 40
# 제목만 있는 줄로 볼 최대 길이(생략 판단에서 "Risk Factors" 같은 헤딩을 찾을 때).
_MAX_TITLE_LINE = 150
# 생략·참조 편입을 말하는 문장. 이 문장에만 나오는 Item은 공시가 생략한 것이다.
_STATED_OMISSION = re.compile(
    r"incorporated\s+(?:\w+\s+){0,3}?by\s+reference|omitted|general\s+instruction|not\s+applicable", re.IGNORECASE
)
_PART_PREFIX = re.compile(r"^part [ivx]+ ?")
# "Part I, Item 4"처럼 Item 언급 바로 앞에 밝힌 Part.
_NAMED_PART = re.compile(r"\bpart\s+(IV|V?I{1,3}|V)\b[\s,.\-—–]*$", re.IGNORECASE)
_NAMED_PART_WINDOW = 15
# 헤딩을 담은 표로 볼 최대 행 수(글자 있는 행). "Item 1." | "Business"처럼 표로 짠 헤딩.
_MAX_HEADING_ROWS = 3
# Item 표기 행이 이만큼 있는 표는 목차다.
_TOC_TABLE_ROWS = 3
# Part 헤딩("PART II", "PART II — OTHER INFORMATION")으로 볼 최대 길이. Item 끝에 붙으면 잘라 낸다.
_PART_HEADING_MAX = 80
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
        context.previous.extend(detection.candidates)

    accepted, resolve_findings = _resolve(candidates, catalog)
    findings.extend(resolve_findings)
    findings.extend(_non_sequential(accepted, catalog))
    items = tuple(_mark_incorporated(item) for item in _build_items(document, catalog, accepted))
    ranged = {key for key, candidate in accepted.items() if candidate.ranges}
    items, reference_findings = resolve_page_references(document, catalog, items, skip=ranged)
    findings.extend(reference_findings)
    findings.extend(_empty_items(document, catalog, items))
    missing = _missing(document, catalog, accepted)
    omitted = _omitted(context, missing)
    if not _is_amendment(document):
        for key in missing:
            if key in context.absent:
                findings.append(
                    Finding(OMITTED_ITEM, f"{key} 본문이 이 문서에 없다({context.absent[key]})", severity=INFO, key=key)
                )
            elif key in omitted:
                findings.append(Finding(OMITTED_ITEM, f"{key} 표기가 문서에 없다", severity=INFO, key=key))
            else:
                findings.append(Finding(MISSING_ITEM, f"{key}을 찾지 못했다(문서에 표기는 있다)", key=key))
    return ItemExtraction(
        document=document,
        catalog=catalog.name,
        items=items,
        missing=missing,
        findings=tuple(findings),
        candidates=tuple(candidates),
        omitted=omitted,
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
                    severity=INFO,
                    key=candidate.key,
                    block=candidate.block,
                    method=candidate.method,
                )
            )
            continue
        accepted[candidate.key] = candidate
    return accepted, findings


def _order_conflict(candidate: Candidate, accepted: dict[ItemKey, Candidate], catalog: FormCatalog) -> Candidate | None:
    """신뢰도가 더 높은 채택 Item 중 카탈로그상 바로 앞·뒤 Item과 위치가 어긋나면 그 Item. 구간을 탐지기가 정한
    Item(교차참조 색인)은 문서 순서와 무관하게 놓이므로 기준으로 삼지 않는다."""
    position = _catalog_index(catalog, candidate.key)
    stronger = [other for other in accepted.values() if other.confidence > candidate.confidence and not other.ranges]
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
    # 결합 헤딩("Items 1 and 2")의 뒤쪽 Item은 앞쪽 Item 자리에 있는 것이 정상이라 빼고 본다. 구간을 탐지기가 정한
    # 후보(교차참조 색인)는 순서와 무관하게 구간이 맞으므로 빼고 본다.
    first_at_block: dict[int, Candidate] = {}
    headed = [candidate for candidate in accepted.values() if not candidate.ranges]
    for candidate in sorted(headed, key=lambda candidate: _catalog_index(catalog, candidate.key)):
        first_at_block.setdefault(candidate.block, candidate)
    ordered = sorted(first_at_block.values(), key=lambda candidate: _catalog_index(catalog, candidate.key))
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
    # 구간이 정해진 후보는 다른 Item의 끝을 자르지 않는다.
    starts = sorted({candidate.block for candidate in ordered if not candidate.ranges})
    last_start = starts[-1] if starts else 0
    end_of_items = _signatures(document, last_start)
    items = []
    for candidate in ordered:
        if candidate.ranges:
            end = candidate.ranges[0][1]
        else:
            later = [start for start in starts if start > candidate.block]
            end = _trim_part_heading(document, candidate.block, later[0] if later else end_of_items)
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
                ranges=candidate.ranges,
            )
        )
    return tuple(items)


def _trim_part_heading(document: SecDocument, start: int, end: int) -> int:
    """구간 끝의 Part 헤딩은 다음 Part의 것이다."""
    while end - 1 > start:
        block = document.blocks[end - 1]
        if not (isinstance(block, Paragraph) and len(block.text) <= _PART_HEADING_MAX and parse_part(block.text)):
            break
        if parse_item_label(block.text) is not None:
            break
        end -= 1
    return end


def _mark_incorporated(item: Item) -> Item:
    body = item_body(item)
    if len(body) <= REFERENCE_BODY_MAX_CHARS and _incorporates(body):
        return replace(item, incorporated_by_reference=True)
    return item


def _incorporates(body: str) -> bool:
    """참조 편입 문구가 있다. "shall not be deemed incorporated by reference"(8-K 2.02·7.01, 10-K 성과 그래프)처럼
    바로 앞에 부정어가 있으면 편입이 아니라 편입하지 말라는 말이다."""
    return any(
        not _NEGATION.search(body, max(0, match.start() - _NEGATION_WINDOW), match.start())
        for match in _INCORPORATION.finditer(body)
    )


def _signatures(document: SecDocument, after: int) -> int:
    """마지막 Item 뒤의 서명란 헤딩 위치. 없으면 문서 끝."""
    for index in range(after + 1, len(document.blocks)):
        block = document.blocks[index]
        if isinstance(block, Paragraph) and normalize_title(block.text) in _SIGNATURES:
            return index
    return len(document.blocks)


def _empty_items(document: SecDocument, catalog: FormCatalog, items: tuple[Item, ...]) -> list[Finding]:
    """제목 블록 하나뿐이고 그 블록에도 제목 말고는 아무것도 없는 Item. "[Reserved]", "None"은 내용으로 본다."""
    findings = []
    for item in items:
        spec = catalog.spec(item.key.part, item.key.number)
        if item.end - item.start > 1 or item.shared_with or spec is None or spec.may_be_incorporated or spec.optional:
            continue
        if item.incorporated_by_reference:
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


def _omitted(context: DetectionContext, missing: tuple[ItemKey, ...]) -> tuple[ItemKey, ...]:
    """공시가 본문이 없다고 밝힌 Item(`context.absent`)과, 목차 밖 어디에도 "Item N" 표기나 그 Item 제목만 있는 줄이
    없는 Item. 목차에만 있으면 본문에서 뺀 것이다. 생략할 수 없는 Item(`ItemSpec.mandatory`)은 빼지 않는다.
    본문 문장에 나오더라도 그 문장이 생략·참조 편입을 말하면("Items 10 through 14 … are incorporated by reference
    pursuant to General Instruction G") 생략이다."""
    if not missing:
        return ()
    document, catalog = context.document, context.catalog
    stated = [key for key in missing if key in context.absent]
    missing = tuple(key for key in missing if key not in context.absent)
    kept_indexes = [
        index
        for index, block in enumerate(document.blocks)
        if not context.is_excluded(index) and not _is_toc_table(block)
    ]
    kept = [document.blocks[index] for index in kept_indexes]
    texts = [block_text(block) for block in kept]
    # 제목 줄은 문단과 헤딩을 담은 작은 표에서만 모은다. 데이터 표 칸의 "Other Information" 행은 헤딩이 아니다.
    lines = {
        normalize_title(line)
        for block in kept
        if _may_hold_heading(block)
        for line in block_text(block).split("\n")
        if len(line) <= _MAX_TITLE_LINE
    } - _part_names(document)
    omitted = []
    for key in missing:
        spec = catalog.spec(key.part, key.number)
        if spec is not None and spec.mandatory:
            continue
        titles = {normalize_title(title) for title in spec.titles} if spec else set()
        # Part마다 번호가 다시 시작하는 서식(10-Q)은 그 Part 구간의 "Item N" 언급만 센다(Part I "Item 3."이 생략한
        # Part II Item 3의 언급이 되지 않게).
        scoped = (
            [text for index, text in zip(kept_indexes, texts, strict=True) if context.part_at(index) == key.part]
            if catalog.part_scoped
            else texts
        )
        if not _mentioned(key, scoped, part_scoped=catalog.part_scoped) and not (titles & lines):
            omitted.append(key)
    return tuple(sorted({*stated, *omitted}, key=lambda key: _catalog_index(catalog, key)))


def _part_names(document: SecDocument) -> set[str]:
    """Part 헤딩의 이름("PART II — OTHER INFORMATION", 줄이나 블록이 나뉜 "PART II" + "OTHER INFORMATION"). 10-Q Part II
    이름은 Part II Item 5 제목과 같아서, 이것을 제목 줄로 보면 생략한 Item 5가 "표기는 있다"로 잡힌다."""
    names = set()
    blocks = document.blocks
    for index, block in enumerate(blocks):
        if not isinstance(block, Paragraph) or len(block.text) > _PART_HEADING_MAX or parse_part(block.text) is None:
            continue
        lines = [line for line in block.text.split("\n") if line.strip()]
        rest = _PART_PREFIX.sub("", normalize_title(lines[0]))
        if not rest and len(lines) > 1:
            rest = normalize_title(lines[1])
        if not rest and index + 1 < len(blocks):
            rest = normalize_title(block_text(blocks[index + 1]).split("\n")[0])
        if rest:
            names.add(rest)
    return names


def _mentioned(key: ItemKey, texts: list[str], *, part_scoped: bool = False) -> bool:
    """ "Item N" 언급이 있다(생략을 밝히는 문장 속 언급은 빼고). Part마다 번호가 다시 시작하는 서식은 다른 Part를
    밝힌 언급("Part I, Item 4 \"Controls and Procedures\"")도 뺀다."""
    mention = re.compile(rf"\bitems?\s*{re.escape(key.number)}(?![\dA-Za-z])", re.IGNORECASE)
    for text in texts:
        if _STATED_OMISSION.search(text):
            continue
        for match in mention.finditer(text):
            named = _NAMED_PART.search(text[max(0, match.start() - _NAMED_PART_WINDOW) : match.start()])
            if not (part_scoped and named and named.group(1).upper() != key.part):
                return True
    return False


def _may_hold_heading(block) -> bool:
    if isinstance(block, Paragraph):
        return True
    return (
        isinstance(block, Table) and sum(1 for row in block.rows if any(cell.text for cell in row)) <= _MAX_HEADING_ROWS
    )


def _is_toc_table(block) -> bool:
    """Item 표기 행이 여럿인 표(링크 없는 목차)."""
    if not isinstance(block, Table):
        return False
    labelled = sum(1 for index in range(len(block.rows)) if parse_item_label(block.row_text(index)) is not None)
    return labelled >= _TOC_TABLE_ROWS


def _is_amendment(document: SecDocument) -> bool:
    return bool(document.form and document.form.endswith("/A"))
