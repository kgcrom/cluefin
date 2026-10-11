"""쪽 번호 표기("pages F-1 through F-30", "4–97, 127–128")를 블록 구간으로 옮긴다.

Item 본문이 같은 문서의 다른 쪽에 있다고만 적은 공시(Item 8 "See pages F-1 through F-30", 연차보고서형
"pages 46–160", 교차참조 색인의 쪽 칸)를 푸는 데 쓴다. 쪽 번호는 `SecDocument.pages`의 `Page.label`(머리말·꼬리말에
찍힌 번호)과 맞춘다.

쪽 목록은 정규식 하나로 반복시키지 않고(중첩 반복은 역추적이 폭발할 수 있다) 범위 하나씩 차례로 읽는다.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass

from cluefin_sec_notes._furniture import Page

# 쪽 번호 하나: "24", "F-3", "F – 3", "II-252", "A1"은 받지 않는다(머리말 쪽 번호와 같은 모양만).
_LABEL = r"(?:[A-Z]{1,3}\s?[-–—]\s?)?\d{1,4}"
_RANGE = re.compile(rf"\s*({_LABEL})(?:\s*(?:[-–—]|through|thru|to)\s*({_LABEL}))?(?![\w-])", re.IGNORECASE)
# 범위 사이: ", ", " and ", ", and ", " & ".
_SEPARATOR = re.compile(r"\s*(?:,\s*(?:and\s+)?|and\s+|&\s*)", re.IGNORECASE)
# 칸 끝의 각주 표시: "*", "**", "(a)", "(1)"
_FOOTNOTE = re.compile(r"\s*(?:\*+|\([a-z0-9]\))", re.IGNORECASE)
_NOT_APPLICABLE = re.compile(r"^\s*(?:not\s+applicable|none|n/?a|—|–|-)\s*\.?\s*$", re.IGNORECASE)
_DASHES = re.compile(r"[–—]")


@dataclass(frozen=True)
class PageList:
    """쪽 목록 표기 하나를 읽은 결과.

    Attributes:
        spans: `(첫 쪽, 끝 쪽)` 번호 쌍(정규화한 라벨). 쪽 하나면 둘이 같다.
        footnote: 각주 표시("*", "(a)")가 붙었다(교차참조 색인에서 위임장 참조 편입을 뜻한다).
        not_applicable: "Not Applicable", "None".
    """

    spans: tuple[tuple[str, str], ...] = ()
    footnote: bool = False
    not_applicable: bool = False


def normalize_label(label: str) -> str:
    """ "F – 3" → "F-3", "f-3" → "F-3"."""
    return _DASHES.sub("-", re.sub(r"\s+", "", label)).upper()


def read_spans(text: str, position: int = 0) -> tuple[tuple[tuple[str, str], ...], int]:
    """`position`부터 "F-1 through F-30", "4–97, 127–128 and 200"을 읽는다. `(쪽 쌍들, 끝 위치)`."""
    spans: list[tuple[str, str]] = []
    while True:
        match = _RANGE.match(text, position)
        if match is None:
            break
        first = normalize_label(match.group(1))
        spans.append((first, normalize_label(match.group(2)) if match.group(2) else first))
        position = match.end()
        separator = _SEPARATOR.match(text, position)
        if separator is None or _RANGE.match(text, separator.end()) is None:
            break
        position = separator.end()
    return tuple(spans), position


def parse_page_list(text: str) -> PageList | None:
    """칸 하나 전체가 쪽 목록이면 읽는다("2, 4–97,\\n127–128", "201, 203–205 *", "(b)", "Not Applicable").
    쪽 목록이 아닌 글자가 남으면 None."""
    if _NOT_APPLICABLE.match(text):
        return PageList(not_applicable=True)
    spans, position = read_spans(text)
    footnote = False
    while position < len(text):
        separator = _SEPARATOR.match(text, position)
        if separator is not None and separator.end() > position:
            position = separator.end()
            continue
        match = _FOOTNOTE.match(text, position)
        if match is None:
            break
        footnote = True
        position = match.end()
    if text[position:].strip() or not (spans or footnote):
        return None
    return PageList(spans=spans, footnote=footnote)


class PageIndex:
    """쪽 번호 → 블록 구간. 같은 번호가 두 쪽 이상에 찍혔으면 그 번호는 풀지 않는다(어느 쪽인지 모른다)."""

    def __init__(self, pages: Sequence[Page]):
        self._pages = tuple(pages)
        self._positions: dict[str, list[int]] = {}
        for position, page in enumerate(self._pages):
            if page.label:
                self._positions.setdefault(normalize_label(page.label), []).append(position)

    def position(self, label: str) -> int | None:
        positions = self._positions.get(normalize_label(label), [])
        return positions[0] if len(positions) == 1 else None

    def is_ambiguous(self, label: str) -> bool:
        return len(self._positions.get(normalize_label(label), [])) > 1

    def ranges(self, spans: Sequence[tuple[str, str]]) -> tuple[tuple[tuple[int, int], ...], tuple[str, ...]]:
        """쪽 쌍들을 블록 구간들로. `(구간들, 못 푼 쪽 쌍 표기)`. 이어지거나 겹치는 구간은 합친다."""
        found: list[tuple[int, int]] = []
        unresolved: list[str] = []
        for first, last in spans:
            start, end = self.position(first), self.position(last)
            if start is None or end is None or end < start:
                unresolved.append(first if first == last else f"{first}–{last}")
                continue
            found.append((self._pages[start].start, self._pages[end].end))
        return _merge(found), tuple(unresolved)

    def lettered_section(self, prefix: str) -> tuple[int, int] | None:
        """ "F-1"(없으면 첫 "F-" 쪽)부터 "F-" 쪽이 끊기지 않고 이어지는 데까지의 블록 구간. 사이의 번호 없는 쪽은
        덮고, 다른 번호가 찍힌 쪽에서 끝난다."""
        prefix = prefix.upper() + "-"
        lettered = [
            position
            for position, page in enumerate(self._pages)
            if page.label and normalize_label(page.label).startswith(prefix)
        ]
        if not lettered:
            return None
        first = self.position(prefix + "1")
        start = first if first is not None else lettered[0]
        end = start
        for position in range(start + 1, len(self._pages)):
            label = self._pages[position].label
            if label is None:
                continue
            if not normalize_label(label).startswith(prefix):
                break
            end = position
        return self._pages[start].start, self._pages[end].end


def _merge(ranges: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1] + 1:  # 사이가 쪽 경계(PageBreak) 하나뿐이면 잇는다
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return tuple(merged)
