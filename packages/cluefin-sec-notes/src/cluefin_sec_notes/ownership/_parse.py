"""Form 3·4·5 XML(`ownershipDocument`) 파서.

원본 XML은 공시 폴더 바로 아래에 있다. 제출 이력의 주 문서명(`xslF345X05/form4.xml`)은 SEC가 XSL로 렌더링한
HTML 경로라, 앞의 `xslF345X0n/`을 떼고 받는다.

값 칸은 `<value>`와 선택적 `<footnoteId id="F1"/>`로 되어 있고, 거래 코드처럼 `<value>` 없이 글자를 바로 담는 칸도 있다.
행은 아래 필드 표(필드명, 행 안의 경로, 변환기)로 채운다. 예상 밖의 불리언·숫자·날짜는 조용히 버리지 않고 `ValueError`를 낸다.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import NamedTuple

from defusedxml.ElementTree import ParseError, fromstring

from cluefin_sec_notes.ownership._model import (
    DOCUMENT_TYPES,
    Holding,
    Issuer,
    OwnershipDocument,
    ReportingOwner,
    Signature,
    Transaction,
)
from cluefin_sec_notes.ownership._xml import Element

_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_TRUE = frozenset({"1", "true"})
_FALSE = frozenset({"0", "false"})


def _text(raw: str) -> str:
    return raw


def _decimal(raw: str) -> Decimal:
    try:
        number = Decimal(raw)
    except InvalidOperation:
        raise ValueError(f"숫자가 아닙니다: {raw!r}") from None
    if not number.is_finite():
        raise ValueError(f"숫자가 아닙니다: {raw!r}")
    return number


def _date(raw: str) -> date:
    # XML date 형식은 시간대를 붙일 수 있다(2005-08-14-05:00). 날짜 부분만 쓴다.
    match = _DATE.match(raw)
    if not match:
        raise ValueError(f"날짜가 아닙니다: {raw!r}")
    return date.fromisoformat(match.group())


def _bool(raw: str) -> bool:
    lowered = raw.lower()
    if lowered in _TRUE:
        return True
    if lowered in _FALSE:
        return False
    raise ValueError(f"불리언이 아닙니다: {raw!r}")


class _Field(NamedTuple):
    name: str
    path: str
    convert: Callable[[str], object]
    # 각주가 값 칸이 아니라 그 부모에 붙는 칸(거래 코드는 transactionCoding에 붙는다).
    notes_path: str | None = None


_TRANSACTION_FIELDS = (
    _Field("security_title", "securityTitle", _text),
    _Field("date", "transactionDate", _date),
    _Field("deemed_execution_date", "deemedExecutionDate", _date),
    _Field("form_type", "transactionCoding/transactionFormType", _text),
    _Field("code", "transactionCoding/transactionCode", _text, notes_path="transactionCoding"),
    _Field("equity_swap", "transactionCoding/equitySwapInvolved", _bool),
    _Field("timeliness", "transactionTimeliness", _text),
    _Field("shares", "transactionAmounts/transactionShares", _decimal),
    _Field("total_value", "transactionAmounts/transactionTotalValue", _decimal),
    _Field("price", "transactionAmounts/transactionPricePerShare", _decimal),
    _Field("acquired_disposed", "transactionAmounts/transactionAcquiredDisposedCode", _text),
    _Field("shares_owned_after", "postTransactionAmounts/sharesOwnedFollowingTransaction", _decimal),
    _Field("value_owned_after", "postTransactionAmounts/valueOwnedFollowingTransaction", _decimal),
    _Field("direct_indirect", "ownershipNature/directOrIndirectOwnership", _text),
    _Field("nature_of_ownership", "ownershipNature/natureOfOwnership", _text),
)
_HOLDING_FIELDS = (
    _Field("security_title", "securityTitle", _text),
    _Field("shares_owned", "postTransactionAmounts/sharesOwnedFollowingTransaction", _decimal),
    _Field("value_owned", "postTransactionAmounts/valueOwnedFollowingTransaction", _decimal),
    _Field("direct_indirect", "ownershipNature/directOrIndirectOwnership", _text),
    _Field("nature_of_ownership", "ownershipNature/natureOfOwnership", _text),
)
_DERIVATIVE_FIELDS = (
    _Field("exercise_price", "conversionOrExercisePrice", _decimal),
    _Field("exercise_date", "exerciseDate", _date),
    _Field("expiration_date", "expirationDate", _date),
    _Field("underlying_title", "underlyingSecurity/underlyingSecurityTitle", _text),
    _Field("underlying_shares", "underlyingSecurity/underlyingSecurityShares", _decimal),
    _Field("underlying_value", "underlyingSecurity/underlyingSecurityValue", _decimal),
)


def load_ownership(path: str | Path) -> OwnershipDocument:
    """파일에서 Form 3·4·5 XML을 읽는다. `parse_ownership` 참고."""
    return parse_ownership(Path(path).read_bytes())


def parse_ownership(source: bytes | str) -> OwnershipDocument:
    """Form 3·4·5(정정 포함) XML을 읽는다.

    Raises:
        ValueError: XML이 아니거나, 루트가 `ownershipDocument`가 아니거나, 서식이 3·4·5가 아니거나,
            불리언·숫자·날짜 칸에 예상 밖의 값이 있을 때
    """
    try:
        root: Element = fromstring(source)
    except ParseError as error:
        raise ValueError(f"XML을 읽을 수 없습니다: {error}") from None
    if root.tag != "ownershipDocument":
        raise ValueError(f"소유 신고 XML이 아닙니다(루트 {root.tag!r})")
    document_type = _plain(root, "documentType")
    if document_type not in DOCUMENT_TYPES:
        raise ValueError(f"Form 3·4·5가 아닙니다: documentType={document_type!r}")

    derivative_fields = _TRANSACTION_FIELDS + _DERIVATIVE_FIELDS
    return OwnershipDocument(
        schema_version=_plain(root, "schemaVersion"),
        document_type=document_type,
        period_of_report=_convert(root, "periodOfReport", _date),
        date_of_original_submission=_convert(root, "dateOfOriginalSubmission", _date),
        issuer=_issuer(root),
        reporting_owners=tuple(_owner(node) for node in root.findall("reportingOwner")),
        non_derivative_transactions=_rows(
            root, "nonDerivativeTable/nonDerivativeTransaction", _TRANSACTION_FIELDS, derivative_fields, Transaction
        ),
        non_derivative_holdings=_rows(
            root,
            "nonDerivativeTable/nonDerivativeHolding",
            _HOLDING_FIELDS,
            _HOLDING_FIELDS + _DERIVATIVE_FIELDS,
            Holding,
        ),
        derivative_transactions=_rows(
            root, "derivativeTable/derivativeTransaction", derivative_fields, derivative_fields, Transaction
        ),
        derivative_holdings=_rows(
            root,
            "derivativeTable/derivativeHolding",
            _HOLDING_FIELDS + _DERIVATIVE_FIELDS,
            _HOLDING_FIELDS + _DERIVATIVE_FIELDS,
            Holding,
        ),
        footnotes=_footnotes(root),
        remarks=_plain(root, "remarks"),
        signatures=tuple(
            Signature(name=_plain(node, "signatureName"), date=_convert(node, "signatureDate", _date))
            for node in root.findall("ownerSignature")
        ),
        aff10b5_one=_convert(root, "aff10b5One", _bool),
        not_subject_to_section16=_convert(root, "notSubjectToSection16", _bool),
        no_securities_owned=_convert(root, "noSecuritiesOwned", _bool),
        form3_holdings_reported=_convert(root, "form3HoldingsReported", _bool),
        form4_transactions_reported=_convert(root, "form4TransactionsReported", _bool),
    )


def _issuer(root: Element) -> Issuer:
    return Issuer(
        cik=_plain(root, "issuer/issuerCik") or "",
        name=_plain(root, "issuer/issuerName"),
        trading_symbol=_plain(root, "issuer/issuerTradingSymbol"),
    )


def _owner(node: Element) -> ReportingOwner:
    relationship = "reportingOwnerRelationship"
    return ReportingOwner(
        cik=_plain(node, "reportingOwnerId/rptOwnerCik") or "",
        name=_plain(node, "reportingOwnerId/rptOwnerName"),
        # 빠진 관계 칸은 그 관계가 아니라는 뜻이다(표본 476건 중 isOther·isTenPercentOwner 생략이 흔하다).
        is_director=bool(_convert(node, f"{relationship}/isDirector", _bool)),
        is_officer=bool(_convert(node, f"{relationship}/isOfficer", _bool)),
        is_ten_percent_owner=bool(_convert(node, f"{relationship}/isTenPercentOwner", _bool)),
        is_other=bool(_convert(node, f"{relationship}/isOther", _bool)),
        officer_title=_plain(node, f"{relationship}/officerTitle"),
        other_text=_plain(node, f"{relationship}/otherText"),
    )


def _rows(
    root: Element,
    path: str,
    fields: tuple[_Field, ...],
    all_fields: tuple[_Field, ...],
    model: type[Transaction] | type[Holding],
) -> tuple:
    """한 표의 행들. 표에 없는 필드(비파생 행의 행사가 등)는 None으로 채운다."""
    derivative = path.startswith("derivativeTable")
    present = {field.name for field in fields}
    rows = []
    for node in root.findall(path):
        values: dict[str, object] = {field.name: None for field in all_fields if field.name not in present}
        notes: dict[str, tuple[str, ...]] = {}
        for field in fields:
            values[field.name], ids = _cell(node, field)
            if ids:
                notes[field.name] = ids
        rows.append(model(derivative=derivative, footnote_ids=notes, **values))
    return tuple(rows)


def _cell(node: Element, field: _Field) -> tuple[object, tuple[str, ...]]:
    """한 칸의 값과 각주 ID."""
    cell = node.find(field.path)
    if cell is None:
        return None, ()
    holder = node.find(field.notes_path) if field.notes_path else cell
    ids = tuple(note.get("id") or "" for note in holder.findall("footnoteId")) if holder is not None else ()
    value_node = cell.find("value")
    raw = _strip(value_node.text if value_node is not None else cell.text)
    if raw is None:
        return None, ids
    try:
        return field.convert(raw), ids
    except ValueError as error:
        raise ValueError(f"{field.path}: {error}") from None


def _footnotes(root: Element) -> dict[str, str]:
    entries = []
    for note in root.findall("footnotes/footnote"):
        entries.append((note.get("id") or "", _strip(note.text) or ""))
    return dict(entries)


def _plain(node: Element, path: str) -> str | None:
    return _strip(node.findtext(path))


def _convert(node: Element, path: str, convert: Callable[[str], object]):
    raw = _plain(node, path)
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
