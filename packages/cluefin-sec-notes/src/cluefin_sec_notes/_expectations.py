"""코퍼스 기대값 검사(통합 테스트와 `scripts/corpus_report.py`가 같이 쓴다).

manifest 항목의 기대값 필드:

- `items`: `{"1A": {"starts_with": "Item 1A. Risk Factors", "chars": 73082}}` — 사람이 경계를 확인한 핵심 Item.
  추출한 Item 텍스트가 `starts_with`로 시작하고 길이가 `chars`의 ±`CHAR_TOLERANCE` 안이어야 한다.
  정확한 길이를 아직 모르면(교차참조형처럼 지금 틀리는 Item) `min_chars`·`max_chars`로 범위만 적는다.
  `incorporated`: 참조 편입(`Item.incorporated_by_reference`) 여부.
- `present`: `["1B", "2", …]` — 있기만 하면 되는 Item.
- `known_bad`: `{"7": "이유"}` — 지금은 틀리는 것으로 알려진 Item. 틀리면 통과, **맞으면** `fixed`로 실패시킨다
  (개선을 manifest에 반영하라는 신호). 반대로 기대값이 틀리면 `failed`(회귀).

Item 키는 10-K는 번호(`"1A"`), Part마다 번호가 다시 시작하는 서식은 `"II:1A"`.
"""

from __future__ import annotations

from dataclasses import dataclass

from cluefin_sec_notes._model import Item, ItemExtraction

CHAR_TOLERANCE = 0.10

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
    incorporated = expectation.get("incorporated")
    if incorporated is not None and item.incorporated_by_reference != incorporated:
        return f"참조 편입 {item.incorporated_by_reference} (기대 {incorporated})"
    return ""
