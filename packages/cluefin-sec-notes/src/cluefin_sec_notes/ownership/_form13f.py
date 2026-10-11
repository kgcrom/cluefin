"""13F 표지(`edgarSubmission`)·정보표(`informationTable`) XML 파서.

공시 폴더에는 표지 `primary_doc.xml`과 정보표 XML 하나가 있다. 정보표 파일명은 공시마다 다르다(`infotable.xml`,
`form13fInfoTable.xml`, 숫자 이름 …). 제출 이력의 주 문서명(`xslForm13F_X02/primary_doc.xml`)은 XSL 렌더링 경로라
파일명만 떼어 받는다. 두 XML 모두 네임스페이스가 있다(Form 3·4·5에는 없다).

정보표는 5만 행(23MB)까지 있어 `iterparse`로 행을 하나씩 읽고 버린다(전체 파싱과 시간은 같고 메모리가 1/30).
예상 밖의 숫자·날짜·불리언은 조용히 버리지 않고 `ValueError`를 낸다.
"""

from __future__ import annotations

import io
import re
import statistics
from collections.abc import Callable, Iterator
from datetime import date
from pathlib import Path
from typing import BinaryIO

from defusedxml.ElementTree import ParseError, fromstring, iterparse

from cluefin_sec_notes.ownership._form13f_model import (
    DOLLAR_VALUES_FROM,
    FORM13F_TYPES,
    Form13F,
    Form13FCover,
    Form13FHolding,
    Form13FManager,
    Form13FTable,
)
from cluefin_sec_notes.ownership._xml import Element

_COVER_NS = "{http://www.sec.gov/edgar/thirteenffiler}"
_TABLE_NS = "{http://www.sec.gov/edgar/document/thirteenf/informationtable}"
# 0을 채우지 않은 날짜(2-8-2018)도 있었다.
_DATE = re.compile(r"(?P<month>\d{1,2})-(?P<day>\d{1,2})-(?P<year>\d{4})")
# 소수점 아래가 0뿐인 정수(12300.00)도 있었다.
_INTEGER = re.compile(r"(?P<whole>-?\d+)(?:\.0*)?")
_SEPARATORS = re.compile(r"[\s,]+")
_SHARES_TYPES = frozenset({"SH", "PRN"})
_PUT_CALL = frozenset({"Put", "Call"})
_DISCRETIONS = frozenset({"SOLE", "DFND", "OTR"})
_TRUE = frozenset({"true", "y"})
_FALSE = frozenset({"false", "n"})

SUSPECT_PRICE_RANGE = (1, 5000)
"""달러로 맞춘 뒤 주식 행 주당 금액(`value / shares`) 중앙값이 이 범위 밖이면 단위를 의심한다.

표본 92건: 제대로 적은 공시는 5.8–300, 경계 뒤에 천 달러로 낸 것은 0.08–0.15, 경계 전에 달러로 낸 것은 43,840.
"""


def load_13f(cover_path: str | Path, table_path: str | Path | None = None, *, filed: date) -> Form13F:
    """공시 폴더에서 받은 표지와 정보표를 읽는다. 통지(13F-NT)는 `table_path`를 비워 둔다.

    Args:
        cover_path: 표지 `primary_doc.xml`
        table_path: 정보표 XML. 13F-HR이면 필수.
        filed: 제출일(`FilingEntry.filing_date`). `value` 단위가 제출일로 갈린다(`DOLLAR_VALUES_FROM`).

    Raises:
        ValueError: `parse_13f_cover`·`parse_13f_table`과 같은 경우, 또는 보유 보고인데 정보표가 없을 때
    """
    cover = parse_13f_cover(Path(cover_path).read_bytes())
    if table_path is None:
        if not cover.is_notice:
            raise ValueError(f"{cover.submission_type}에는 정보표가 있어야 합니다")
        return Form13F(cover=cover, table=None)
    with open(table_path, "rb") as stream:
        return Form13F(cover=cover, table=_read_table(stream, filed))


