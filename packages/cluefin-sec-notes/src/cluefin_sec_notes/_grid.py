"""표를 행렬로 편다(`Table.grid()`)와 금액 칸을 숫자로 바꾼다(`parse_amount`).

공시 표는 원문 칸 그대로면 열이 맞지 않는다. Workiva는 값 하나를 `"$" | "59,792" | ""` 세 칸에, `$` 없는 행은
`"25,433"(폭 2) | ""`에 싣고 머리 "2025"는 폭 3이다. DFIN 등은 음수 괄호를 옆 칸에 둔다(`"(3,787" | ")"`).

1. 행마다 기호 칸을 옆 값에 붙인다: 통화 기호(`$`)는 오른쪽 값 앞에, 닫는 괄호·퍼센트(`)`, `%`, `)%`)와 각주 표시만
   있는 칸("(a)", "(2)(9)", 숫자 하나 "(5)"는 음수라 빼고)은 왼쪽 값 뒤에.
2. `col_span`·`row_span`을 펴서 칸마다 격자 위 열 구간을 정한다(HTML 표 배치 규칙).
3. 숫자 칸(금액·퍼센트·대시)이 덮는 열끼리 하나의 열로 묶는다. 같은 값 열의 `$` 칸·값 칸·여백 칸이 한 열이 된다.
   맨 숫자 연도("2025")는 머리라서 묶지 않는다.
4. 글자 칸(라벨, 머리)은 자기가 덮는 첫 숫자 열 묶음에 넣는다. 덮는 묶음이 없으면(맨 왼쪽 라벨) 시작 열에 제 열을 만든다.
   여러 해에 걸친 머리("December 31,")가 두 해의 열을 합치지 않게, 글자 칸은 열을 묶지 않는다.
5. 글자 없는 열과 행을 지운다(열 너비용 첫 행 등).
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cluefin_sec_notes._blocks import Table

_CURRENCY = frozenset({"$", "€", "£", "¥", "US$", "C$", "A$"})
_SUFFIXES = frozenset({")", "%", ")%", "%)"})
_DASHES = frozenset({"—", "–", "-", "−", "— —", "—%", "-%"})
# 금액: 앞 괄호·음수 기호, 숫자(쉼표), 소수, 닫는 괄호. 통화 기호·퍼센트·각주는 미리 뗀다.
_NUMBER = re.compile(r"(?P<sign>[(\-−–])?(?P<digits>\d[\d,]*(?:\.\d+)?|\.\d+)(?P<close>\))?")
_FOOTNOTE = re.compile(r"\s*(?:\([a-z0-9]{1,2}\)|\*+|†+)$", re.IGNORECASE)
_FOOTNOTE_MARK = re.compile(r"\s*(?:\([a-z0-9]{1,2}\)|\*|†)", re.IGNORECASE)
_CURRENCY_PREFIX = re.compile(r"^(?:US|C|A)?[$€£¥]\s*")
# 연도 머리("2025")는 숫자지만 열을 묶지 않는다. 하위 열 여러 개(Loans | Derivatives …)를 덮는 머리가 그 열들을 합치지 않게.
_YEAR = re.compile(r"(?:19|20)\d{2}")


def parse_amount(text: str) -> Decimal | None:
    """금액 칸을 숫자로. "$59,792" → 59792, "(3,787)" → -3787, "$(1.5)" → -1.5, "12.5%" → 12.5, "−4" → -4.

    통화 기호·쉼표·퍼센트·끝의 각주 표시("(a)", "*")는 뗀다. 대시("—")·빈 칸·숫자가 아닌 글자는 None. 표 머리의
    단위("in millions")는 곱하지 않는다.
    """
    value = " ".join(text.split())
    while True:
        stripped = _FOOTNOTE.sub("", value)
        if stripped == value:
            break
        value = stripped
    value = value.replace(" ", "")
    negative_paren = value.startswith("(")
    if negative_paren:
        value = value[1:]
    value = _CURRENCY_PREFIX.sub("", value)
    if negative_paren:
        value = "(" + value
    value = value.removesuffix("%").replace("%)", ")")
    match = _NUMBER.fullmatch(value)
    if match is None:
        return None
    sign, close = match.group("sign"), match.group("close")
    if (sign == "(") != bool(close):
        return None
    try:
        amount = Decimal(match.group("digits").replace(",", ""))
    except InvalidOperation:
        return None
    return -amount if sign else amount


def table_grid(table: Table) -> tuple[tuple[str, ...], ...]:
    """표를 직사각형 문자열 행렬로. 칸 글자는 원문 그대로(기호만 붙임), 숫자로는 `parse_amount`로 바꾼다."""
    placed = _place(table)
    groups = _numeric_groups(placed)
    labels = _label_columns(placed, groups)
    cells: list[list[tuple[tuple[str, int], str]]] = []
    for row in placed:
        row_cells = []
        for start, end, text in row:
            if text:
                row_cells.append((_column_key(start, end, text, groups, labels), text))
        cells.append(row_cells)
    order = sorted({key for row_cells in cells for key, _ in row_cells}, key=lambda key: (key[1], key[0] == "number"))
    position = {key: index for index, key in enumerate(order)}
    grid = []
    for row_cells in cells:
        if not row_cells:
            continue
        values = [""] * len(order)
        for key, text in row_cells:
            index = position[key]
            values[index] = f"{values[index]} {text}" if values[index] else text
        grid.append(tuple(values))
    return tuple(grid)


def _column_key(
    start: int, end: int, text: str, groups: dict[int, tuple[str, int]], labels: set[int]
) -> tuple[str, int]:
    """칸이 들어갈 출력 열. 숫자 칸은 제 묶음. 글자 칸은 라벨 열을 덮으면("(In millions)" 폭 8) 그 라벨 열, 아니면
    덮는 첫 숫자 묶음(값 열 위 머리), 둘 다 아니면 시작 열에 제 열."""
    if _is_numeric(text) and not _YEAR.fullmatch(text) and start in groups:
        return groups[start]
    label = next((column for column in range(start, end) if column in labels), None)
    if label is not None:
        return ("text", label)
    return next((groups[column] for column in range(start, end) if column in groups), ("text", start))


def _label_columns(placed: list[list[tuple[int, int, str]]], groups: dict[int, tuple[str, int]]) -> set[int]:
    """숫자가 있는 행에서 숫자 묶음과 겹치지 않는 글자 칸이 시작하는 열(행 라벨 열)."""
    labels = set()
    for row in placed:
        if not any(text and _is_numeric(text) for _, _, text in row):
            continue
        for start, end, text in row:
            if text and not _is_numeric(text) and not any(column in groups for column in range(start, end)):
                labels.add(start)
    return labels


def _place(table: Table) -> list[list[tuple[int, int, str]]]:
    """행마다 `(시작 열, 끝 열, 글자)`. 기호 칸은 옆 값에 붙인 뒤 빈 글자로 남긴다. 위 행의 `row_span`이 덮는 열은 건너뛴다."""
    occupied: dict[int, set[int]] = {}
    placed = []
    for row_index, row in enumerate(table.rows):
        texts = _merge_symbols([" ".join(cell.text.split()) for cell in row])
        taken = occupied.pop(row_index, set())
        column = 0
        row_cells = []
        for cell, text in zip(row, texts, strict=True):
            while column in taken:
                column += 1
            span = max(cell.col_span, 1)
            row_cells.append((column, column + span, text))
            for below in range(row_index + 1, row_index + max(cell.row_span, 1)):
                occupied.setdefault(below, set()).update(range(column, column + span))
            column += span
        placed.append(row_cells)
    return placed


def _merge_symbols(texts: list[str]) -> list[str]:
    merged = list(texts)
    for index, text in enumerate(merged):
        if text in _CURRENCY or text == "(":
            target = _next_filled(merged, range(index + 1, len(merged)))
            if target is not None and not _is_symbol(merged[target]):
                merged[target] = text + merged[target]
                merged[index] = ""
        elif text in _SUFFIXES or _is_footnote_marks(text):
            target = _next_filled(merged, range(index - 1, -1, -1))
            if target is not None and not _is_symbol(merged[target]):
                merged[target] = merged[target] + text
                merged[index] = ""
    return merged


def _next_filled(texts: list[str], indexes: range) -> int | None:
    return next((index for index in indexes if texts[index]), None)


def _is_symbol(text: str) -> bool:
    return text in _CURRENCY or text in _SUFFIXES or text == "(" or _is_footnote_marks(text)


def _is_footnote_marks(text: str) -> bool:
    """각주 표시만 있는 칸("(a)", "(2)(9)", "*"). 숫자 표시 하나("(5)")는 작은 음수와 구별할 수 없어 각주로 보지 않는다.
    정규식 하나로 반복시키지 않고 표시를 하나씩 읽는다."""
    position, marks, numbered = 0, 0, False
    while position < len(text):
        match = _FOOTNOTE_MARK.match(text, position)
        if match is None:
            return False
        marks += 1
        numbered = numbered or any(char.isdigit() for char in match.group(0))
        position = match.end()
    return marks > 1 or (marks == 1 and not numbered)


def _numeric_groups(placed: list[list[tuple[int, int, str]]]) -> dict[int, tuple[str, int]]:
    """숫자 칸이 덮는 열끼리 묶는다. 열 → 묶음 키(묶음의 가장 왼쪽 열)."""
    parent: dict[int, int] = {}

    def find(column: int) -> int:
        while parent[column] != column:
            parent[column] = parent[parent[column]]
            column = parent[column]
        return column

    for row in placed:
        for start, end, text in row:
            if not text or not _is_numeric(text) or _YEAR.fullmatch(text):
                continue
            for column in range(start, end):
                parent.setdefault(column, column)
            root = find(start)
            for column in range(start + 1, end):
                other = find(column)
                if other != root:
                    parent[max(root, other)] = min(root, other)
                    root = min(root, other)
    return {column: ("number", find(column)) for column in parent}


def _is_numeric(text: str) -> bool:
    return text in _DASHES or parse_amount(text) is not None
