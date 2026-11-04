"""10-K 주석 표를 여러 해로 잇는다(`sec note-series`).

공시 한 편을 주석으로 나누는 일은 cluefin-sec-notes(`split_notes`)가 하고, 이 모듈은 나뉜 표를 해끼리 맞춘다.
네트워크를 쓰지 않는다 — 핸들러가 공시를 받아 `FilingNotes`로 넘긴다.

해를 이을 때 걸리는 문제와 푸는 순서:

1. 주석 번호가 바뀐다(Income Taxes 13번 → 7번 → 6번): 번호가 아니라 정규화한 제목으로 맞춘다.
2. 표 단위가 바뀐다(천 달러 → 백만 달러): 값을 백만으로 맞추고 원래 단위를 `unit_filed`로 남긴다.
3. 같은 주석 안의 표 순서가 바뀐다: 행 이름 집합의 Jaccard가 가장 높은 짝(0.5 이상, 못 넘으면 낱말 Jaccard 0.7 이상).
4. 행 이름이 바뀐다: 낱말 순서·복수형·구두점만 다르면 같은 행으로 보고, 그 밖에는 잇지 않고 `label_changed` 후보만 단다.
5. 다음 해 비교 열이 그해 값과 다르다(재작성): 고치지 않고 `restated`로 표시한다.

값은 각 10-K의 당해 열이다. 비교 열(전년)은 재작성 검사에만 쓴다.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from itertools import zip_longest

from cluefin_sec_notes import parse_amount

# 단위 → 백만 단위로 바꾸는 배수. 이 배수가 그 단위의 해상도(백만 단위)이기도 하다.
_TO_MILLIONS = {"thousands": Decimal("0.001"), "millions": Decimal(1), "billions": Decimal(1000)}
_UNIT_WORD = re.compile(r"\bin\s+(thousands|millions|billions)\b", re.IGNORECASE)
_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
_BARE_YEAR = re.compile(r"(?:19|20)\d{2}")
_WORD = re.compile(r"[a-z0-9]+")
_FOOTNOTE_MARK = re.compile(r"\((?:[a-z]|\d{1,2})\)|[*†]")
_DASHES = frozenset({"—", "–", "-", "−", "—%", "-%", "$—", "$-", "$ —"})
_PER_SHARE = re.compile(r"\bper\s+(?:share|unit)\b", re.IGNORECASE)

TABLE_MATCH_MIN = 0.5
"""표 짝을 지을 최소 Jaccard(행 이름 집합)."""
TABLE_WORD_MATCH_MIN = 0.7
"""행 이름 Jaccard가 모자랄 때 표 짝을 지을 최소 Jaccard(표 전체 낱말). 행이 갈라지거나("Foreign" → "Foreign - Korea",
"Foreign - Other") 합쳐진 표를 잇는다."""
TITLE_MATCH_MIN = 0.75
"""정규화한 제목이 같지 않을 때 주석 짝을 지을 최소 Jaccard(제목 낱말)."""
LABEL_CHANGE_MIN = 0.5
"""끊긴 행 두 개를 `label_changed` 후보로 묶을 최소 Jaccard(행 이름 낱말)."""
RESTATED_MIN = Decimal("0.005")
"""재작성으로 볼 최소 상대 차이. 그 아래는 반올림으로 본다."""

# 제목이 바뀐 주석. 정규화한 제목(낱말 순서 그대로) → 대표 제목.
TITLE_ALIASES = {
    "loss per share": "earnings per share",
    "income per share": "earnings per share",
    "income loss per share": "earnings per share",
    "earnings loss per share": "earnings per share",
    "loss income per share": "earnings per share",
}
_TITLE_DROP = frozenset({"net"})


# 입력 ----------------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TableInput:
    """주석 표 하나: `Table.grid()`와 `Table.unit`."""

    grid: tuple[tuple[str, ...], ...]
    unit: str | None


@dataclass(frozen=True, slots=True)
class NoteInput:
    number: int | None
    title: str
    tables: tuple[TableInput, ...]


@dataclass(frozen=True, slots=True)
class FilingNotes:
    """10-K 한 편의 주석.

    Attributes:
        fy: 회계연도. 당해 열("2025", "December 31, 2025")을 고르는 데 쓴다.
        statements_unit: 본표 단위. 단위가 적히지 않은 주석 표에 쓴다.
    """

    fy: int
    period_end: date | None
    accession_number: str
    notes: tuple[NoteInput, ...]
    statements_unit: str | None = None


# 표 읽기 --------------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ReadRow:
    """표 행 하나.

    Attributes:
        key: 해끼리 같은 행을 찾는 열쇠(구역·행 이름·열 머리를 정규화해 `/`로 이음).
        name: 구역을 뺀 행 이름 정규화. 구역 머리가 해마다 달라도 행을 잇는 데 쓴다.
        current, prior: 당해·전년 값(백만 단위, 퍼센트·주당 값은 그대로).
    """

    key: str
    name: str
    label: str
    section: str
    current: Decimal | None
    prior: Decimal | None
    unit_filed: str | None
    kind: str  # amount | percent | per_share


@dataclass(frozen=True, slots=True)
class ReadTable:
    rows: tuple[ReadRow, ...]

    @property
    def has_current(self) -> bool:
        return any(row.current is not None for row in self.rows)

    @property
    def names(self) -> frozenset[str]:
        return frozenset(row.name for row in self.rows)

    @property
    def words(self) -> frozenset[str]:
        return frozenset(word for row in self.rows for word in row.name.split())


def read_table(
    table: TableInput, fy: int, fallback_unit: str | None = None, period_year: int | None = None
) -> ReadTable:
    """행렬에서 당해 열과 전년 열 값을 읽는다.

    당해 열은 머리 연도가 `period_year`(기간말의 연도)인 열, 없으면 `fy`인 열이다. 회계연도가 1월에 끝나는 회사는
    머리가 "February 1, 2025"(기간말)이기도 하고 "Fiscal 2024"(회계연도)이기도 해서 둘 다 본다. 기간말 연도를 먼저 보는
    것은 "February 1, 2025 | February 3, 2024" 표에서 `fy`(2024)가 전년 열에 맞기 때문이다.

    - 열의 연도는 첫 값 행 위 머리 행에서 찾는다. 연도 머리 한 열 오른쪽에 제 머리가 있는 열(하위 열)도 그 해로 본다.
    - 연도 머리가 없는 표(만기표·가정표)는 값 열 전부를 당해 값으로 보고, 값 열이 둘 이상이면 열 머리를 행 열쇠에 붙인다.
      연도가 구역 머리에 있으면("December 31, 2024") 당해·전년 구역으로 읽는다.
    - 값 없는 행은 구역 머리("Current taxes:")다. 다음 합계 행("Total …", 구역 이름과 같은 행)에서 구역이 닫힌다.
    - 행 이름이 연도뿐이고 첫 해가 다음 회계연도면 만기표로 보고 상대 연도("fy+1")로 바꾼다. 그 밖의 연도 행(이월결손금 만료
      연도 등)은 그대로 둔다.
    """
    grid = [row for row in table.grid if any(cell.strip() for cell in row)]
    if not grid:
        return ReadTable(rows=())
    width = max(len(row) for row in grid)
    grid = [tuple(row) + ("",) * (width - len(row)) for row in grid]
    first_value = next((index for index, row in enumerate(grid) if _is_value_row(row)), len(grid))
    # 머리는 값 열에 글자가 있는 마지막 행까지. 그 뒤 첫 칸만 있는 행("Current taxes")은 구역 머리다.
    head_end = max(
        (index + 1 for index in range(first_value) if any(cell.strip() for cell in grid[index][1:])), default=0
    )
    body = grid[head_end:]
    headers = [" ".join(row[column] for row in grid[:head_end] if row[column]) for column in range(width)]
    year_columns = {column: year for column in range(1, width) if (year := _last_year(headers[column])) is not None}
    unit = table.unit or _head_unit(headers) or fallback_unit
    scale = _scale(unit)
    found = set(year_columns.values()) or {_last_year(row[0]) for row in body if not _is_value_row(row)}
    year = period_year if period_year is not None and period_year in found else fy
    if year_columns:
        current = _columns_for(year_columns, headers, body, year)
        prior = _columns_for(year_columns, headers, body, year - 1)
    else:
        current = [column for column in range(1, width) if any(_is_number(row[column]) for row in body)]
        prior = []
    # 당해 열과 같은 자리의 전년 열. 당해 열이 없는 표(전년 것만 남은 옛 서식)도 전년 값은 읽어 둔다.
    pairs = list(zip_longest(current, prior))
    suffixes = {
        column: normalize_label(_YEAR.sub("", headers[column])) or str(column)
        for pair in pairs
        for column in pair
        if column is not None
    }
    label_years = [int(row[0].strip()) for row in body if _BARE_YEAR.fullmatch(row[0].strip()) and _is_value_row(row)]
    # 만기표의 첫 해는 다음 회계연도다. 1월 결산 회사는 그 해를 기간말 연도로 적기도 해서 둘 다 본다.
    relative_to = min(label_years) - 1 if label_years and min(label_years) in (fy + 1, year + 1) else None

    rows: list[ReadRow] = []
    section, section_label, section_year = "", "", None
    for row in body:
        label = row[0].strip()
        if not _is_value_row(row):
            if label:
                section, section_year = _section(label)
                section_label = label
            continue
        stacked = not year_columns and section_year is not None
        if stacked and section_year not in (year, year - 1):
            continue
        name = _row_name(label, relative_to)
        for column, prior_column in pairs:
            shown = column if column is not None else prior_column
            kind = _kind(label, row[shown], headers[shown])
            multiplier = scale if kind == "amount" else None
            value = _value(row[column], multiplier) if column is not None else None
            prior_value = _value(row[prior_column], multiplier) if prior_column is not None else None
            if stacked and section_year == year - 1:
                value, prior_value = None, value
            if value is None and prior_value is None:
                continue
            suffix = suffixes[shown] if len(pairs) > 1 else ""
            key = "/".join(part for part in (section, name, suffix) if part)
            unit_filed = unit if kind == "amount" else None
            rows.append(ReadRow(key, name, label, section_label, value, prior_value, unit_filed, kind))
        if _closes_section(label, section):
            section, section_label, section_year = "", "", None
    return ReadTable(rows=tuple(_merge_stacked(rows)))


def _merge_stacked(rows: list[ReadRow]) -> list[ReadRow]:
    """당해 구역과 전년 구역에 나뉜 같은 행(한쪽은 당해 값만, 다른 쪽은 전년 값만)을 한 행으로 합친다."""
    merged: list[ReadRow] = []
    for row in rows:
        partner = next(
            (
                index
                for index, other in enumerate(merged)
                if other.key == row.key
                and (other.current is None) != (row.current is None)
                and (other.prior is None) != (row.prior is None)
            ),
            None,
        )
        if partner is None:
            merged.append(row)
            continue
        other = merged[partner]
        merged[partner] = ReadRow(
            other.key,
            other.name,
            other.label if other.current is not None else row.label,
            other.section if other.current is not None else row.section,
            other.current if other.current is not None else row.current,
            other.prior if other.prior is not None else row.prior,
            other.unit_filed or row.unit_filed,
            other.kind,
        )
    return merged


def _columns_for(year_columns: dict[int, int], headers: list[str], body: list[tuple[str, ...]], year: int) -> list[int]:
    """그 해 값 열. 연도 머리가 한 열에만 붙고 오른쪽 열에 제 머리(하위 열)가 있으면 그 열들도 그 해로 본다."""
    columns = [column for column, column_year in sorted(year_columns.items()) if column_year == year]
    if len(columns) != 1:
        return columns
    following = columns[0] + 1
    while following < len(headers) and following not in year_columns and headers[following].strip():
        if any(_is_number(row[following]) for row in body):
            columns.append(following)
        following += 1
    return columns


def _is_value_row(row: tuple[str, ...]) -> bool:
    return any(_is_number(cell) and not _BARE_YEAR.fullmatch(cell.strip()) for cell in row[1:])


def _is_number(text: str) -> bool:
    text = text.strip()
    return bool(text) and (text in _DASHES or parse_amount(text) is not None)


def _value(text: str, multiplier: Decimal | None) -> Decimal | None:
    """칸 값. 대시는 0. `multiplier`가 있으면 백만 단위로 바꾼다."""
    text = text.strip()
    if not text:
        return None
    if text in _DASHES:
        return Decimal(0)
    amount = parse_amount(text)
    if amount is None:
        return None
    return amount * multiplier if multiplier is not None else amount


def _last_year(text: str) -> int | None:
    found = _YEAR.findall(text)
    return int(found[-1]) if found else None


def _head_unit(headers: list[str]) -> str | None:
    return next((header for header in headers if _UNIT_WORD.search(header)), None)


def _scale(unit: str | None) -> Decimal | None:
    match = _UNIT_WORD.search(unit or "")
    return _TO_MILLIONS[match.group(1).lower()] if match else None


def _kind(label: str, cell: str, header: str) -> str:
    """값의 종류. 퍼센트("21.0%", 머리 "(%)")와 주당 값은 백만으로 바꾸지 않는다."""
    if "%" in cell or "%" in header:
        return "percent"
    if _PER_SHARE.search(label) or _PER_SHARE.search(header):
        return "per_share"
    return "amount"


def _section(label: str) -> tuple[str, int | None]:
    """구역 머리 → (정규화한 구역 이름, 구역 머리에 적힌 연도). 연도는 이름에서 뺀다("December 31, 2024")."""
    year = _last_year(label)
    return normalize_label(_YEAR.sub("", label)), year


def _closes_section(label: str, section: str) -> bool:
    """합계 행("Total net revenues", 구역 이름과 같은 "Current taxes")이 구역을 닫는다."""
    return bool(section) and (label.lower().startswith("total") or normalize_label(label) == section)


def _row_name(label: str, relative_to: int | None) -> str:
    stripped = label.strip()
    if relative_to is not None and _BARE_YEAR.fullmatch(stripped):
        return f"fy{int(stripped) - relative_to:+d}"
    return normalize_label(label)


def normalize_label(label: str) -> str:
    """행 이름 정규화: 소문자, 각주 표시·구두점 제거, 복수형 s 제거, 낱말 집합을 정렬.

    순서·복수형·중복만 다른 이름("Income tax expense (benefit)"과 "(benefit) expense")은 같아진다.
    """
    text = _FOOTNOTE_MARK.sub(" ", label.lower()).replace("&", " and ").replace("u.s.", "us").replace("u.s", "us")
    return " ".join(sorted({_singular(word) for word in _WORD.findall(text)}))


def _singular(word: str) -> str:
    return word[:-1] if len(word) > 3 and word.endswith("s") and not word.endswith("ss") else word


def normalize_title(title: str) -> str:
    """주석 제목 정규화: 소문자, 괄호·구두점·"net" 제거, 별칭 적용. 낱말 순서는 둔다."""
    words = [word for word in _WORD.findall(title.lower().replace("&", " and ")) if word not in _TITLE_DROP]
    text = " ".join(words)
    return TITLE_ALIASES.get(text, text)


def jaccard(left: Iterable[str], right: Iterable[str]) -> float:
    left, right = set(left), set(right)
    if not left and not right:
        return 0.0
    return len(left & right) / len(left | right)


# 시계열 ------------------------------------------------------------------------------------------------------------


@dataclass(slots=True)
class _RowSeries:
    """행 하나의 시계열. 해마다 당해 값과, 다음 해 공시가 비교 열에 적은 그해 값(`later`)."""

    key: str
    name: str
    kind: str
    values: dict[int, Decimal] = field(default_factory=dict)
    unit_filed: dict[int, str | None] = field(default_factory=dict)
    labels: dict[int, str] = field(default_factory=dict)
    sections: dict[int, str] = field(default_factory=dict)
    later: dict[int, Decimal] = field(default_factory=dict)
    later_unit: dict[int, str | None] = field(default_factory=dict)


@dataclass(slots=True)
class _TableSeries:
    rows: list[_RowSeries] = field(default_factory=list)
    index_by_fy: dict[int, int] = field(default_factory=dict)
    names: frozenset[str] = frozenset()
    words: frozenset[str] = frozenset()
    comparatives: list[tuple[int, ReadRow]] = field(default_factory=list)  # (비교 열의 해, 행)

    def find(self, key: str, name: str, fy: int) -> _RowSeries | None:
        """그해 값이 아직 없는 행 중 열쇠가 같은 것, 없으면 구역 빼고 이름이 같은 행이 하나뿐일 때 그것."""
        free = [row for row in self.rows if fy not in row.values]
        exact = next((row for row in free if row.key == key), None)
        if exact is not None:
            return exact
        same_name = [row for row in free if row.name == name]
        return same_name[0] if len(same_name) == 1 else None


@dataclass(slots=True)
class _NoteSeries:
    normalized: str
    numbers: dict[int, int | None] = field(default_factory=dict)
    titles: dict[int, str] = field(default_factory=dict)
    tables: list[_TableSeries] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)


def build_series(filings: list[FilingNotes], selector: Callable[[str, int | None], bool] | None = None) -> list[dict]:
    """주석 시계열. `filings`는 순서 무관(최근 해부터 맞춘다).

    `selector(title, number)`가 있으면 그 주석만 낸다. 번호는 최근 해의 번호로, 제목은 아무 해의 제목으로 묻는다.
    """
    ordered = sorted(filings, key=lambda filing: filing.fy, reverse=True)
    fys = [filing.fy for filing in ordered]
    series: list[_NoteSeries] = []
    for filing in ordered:
        _add_filing(series, filing)
    for note in series:
        for table in note.tables:
            _attach_comparatives(table)
    selected = [note for note in series if selector is None or _selected(note, selector, fys)]
    return [_note_payload(note, fys) for note in selected]


def _selected(note: _NoteSeries, selector: Callable[[str, int | None], bool], fys: list[int]) -> bool:
    latest = next(fy for fy in fys if fy in note.numbers)
    return selector(note.titles[latest], note.numbers[latest]) or any(
        selector(title, None) for title in note.titles.values()
    )


def _add_filing(series: list[_NoteSeries], filing: FilingNotes) -> None:
    used: set[int] = set()
    for note in filing.notes:
        if note.number is None:
            continue
        index = _match_note(series, note.title, used, filing.fy)
        if index is None:
            series.append(_NoteSeries(normalized=normalize_title(note.title)))
            index = len(series) - 1
        used.add(index)
        target = series[index]
        target.numbers[filing.fy] = note.number
        target.titles[filing.fy] = note.title
        _add_tables(target, note, filing)


def _match_note(series: list[_NoteSeries], title: str, used: set[int], fy: int) -> int | None:
    normalized = normalize_title(title)
    free = [index for index, note in enumerate(series) if index not in used and fy not in note.numbers]
    exact = next((index for index in free if series[index].normalized == normalized), None)
    if exact is not None:
        return exact
    scored = [(jaccard(normalized.split(), series[index].normalized.split()), index) for index in free]
    score, index = max(scored, default=(0.0, None))
    return index if score >= TITLE_MATCH_MIN else None


def _add_tables(note: _NoteSeries, source: NoteInput, filing: FilingNotes) -> None:
    read: list[tuple[int, ReadTable]] = []
    for index, table in enumerate(source.tables):
        period_year = filing.period_end.year if filing.period_end else None
        parsed = read_table(table, filing.fy, filing.statements_unit, period_year)
        if not parsed.rows:
            continue
        if not parsed.has_current:
            note.skipped.append({"fy": filing.fy, "table": index, "reason": "no current-year column"})
            continue
        read.append((index, parsed))
    assigned = _pair_tables(read, note.tables, filing.fy)
    for position, (index, parsed) in enumerate(read):
        if position in assigned:
            target = note.tables[assigned[position]]
        else:
            target = _TableSeries()
            note.tables.append(target)
        target.index_by_fy[filing.fy] = index
        target.names, target.words = parsed.names, parsed.words
        _add_rows(target, parsed, filing.fy)


def _pair_tables(read: list[tuple[int, ReadTable]], tables: list[_TableSeries], fy: int) -> dict[int, int]:
    """이 해 표(위치) → 표 시계열(위치). 점수가 높은 짝부터 하나씩."""
    pairs = []
    for position, (_, parsed) in enumerate(read):
        for series_index, series in enumerate(tables):
            if fy in series.index_by_fy:
                continue
            by_name, by_word = jaccard(parsed.names, series.names), jaccard(parsed.words, series.words)
            if by_name >= TABLE_MATCH_MIN or by_word >= TABLE_WORD_MATCH_MIN:
                pairs.append((by_name, by_word, position, series_index))
    assigned: dict[int, int] = {}
    taken: set[int] = set()
    for _, _, position, series_index in sorted(pairs, reverse=True):
        if position not in assigned and series_index not in taken:
            assigned[position] = series_index
            taken.add(series_index)
    return assigned


def _add_rows(table: _TableSeries, parsed: ReadTable, fy: int) -> None:
    previous: _RowSeries | None = None
    for row in parsed.rows:
        if row.prior is not None:
            table.comparatives.append((fy - 1, row))
        if row.current is None:
            continue  # 비교 열에만 있는 행(그해 삭제된 행)
        series = table.find(row.key, row.name, fy)
        if series is None:
            series = _RowSeries(key=row.key, name=row.name, kind=row.kind)
            position = table.rows.index(previous) + 1 if previous is not None else 0
            table.rows.insert(position, series)
        series.values[fy] = row.current
        series.unit_filed[fy] = row.unit_filed
        series.labels[fy] = row.label
        series.sections[fy] = row.section
        previous = series


def _attach_comparatives(table: _TableSeries) -> None:
    """다음 해 공시의 비교 열(전년 값)을 그해 행에 붙인다. 같은 표 시계열 안에서, 행은 `_TableSeries.find`처럼 찾는다."""
    for fy, row in table.comparatives:
        same_key = [series for series in table.rows if series.key == row.key and fy in series.values]
        candidates = same_key or [series for series in table.rows if series.name == row.name and fy in series.values]
        if len(candidates) == 1 and fy not in candidates[0].later:
            candidates[0].later[fy] = row.prior  # type: ignore[assignment]
            candidates[0].later_unit[fy] = row.unit_filed


# 출력 --------------------------------------------------------------------------------------------------------------


def _note_payload(note: _NoteSeries, fys: list[int]) -> dict:
    latest = next(fy for fy in fys if fy in note.numbers)
    present = [fy for fy in fys if fy in note.numbers]
    payload = {
        "title": note.titles[latest],
        "numbers_by_fy": {str(fy): note.numbers[fy] for fy in present},
        "titles_by_fy": {str(fy): note.titles[fy] for fy in present},
        "tables": [
            {
                "index_by_fy": {str(fy): table.index_by_fy[fy] for fy in fys if fy in table.index_by_fy},
                "unmatched": [fy for fy in present if fy not in table.index_by_fy],
                "rows": _rows_payload(table.rows, fys),
            }
            for table in note.tables
        ],
    }
    if note.skipped:
        payload["skipped_tables"] = note.skipped
    return payload


def _rows_payload(rows: list[_RowSeries], fys: list[int]) -> list[dict]:
    candidates = _label_changes(rows)
    payload = []
    for row in rows:
        latest = next(fy for fy in fys if fy in row.values)
        entry: dict = {"label": row.labels[latest]}
        if row.sections[latest]:
            entry["section"] = row.sections[latest]
        entry["kind"] = row.kind
        entry["values_by_fy"] = {str(fy): _number(row.values[fy]) for fy in fys if fy in row.values}
        units = {str(fy): row.unit_filed[fy] for fy in fys if row.unit_filed.get(fy)}
        if units:
            entry["unit_filed"] = units
        restated = _restated(row)
        if restated:
            entry["restated"] = restated
        if id(row) in candidates:
            entry["label_changed"] = candidates[id(row)]
        payload.append(entry)
    return payload


def _restated(row: _RowSeries) -> list[dict]:
    """다음 해 비교 열이 그해 당해 값과 다른 해. 차이가 두 단위 중 거친 쪽의 한 단위 미만이거나 0.5% 미만이면 같다고 본다.

    반 단위가 아니라 한 단위인 것은 합계를 맞추려 반올림 방향을 바꾸는 공시가 있어서다(천 달러 28,513 → 백만 달러 28).
    """
    flagged = []
    for fy, filed in sorted(row.values.items()):
        later = row.later.get(fy)
        if later is None:
            continue
        difference = abs(later - filed)
        resolution = max(_resolution(row.unit_filed.get(fy)), _resolution(row.later_unit.get(fy)))
        base = max(abs(filed), abs(later))
        if difference < resolution or base == 0 or difference / base < RESTATED_MIN:
            continue
        flagged.append({"fy": fy, "filed_value": _number(filed), "later_value": _number(later)})
    return flagged


def _resolution(unit: str | None) -> Decimal:
    return _scale(unit) or Decimal(0)


def _label_changes(rows: list[_RowSeries]) -> dict[int, list[str]]:
    """옛 행이 끝난 다음 해에 새 행이 시작하고(해가 겹치지 않음) 이름 낱말이 비슷하면 새 행에 옛 이름을 후보로 단다."""
    found: dict[int, list[str]] = {}
    for old in rows:
        old_last = max(old.values)
        old_words = set(old.name.split())
        for new in rows:
            if new is old or min(new.values) != old_last + 1 or new.kind != old.kind:
                continue
            if set(new.values) & set(old.values) or new.key.rpartition("/")[0] != old.key.rpartition("/")[0]:
                continue
            new_words = set(new.name.split())
            if jaccard(old_words, new_words) >= LABEL_CHANGE_MIN or old_words <= new_words or new_words <= old_words:
                found.setdefault(id(new), []).append(old.labels[old_last])
    return found


def _number(value: Decimal) -> float | int:
    """JSON 숫자. 정수면 int, 아니면 소수 셋째 자리까지(천 달러 → 백만 달러의 해상도)."""
    rounded = value.quantize(Decimal("0.001"))
    return int(rounded) if rounded == rounded.to_integral_value() else float(rounded)
