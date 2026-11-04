"""재무제표 Item(10-K Item 8)을 주석 단위로 나눈다(`split_notes`).

Item 블록을 순서대로 따라가며 "N. 제목" 헤딩에서 끊는다. 헤딩 모양은 세 가지다.

- 문단 하나: "3. Net Revenues", "Note 3 — Leases", "NOTE 3: INCOME TAXES"(굵기는 보지 않는다. 같은 회사도 해마다 다르다).
- 표 첫 행: "3." | "Net Revenues"(칸 둘로 짠 헤딩).
- 두 문단: "Note 3"과 다음 문단 "Leases".

본문 속 번호 목록("2. The Company recognizes …")과 헤딩을 가르는 것은 번호 순서다. 다음 번호(건너뛰면 두 개까지)만 헤딩으로
보고, 건너뛰면 `note_sequence_gap`을 낸다. 제목은 길이로 자르지 않는다(70자 넘는 제목이 있다).
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass

from cluefin_sec_notes._blocks import Block, Paragraph, Table
from cluefin_sec_notes._document import block_text
from cluefin_sec_notes._model import Finding, Item

NOTE_SEQUENCE_GAP = "note_sequence_gap"
"""주석 번호가 1부터 이어지지 않는다(번호를 건너뛰었다). 건너뛴 주석의 헤딩을 못 찾았을 수 있다."""
EMPTY_NOTE = "empty_note"
"""주석 헤딩 뒤에 본문이 없다(다음 헤딩이 바로 온다)."""

STATEMENTS_TITLE = "statements"
"""첫 주석 앞 구간(감사보고서·본표)의 제목."""

# "3. Title", "(3) Title", "3) Title", "Note 3 — Title", "NOTE 3: TITLE", "Note 3 Title", "Note C – Title", "C. TITLE".
# 번호만 있는 줄("Note 3", "3.")은 다음 문단이 제목이다.
_HEADING = re.compile(
    r"^(?P<prefix>(?:NOTE|Note|note)\s+)?"
    r"(?:\((?P<paren>\d{1,2}|[A-Z])\)|(?P<label>\d{1,2}|[A-Z])(?P<separator>[.:)—–-])?)"
    r"(?P<title>\s.*|[^\s\d].*)?$"
)
_HEADING_MAX_CHARS = 250
_TITLE_MAX_WORDS = 20
# 건너뛸 수 있는 번호 수. 헤딩 하나를 못 읽어도 뒤가 이어지게 하되, 본문 번호 목록을 헤딩으로 잡지 않을 만큼 좁게.
_MAX_SKIP = 2
# 제목 끝 마침표로 문장을 가른다. 약어로 끝나는 제목("… Co., Ltd.")은 예외.
_ABBREVIATIONS = ("inc.", "ltd.", "co.", "corp.", "l.p.", "llc.", "n.a.", "s.a.")


@dataclass(frozen=True, slots=True)
class Note:
    """주석 하나. `start`(헤딩 블록)부터 `end` 직전까지 `Item.blocks`의 구간.

    Attributes:
        number: 주석 순번. 숫자 번호는 그대로, 문자 번호("Note C")는 A=1부터 센 값. 첫 주석 앞 구간(감사보고서·본표)은
            None이고 제목은 "statements".
        label: 헤딩에 적힌 번호("3", "C"). 첫 주석 앞 구간은 None.
        title: 헤딩의 제목(번호·"Note"·구분 기호를 뗀 것). 길이로 자르지 않는다.
        blocks: 헤딩 블록을 포함한 구간의 블록.
    """

    number: int | None
    label: str | None
    title: str
    start: int
    end: int
    blocks: tuple[Block, ...]

    @property
    def tables(self) -> tuple[Table, ...]:
        """구간 안의 표(문서 순서). 단위는 `table.unit`, 열 맞춘 행렬은 `table.grid()`."""
        return tuple(block for block in self.blocks if isinstance(block, Table))

    @property
    def text(self) -> str:
        """헤딩을 포함한 구간 텍스트. `SecDocument.text`처럼 빈 블록을 빼고 빈 줄로 잇는다."""
        return "\n\n".join(text for block in self.blocks if (text := block_text(block)))


@dataclass(frozen=True, slots=True)
class NoteSplit:
    """`split_notes` 결과. 첫 원소는 첫 주석 앞 구간(`number=None`)이고, 헤딩을 하나도 못 찾으면 그것 하나뿐이다."""

    notes: tuple[Note, ...]
    findings: tuple[Finding, ...] = ()

    def note(self, number: int) -> Note | None:
        return next((note for note in self.notes if note.number == number), None)

    def __iter__(self) -> Iterator[Note]:
        return iter(self.notes)

    def __len__(self) -> int:
        return len(self.notes)


@dataclass(frozen=True, slots=True)
class _Heading:
    label: str
    title: str
    width: int  # 헤딩이 차지한 블록 수(번호와 제목이 두 문단이면 2)
    style: str = ""  # 번호 표기("Note", 괄호, 구분 기호). 한 공시의 주석 헤딩은 같은 표기를 쓴다.

    @property
    def lettered(self) -> bool:
        return not self.label.isdigit()

    @property
    def number(self) -> int:
        return int(self.label) if self.label.isdigit() else ord(self.label) - ord("A") + 1


def split_notes(item: Item) -> NoteSplit:
    """재무제표 Item을 주석으로 나눈다. 10-K Item 8, 10-Q Part I Item 1에 쓴다.

    1번(또는 A) 헤딩 후보마다 같은 번호 방식(숫자·문자)의 다음 번호를 따라 사슬을 만들고, 본문이 있는 주석이 가장 많은
    사슬(같으면 건너뛴 번호가 적은 것, 그다음 앞의 것)을 쓴다. 본표 아래 각주("(1) Including amounts from …")도 1부터
    이어지지만 본문 없이 붙어 있어 진짜 주석 사슬에 진다.
    """
    blocks = item.blocks
    candidates = [(index, heading) for index in range(len(blocks)) if (heading := _heading_at(blocks, index))]
    chains = [_chain(candidates, first) for first, (_, heading) in enumerate(candidates) if heading.number == 1]
    starts = max(chains, key=lambda chain: _score(chain, len(blocks)), default=[])

    findings: list[Finding] = []
    first = starts[0][0] if starts else len(blocks)
    notes = [Note(None, None, STATEMENTS_TITLE, 0, first, tuple(blocks[:first]))]
    for position, (start, heading) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(blocks)
        if position and heading.number > starts[position - 1][1].number + 1:
            previous = starts[position - 1][1]
            skipped = heading.number - previous.number - 1
            message = f"note {heading.label} follows note {previous.label} ({skipped} skipped)"
            findings.append(Finding(NOTE_SEQUENCE_GAP, message, key=item.key))
        if end - start <= heading.width:
            findings.append(Finding(EMPTY_NOTE, f"note {heading.label} has no body after its heading", key=item.key))
        notes.append(Note(heading.number, heading.label, heading.title, start, end, tuple(blocks[start:end])))
    return NoteSplit(notes=tuple(notes), findings=tuple(findings))


def _chain(candidates: list[tuple[int, _Heading]], first: int) -> list[tuple[int, _Heading]]:
    chain = [candidates[first]]
    for index, heading in candidates[first + 1 :]:
        last_index, last = chain[-1]
        if index >= last_index + last.width and _follows(heading, last):
            chain.append((index, heading))
    return chain


def _score(chain: list[tuple[int, _Heading]], total: int) -> tuple[int, int, int]:
    """(본문 있는 주석 수, -건너뛴 번호 수, 가장 흔한 번호 표기를 쓴 헤딩 수).

    마지막 값은 본표 각주 "(1) …" 하나로 시작해 "NOTE 2 –"로 이어지는 사슬이 진짜 "NOTE 1 –" 사슬과 비길 때 가른다.
    """
    ends = [index for index, _ in chain[1:]] + [total]
    with_body = sum(1 for (start, heading), end in zip(chain, ends, strict=True) if end - start > heading.width)
    skipped = chain[-1][1].number - len(chain)
    styles = Counter(heading.style for _, heading in chain)
    return with_body, -skipped, styles.most_common(1)[0][1]


def _follows(heading: _Heading, previous: _Heading) -> bool:
    expected = previous.number + 1
    return heading.lettered == previous.lettered and expected <= heading.number <= expected + _MAX_SKIP


def _heading_at(blocks: tuple[Block, ...], index: int) -> _Heading | None:
    block = blocks[index]
    if isinstance(block, Table):
        return _table_heading(block)
    if not isinstance(block, Paragraph) or len(block.text) > _HEADING_MAX_CHARS:
        return None
    parsed = _parse(" ".join(block.text.split()))
    if parsed is None:
        return None
    label, title, style = parsed
    if title:
        return _Heading(label, title.rstrip(":"), 1, style) if _is_title(title) else None
    # "Note 3" / "3." 뒤 문단이 제목.
    following = blocks[index + 1] if index + 1 < len(blocks) else None
    if not isinstance(following, Paragraph) or len(following.text) > _HEADING_MAX_CHARS:
        return None
    title = " ".join(following.text.split())
    return _Heading(label, title.rstrip(":"), 2, style) if _is_title(title) else None


def _table_heading(table: Table) -> _Heading | None:
    """첫 행(빈 행은 건너뜀)이 "3." | "Net Revenues"인 표. 칸이 셋 이상이면 데이터 표다."""
    for row in table.rows:
        cells = [" ".join(cell.text.split()) for cell in row if cell.text.strip()]
        if not cells:
            continue
        if len(cells) > 2:
            return None
        parsed = _parse(" ".join(cells))
        if parsed is None or not parsed[1] or not _is_title(parsed[1]):
            return None
        return _Heading(parsed[0], parsed[1].rstrip(":"), 1, parsed[2])
    return None


def _parse(text: str) -> tuple[str, str, str] | None:
    """헤딩이면 (번호, 제목, 표기). 제목이 없으면 빈 글자. 번호 뒤 구분 기호(".", ")", "—", 괄호)나 앞 "Note"가 없으면 None.

    "Note"가 붙었거나 대문자뿐인 제목은 끝 마침표를 떼고 본다("NOTE 1 – BASIS OF PREPARATION."). 그 밖의 끝 마침표는
    문장이라는 뜻으로 남겨 `_is_title`이 거른다.
    """
    match = _HEADING.match(text)
    if match is None:
        return None
    label = match.group("paren") or match.group("label")
    if not (match.group("paren") or match.group("separator") or match.group("prefix")):
        return None
    title = (match.group("title") or "").lstrip(" .:)—–-").rstrip()
    if match.group("prefix") or title.upper() == title:
        title = title.rstrip(".")
    style = ("note " if match.group("prefix") else "") + (
        "()" if match.group("paren") else match.group("separator") or ""
    )
    return label, title, style


def _is_title(title: str) -> bool:
    """제목다운가. 소문자로 시작하지 않고, 낱말이 많지 않고, 문장처럼 마침표로 끝나지 않는다."""
    if not title or title[0].islower() or not (title[0].isalnum() or title[0] in "(["):
        return False
    if len(title.split()) > _TITLE_MAX_WORDS:
        return False
    lowered = title.lower()
    return not (lowered.endswith((".", ";", ",")) and not lowered.endswith(_ABBREVIATIONS))
