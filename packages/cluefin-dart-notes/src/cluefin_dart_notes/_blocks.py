"""섹션 본문을 문단·소제목·표 블록으로 읽는다."""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Union

from cluefin_dart_notes.repair._rules import LINE_BREAK

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element

_SECTION_TAGS = frozenset({"SECTION-1", "SECTION-2", "SECTION-3", "CORRECTION"})
_CELL_TAGS = frozenset({"TD", "TH", "TE", "TU"})
_HEADER_CELL_TAGS = frozenset({"TH", "TU"})
# 내용 없이 지나가는 태그. IMAGE 는 원문에 이미지 파일 이름만 있어 블록으로 만들지 않는다.
_SKIPPED_TAGS = frozenset({"PGBRK", "IMAGE", "IMG", "IMG-CAPTION", "COLGROUP", "COL"})
_UNIT = re.compile(r"단위\s*[:：]\s*([^)）]*)")
# 캡션 표: 단위가 적힌 작은 테두리 없는 표. 주석은 1~2행(기준일·단위), 재무제표 본표 앞은 3~5행(표 이름·기수·단위)이다.
_CAPTION_MAX_ROWS = 6
_CAPTION_MAX_LENGTH = 200
# 단위만 적힌 문단으로 볼 최대 길이. 긴 문단 안의 "단위:"는 표 단위가 아니다.
_UNIT_PARAGRAPH_MAX_LENGTH = 40
# 굵은 런의 시작·끝 표식. 정규화가 끝나면 지우고 위치만 남긴다. 원문에는 쓰이지 않는다(사용자 영역 문자).
_BOLD_START = "\ue000"
_BOLD_END = "\ue001"


@dataclass(frozen=True)
class Paragraph:
    """문단. `text`의 줄바꿈은 원문의 `&cr;`·`BR`에서 온 것만 남는다.

    Attributes:
        bold_spans: 굵은 글씨(`USERMARK`의 `B`) 구간 `(시작, 끝)`. `text[시작:끝]`이 굵은 글자다. 문단 중간에
            붙은 소제목과 그 끝을 찾는 데 쓴다(콜론 없이 앞 문장에 붙은 주석 제목 등). 이어진 구간은 합친다.
    """

    text: str
    bold_spans: tuple[tuple[int, int], ...] = ()


@dataclass(frozen=True)
class Heading:
    """섹션이 아닌 `TITLE`. 2024년 이후 상장사 주석에서는 노트마다 `TABLE-GROUP > TITLE`이 붙는다."""

    text: str
    assoc_code: str | None = None
    toc_id: str | None = None


@dataclass(frozen=True)
class Cell:
    """표 셀. 병합 셀은 격자에서 차지하는 칸마다 같은 객체가 들어간다(`row`·`col`은 왼쪽 위 칸).

    Attributes:
        tag: TD(일반)·TH(머리글)·TE(입력 항목)·TU(단위가 붙은 머리글).
        acode: TE의 `ACODE` 항목 코드.
        aunit, aunit_value: TU의 `AUNIT`·`AUNITVALUE` 단위.
    """

    text: str
    tag: str
    row: int
    col: int
    row_span: int = 1
    col_span: int = 1
    acode: str | None = None
    aunit: str | None = None
    aunit_value: str | None = None

    @property
    def is_header(self) -> bool:
        return self.tag in _HEADER_CELL_TAGS


