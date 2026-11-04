"""표 단위("(in thousands)", "(In millions, except per share data)")를 찾아 `Table.unit`에 단다.

단위는 표 머리 행의 칸이나 표 바로 앞의 짧은 문단에 있다(재무제표 본표는 표 위 문단, 주석 표는 머리 행이 흔하다).
찾은 글자만 싣고 값을 곱하지 않는다(`cluefin-dart-notes`의 `Table.unit`과 같은 계약).
"""

from __future__ import annotations

import dataclasses
import re

from cluefin_sec_notes._blocks import Block, PageBreak, Paragraph, Table
from cluefin_sec_notes._grid import parse_amount

# "in thousands" 꼴. 앞에 "$"·"dollars"·"amounts"가 붙거나("$ in millions", "Dollars in thousands") 뒤에 "except …"가 붙는다.
_UNIT_WORD = re.compile(r"\bin\s+(thousands|millions|billions)\b", re.IGNORECASE)
_PARENTHESIZED = re.compile(r"\(([^()]*)\)")
# 단위 문단은 짧다. "(in thousands, except share and per share amounts)"가 50자 남짓이다.
_UNIT_PARAGRAPH_MAX_CHARS = 120
_UNIT_CELL_MAX_CHARS = 120
# 머리 행은 첫 숫자 행 앞까지 본다. 숫자가 없는 표(가정·서술 표)는 앞 몇 행만.
_HEAD_ROWS_MAX = 4

SCALES = {"thousands": 1_000, "millions": 1_000_000, "billions": 1_000_000_000}


def unit_scale(unit: str | None) -> int | None:
    """단위 글자의 배수. "in thousands, except per share data" → 1000. 단위 낱말이 없으면 None."""
    if not unit:
        return None
    match = _UNIT_WORD.search(unit)
    return SCALES[match.group(1).lower()] if match else None


def attach_units(blocks: list[Block]) -> list[Block]:
    """표마다 단위를 찾아 `unit`을 채운 블록 목록. 머리 행이 앞 문단보다 우선한다."""
    result: list[Block] = []
    previous: Paragraph | None = None
    for block in blocks:
        if isinstance(block, Table):
            unit = _head_unit(block) or (_paragraph_unit(previous) if previous is not None else None)
            if unit is not None:
                block = dataclasses.replace(block, unit=unit)
            previous = None
        elif isinstance(block, Paragraph):
            previous = block
        elif not isinstance(block, PageBreak):
            previous = None
        result.append(block)
    return result


def _head_unit(table: Table) -> str | None:
    for index, row in enumerate(table.rows[:_HEAD_ROWS_MAX]):
        if index and any(parse_amount(cell.text) is not None and not _is_year(cell.text) for cell in row):
            return None
        for cell in row:
            text = " ".join(cell.text.split())
            if len(text) <= _UNIT_CELL_MAX_CHARS and _UNIT_WORD.search(text):
                return _unit_text(text)
    return None


def _paragraph_unit(paragraph: Paragraph) -> str | None:
    """표 바로 앞 문단이 단위 문단이면 그 단위. 긴 문단은 괄호 단위로 끝날 때만("… as follows (in millions).") 본다."""
    text = " ".join(paragraph.text.split())
    if len(text) <= _UNIT_PARAGRAPH_MAX_CHARS:
        return _unit_text(text) if _UNIT_WORD.search(text) else None
    last = text.rstrip(".:; ").rsplit("(", 1)
    if len(last) == 2 and last[1].endswith(")") and _UNIT_WORD.search(last[1]):
        return _unit_text("(" + last[1])
    return None


def _unit_text(text: str) -> str:
    """괄호 안 단위 문구("in thousands, except per share amounts"). 괄호가 없으면 글자 그대로."""
    for match in _PARENTHESIZED.finditer(text):
        if _UNIT_WORD.search(match.group(1)):
            return match.group(1).strip()
    return text.strip()


def _is_year(text: str) -> bool:
    stripped = text.strip()
    return len(stripped) == 4 and stripped.isdigit() and stripped[:2] in ("19", "20")
