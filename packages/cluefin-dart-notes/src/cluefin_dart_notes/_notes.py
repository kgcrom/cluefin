"""재무제표 주석을 노트 단위로 나눈다."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Literal

from cluefin_dart_notes._blocks import Block, Heading, Paragraph
from cluefin_dart_notes._document import DartDocument, Section
from cluefin_dart_notes._find import find_section

logger = logging.getLogger(__name__)

Basis = Literal["consolidated", "separate"]
SplitMethod = Literal["heading", "sequence"]

# 노트 소제목의 번호: "7", "9-1", "6-A", "9&10", "15 & 16".
_HEADING_NUMBER = re.compile(r"\s*(\d+(?:\s*[-&]\s*(?:\d+|[A-Za-z]))*)\s*\.\s*(.*)", re.DOTALL)
_BASIS_SUFFIX = re.compile(r"\s*\((?:연결|별도)\)\s*$")
# 순번 유도 탐색에서 제목 뒤에 와야 하는 글자: 한글·영문·여는 괄호. "2.1"·"57.18" 같은 숫자는 제목이 아니다.
_TITLE_START = r"(?=[가-힣A-Za-z(])"
# 문단 중간 제목 앞에 올 수 있는 문장 끝 글자.
_SENTENCE_END = r"(?<=[다요음함됨임.)\]」』])"
_MAX_TITLE_LENGTH = 40
# 굵은 구간을 제목으로 볼 최대 길이. 이보다 길면 굵게 쓴 본문이다.
_MAX_BOLD_TITLE_LENGTH = 60
# 제목과 본문이 붙어 있을 때 본문이 시작하는 표지: 주어("회사는"·"주식회사"·"당기"…)나 하위 번호("가."·"(1)"·"1)"·"1.1").
_BODY_START = re.compile(
    r"\s?(?:(?:연결)?회사[는의가]|주식회사|지배(?:기업|회사)[은는의가]|당사[는의가]|당(?:반|분)?기\s|당(?:반|분)?기말"
    r"|전기말|보고기간\s?말\s?현재|(?:연결)?재무제표(?:는|를|\s?작성에는)"
    r"|가\.\s|\(1\)|1\)\s|\d+\.\d+\.?\s?)"
)
# 노트가 끝난 뒤에도 이 범위의 번호가 문단 시작에 보이면 놓친 노트일 수 있다고 경고한다.
_LOOKAHEAD_NUMBERS = 4


@dataclass(frozen=True, eq=False)
class Note:
    """주석 노트 하나.

    Attributes:
        number: 노트 번호. 문자열로 둔다("7", "9-1", "6-A", "9&10").
        title: 제목(번호, 끝의 "(연결)"·"(별도)", 콜론 제외).
        basis: 연결(consolidated) 또는 별도(separate) 재무제표의 주석.
        heading: 원문의 제목 줄 그대로(예: "7. 유형자산 (연결)").
        blocks: 제목 다음부터 다음 노트 전까지의 블록.
    """

    number: str
    title: str
    basis: Basis
    heading: str
    blocks: tuple[Block, ...] = field(repr=False)


@dataclass(frozen=True, eq=False)
class NoteSplit:
    """주석 섹션 하나를 나눈 결과와 진단.

    Attributes:
        method: heading(노트별 소제목으로 나눔) 또는 sequence(문단의 번호를 1, 2, 3… 순서로 따라가며 나눔).
        preamble: 첫 노트 앞의 블록.
        warnings: 번호가 빠졌거나, 놓친 노트가 있어 보이는 경우.
    """

    section: Section
    basis: Basis
    method: SplitMethod
    notes: tuple[Note, ...]
    preamble: tuple[Block, ...] = ()
    warnings: tuple[str, ...] = ()


def notes_sections(document: DartDocument) -> list[tuple[Section, Basis]]:
    """문서의 주석 섹션과 그 기준(연결·별도). 정기보고서는 연결·별도 순서, 감사보고서는 "주석" 하나."""
    if document.is_audit_report:
        section = find_section(document, title="주석")
        basis: Basis = "consolidated" if document.document_code == "00761" else "separate"
        return [(section, basis)] if section is not None else []
    found: list[tuple[Section, Basis]] = []
    for code, title, basis in (
        ("D-0-3-3-0", "연결재무제표 주석", "consolidated"),
        ("D-0-3-5-0", "재무제표 주석", "separate"),
    ):
        section = find_section(document, assoc_code=code) or find_section(document, title=title)
        if section is not None:
            found.append((section, basis))
    return found


def extract_notes(document: DartDocument) -> list[Note]:
    """문서의 모든 주석 노트(연결 다음 별도). 분할 경고는 로그로 남는다. 진단이 필요하면 `split_notes`를 쓴다."""
    notes: list[Note] = []
    for section, basis in notes_sections(document):
        result = split_notes(section, basis)
        for warning in result.warnings:
            logger.warning("%s %s: %s", document.rcept_no or document.company_name, section.title, warning)
        notes.extend(result.notes)
    return notes


def split_notes(section: Section, basis: Basis) -> NoteSplit:
    """주석 섹션을 노트로 나눈다. 노트별 소제목(`Heading`)이 있으면 그것으로, 없으면 순번 유도 탐색으로."""
    blocks = section.blocks
    if any(isinstance(block, Heading) and _HEADING_NUMBER.fullmatch(block.text) for block in blocks):
        return _split_by_headings(section, basis, blocks)
    return _SequenceSplitter(section, basis).split(blocks)


# --- 소제목 방식 ------------------------------------------------------------


def _split_by_headings(section: Section, basis: Basis, blocks: tuple[Block, ...]) -> NoteSplit:
    builder = _NoteBuilder(basis)
    for block in blocks:
        match = _HEADING_NUMBER.fullmatch(block.text) if isinstance(block, Heading) else None
        if match:
            builder.start(_compact_number(match.group(1)), match.group(2), block.text)
        else:
            builder.add(block)
    return NoteSplit(section, basis, "heading", builder.notes(), builder.preamble_blocks())


# --- 순번 유도 탐색 -----------------------------------------------------------


@dataclass(frozen=True)
class _Hit:
    number: int
    start: int  # 제목 줄이 시작하는 위치("N.")
    title_end: int  # 제목이 끝나는 위치
    body_start: int  # 본문이 시작하는 위치(콜론 뒤 등)


class _SequenceSplitter:
    """노트 소제목이 없는 문서(오래된 공시, 비상장사, 감사보고서)를 문단의 번호로 나눈다.

    다음 번호 N(또는 하나 건너뛴 N+1)만 찾는다. 후보는 세 가지다.
      - 문단 시작의 `N. 제목` (콜론 없어도 됨)
      - 문단 중간, 문장 끝 바로 뒤의 `N. 제목 :` (콜론 필수)
      - 문단 중간이라도 굵은 구간이 `N. 제목`으로 시작하는 곳 (콜론 없어도 됨)
    표 셀은 블록 단계에서 이미 빠져 있어 후보가 아니다("4. 당기순이익" 같은 셀 오탐 방지).
    """

    def __init__(self, section: Section, basis: Basis) -> None:
        self.section = section
        self.builder = _NoteBuilder(basis)
        self.expected = 1
        self.warnings: list[str] = []

    def split(self, blocks: tuple[Block, ...]) -> NoteSplit:
        for block in blocks:
            if isinstance(block, Paragraph):
                self._paragraph(block)
            else:
                self.builder.add(block)
        notes = self.builder.notes()
        if notes:
            self._warn_possible_misses(notes[-1])
        else:
            self.warnings.append("노트를 하나도 찾지 못했습니다.")
        return NoteSplit(
            self.section, self.builder.basis, "sequence", notes, self.builder.preamble_blocks(), tuple(self.warnings)
        )

    def _paragraph(self, paragraph: Paragraph) -> None:
        allow_start = True
        while True:
            hit = self._find(paragraph, allow_start)
            if hit is None:
                self.builder.add(paragraph)
                return
            before = _slice(paragraph, 0, hit.start)
            if before.text:
                self.builder.add(before)
            if hit.number == self.expected + 1:
                self.warnings.append(f"{self.expected}번 노트가 없습니다({hit.number}번으로 건너뜀).")
            heading = paragraph.text[hit.start : hit.title_end].strip()
            match = _HEADING_NUMBER.fullmatch(heading)
            title = match.group(2) if match else heading
            self.builder.start(str(hit.number), title, heading)
            self.expected = hit.number + 1
            paragraph = _slice(paragraph, hit.body_start, len(paragraph.text))
            allow_start = False
            if not paragraph.text:
                return

    def _find(self, paragraph: Paragraph, allow_start: bool) -> _Hit | None:
        hits = [
            hit
            for number in (self.expected, self.expected + 1)
            for hit in (
                _start_hit(paragraph, number) if allow_start else None,
                _colon_hit(paragraph, number),
                _bold_hit(paragraph, number),
            )
            if hit is not None
        ]
        return min(hits, key=lambda hit: (hit.start, hit.number)) if hits else None

    def _warn_possible_misses(self, last: Note) -> None:
        later = range(self.expected + 1, self.expected + 1 + _LOOKAHEAD_NUMBERS)
        for block in last.blocks:
            if not isinstance(block, Paragraph):
                continue
            number = next((n for n in later if _start_hit(block, n)), None)
            if number is not None:
                self.warnings.append(
                    f"마지막 {last.number}번 노트 안에 {number}번 제목 같은 문단이 있습니다. 노트를 놓쳤을 수 있습니다."
                )
                return


def _start_hit(paragraph: Paragraph, number: int) -> _Hit | None:
    match = re.match(rf"\s*{number}\.\s*{_TITLE_START}", paragraph.text)
    if match is None:
        return None
    return _title_bounds(paragraph, number, 0) or _line_title(paragraph, number)


def _colon_hit(paragraph: Paragraph, number: int) -> _Hit | None:
    pattern = rf"{_SENTENCE_END}\s*({number}\.\s*{_TITLE_START}[^.:：\n]{{1,{_MAX_TITLE_LENGTH}}}?)\s*[:：]"
    match = re.search(pattern, paragraph.text)
    if match is None:
        return None
    return _Hit(number, match.start(1), match.end(1), match.end())


def _bold_hit(paragraph: Paragraph, number: int) -> _Hit | None:
    for start, _ in paragraph.bold_spans:
        if start > 0 and re.match(rf"{number}\.\s*{_TITLE_START}", paragraph.text[start:]):
            return _title_bounds(paragraph, number, start)
    return None


def _title_bounds(paragraph: Paragraph, number: int, start: int) -> _Hit | None:
    """`start`에서 시작하는 굵은 구간이 제목이면 그 끝까지가 제목이다."""
    for span_start, span_end in paragraph.bold_spans:
        if span_start == start and span_end - start <= _MAX_BOLD_TITLE_LENGTH:
            end = _cut_long_title(paragraph.text, _cut_at_colon(paragraph.text, start, span_end), start)
            return _Hit(number, start, end, _skip_colon(paragraph.text, end))
    return None


def _line_title(paragraph: Paragraph, number: int) -> _Hit:
    """굵은 구간이 없을 때: 첫 줄(콜론이 있으면 콜론 앞)이 제목이다. 본문이 붙어 있으면 `_cut_long_title`로 자른다."""
    text = paragraph.text
    line_end = text.find("\n")
    line_end = len(text) if line_end < 0 else line_end
    end = _cut_long_title(text, _cut_at_colon(text, 0, line_end), 0)
    return _Hit(number, 0, end, _skip_colon(text, end))


def _cut_at_colon(text: str, start: int, end: int) -> int:
    colon = min((i for i in (text.find(":", start, end), text.find("：", start, end)) if i >= 0), default=-1)
    return colon if colon >= 0 else end


def _skip_colon(text: str, end: int) -> int:
    return end + 1 if end < len(text) and text[end] in ":：" else end


def _cut_long_title(text: str, end: int, start: int) -> int:
    """제목과 본문이 표시 없이 붙은 첫 줄("32. 보고기간후사건회사는 …")에서 제목 끝을 고른다.

    원문(주로 감사보고서)에 경계 정보가 없어 본문이 흔히 시작하는 말 앞에서 자른다. 없는데 제목(번호 제외)이
    40자를 넘으면 40자 안의 마지막 공백·마침표에서 자른다.
    """
    number_end = re.compile(r"\s*\d+\.\s*").match(text, start)
    title_start = number_end.end() if number_end else start
    marker = _BODY_START.search(text, title_start + 2, min(end, title_start + _MAX_TITLE_LENGTH))
    if marker:
        return marker.start()
    if end - title_start <= _MAX_TITLE_LENGTH:
        return end
    limit = title_start + _MAX_TITLE_LENGTH
    cut = max(text.rfind(" ", title_start, limit), text.rfind(".", title_start, limit))
    return cut if cut > 0 else limit


# --- 공통 -----------------------------------------------------------------


class _NoteBuilder:
    def __init__(self, basis: Basis) -> None:
        self.basis = basis
        self.collected: list[Note] = []
        self._preamble: list[Block] = []
        self._current: tuple[str, str, str] | None = None
        self._blocks: list[Block] = []

    def start(self, number: str, title: str, heading: str) -> None:
        self._flush()
        self._current = (number, _clean_title(title), heading)

    def add(self, block: Block) -> None:
        (self._blocks if self._current else self._preamble).append(block)

    def notes(self) -> tuple[Note, ...]:
        self._flush()
        return tuple(self.collected)

    def preamble_blocks(self) -> tuple[Block, ...]:
        return tuple(self._preamble)

    def _flush(self) -> None:
        if self._current is None:
            return
        number, title, heading = self._current
        self.collected.append(Note(number, title, self.basis, heading, tuple(self._blocks)))
        self._current = None
        self._blocks = []


def _clean_title(title: str) -> str:
    return _BASIS_SUFFIX.sub("", title.strip().rstrip(":：").strip())


def _compact_number(number: str) -> str:
    return re.sub(r"\s+", "", number)


def _slice(paragraph: Paragraph, start: int, end: int) -> Paragraph:
    """문단의 일부를 새 문단으로. 굵은 구간은 잘라서 옮긴다. 앞뒤 공백은 지운다."""
    raw = paragraph.text[start:end]
    stripped_left = len(raw) - len(raw.lstrip())
    text = raw.strip()
    offset = start + stripped_left
    spans = tuple(
        (max(a, offset) - offset, min(b, offset + len(text)) - offset)
        for a, b in paragraph.bold_spans
        if min(b, offset + len(text)) > max(a, offset)
    )
    return Paragraph(text, spans)
