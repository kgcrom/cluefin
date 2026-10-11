"""Item 표기 읽기: "Item 1A. Risk Factors", "Items 1 and 2.", "PART II — Item 7", 번호 없는 제목."""

from __future__ import annotations

import re
from dataclasses import dataclass

from cluefin_sec_notes._catalog import FormCatalog, ItemSpec

_ROMAN = r"(?:IV|V?I{1,3}|V)"
# 줄 맨 앞의 "Part II", "PART II." 등. Item 표기 앞에 붙어 오기도 한다("Part II, Item 7").
_PART = re.compile(rf"^\s*part\s+({_ROMAN})\b[\s.,:;—–-]*", re.IGNORECASE)
# "Item 1A.", "ITEM 7A:", "Items 1 and 2.", "ITEMS 1. AND 2.", "Items 10, 11, 12, 13 and 14", "Item 2.02", "Item 9A(T)"
# 결합 표기는 정규식 하나로 반복시키지 않고(중첩 반복은 역추적이 폭발할 수 있다) 번호와 구분자를 차례로 읽는다.
_NUMBER = r"\d{1,2}[A-D]?(?:\.\d{2})?(?:\(T\))?"
_ITEM_PREFIX = re.compile(r"\s*items?\s*", re.IGNORECASE)
_ITEM_NUMBER = re.compile(_NUMBER, re.IGNORECASE)
# 번호 사이: ", ", " and ", ". AND ", ", and ", " & ", " through ", " to ". 뒤에 "Item"이 다시 붙기도 한다.
_SEPARATOR = re.compile(r"\.?\s*(?:,\s*(?:and\s+|&\s*)?|and\s+|&\s*|(through|to)\s+)(?:items?\s*)?", re.IGNORECASE)
_LABEL_END = re.compile(r"[\s.,:;—–-]*")
_MAX_RANGE = 10
# 목차 행에서 제목 뒤에 오는 칸의 토큰(정규화 후). Part·Item 번호·페이지("I 1 5", "1A 13", "ii 253", "pages 10 to 12").
_TOC_TAIL_TOKEN = re.compile(r"[ivx]+|\d+[a-d]?|pages?|part|item|and|to|through")
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
    prefix = _ITEM_PREFIX.match(text)
    if prefix is None:
        return None
    numbers, position = _read_numbers(text, prefix.end())
    if not numbers or (position < len(text) and (text[position].isalnum() or text[position] == "_")):
        return None
    position = _LABEL_END.match(text, position).end()
    return ItemLabel(part=part, numbers=numbers, rest=text[position:].strip())


def parse_part(text: str) -> str | None:
    """Part 표기("PART II", "Part II — Other Information")로 시작하면 그 Part."""
    match = _PART.match(text)
    return match.group(1).upper() if match else None


def _read_numbers(text: str, position: int) -> tuple[tuple[str, ...], int]:
    """`position`부터 "1A", "1 and 2", "10, 11 and 12", "10 through 14"를 읽는다. `(번호들, 끝 위치)`."""
    numbers: list[str] = []
    pending_range = False
    while True:
        match = _ITEM_NUMBER.match(text, position)
        if match is None:
            break
        number = match.group(0).upper().replace("(T)", "")
        if pending_range and numbers[-1].isdigit() and number.isdigit():
            first, last = int(numbers[-1]), int(number)
            if 0 < last - first <= _MAX_RANGE:
                numbers.extend(str(value) for value in range(first + 1, last))
        numbers.append(number)
        position = match.end()
        separator = _SEPARATOR.match(text, position)
        if separator is None or _ITEM_NUMBER.match(text, separator.end()) is None:
            break
        pending_range = separator.group(1) is not None
        position = separator.end()
    return tuple(dict.fromkeys(numbers)), position


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
    """제목과 같거나, 제목 뒤에 Part·Item 번호·페이지 칸만 붙었다. "Business Overview"는 "Business"가 아니다."""
    if not normalized.startswith(title):
        return False
    rest = normalized[len(title) :]
    if rest and not rest.startswith(" "):
        return False
    return all(_TOC_TAIL_TOKEN.fullmatch(token) for token in rest.split())