@dataclass(frozen=True, eq=False)
class Table:
    """표. `grid`는 COLSPAN·ROWSPAN을 펼친 직사각형 격자이고, 비는 칸은 None이다.

    Attributes:
        bordered: `BORDER="1"` 인지. 테두리 있는 표가 데이터 표다.
        caption: 바로 앞 캡션 표(기준일·단위가 적힌 1~2행 테두리 없는 표)의 텍스트.
        unit: 캡션이나 바로 앞 단위 문단의 "(단위 : …)" 값. 값을 환산하지는 않는다.
    """

    grid: tuple[tuple[Cell | None, ...], ...]
    bordered: bool
    caption: str | None = None
    unit: str | None = None
    element: Element | None = field(default=None, repr=False)

    @property
    def n_rows(self) -> int:
        return len(self.grid)

    @property
    def n_cols(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def to_rows(self) -> list[list[str]]:
        """셀 텍스트 격자. 병합 셀은 차지하는 칸마다 같은 텍스트가 반복된다."""
        return [[cell.text if cell else "" for cell in row] for row in self.grid]


Block = Union[Paragraph, Heading, Table]


def table_to_rows(table: Table) -> list[list[str]]:
    """`Table.to_rows()`와 같다. pandas 없이 `pd.DataFrame(rows[1:], columns=rows[0])`로 넘기기 좋게."""
    return table.to_rows()


def extract_blocks(element: Element) -> list[Block]:
    """요소 안의 블록을 문서 순서로. 직속 `TITLE`(섹션 제목)과 하위 섹션은 건너뛴다."""
    blocks: list[Block] = []
    for child in element:
        if child.tag == "TITLE":
            continue
        blocks.extend(_blocks_of(child))
    return _attach_captions(blocks)


def _blocks_of(element: Element) -> Iterator[Block | _Caption]:
    tag = element.tag
    if tag in _SECTION_TAGS or tag in _SKIPPED_TAGS:
        return
    if tag == "P":
        paragraph = _paragraph(element)
        if paragraph.text:
            yield paragraph
    elif tag == "TITLE":
        text = _normalize(_raw_text(element, bold=False))
        if text:
            yield Heading(text, element.get("AASSOCNOTE") or None, element.get("ATOCID") or None)
    elif tag == "TABLE":
        yield from _table_blocks(element)
    else:
        # LIBRARY·TABLE-GROUP·INSERTION 같은 묶음은 투명하게 통과한다.
        for child in element:
            yield from _blocks_of(child)


# --- 텍스트 ---------------------------------------------------------------


def _paragraph(element: Element) -> Paragraph:
    return next(_inline_paragraph([_raw_text(element, bold=False)]), Paragraph(""))


def _is_bold(element: Element) -> bool:
    return "B" in (element.get("USERMARK") or "").split()


def _raw_text(element: Element, *, bold: bool) -> str:
    """요소의 텍스트. 굵은 런을 표식으로 감싸고, BR 과 (셀 안의) 둘째 이후 문단 앞에 줄바꿈을 넣는다."""
    is_bold = bold or _is_bold(element)
    parts = [element.text or ""]
    seen_paragraph = False
    for child in element:
        if child.tag == "BR":
            parts.append(LINE_BREAK)
        elif child.tag != "TABLE":  # 셀 안의 표는 따로 블록이 된다
            if child.tag == "P":
                if seen_paragraph:
                    parts.append(LINE_BREAK)
                seen_paragraph = True
            parts.append(_raw_text(child, bold=is_bold))
        parts.append(child.tail or "")
    text = "".join(parts)
    if is_bold and not bold and text.strip():
        return f"{_BOLD_START}{text}{_BOLD_END}"
    return text


def _normalize(raw: str) -> str:
    return _normalize_with_marks(raw)[0]


def _normalize_with_marks(raw: str) -> tuple[str, tuple[tuple[int, int], ...]]:
    """공백을 한 칸으로 줄이고 `LINE_BREAK`만 `\n`으로 살린다(앞뒤 공백 제거). 굵은 표식은 지우고 구간을 돌려준다."""
    if _BOLD_START not in raw:
        lines = (" ".join(part.split()) for part in raw.split(LINE_BREAK))
        return "\n".join(line for line in lines if line), ()
    out: list[str] = []
    spans: list[tuple[int, int]] = []
    span_start: int | None = None
    pending_start = False
    gap = ""
    for char in raw:
        if char == _BOLD_START:
            pending_start = True
        elif char == _BOLD_END:
            if span_start is not None:
                _add_span(spans, span_start, len(out))
            span_start, pending_start = None, False
        elif char == LINE_BREAK:
            gap = "\n"
        elif char.isspace():
            gap = gap or " "
        else:
            if gap and out:
                out.append(gap)
            gap = ""
            if pending_start:
                span_start, pending_start = len(out), False
            out.append(char)
    return "".join(out), tuple(spans)


def _add_span(spans: list[tuple[int, int]], start: int, end: int) -> None:
    # 굵은 SPAN 두 개가 공백 하나를 사이에 두고 이어지면 한 구간으로 본다("16." + "영업 현금").
    if spans and start <= spans[-1][1] + 1:
        spans[-1] = (spans[-1][0], end)
    else:
        spans.append((start, end))


# --- 표 -------------------------------------------------------------------


@dataclass(frozen=True)
class _Caption:
    text: str
    unit: str | None
    table: Table


def _table_blocks(element: Element) -> Iterator[Block | _Caption]:
    rows = _direct_rows(element)
    cells = [cell for row in rows for cell in row if cell.tag in _CELL_TAGS]
    if len(cells) <= 1 or any(child.tag == "TABLE" for cell in cells for child in cell.iter() if child is not cell):
        # 레이아웃 표(1×1, 또는 셀 안에 실제 표를 담은 래퍼): 셀 내용을 블록으로 꺼낸다.
        for cell in cells:
            yield from _cell_blocks(cell)
        return
    table = Table(grid=_grid(rows), bordered=element.get("BORDER") == "1", element=element)
    if not table.bordered and table.n_rows <= _CAPTION_MAX_ROWS:
        text = " ".join(cell.text for row in table.grid for cell in _unique(row) if cell.text)
        unit = _find_unit(text) if len(text) <= _CAPTION_MAX_LENGTH else None
        if unit is not None:
            yield _Caption(text, unit, table)
            return
    yield table


def _direct_rows(table: Element) -> list[Element]:
    """이 표의 TR 만. `iter("TR")`는 셀 안에 중첩된 표의 TR 까지 돌려준다."""
    rows: list[Element] = []
    for child in table:
        if child.tag == "TR":
            rows.append(child)
        elif child.tag in ("THEAD", "TBODY"):
            rows.extend(row for row in child if row.tag == "TR")
    return rows


def _cell_blocks(cell: Element) -> Iterator[Block | _Caption]:
    """레이아웃 셀의 내용. 문단(P)·표는 각각 블록이 되고, 그 사이의 글자·SPAN 은 한 문단으로 묶는다."""
    inline = [cell.text or ""]
    for child in cell:
        if child.tag in ("P", "TABLE"):
            yield from _inline_paragraph(inline)
            yield from _blocks_of(child)
        elif child.tag == "BR":
            inline.append(LINE_BREAK)
        else:
            inline.append(_raw_text(child, bold=_is_bold(cell)))
        inline.append(child.tail or "")
    yield from _inline_paragraph(inline)


def _inline_paragraph(parts: list[str]) -> Iterator[Paragraph]:
    text, bold_spans = _normalize_with_marks("".join(parts))
    parts.clear()
    if text:
        yield Paragraph(text, bold_spans)


def _grid(rows: list[Element]) -> tuple[tuple[Cell | None, ...], ...]:
    placed: dict[tuple[int, int], Cell] = {}
    width = 0
    for r, row in enumerate(rows):
        c = 0
        for element in (child for child in row if child.tag in _CELL_TAGS):
            while (r, c) in placed:
                c += 1
            cell = _cell(element, r, c)
            for dr in range(cell.row_span):
                for dc in range(cell.col_span):
                    placed[(r + dr, c + dc)] = cell
            c += cell.col_span
            width = max(width, c)
    height = len(rows)
    return tuple(tuple(placed.get((r, c)) for c in range(width)) for r in range(height))


def _cell(element: Element, row: int, col: int) -> Cell:
    return Cell(
        text=_normalize(_raw_text(element, bold=False)),
        tag=element.tag,
        row=row,
        col=col,
        row_span=_span(element.get("ROWSPAN")),
        col_span=_span(element.get("COLSPAN")),
        acode=element.get("ACODE") or None,
        aunit=element.get("AUNIT") or None,
        aunit_value=element.get("AUNITVALUE") or None,
    )


def _span(value: str | None) -> int:
    try:
        return max(1, int(value or 1))
    except ValueError:
        return 1


def _unique(row: tuple[Cell | None, ...]) -> list[Cell]:
    return list(dict.fromkeys(cell for cell in row if cell is not None))


def _find_unit(text: str) -> str | None:
    match = _UNIT.search(text)
    if match is None:
        return None
    return match.group(1).strip() or None


def _attach_captions(items: list[Block | _Caption]) -> list[Block]:
    """캡션 표를 바로 다음 데이터 표에 붙인다. 붙일 표가 없으면 캡션 표를 그대로 블록으로 둔다.

    캡션이 없는 데이터 표는 바로 앞 문단이 짧은 단위 문단("(단위 : 백만원)")이면 그 단위를 쓴다.
    """
    blocks: list[Block] = []
    pending: _Caption | None = None
    for item in items:
        if isinstance(item, _Caption):
            if pending is not None:
                blocks.append(pending.table)
            pending = item
            continue
        if isinstance(item, Table) and item.bordered:
            if pending is not None:
                item = _with_caption(item, pending.text, pending.unit)
            else:
                unit = _unit_paragraph(blocks[-1]) if blocks and isinstance(blocks[-1], Paragraph) else None
                unit = unit or _first_row_unit(item)
                if unit is not None:
                    item = _with_caption(item, None, unit)
            pending = None
        elif pending is not None:
            blocks.append(pending.table)
            pending = None
        blocks.append(item)
    if pending is not None:
        blocks.append(pending.table)
    return blocks


def _unit_paragraph(paragraph: Paragraph) -> str | None:
    """문단의 마지막 줄이 짧은 단위 줄이면 그 단위. 오래된 공시는 설명 문단 끝줄에 "(단위: 주)"를 붙인다."""
    last_line = paragraph.text.rsplit("\n", 1)[-1]
    if len(last_line) > _UNIT_PARAGRAPH_MAX_LENGTH:
        return None
    return _find_unit(last_line)


def _first_row_unit(table: Table) -> str | None:
    """데이터 표의 첫 행이 단위 행("(단위: 천원)")인 경우."""
    text = " ".join(cell.text for cell in _unique(table.grid[0]))
    return _find_unit(text) if len(text) <= _UNIT_PARAGRAPH_MAX_LENGTH * 2 else None


def _with_caption(table: Table, caption: str | None, unit: str | None) -> Table:
    return Table(grid=table.grid, bordered=table.bordered, caption=caption, unit=unit, element=table.element)
