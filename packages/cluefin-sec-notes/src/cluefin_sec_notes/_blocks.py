"""노드 트리를 문서 순서의 평평한 블록 목록(문단·표·페이지 경계)으로 편다.

Item 탐지는 이 목록만 본다. 블록마다 원문 위치, 블록이 시작되는 앵커(`id`·`<a name>` 중 문서 안 링크가
가리키는 것), 문서 안 링크, 굵기·글자 크기·정렬 같은 헤딩 단서를 달아 둔다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from cluefin_sec_notes._report import HIDDEN_CONTENT, LAYOUT_TABLE, ReportCollector
from cluefin_sec_notes._tree import EDGAR_HEADER_TAGS, Node

_BLOCK_TAGS = frozenset(
    {
        "address", "article", "aside", "blockquote", "body", "caption", "center", "dd", "div", "dl", "dt",
        "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "html",
        "li", "main", "nav", "ol", "p", "page", "pre", "section", "td", "th", "tr", "ul",
    }
)  # fmt: skip
_SKIPPED_TAGS = frozenset({"head", "script", "style", "title", "noscript"})
_HEADING_SIZES = {"h1": 24.0, "h2": 18.0, "h3": 14.0, "h4": 12.0, "h5": 10.0, "h6": 8.0}
_FONT_TAG_SIZES = {1: 7.5, 2: 10.0, 3: 12.0, 4: 13.5, 5: 18.0, 6: 24.0, 7: 36.0}
_BOLD_TAGS = frozenset({"b", "strong"}) | frozenset(_HEADING_SIZES)
_HARD_BREAK = ""  # `<br>` 자리. 공백 정규화가 끝나면 줄바꿈으로 바꾼다(사용자 영역 문자, 원문에 안 쓰인다).
_WHITESPACE = re.compile(r"[\s ​﻿]+")
_PRE_PARAGRAPH = re.compile(r"\n[ \t]*\n")
_STYLE_DECLARATION = re.compile(r"([a-z-]+)\s*:\s*([^;]+)")
_LENGTH = re.compile(r"^(-?\d+(?:\.\d+)?)\s*(pt|px|em|rem|%)?$")
_PAGE_BREAK_VALUES = frozenset({"always", "page", "left", "right"})


@dataclass(frozen=True, slots=True)
class Link:
    """문서 안 링크(`href="#…"`). `target`은 `#`을 뗀 앵커 이름."""

    target: str
    text: str


@dataclass(frozen=True, slots=True)
class Paragraph:
    """문단 하나. `text`의 줄바꿈은 `<br>`(과 `<pre>` 안 줄바꿈)에서 온 것만 남는다.

    Attributes:
        bold: 공백이 아닌 글자가 전부 굵다.
        font_size: 글자 수가 가장 많은 크기(pt). 원문에 크기가 없으면 None.
        align: 가장 가까운 블록의 `text-align`(`left`·`center`·`right`·`justify`). 없으면 None.
        anchors: 이 문단에서 시작하는 앵커.
        links: 문단 안의 문서 안 링크.
    """

    text: str
    line: int
    column: int
    bold: bool = False
    font_size: float | None = None
    align: str | None = None
    anchors: tuple[str, ...] = ()
    links: tuple[Link, ...] = ()


@dataclass(frozen=True, slots=True)
class Cell:
    """표 칸 하나(병합을 펼치지 않은 원문 그대로). 칸 안의 문단은 줄바꿈으로 잇는다."""

    text: str
    col_span: int = 1
    row_span: int = 1
    bold: bool = False
    links: tuple[Link, ...] = ()


@dataclass(frozen=True, slots=True)
class Table:
    """데이터 표. 배치용 표(칸 하나, 칸 안에 표)는 표가 아니라 그 안의 블록으로 펼쳐진다."""

    rows: tuple[tuple[Cell, ...], ...]
    line: int
    column: int
    anchors: tuple[str, ...] = ()

    @property
    def links(self) -> tuple[Link, ...]:
        return tuple(link for row in self.rows for cell in row for link in cell.links)

    def row_text(self, index: int) -> str:
        """한 행의 비지 않은 칸을 공백으로 이은 것. 표로 짠 헤딩("Item 1." | "Business")을 읽는 데 쓴다."""
        return " ".join(cell.text for cell in self.rows[index] if cell.text)

    def grid(self) -> tuple[tuple[str, ...], ...]:
        """열을 맞춘 문자열 행렬. 병합 칸을 펴고, `$`·`)`·`%` 칸을 옆 값에 붙이고, 빈 행·열을 지운다
        (`_grid.table_grid`). 금액은 `parse_amount`로 숫자로 바꾼다."""
        from cluefin_sec_notes._grid import table_grid

        return table_grid(self)


@dataclass(frozen=True, slots=True)
class PageBreak:
    """페이지 경계(`page-break-before/after`, `<hr>`). 연속된 경계는 하나로 합친다."""

    line: int
    column: int


Block = Paragraph | Table | PageBreak


@dataclass(frozen=True, slots=True)
class _Style:
    bold: bool = False
    size: float | None = None
    align: str | None = None
    pre: bool = False


@dataclass(slots=True)
class _Run:
    text: str
    bold: bool
    size: float | None


@dataclass
class _ParagraphBuilder:
    runs: list[_Run] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)
    line: int = 0
    column: int = 0
    align: str | None = None
    has_text: bool = False


@dataclass
class LinearizedDocument:
    blocks: list[Block]
    anchors: dict[str, int]
    dei: dict[str, str]
    edgar_header: dict[str, str]


class _Linearizer:
    """트리를 블록으로. `in_cell`이면 표를 만들지 않고 칸 안 내용을 문단으로만 읽는다."""

    def __init__(self, targets: frozenset[str], collector: ReportCollector, dei: dict[str, str], *, in_cell: bool):
        self.targets = targets
        self.folded_targets = {target.lower(): target for target in targets}
        self.collector = collector
        self.dei = dei
        self.in_cell = in_cell
        self.blocks: list[Block] = []
        self.pending_anchors: list[str] = []
        self.paragraph = _ParagraphBuilder()
        self.position = (0, 0)  # 마지막으로 들어간 요소의 원문 위치. 문단 위치로 쓴다.
        self.edgar_header: dict[str, str] = {}

    def run(self, root: Node, style: _Style) -> list[Block]:
        # (노드, 스타일) 또는 (노드, None) = 그 노드를 나가는 표시
        stack: list[tuple[Node | str, _Style | None]] = [(root, style)]
        while stack:
            item, item_style = stack.pop()
            if isinstance(item, str):
                assert item_style is not None
                self._text(item, item_style)
            elif item_style is None:
                self._exit(item)
            else:
                self._enter(item, item_style, stack)
        self._flush()
        return self.blocks

    # 방문 -----------------------------------------------------------------------------------------------------

    def _enter(self, node: Node, parent_style: _Style, stack: list) -> None:
        tag = node.tag
        if tag in _SKIPPED_TAGS:
            return
        if tag in EDGAR_HEADER_TAGS:
            self.edgar_header.setdefault(tag, _normalize(node.text()))
            return
        declarations = _style_declarations(node)
        if tag == "ix:header" or declarations.get("display") == "none":
            self._hide(node)
            return
        if tag == "ix:nonnumeric" and node.attrs.get("name", "").startswith("dei:"):
            self.dei.setdefault(node.attrs["name"][4:], _normalize(node.text()))
        style = _child_style(node, declarations, parent_style)
        block = tag in _BLOCK_TAGS
        if block or tag == "table" or tag == "hr":
            self._flush()
        if _breaks_page(declarations, "page-break-before", "break-before"):
            self._page_break(node)
        self._anchor(node)
        if tag == "hr":
            self._page_break(node)
            return
        if tag == "br":
            self._append(_HARD_BREAK, style)
            return
        if tag == "table" and not self.in_cell and self._table(node, style):
            if _breaks_page(declarations, "page-break-after", "break-after"):
                self._page_break(node)
            return
        if tag == "a" and node.attrs.get("href", "").startswith("#") and len(node.attrs["href"]) > 1:
            self.paragraph.links.append(Link(target=node.attrs["href"][1:], text=_normalize(node.text())))
        if block and style.align is not None and not self.paragraph.has_text:
            self.paragraph.align = style.align
        stack.append((node, None))
        stack.extend((child, style) for child in reversed(node.children))

    def _exit(self, node: Node) -> None:
        if node.tag in _BLOCK_TAGS:
            self._flush()
        if _breaks_page(_style_declarations(node), "page-break-after", "break-after"):
            self._flush()
            self._page_break(node)

    def _text(self, text: str, style: _Style) -> None:
        if not style.pre:
            self._append(text, style)
            return
        for index, part in enumerate(_PRE_PARAGRAPH.split(text)):
            if index:
                self._flush()
            self._append(part.replace("\n", _HARD_BREAK), style)

    # 블록 만들기 ----------------------------------------------------------------------------------------------

    def _append(self, text: str, style: _Style) -> None:
        builder = self.paragraph
        builder.runs.append(_Run(text, style.bold, style.size))
        if not builder.has_text and _WHITESPACE.sub("", text.replace(_HARD_BREAK, "")):
            builder.has_text = True
            builder.line, builder.column = self.position

    def _anchor(self, node: Node) -> None:
        self.position = (node.line, node.column)
        for name in (node.attrs.get("id"), node.attrs.get("name") if node.tag == "a" else None):
            # 오래된 공시는 `href="#item1"`과 `<a name="Item1">`처럼 대소문자가 다르다(브라우저 쿼크 모드에서는 이동한다).
            target = name if name in self.targets else self.folded_targets.get(name.lower()) if name else None
            if target and target not in self.pending_anchors:
                self.pending_anchors.append(target)

    def _flush(self) -> None:
        builder = self.paragraph
        self.paragraph = _ParagraphBuilder()
        if not builder.has_text:
            # 텍스트 없는 문단의 링크는 버리지만 앵커는 다음 블록으로 넘긴다.
            return
        text, bold, size = _merge_runs(builder.runs)
        if not text:
            return
        self.blocks.append(
            Paragraph(
                text=text,
                line=builder.line,
                column=builder.column,
                bold=bold,
                font_size=size,
                align=builder.align,
                anchors=self._take_anchors(),
                links=tuple(builder.links),
            )
        )

    def _take_anchors(self) -> tuple[str, ...]:
        anchors = tuple(self.pending_anchors)
        self.pending_anchors.clear()
        return anchors

    def _page_break(self, node: Node) -> None:
        if self.in_cell or (self.blocks and isinstance(self.blocks[-1], PageBreak)):
            return
        self.blocks.append(PageBreak(line=node.line, column=node.column))

    def _table(self, node: Node, style: _Style) -> bool:
        """데이터 표면 블록을 만들고 True. 배치용 표면 False(호출한 쪽이 안을 흐름으로 읽는다)."""
        rows = []
        for row in _table_rows(node):
            visible = []
            for cell in row:
                if _style_declarations(cell).get("display") == "none":
                    self._hide(cell)  # 브라우저에서 칸 자체가 없어진다
                else:
                    visible.append(cell)
            rows.append(visible)
        cells = [cell for row in rows for cell in row]
        if len(cells) <= 1 or any(inner.tag == "table" for cell in cells for inner in cell.iter()):
            self.collector.add(LAYOUT_TABLE, node.line, node.column, f"{len(cells)} cell(s)")
            return False
        anchors: list[str] = []
        built_rows = []
        for row in rows:
            built = []
            for cell in row:
                built.append(self._cell(cell, style, anchors))
            if built:
                built_rows.append(tuple(built))
        for name in anchors:
            if name not in self.pending_anchors:
                self.pending_anchors.append(name)
        if not any(cell.text for row in built_rows for cell in row):
            return True  # 간격용 빈 표. 앵커는 다음 블록으로 넘어간다.
        self.blocks.append(
            Table(rows=tuple(built_rows), line=node.line, column=node.column, anchors=self._take_anchors())
        )
        return True

    def _cell(self, cell: Node, style: _Style, anchors: list[str]) -> Cell:
        inner = _Linearizer(self.targets, self.collector, self.dei, in_cell=True)
        paragraphs = [block for block in inner.run(cell, style) if isinstance(block, Paragraph)]
        for block in paragraphs:
            anchors.extend(block.anchors)
        anchors.extend(inner.pending_anchors)
        return Cell(
            text="\n".join(block.text for block in paragraphs),
            col_span=_span(cell.attrs.get("colspan")),
            row_span=_span(cell.attrs.get("rowspan")),
            bold=bool(paragraphs) and all(block.bold for block in paragraphs),
            links=tuple(link for block in paragraphs for link in block.links),
        )

    def _hide(self, node: Node) -> None:
        """숨김 요소를 건너뛴다. 글자가 있었을 때만 기록한다(Workiva는 열 너비용 빈 `<td style="display:none"/>`를 쓴다)."""
        self._collect_dei(node)
        text = _normalize(node.text())
        if text:
            self.collector.add(HIDDEN_CONTENT, node.line, node.column, f"<{node.tag}> {text[:60]}")

    def _collect_dei(self, node: Node) -> None:
        for element in node.iter():
            name = element.attrs.get("name", "")
            if element.tag == "ix:nonnumeric" and name.startswith("dei:"):
                self.dei.setdefault(name[4:], _normalize(element.text()))


def linearize(root: Node, collector: ReportCollector) -> LinearizedDocument:
    targets = frozenset(
        node.attrs["href"][1:]
        for node in root.iter()
        if node.tag == "a" and node.attrs.get("href", "").startswith("#") and len(node.attrs["href"]) > 1
    )
    dei: dict[str, str] = {}
    linearizer = _Linearizer(targets, collector, dei, in_cell=False)
    blocks = linearizer.run(root, _Style())
    anchors: dict[str, int] = {}
    for index, block in enumerate(blocks):
        for name in getattr(block, "anchors", ()):
            anchors.setdefault(name, index)
    for name in linearizer.pending_anchors:  # 문서 끝, 뒤에 블록이 없는 앵커
        anchors.setdefault(name, len(blocks))
    return LinearizedDocument(blocks=blocks, anchors=anchors, dei=dei, edgar_header=linearizer.edgar_header)


# 도움 함수 -------------------------------------------------------------------------------------------------------


def _table_rows(table: Node) -> list[list[Node]]:
    rows: list[list[Node]] = []
    for child in table.children:
        if not isinstance(child, Node):
            continue
        if child.tag == "tr":
            rows.append(_row_cells(child))
        elif child.tag in ("thead", "tbody", "tfoot"):
            rows.extend(_row_cells(row) for row in child.children if isinstance(row, Node) and row.tag == "tr")
    return rows


def _row_cells(row: Node) -> list[Node]:
    return [cell for cell in row.children if isinstance(cell, Node) and cell.tag in ("td", "th")]


def _span(value: str | None) -> int:
    if value is None:
        return 1
    digits = value.strip()
    return int(digits) if digits.isdigit() and int(digits) > 0 else 1


def _style_declarations(node: Node) -> dict[str, str]:
    style = node.attrs.get("style")
    if not style:
        return {}
    return {name: value.strip().lower() for name, value in _STYLE_DECLARATION.findall(style.lower())}


def _breaks_page(declarations: dict[str, str], *names: str) -> bool:
    return any(declarations.get(name) in _PAGE_BREAK_VALUES for name in names)


def _child_style(node: Node, declarations: dict[str, str], parent: _Style) -> _Style:
    tag = node.tag
    bold = parent.bold or tag in _BOLD_TAGS
    weight = declarations.get("font-weight")
    if weight is not None:
        bold = _is_bold_weight(weight, parent.bold)
    size = _HEADING_SIZES.get(tag, parent.size)
    if tag == "font":
        size = _font_tag_size(node.attrs.get("size"), size)
    if "font-size" in declarations:
        size = _css_size(declarations["font-size"], parent.size)
    align = declarations.get("text-align") or node.attrs.get("align", "").lower() or parent.align
    return _Style(bold=bold, size=size, align=align or None, pre=parent.pre or tag == "pre")


def _is_bold_weight(value: str, inherited: bool) -> bool:
    if value in ("bold", "bolder"):
        return True
    if value in ("normal", "lighter"):
        return False
    return int(value) >= 600 if value.isdigit() else inherited


def _font_tag_size(value: str | None, inherited: float | None) -> float | None:
    if not value or not value.strip().lstrip("+-").isdigit():
        return inherited
    value = value.strip()
    level = 3 + int(value) if value[0] in "+-" else int(value)
    return _FONT_TAG_SIZES[min(max(level, 1), 7)]


def _css_size(value: str, inherited: float | None) -> float | None:
    match = _LENGTH.match(value)
    if match is None:
        return inherited
    number, unit = float(match.group(1)), match.group(2) or "px"
    if unit == "pt":
        return number
    if unit == "px":
        return number * 0.75
    if inherited is None:
        return None
    return inherited * (number / 100 if unit == "%" else number)


def _merge_runs(runs: list[_Run]) -> tuple[str, bool, float | None]:
    text = _normalize("".join(run.text for run in runs))
    bold = True
    sizes: dict[float | None, int] = {}
    for run in runs:
        visible = len(_WHITESPACE.sub("", run.text.replace(_HARD_BREAK, "")))
        if not visible:
            continue
        bold = bold and run.bold
        sizes[run.size] = sizes.get(run.size, 0) + visible
    size = max(sizes, key=lambda key: sizes[key]) if sizes else None
    return text, bold and bool(sizes), size


def _normalize(text: str) -> str:
    lines = (_WHITESPACE.sub(" ", line).strip() for line in text.split(_HARD_BREAK))
    return "\n".join(line for line in lines if line)
