"""공시 주 문서 하나를 읽는다."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from cluefin_sec_notes._blocks import Block, Paragraph, Table, linearize
from cluefin_sec_notes._decode import decode_html
from cluefin_sec_notes._furniture import Page, remove_page_furniture
from cluefin_sec_notes._report import ENCODING_FALLBACK, ParseReport, ReportCollector
from cluefin_sec_notes._tree import build_tree

# 표지에서 서식을 찾는 범위(블록 수). 표지는 문서 맨 앞 한두 페이지다.
_COVER_BLOCKS = 80
_COVER_FORM = re.compile(r"\bFORM\s+(10-KT?|10-K405|10-QT?|8-K)(\s*/\s*A)?\b", re.IGNORECASE)
_MONTH_DATE = r"[A-Z][a-z]{2,8}\.?\s+\d{1,2}\s*,?\s*\d{4}"
# 표지의 "For the fiscal year ended December 31, 2025", "For the quarterly period ended June 30, 2025",
# 8-K의 "Date of Report (Date of earliest event reported): May 1, 2025"
_COVER_PERIOD = re.compile(
    rf"(?:year|period)\s+ended:?\s*({_MONTH_DATE})|date\s+of\s+report[^:]*:?\s*({_MONTH_DATE})", re.IGNORECASE
)
_DATE_FORMATS = ("%Y-%m-%d", "%B %d %Y", "%b %d %Y", "%m/%d/%Y")


@dataclass(frozen=True, eq=False)
class SecDocument:
    """공시 주 문서.

    Attributes:
        blocks: 문서 순서의 문단·표·페이지 경계.
        anchors: 문서 안 링크가 가리키는 앵커 → 그 앵커가 시작하는 블록 위치. 뒤에 블록이 없으면 `len(blocks)`.
        form: 서식(`10-K`, `10-Q`, `8-K`, 정정은 `/A`). 호출자가 준 값, 인라인 XBRL `dei:DocumentType`,
            2000년대 공시를 감싼 EDGAR SGML의 `<TYPE>`, 표지 순으로 정한다. 못 정하면 None.
        dei: 인라인 XBRL의 `dei:` 사실(`DocumentType`, `EntityRegistrantName`, `DocumentPeriodEndDate` …).
            2019년 이전 공시는 비어 있다.
        pages: 쪽 구간과 머리말·꼬리말의 쪽 번호. 쪽 경계가 없는 공시는 비어 있다.
        period_end: 보고 기간 말(`dei:DocumentPeriodEndDate`, 없으면 표지의 "fiscal year ended …").
            카탈로그의 Item 적용 시점(1C 등)을 판단하는 데 쓴다. 못 찾으면 None.
        report: 읽으며 고친 것.
        source: 파일에서 읽었으면 그 경로.
    """

    blocks: tuple[Block, ...]
    anchors: dict[str, int]
    form: str | None
    dei: dict[str, str]
    report: ParseReport
    source: Path | None = None
    period_end: date | None = None
    pages: tuple[Page, ...] = ()

    def text(self, start: int = 0, end: int | None = None) -> str:
        """블록 구간의 텍스트. 문단은 그대로, 표는 행마다 칸을 탭으로 잇는다. 블록 사이는 빈 줄."""
        return "\n\n".join(block_text(block) for block in self.blocks[start:end] if block_text(block))


def block_text(block: Block) -> str:
    if isinstance(block, Paragraph):
        return block.text
    if isinstance(block, Table):
        return "\n".join("\t".join(cell.text for cell in row) for row in block.rows if any(cell.text for cell in row))
    return ""


def parse_filing(data: bytes | str, *, form: str | None = None, source: Path | None = None) -> SecDocument:
    """원문 바이트(또는 디코딩한 문자열)를 읽는다.

    Args:
        data: 주 문서 HTML. 바이트면 선언된 인코딩 → UTF-8 → windows-1252 순으로 디코딩한다.
        form: 서식을 알면 준다(`FilingEntry.form`). 없으면 문서에서 찾는다.
    """
    collector = ReportCollector()
    if isinstance(data, bytes):
        html, encoding, declared = decode_html(data)
        if declared is not None and encoding != declared:
            collector.add(ENCODING_FALLBACK, 1, 1, f"declared {declared}, read as {encoding}")
    else:
        html, encoding, declared = data, "str", None
    linearized = linearize(build_tree(html, collector), collector)
    kept, mapping, pages = remove_page_furniture(linearized.blocks, collector)
    blocks = tuple(kept)
    anchors = {
        name: mapping[index] if index < len(mapping) else len(blocks) for name, index in linearized.anchors.items()
    }
    return SecDocument(
        blocks=blocks,
        anchors=anchors,
        pages=tuple(pages),
        form=_normalize_form(form)
        or _normalize_form(linearized.dei.get("DocumentType"))
        or _normalize_form(linearized.edgar_header.get("type"))
        or _cover_form(blocks),
        dei=linearized.dei,
        report=collector.build(encoding, declared),
        source=source,
        period_end=parse_date(linearized.dei.get("DocumentPeriodEndDate")) or _cover_period(blocks),
    )


def load_filing(path: Path | str, *, form: str | None = None) -> SecDocument:
    """파일에서 읽는다. `cluefin_openapi.sec`의 `archives.download_filing_document()`로 받은 주 문서."""
    path = Path(path)
    return parse_filing(path.read_bytes(), form=form, source=path)


def _normalize_form(form: str | None) -> str | None:
    if not form:
        return None
    return re.sub(r"\s+", "", form).upper() or None


def _cover_form(blocks: tuple[Block, ...]) -> str | None:
    for block in blocks[:_COVER_BLOCKS]:
        text = block.text if isinstance(block, Paragraph) else block_text(block)
        match = _COVER_FORM.search(text)
        if match:
            return match.group(1).upper() + ("/A" if match.group(2) else "")
    return None


def parse_date(text: str | None) -> date | None:
    """ "2025-12-31", "December 31, 2025", "Dec. 31, 2025", "12/31/2025"."""
    if not text:
        return None
    cleaned = re.sub(r"\s+", " ", text.replace(",", " ").replace(".", " ")).strip()
    cleaned = re.sub(r"\bSept\b", "Sep", cleaned, flags=re.IGNORECASE)
    for date_format in _DATE_FORMATS:
        try:
            return datetime.strptime(cleaned, date_format).date()
        except ValueError:
            continue
    return None


def _cover_period(blocks: tuple[Block, ...]) -> date | None:
    for block in blocks[:_COVER_BLOCKS]:
        match = _COVER_PERIOD.search(block_text(block).replace("\n", " "))
        if match:
            return parse_date(match.group(1) or match.group(2))
    return None