def parse_13f_cover(source: bytes | str) -> Form13FCover:
    """13F 표지 XML(`primary_doc.xml`)을 읽는다.

    Raises:
        ValueError: XML이 아니거나, 루트가 13F 표지가 아니거나, 서식이 13F가 아니거나, 숫자·날짜·불리언 칸에
            예상 밖의 값이 있을 때
    """
    try:
        root: Element = fromstring(source)
    except ParseError as error:
        raise ValueError(f"XML을 읽을 수 없습니다: {error}") from None
    if root.tag != f"{_COVER_NS}edgarSubmission":
        raise ValueError(f"13F 표지 XML이 아닙니다(루트 {root.tag!r})")
    submission_type = _plain(root, "headerData/submissionType", _COVER_NS)
    if submission_type not in FORM13F_TYPES:
        raise ValueError(f"13F가 아닙니다: submissionType={submission_type!r}")

    cover, summary, signature = "formData/coverPage", "formData/summaryPage", "formData/signatureBlock"
    return Form13FCover(
        submission_type=submission_type,
        report_type=_cover_text(root, f"{cover}/reportType"),
        period_of_report=_cover(root, "headerData/filerInfo/periodOfReport", _date),
        filer_cik=_cover_text(root, "headerData/filerInfo/filer/credentials/cik"),
        manager_name=_cover_text(root, f"{cover}/filingManager/name"),
        form13f_file_number=_cover_text(root, f"{cover}/form13FFileNumber"),
        amendment_no=_cover(root, f"{cover}/amendmentNo", _integer),
        amendment_type=_cover_text(root, f"{cover}/amendmentInfo/amendmentType"),
        conf_denied_expired=_cover(root, f"{cover}/amendmentInfo/confDeniedExpired", _bool),
        other_managers=tuple(
            _manager(node, None) for node in _findall(root, f"{cover}/otherManagersInfo/otherManager", _COVER_NS)
        ),
        included_managers=tuple(
            _manager(_find(node, "otherManager", _COVER_NS), _cover(node, "sequenceNumber", _integer))
            for node in _findall(root, f"{summary}/otherManagers2Info/otherManager2", _COVER_NS)
        ),
        other_included_managers_count=_cover(root, f"{summary}/otherIncludedManagersCount", _integer),
        table_entry_total=_cover(root, f"{summary}/tableEntryTotal", _integer),
        table_value_total=_cover(root, f"{summary}/tableValueTotal", _integer),
        is_confidential_omitted=_cover(root, f"{summary}/isConfidentialOmitted", _bool),
        signature_name=_cover_text(root, f"{signature}/name"),
        signature_title=_cover_text(root, f"{signature}/title"),
        signature_date=_cover(root, f"{signature}/signatureDate", _date),
    )


def parse_13f_table(source: bytes | str, *, filed: date) -> Form13FTable:
    """13F 정보표 XML(`informationTable`)을 읽는다.

    Args:
        source: 정보표 XML
        filed: 제출일. 2023-01-03 전이면 `value`(천 달러)에 1,000을 곱한다.

    Raises:
        ValueError: XML이 아니거나, 루트가 정보표가 아니거나, 숫자 칸에 정수가 아닌 값이 있을 때
    """
    data = source.encode() if isinstance(source, str) else source
    return _read_table(io.BytesIO(data), filed)


def _read_table(stream: BinaryIO, filed: date) -> Form13FTable:
    multiplier = 1 if filed >= DOLLAR_VALUES_FROM else 1000
    holdings = tuple(_holding(node, multiplier) for node in _table_rows(stream))
    return Form13FTable(holdings=holdings, value_multiplier=multiplier, value_unit_suspect=_unit_suspect(holdings))


def _table_rows(stream: BinaryIO) -> Iterator[Element]:
    """정보표의 `infoTable` 요소를 하나씩 내고, 다 읽은 행은 비운다."""
    row_tag = f"{_TABLE_NS}infoTable"
    events = iterparse(stream, events=("start", "end"))
    try:
        _, root = next(events)
        if root.tag != f"{_TABLE_NS}informationTable":
            raise ValueError(f"13F 정보표 XML이 아닙니다(루트 {root.tag!r})")
        for event, node in events:
            if event == "end" and node.tag == row_tag:
                yield node
                node.clear()
    except ParseError as error:
        raise ValueError(f"XML을 읽을 수 없습니다: {error}") from None


def _holding(node: Element, multiplier: int) -> Form13FHolding:
    value = _table(node, "value", _integer)
    cusip = _table_text(node, "cusip")
    other_managers = _table_text(node, "otherManager")
    return Form13FHolding(
        name_of_issuer=_table_text(node, "nameOfIssuer"),
        title_of_class=_table_text(node, "titleOfClass"),
        cusip=cusip.upper() if cusip else None,
        figi=_table_text(node, "figi"),
        value=value * multiplier if value is not None else None,
        shares=_table(node, "shrsOrPrnAmt/sshPrnamt", _integer),
        shares_type=_table(node, "shrsOrPrnAmt/sshPrnamtType", _one_of(_SHARES_TYPES)),
        put_call=_table(node, "putCall", _one_of(_PUT_CALL)),
        investment_discretion=_table(node, "investmentDiscretion", _one_of(_DISCRETIONS)),
        other_managers=_numbers(other_managers),
        other_managers_text=other_managers,
        voting_sole=_table(node, "votingAuthority/Sole", _integer),
        voting_shared=_table(node, "votingAuthority/Shared", _integer),
        voting_none=_table(node, "votingAuthority/None", _integer),
    )


