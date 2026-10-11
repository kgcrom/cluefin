"""코퍼스 기대값 검사(통합 테스트와 `scripts/corpus_report.py`가 같이 쓴다).

manifest 항목의 기대값 필드:

- `items`: `{"1A": {"starts_with": "Item 1A. Risk Factors", "chars": 73082}}` — 사람이 경계를 확인한 핵심 Item.
  추출한 Item 텍스트가 `starts_with`로 시작하고 길이가 `chars`의 ±`CHAR_TOLERANCE` 안이어야 한다.
  정확한 길이를 아직 모르면(교차참조형처럼 지금 틀리는 Item) `min_chars`·`max_chars`로 범위만 적는다.
  `incorporated`: 참조 편입(`Item.incorporated_by_reference`) 여부. `excludes`: 들어 있으면 안 되는 문자열
  (다음 Item 헤딩이 섞이지 않았는지).
- `present`: `["1B", "2", …]` — 있기만 하면 되는 Item.
- `known_bad`: `{"7": "이유"}` — 지금은 틀리는 것으로 알려진 Item. 틀리면 통과, **맞으면** `fixed`로 실패시킨다
  (개선을 manifest에 반영하라는 신호. `scripts/draft_expectations.py --accept`로 반영한다). 반대로 기대값이 틀리면
  `failed`(회귀).

Item 키는 10-K는 번호(`"1A"`), Part마다 번호가 다시 시작하는 서식은 `"II:1A"`.

스모크 코퍼스는 사람이 본 기대값 대신 자동 불변식(`invariant_violations`)만 본다. manifest의 `baseline`에
지금 위반 목록을 적어 두고, 새 위반이 생기면 회귀, 사라지면 개선으로 알린다.
"""

from __future__ import annotations

from dataclasses import dataclass

from cluefin_sec_notes._blocks import Table
from cluefin_sec_notes._model import MISSING_ITEM, Item, ItemExtraction

CHAR_TOLERANCE = 0.10
# 수락할 때 `starts_with`로 적는 헤딩 길이와, 새로 쓰는 기대값 필드.
_STARTS_WITH_CHARS = 60
_LENGTH_FIELDS = frozenset({"starts_with", "chars", "min_chars", "max_chars"})
# 스모크 불변식: Item 1A가 이보다 짧으면(참조 편입이 아니면) 경계를 의심한다. 소규모 보고회사는 "해당 없음" 한 줄이라 뺀다.
MIN_RISK_FACTORS_CHARS = 1000
_SMALLER_REPORTING = ("smaller reporting compan", "not required", "not applicable")

OK = "ok"
FAILED = "failed"
KNOWN_BAD = "known_bad"
FIXED = "fixed"


@dataclass(frozen=True)
class ItemCheck:
    key: str
    status: str
    detail: str = ""


def item_by_key(extraction: ItemExtraction, key: str) -> Item | None:
    part, _, number = key.rpartition(":")
    return extraction.item(number, part or None)


def check_expectations(extraction: ItemExtraction, entry: dict) -> list[ItemCheck]:
    known_bad: dict[str, str] = entry.get("known_bad", {})
    checks = []
    expected: dict[str, dict] = {key: dict(value) for key, value in entry.get("items", {}).items()}
    for key in entry.get("present", ()):
        expected.setdefault(key, {})
    for key in list(known_bad):
        expected.setdefault(key, {})
    for key, expectation in expected.items():
        problem = _problem(item_by_key(extraction, key), expectation)
        if key in known_bad:
            status = KNOWN_BAD if problem else FIXED
            checks.append(ItemCheck(key, status, problem or f"known_bad가 고쳐졌다: {known_bad[key]}"))
        else:
            checks.append(ItemCheck(key, FAILED if problem else OK, problem))
    return checks


def accept_items(extraction: ItemExtraction, entry: dict, keys: list[str]) -> list[str]:
    """지금 추출 결과를 `keys` Item의 기대값으로 쓰고 `known_bad`·`present`에서 뺀다(고쳐진 known_bad 반영).

    길이·시작 기대값(`starts_with`·`chars`·`min_chars`·`max_chars`)은 새로 쓰고 `excludes`·`incorporated`는 남긴다.
    추출 결과에 없는 Item은 건너뛰고 그 키를 돌려준다.
    """
    items: dict[str, dict] = entry.setdefault("items", {})
    known_bad: dict[str, str] = entry.get("known_bad", {})
    skipped = []
    for key in keys:
        item = item_by_key(extraction, key)
        if item is None:
            skipped.append(key)
            continue
        kept = {name: value for name, value in items.get(key, {}).items() if name not in _LENGTH_FIELDS}
        items[key] = {"starts_with": item.heading[:_STARTS_WITH_CHARS], "chars": len(item.text), **kept}
        known_bad.pop(key, None)
        if key in entry.get("present", ()):
            entry["present"].remove(key)
    if "known_bad" in entry and not known_bad:
        del entry["known_bad"]
    return skipped


def _problem(item: Item | None, expectation: dict) -> str:
    if item is None:
        return "없음"
    starts_with = expectation.get("starts_with")
    text = item.text
    if starts_with and not text.startswith(starts_with):
        return f"시작이 다름: {text[: len(starts_with) + 20]!r}"
    chars = expectation.get("chars")
    if chars and abs(len(text) - chars) > chars * CHAR_TOLERANCE:
        return f"길이 {len(text)} (기대 {chars})"
    if len(text) < expectation.get("min_chars", 0):
        return f"길이 {len(text)} (최소 {expectation['min_chars']})"
    if "max_chars" in expectation and len(text) > expectation["max_chars"]:
        return f"길이 {len(text)} (최대 {expectation['max_chars']})"
    excluded = expectation.get("excludes")
    if excluded and excluded in text:
        return f"들어 있으면 안 되는 {excluded!r}가 있다"
    incorporated = expectation.get("incorporated")
    if incorporated is not None and item.incorporated_by_reference != incorporated:
        return f"참조 편입 {item.incorporated_by_reference} (기대 {incorporated})"
    return ""


def invariant_violations(extraction: ItemExtraction, *, part_scoped: bool = False) -> list[str]:
    """기대값 없이 볼 수 있는 이상: 필수 Item 누락, 경고 코드, 너무 짧은 1A, 표 없는 Item 8."""
    violations = set()
    for key in extraction.missing:
        if key not in extraction.omitted:
            violations.add(f"missing:{key.part}:{key.number}" if part_scoped else f"missing:{key.number}")
    for finding in extraction.warnings:
        if finding.code != MISSING_ITEM:
            violations.add(f"warning:{finding.code}")
    risk = extraction.item("1A")
    if (
        risk is not None
        and not risk.incorporated_by_reference
        and len(risk.text) < MIN_RISK_FACTORS_CHARS
        and not any(phrase in risk.text.lower() for phrase in _SMALLER_REPORTING)
    ):
        violations.add("short:1A")
    statements = extraction.item("8")
    if (
        statements is not None
        and not statements.incorporated_by_reference
        and not any(isinstance(block, Table) for block in statements.blocks)
    ):
        violations.add("no_table:8")
    return sorted(violations)
