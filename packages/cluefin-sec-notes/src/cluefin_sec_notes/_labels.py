"""Item 표기 읽기: "Item 1A. Risk Factors", "Items 1 and 2.", "PART II — Item 7", 번호 없는 제목."""

from __future__ import annotations

import re
from dataclasses import dataclass

from cluefin_sec_notes._catalog import FormCatalog, ItemSpec

_ROMAN = r"(?:IV|V?I{1,3}|V)"
# 줄 맨 앞의 "Part II", "PART II." 등. Item 표기 앞에 붙어 오기도 한다("Part II, Item 7").
_PART = re.compile(rf"^\s*part\s+({_ROMAN})\b[\s.,:;—–-]*", re.IGNORECASE)
# "Item 1A.", "ITEM 7A:", "Items 1 and 2.", "Items 10, 11, 12, 13 and 14", "Item 2.02", "Item 9A(T)"
_NUMBER = r"\d{1,2}[A-D]?(?:\.\d{2})?(?:\(T\))?"
_ITEM = re.compile(
    rf"^\s*items?\s*({_NUMBER}(?:(?:\s*(?:,|and|&|through|to))+\s*(?:items?\s*)?{_NUMBER})*)(?![\w])[\s.,:;—–-]*",
    re.IGNORECASE,
)
_ITEM_NUMBER = re.compile(_NUMBER, re.IGNORECASE)
_RANGE = re.compile(r"(\d{1,2})\s*(?:through|to)\s*(\d{1,2})$", re.IGNORECASE)
_MAX_RANGE = 10
# 목차 행에서 제목 뒤에 오는 페이지 표기("5", "II-253", "Pages 10 to 12"), 정규화 후 모양.
_PAGE_REFERENCE = re.compile(r"(?:pages? )?(?:[ivx]+ )?\d+(?: (?:and|to|through) (?:[ivx]+ )?\d+)?")
_NON_WORD = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class ItemLabel:
    """Item 표기 하나를 읽은 결과.

    Attributes:
        part: 앞에 붙은 Part(`II`). 없으면 None.
        numbers: Item 번호들(대문자). 결합 표기("Items 1 and 2")면 여러 개.
        rest: 번호 뒤의 나머지(보통 제목).
    """

    part: str | None
    numbers: tuple[str, ...]
    rest: str


def parse_item_label(text: str) -> ItemLabel | None:
    """문자열 맨 앞이 Item 표기면 읽는다. 아니면 None. 문장 중간의 "see Item 7"은 읽지 않는다."""
    part = None
    match = _PART.match(text)
    if match:
        part = match.group(1).upper()
        text = text[match.end() :]
    match = _ITEM.match(text)
    if match is None:
        return None
    return ItemLabel(part=part, numbers=_numbers(match.group(1)), rest=text[match.end() :].strip())


def parse_part(text: str) -> str | None:
    """Part 표기("PART II", "Part II — Other Information")로 시작하면 그 Part."""
    match = _PART.match(text)
    return match.group(1).upper() if match else None


def _numbers(text: str) -> tuple[str, ...]:
    numbers = [number.upper().replace("(T)", "") for number in _ITEM_NUMBER.findall(text)]
    range_match = _RANGE.search(text)
    if range_match:  # "Items 10 through 14"
        first, last = int(range_match.group(1)), int(range_match.group(2))
        if 0 < last - first <= _MAX_RANGE:
            numbers = numbers[:-2] + [str(number) for number in range(first, last + 1)]
    return tuple(dict.fromkeys(numbers))


def normalize_title(text: str) -> str:
    """제목 비교용: 소문자, 영숫자 외 전부 공백 하나로. "Management’s" → "management s"."""
    return _NON_WORD.sub(" ", text.lower().replace("’", "'")).strip()


def match_title(catalog: FormCatalog, text: str, part: str | None = None) -> ItemSpec | None:
    """번호 없이 제목만 있는 표기를 카탈로그 Item으로. 가장 긴 제목이 앞부분과 맞는 것."""
    normalized = normalize_title(text)
    if not normalized:
        return None
    best: tuple[int, ItemSpec] | None = None
    for spec in catalog.items:
        if part is not None and catalog.part_scoped and spec.part != part:
            continue
        for title in spec.titles:
            candidate = normalize_title(title)
            if _is_title_with_page(normalized, candidate) and (best is None or len(candidate) > best[0]):
                best = (len(candidate), spec)
    return best[1] if best else None


def _is_title_with_page(normalized: str, title: str) -> bool:
    """제목과 같거나, 제목 뒤에 페이지 표기만 붙었다. "Business Overview"는 "Business"가 아니다."""
    if not normalized.startswith(title):
        return False
    rest = normalized[len(title) :]
    return not rest or (rest.startswith(" ") and _PAGE_REFERENCE.fullmatch(rest.strip()) is not None)
