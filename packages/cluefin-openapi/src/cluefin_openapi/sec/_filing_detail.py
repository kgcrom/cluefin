"""공시 상세 페이지(`{접수번호}-index.html`) 읽기.

`index.json`은 파일명만 주고 문서 종류(EX-99.1 등)를 주지 않는다. `-index-headers.html`(SGML 헤더)은 2015년 이후
공시에만 받힌다(그 전은 폴더 목록에 있어도 404, 2026-10 실측). 상세 페이지는 2001년 공시까지 같은 모양이라 이것을 읽는다.
"""

from __future__ import annotations

from datetime import date
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlsplit

from ._archives_types import FilingDetail, FilingDocument, FilingParty
from ._exceptions import SecAPIError
from ._ids import accession_dashed, accession_plain

# 문서 표의 칸: Seq | Description | Document | Type | Size
_DOCUMENT_CELLS = 5


class _DetailPage(HTMLParser):
    """상세 페이지에서 서식명, 정보 칸(infoHead/info), 문서 표 행, 당사자(companyName)를 모은다."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.form = ""
        self.info: dict[str, str] = {}
        self.rows: list[tuple[bool, list[str], str]] = []
        self.parties: list[tuple[str, str]] = []
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._label = ""
        self._in_form_name = False
        self._data_files: bool | None = None
        self._cells: list[str] | None = None
        self._href = ""
        self._cik = ""

    def _start(self, what: str) -> None:
        self._capture = what
        self._buffer = []

    def _finish(self) -> str:
        self._capture = None
        return "".join(self._buffer)

    def handle_starttag(self, tag: str, attrs) -> None:
        attributes = dict(attrs)
        css = attributes.get("class") or ""
        href = attributes.get("href") or ""
        if tag == "div" and attributes.get("id") == "formName":
            self._in_form_name = True
        elif tag == "strong" and self._in_form_name:
            self._start("form")
        elif tag == "div" and css in ("infoHead", "info"):
            self._start(css)
        elif tag == "br" and self._capture == "info":
            self._buffer.append("\n")
        elif tag == "table" and "tableFile" in css:
            self._data_files = attributes.get("summary") == "Data Files"
        elif tag == "tr" and self._data_files is not None:
            self._cells, self._href = [], ""
        elif tag == "td" and self._cells is not None:
            self._start("cell")
        elif tag == "a" and self._capture == "cell" and not self._href:
            self._href = href
        elif tag == "span" and css == "companyName":
            self._start("party")
            self._cik = ""
        elif tag == "a" and self._capture == "party" and "action=getcompany" in href:
            self._cik = (parse_qs(urlsplit(href).query).get("CIK") or [""])[0]

    def handle_endtag(self, tag: str) -> None:
        if tag == "strong" and self._capture == "form":
            self.form = _squash(self._finish())
            self._in_form_name = False
        elif tag == "div" and self._capture == "infoHead":
            self._label = _squash(self._finish())
        elif tag == "div" and self._capture == "info":
            self.info[self._label] = self._finish()
        elif tag == "td" and self._capture == "cell" and self._cells is not None:
            self._cells.append(_squash(self._finish()))
        elif tag == "tr" and self._cells is not None:
            if len(self._cells) == _DOCUMENT_CELLS and self._data_files is not None:
                self.rows.append((self._data_files, self._cells, self._href))
            self._cells = None
        elif tag == "table":
            self._data_files = None
        elif tag == "span" and self._capture == "party":
            self.parties.append((_squash(self._finish()), self._cik))

    def handle_data(self, data: str) -> None:
        if self._capture:
            # Only <br> separates lines in an info cell; source line breaks are plain whitespace.
            self._buffer.append(data.replace("\n", " "))


def parse_filing_detail(html: str, accession_number: str) -> FilingDetail:
    """상세 페이지 HTML을 읽는다. 서식명이 없으면(다른 페이지) `SecAPIError`."""
    page = _DetailPage()
    page.feed(html)
    page.close()
    form = page.form.removeprefix("Form ").strip()
    if not form:
        raise SecAPIError(f"공시 상세 페이지에서 서식을 찾지 못했습니다: {accession_number}")

    folder = f"/{accession_plain(accession_number)}/"
    return FilingDetail(
        accession_number=accession_dashed(accession_number),
        form=form,
        filing_date=_date(page.info.get("Filing Date")),
        period_of_report=_date(page.info.get("Period of Report")),
        items=_lines(page.info.get("Items")),
        documents=[_document(data_file, cells, href, folder) for data_file, cells, href in page.rows],
        parties=[party for text, cik in page.parties if (party := _party(text, cik)) is not None],
    )


def _document(data_file: bool, cells: list[str], href: str, folder: str) -> FilingDocument:
    sequence, description, shown, kind, size = cells
    # 인라인 XBRL 문서는 뷰어 링크(`/ix?doc=/Archives/...`)다. 폴더 뒤 경로가 파일명(Form 4 렌더링은 하위 폴더 포함).
    path = href.partition("doc=")[2] or href
    name = path.partition(folder)[2] or shown
    return FilingDocument(
        sequence=_int(sequence),
        description=description or None,
        name=name,
        type=kind or None,
        size=_int(size),
        data_file=data_file,
    )


def _party(text: str, cik: str) -> FilingParty | None:
    """`MICRON TECHNOLOGY INC (Issuer) CIK: 0000723125 (see all company filings)` → 이름·역할·CIK."""
    number = _int(cik)
    if number is None:
        return None
    label = text.partition(" CIK:")[0].strip()
    name, _, role = label.rpartition(" (")
    if not name:
        return FilingParty(cik=number, name=label)
    return FilingParty(cik=number, name=name, role=role.removesuffix(")") or None)


def _squash(text: str) -> str:
    return " ".join(text.split())


def _lines(text: str | None) -> list[str]:
    return [line for line in map(_squash, (text or "").split("\n")) if line]


def _int(text: str) -> int | None:
    text = text.strip()
    return int(text) if text.isdigit() else None


def _date(text: str | None) -> date | None:
    try:
        return date.fromisoformat(_squash(text or ""))
    except ValueError:
        return None
