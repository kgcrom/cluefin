"""쪽 머리말·꼬리말("Example Corp. | 2025 Form 10-K | 4", "Table of Contents", "II-252")을 본문에서 뺀다.

Item 본문 중간과 끝에 끼어드는 것을 막는다. 판단 근거는 두 가지다.

- 쪽 번호만 있는 블록이 쪽 맨 위·맨 아래에 있다.
- 쪽 맨 위·맨 아래의 짧은 블록이 여러 쪽에서 반복된다. 마침표로 끝나는 문장("None.", "Not applicable.")은
  쪽 끝에 여러 번 와도 본문이라 제외한다. 숫자(쪽 번호)는 지우고 비교하지만, Item·Part 표기는
  글자 그대로 비교한다. 쪽마다 새 Item이 시작하는 공시의 "Item 9." 같은 진짜 헤딩을 머리말로 오인하지 않게.

지운 블록은 `page_furniture`로 기록하고, 꼬리말(없으면 머리말)의 쪽 번호는 `Page.label`로 남긴다(교차참조 색인의
쪽 번호를 블록 구간으로 옮길 때 쓴다).
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from cluefin_sec_notes._blocks import Block, PageBreak, Paragraph, Table
from cluefin_sec_notes._labels import parse_item_label, parse_part
from cluefin_sec_notes._report import PAGE_FURNITURE, ReportCollector

# 쪽 가장자리에서 살펴볼 블록 수와 머리말·꼬리말로 볼 최대 길이.
_EDGE_BLOCKS = 3
_MAX_LENGTH = 120
# 이만큼의 쪽(최소 3쪽, 전체의 5%)에서 반복돼야 머리말·꼬리말이다.
_MIN_REPEATS = 3
_MIN_REPEAT_SHARE = 0.05
# "24", "II-252", "F-3", "(14)", "- 5 -", "Page 12", "PAGE 12", "A-1"
_PAGE_NUMBER = re.compile(r"^(?:page\s+)?[-–(]?\s*(?:[A-Z]{1,3}\s?[-–]\s?)?\d{1,4}\s*[-–)]?$", re.IGNORECASE)
# 비교용으로 숫자를 지울 때: 쪽 번호·연도. "Form 10-K"의 10은 남긴다.
_PAGE_NUMBER_IN_TEXT = re.compile(r"(?<![\w.,$])(?:[A-Z]{1,3}[-–])?\d{1,4}(?![\w.,%]|[-–][A-Za-z])")
# 머리말·꼬리말 끝(없으면 앞)의 쪽 번호: "… Form 10-K | 4", "5 December 2025 Form 10-K", "(14)"
_TRAILING_PAGE = re.compile(r"(?:^|[\s|])\(?((?:[A-Z]{1,3}\s?[-–]\s?)?\d{1,4})\)?$")
_LEADING_PAGE = re.compile(r"^\(?((?:[A-Z]{1,3}\s?[-–]\s?)?\d{1,4})\)?(?:\s|$)")


@dataclass(frozen=True)
class Page:
    """쪽 하나. `start`·`end`는 `SecDocument.blocks` 구간 `[start, end)`(쪽 끝 PageBreak 제외).

    Attributes:
        label: 머리말·꼬리말에 찍힌 쪽 번호("24", "II-252", "F-3"). 없으면 None.
    """

    start: int
    end: int
    label: str | None = None


def remove_page_furniture(blocks: list[Block], collector: ReportCollector) -> tuple[list[Block], list[int], list[Page]]:
    """`(남은 블록, 원래 위치 → 남은 블록 위치, 쪽 목록)`. 지운 블록의 위치는 그다음 남은 블록을 가리킨다."""
    pages = _pages(blocks)
    counts = Counter(key for page in pages for index in _edges(page) if (key := _repeat_key(blocks[index])))
    min_repeats = max(_MIN_REPEATS, math.ceil(len(pages) * _MIN_REPEAT_SHARE))
    removed: set[int] = set()
    labels: list[str | None] = []
    for page in pages:
        footer = _edge_furniture(blocks, list(reversed(page)), counts, min_repeats)
        header = _edge_furniture(blocks, page, counts, min_repeats)
        removed.update(footer, header)
        labels.append(
            next((number for index in footer + header if (number := _page_number(_text(blocks[index])))), None)
        )

    kept: list[Block] = []
    mapping: list[int] = []
    for index, block in enumerate(blocks):
        if index in removed:
            collector.add(PAGE_FURNITURE, getattr(block, "line", 0), getattr(block, "column", 0), _text(block))
            mapping.append(-1)
            continue
        mapping.append(len(kept))
        kept.append(block)
    mapping.append(len(kept))
    # 지운 블록은 그다음 남은 블록으로(앵커가 지운 머리말에 붙어 있던 경우).
    for index in range(len(mapping) - 2, -1, -1):
        if mapping[index] == -1:
            mapping[index] = mapping[index + 1]
    kept_pages = [
        Page(start=mapping[page[0]], end=mapping[page[-1] + 1], label=label)
        for page, label in zip(pages, labels, strict=True)
    ]
    return kept, mapping[:-1], [page for page in kept_pages if page.end > page.start]


def _edge_furniture(blocks: list[Block], edge_order: list[int], counts: Counter[str], min_repeats: int) -> list[int]:
    found = []
    for index in edge_order[:_EDGE_BLOCKS]:
        if not _is_furniture(blocks[index], counts, min_repeats):
            break
        found.append(index)
    return found


def _pages(blocks: list[Block]) -> list[list[int]]:
    """PageBreak로 나눈 쪽마다 내용 블록 위치."""
    pages: list[list[int]] = [[]]
    for index, block in enumerate(blocks):
        if isinstance(block, PageBreak):
            pages.append([])
        else:
            pages[-1].append(index)
    return [page for page in pages if page] if len(pages) > 1 else []


def _edges(page: list[int]) -> set[int]:
    return set(page[:_EDGE_BLOCKS]) | set(page[-_EDGE_BLOCKS:])


def _text(block: Block) -> str:
    if isinstance(block, Paragraph):
        return block.text
    if isinstance(block, Table):
        return " ".join(cell.text for row in block.rows for cell in row if cell.text)
    return ""


def _repeat_key(block: Block) -> str | None:
    text = _text(block)
    if not text or len(text) > _MAX_LENGTH or (isinstance(block, Table) and _filled_rows(block) > 2):
        return None
    if text.rstrip().endswith("."):
        return None
    flat = " ".join(text.split()).lower()
    if parse_item_label(text) or parse_part(text):
        return "=" + flat
    return _PAGE_NUMBER_IN_TEXT.sub("#", flat)


def _is_furniture(block: Block, counts: Counter[str], min_repeats: int) -> bool:
    text = _text(block)
    if text and _PAGE_NUMBER.match(text.strip()):
        return True
    key = _repeat_key(block)
    return key is not None and counts[key] >= min_repeats


def _filled_rows(table: Table) -> int:
    return sum(1 for row in table.rows if any(cell.text for cell in row))


def _page_number(text: str) -> str | None:
    """머리말·꼬리말 끝(없으면 앞)의 쪽 번호."""
    text = " ".join(text.split())
    match = _TRAILING_PAGE.search(text) or _LEADING_PAGE.match(text)
    return match.group(1).replace(" ", "") if match else None