def _unit_suspect(holdings: tuple[Form13FHolding, ...]) -> bool:
    prices = [(row.value or 0) / (row.shares or 1) for row in holdings if _priced_share_row(row)]
    if not prices:
        return False
    low, high = SUSPECT_PRICE_RANGE
    return not low <= statistics.median(prices) <= high


def _priced_share_row(row: Form13FHolding) -> bool:
    return row.shares_type == "SH" and (row.shares or 0) > 0 and (row.value or 0) > 0


def _manager(node: Element | None, sequence_number: int | None) -> Form13FManager:
    def text(path: str) -> str | None:
        return _plain(node, path, _COVER_NS) if node is not None else None

    return Form13FManager(
        sequence_number=sequence_number,
        cik=text("cik"),
        name=text("name"),
        form13f_file_number=text("form13FFileNumber"),
        crd_number=text("crdNumber"),
        sec_file_number=text("secFileNumber"),
    )


def _integer(raw: str) -> int:
    match = _INTEGER.fullmatch(raw)
    if not match:
        raise ValueError(f"정수가 아닙니다: {raw!r}")
    return int(match.group("whole"))


def _numbers(raw: str | None) -> tuple[int, ...]:
    """다른 운용사 순번 목록. 쉼표나 공백으로 나눈다("1,2,15", "1 2", "1, 2").

    이 칸은 자유 텍스트라 "None"·"N/A"·"-"·운용사 이름도 있었다. 숫자가 아닌 토큰이 하나라도 있으면 빈 튜플이고,
    원문은 `other_managers_text`에 남는다.
    """
    parts = [part for part in _SEPARATORS.split(raw or "") if part]
    if not all(part.isascii() and part.isdigit() for part in parts):
        return ()
    return tuple(int(part) for part in parts)


def _one_of(allowed: frozenset[str]) -> Callable[[str], str]:
    def convert(raw: str) -> str:
        if raw not in allowed:
            raise ValueError(f"{sorted(allowed)} 중 하나가 아닙니다: {raw!r}")
        return raw

    return convert


def _date(raw: str) -> date:
    match = _DATE.fullmatch(raw)
    if not match:
        raise ValueError(f"날짜(MM-DD-YYYY)가 아닙니다: {raw!r}")
    groups = match.groupdict()
    return date(int(groups["year"]), int(groups["month"]), int(groups["day"]))


def _bool(raw: str) -> bool:
    lowered = raw.lower()
    if lowered in _TRUE:
        return True
    if lowered in _FALSE:
        return False
    raise ValueError(f"불리언이 아닙니다: {raw!r}")


def _cover_text(node: Element, path: str) -> str | None:
    return _plain(node, path, _COVER_NS)


def _cover(node: Element, path: str, convert: Callable[[str], object]):
    return _convert(node, path, _COVER_NS, convert)


def _table_text(node: Element, path: str) -> str | None:
    return _plain(node, path, _TABLE_NS)


def _table(node: Element, path: str, convert: Callable[[str], object]):
    return _convert(node, path, _TABLE_NS, convert)


def _qualified(path: str, namespace: str) -> str:
    return "/".join(namespace + part for part in path.split("/"))


def _find(node: Element, path: str, namespace: str) -> Element | None:
    return node.find(_qualified(path, namespace))


def _findall(node: Element, path: str, namespace: str) -> list[Element]:
    return node.findall(_qualified(path, namespace))


def _plain(node: Element, path: str, namespace: str) -> str | None:
    return _strip(node.findtext(_qualified(path, namespace)))


def _convert(node: Element, path: str, namespace: str, convert: Callable[[str], object]):
    raw = _plain(node, path, namespace)
    if raw is None:
        return None
    try:
        return convert(raw)
    except ValueError as error:
        raise ValueError(f"{path}: {error}") from None


def _strip(raw: str | None) -> str | None:
    if raw is None:
        return None
    stripped = raw.strip()
    return stripped or None
