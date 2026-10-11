"""HTML을 노드 트리로 만든다(stdlib `html.parser`). 브라우저처럼 고쳐 읽되, 고친 곳은 전부 기록한다.

lxml은 쓰지 않는다. libxml2는 `huge_tree` 없이 깊이 256을 넘는 부분을 말없이 버리고, `recover=True`는 무엇을
버렸는지 알려 주지 않는다. 여기서는 스택으로 트리를 쌓으므로 깊이 제한이 없고, 텍스트는 하나도 버리지 않는다.
트리를 도는 코드도 재귀를 쓰지 않는다(Python 재귀 한도 1000).
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from html.parser import HTMLParser

from cluefin_sec_notes._report import (
    IMPLICIT_CLOSE,
    MISNESTED_END,
    STRAY_END_TAG,
    UNCLOSED_AT_EOF,
    UNKNOWN_TAG,
    ReportCollector,
)

VOID_TAGS = frozenset(
    {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
)
HTML_TAGS = VOID_TAGS | frozenset(
    {
        "a", "abbr", "acronym", "address", "article", "aside", "b", "basefont", "bdi", "bdo", "big", "blockquote",
        "body", "button", "caption", "center", "cite", "code", "colgroup", "dd", "del", "dfn", "dir", "div", "dl",
        "dt", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6",
        "head", "header", "html", "i", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "menu", "nav",
        "nobr", "noscript", "object", "ol", "optgroup", "option", "p", "page", "pre", "q", "s", "samp", "script",
        "section", "select", "small", "span", "strike", "strong", "style", "sub", "sup", "table", "tbody", "td",
        "textarea", "tfoot", "th", "thead", "title", "tr", "tt", "u", "ul", "var",
    }
)  # fmt: skip
# 인라인 XBRL(2019년~). `ix:header` 안의 xbrli·link 등은 접두어로 받아 준다.
IX_TAGS = frozenset(
    {
        "ix:header", "ix:hidden", "ix:references", "ix:resources", "ix:nonnumeric", "ix:nonfraction",
        "ix:continuation", "ix:exclude", "ix:footnote", "ix:fraction", "ix:numerator", "ix:denominator",
        "ix:relationship", "ix:tuple",
    }
)  # fmt: skip
_KNOWN_PREFIXES = ("xbrli:", "xbrldi:", "link:")
# EDGAR가 2000년대 공시 문서를 감싼 SGML(`<DOCUMENT><TYPE>10-K<SEQUENCE>1<FILENAME>…<TEXT><HTML>…`).
# 머리 태그는 닫히지 않으므로 다음 태그가 나오면 닫는다(그러지 않으면 문서 전체가 TYPE 안에 들어간다).
EDGAR_HEADER_TAGS = frozenset({"type", "sequence", "filename", "description"})
EDGAR_TAGS = EDGAR_HEADER_TAGS | frozenset({"document", "text"})
_STRUCTURAL_TAGS = frozenset({"html", "head", "body"})

# 브라우저의 "scope": 닫는 태그가 이 경계를 넘어 바깥 태그를 찾지 않는다. 표 칸 안의 짝 없는 `</div>`가
# 표 바깥 div를 닫아 표를 깨뜨리는 것을 막는다.
_DEFAULT_SCOPE = frozenset({"table", "td", "th", "caption", "html"})
_TABLE_PART_TAGS = frozenset({"td", "th", "tr", "thead", "tbody", "tfoot", "caption"})
# `<p>`를 닫는 블록 태그(HTML 명세의 목록 중 공시에 나오는 것).
_CLOSES_P = frozenset(
    {
        "address", "article", "aside", "blockquote", "center", "div", "dl", "fieldset", "figure", "footer", "form",
        "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "main", "menu", "nav", "ol", "p", "pre", "section",
        "table", "ul",
    }
)  # fmt: skip
# 여는 태그 → (닫을 열린 태그, 찾기를 멈출 경계)
_IMPLICIT_CLOSERS: dict[str, tuple[frozenset[str], frozenset[str]]] = {
    "li": (frozenset({"li"}), frozenset({"ul", "ol"}) | _DEFAULT_SCOPE),
    "dt": (frozenset({"dt", "dd"}), frozenset({"dl"}) | _DEFAULT_SCOPE),
    "dd": (frozenset({"dt", "dd"}), frozenset({"dl"}) | _DEFAULT_SCOPE),
    "tr": (frozenset({"tr"}), frozenset({"table"})),
    "td": (frozenset({"td", "th"}), frozenset({"tr", "table"})),
    "th": (frozenset({"td", "th"}), frozenset({"tr", "table"})),
    "thead": (frozenset({"thead", "tbody", "tfoot"}), frozenset({"table"})),
    "tbody": (frozenset({"thead", "tbody", "tfoot"}), frozenset({"table"})),
    "tfoot": (frozenset({"thead", "tbody", "tfoot"}), frozenset({"table"})),
    "option": (frozenset({"option"}), frozenset({"select"}) | _DEFAULT_SCOPE),
}
_P_CLOSER = (frozenset({"p"}), _DEFAULT_SCOPE | frozenset({"button"}))
# head 안에 올 수 있는 태그. 이 밖의 태그가 열리면 열린 head를 닫는다.
_HEAD_CONTENT = frozenset({"head", "title", "meta", "link", "style", "script", "base", "noscript"})
_HEAD_CLOSER = (frozenset({"head"}), frozenset({"html"}))
# 끝 태그를 생략해도 되는 요소(HTML 명세).
_OPTIONAL_END_TAGS = frozenset({"p", "li", "dt", "dd", "tr", "td", "th", "thead", "tbody", "tfoot", "option"})


@dataclass(eq=False, slots=True)
class Node:
    """요소 하나. `children`은 문서 순서의 `Node`와 텍스트(`str`). `line`·`column`은 여는 태그 위치(1부터)."""

    tag: str
    attrs: dict[str, str]
    line: int
    column: int
    children: list[Node | str] = field(default_factory=list)

    def iter(self) -> Iterator[Node]:
        """자신과 모든 하위 요소를 문서 순서로. 재귀 없이 돈다."""
        stack: list[Node] = [self]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(child for child in reversed(node.children) if isinstance(child, Node))

    def text(self) -> str:
        """하위 텍스트를 이어 붙인 것(공백 정규화 없음)."""
        parts: list[str] = []
        stack: list[Node | str] = [self]
        while stack:
            item = stack.pop()
            if isinstance(item, str):
                parts.append(item)
            else:
                stack.extend(reversed(item.children))
        return "".join(parts)


class _TreeBuilder(HTMLParser):
    def __init__(self, collector: ReportCollector) -> None:
        super().__init__(convert_charrefs=True)
        self.collector = collector
        self.root = Node(tag="#document", attrs={}, line=1, column=1)
        self.stack: list[Node] = [self.root]

    # HTMLParser 콜백 -------------------------------------------------------------------------------------------

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._open(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._open(tag, attrs, self_closing=True)

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            return
        index = self._find_open(tag, _TABLE_SCOPE_FOR.get(tag, _DEFAULT_SCOPE))
        if index is None:
            self._record(STRAY_END_TAG, f"</{tag}>")
            return
        inner = [node.tag for node in self.stack[index + 1 :]]
        if inner:
            # `<td><p>…</td>`처럼 끝 태그를 생략해도 되는 요소만 남았으면 정상 HTML이다.
            kind = IMPLICIT_CLOSE if all(name in _OPTIONAL_END_TAGS for name in inner) else MISNESTED_END
            self._record(kind, f"</{tag}> closes {' '.join(inner)}")
        del self.stack[index:]

    def handle_data(self, data: str) -> None:
        if data:
            self.stack[-1].children.append(data)

    # 내부 ------------------------------------------------------------------------------------------------------

    def _open(self, tag: str, attrs: list[tuple[str, str | None]], *, self_closing: bool) -> None:
        if self.stack[-1].tag in EDGAR_HEADER_TAGS:
            self.stack.pop()
        if self._is_unknown(tag):
            self.collector.unknown_tags[tag] += 1
            self._record(UNKNOWN_TAG, self.get_starttag_text() or tag)
        if tag not in _HEAD_CONTENT:
            # `</HEAD>` 없이 `<BODY>`나 본문 태그가 오면 브라우저는 head를 닫는다. 안 닫으면 head를 건너뛰는 선형화가
            # 본문 전체를 버린다(2006년 8-K에서 블록 0개).
            self._close_implicitly(tag, *_HEAD_CLOSER)
        if tag in _CLOSES_P:
            self._close_implicitly(tag, *_P_CLOSER)
        closer = _IMPLICIT_CLOSERS.get(tag)
        if closer is not None:
            self._close_implicitly(tag, *closer)
        line, offset = self.getpos()
        node = Node(tag=tag, attrs={name: value or "" for name, value in attrs}, line=line, column=offset + 1)
        self.stack[-1].children.append(node)
        # XHTML식 `<div/>`는 브라우저에서 열린 채로 남지만, 공시(Workiva 등)는 빈 요소 뜻으로 쓴다.
        if tag not in VOID_TAGS and not self_closing:
            self.stack.append(node)

    def _is_unknown(self, tag: str) -> bool:
        if tag in HTML_TAGS or tag in IX_TAGS or tag in EDGAR_TAGS or tag.startswith(_KNOWN_PREFIXES):
            return False
        # `ix:header` 안의 typed dimension은 회사가 정한 요소 이름(`us-gaap:…Axis.domain`)을 쓴다.
        return not (":" in tag and any(node.tag == "ix:header" for node in self.stack))

    def _close_implicitly(self, tag: str, targets: frozenset[str], boundary: frozenset[str]) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            open_tag = self.stack[index].tag
            if open_tag in targets:
                self._record(IMPLICIT_CLOSE, f"<{tag}> closes <{open_tag}>")
                del self.stack[index:]
                return
            if open_tag in boundary:
                return

    def _find_open(self, tag: str, boundary: frozenset[str]) -> int | None:
        for index in range(len(self.stack) - 1, 0, -1):
            open_tag = self.stack[index].tag
            if open_tag == tag:
                return index
            if open_tag in boundary:
                return None
        return None

    def _record(self, kind: str, context: str) -> None:
        line, offset = self.getpos()
        self.collector.add(kind, line, offset + 1, context)

    def finish(self) -> Node:
        self.close()
        for node in self.stack[1:]:
            if node.tag not in _STRUCTURAL_TAGS:
                self.collector.add(UNCLOSED_AT_EOF, node.line, node.column, f"<{node.tag}>")
        self.stack = [self.root]
        return self.root


# 표 부품의 닫는 태그는 표 안에서만 찾는다. `</table>`은 칸 경계를 넘어 자기 표를 찾는다.
_TABLE_SCOPE_FOR: dict[str, frozenset[str]] = {tag: frozenset({"table", "html"}) for tag in _TABLE_PART_TAGS}
_TABLE_SCOPE_FOR["table"] = frozenset({"html"})


def build_tree(html: str, collector: ReportCollector) -> Node:
    """문자열 전체를 트리로. 루트는 `#document`이다."""
    builder = _TreeBuilder(collector)
    builder.feed(html)
    return builder.finish()
