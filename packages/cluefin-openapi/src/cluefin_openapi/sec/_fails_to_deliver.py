"""Fails-to-Deliver 데이터 (www.sec.gov/data-research/sec-markets-data/fails-deliver-data).

결제일·CUSIP·티커가 한 행에 있어 SEC 안에서 CUSIP→티커를 얻을 수 있는 원천이다. 13F 정보표에는 티커가 없다.
결제 불이행이 한 번이라도 있었던 종목만 실리지만, 6개월치로 2026년 13F 12건의 금액 99.7–99.9%가 매핑됐다(2026-10 실측).
"""

from __future__ import annotations

import io
import re
import zipfile
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Dict, Iterable, List, Optional

from ._client import WWW_BASE_URL, Client
from ._exceptions import SecAPIError
from ._fails_to_deliver_types import FailsToDeliverFile, FailToDeliver

LIST_URL = f"{WWW_BASE_URL}/data-research/sec-markets-data/fails-deliver-data"

# 파일 폴더는 시기마다 다르고(fails-deliver-data, other/…, frequently-requested-foia-document-…, node/add/…)
# 이름 끝에 `_0`이 붙은 것도 있어 URL을 조립하지 않고 목록 페이지의 링크를 읽는다.
_LINK = re.compile(
    r'href="(?P<path>/files/[\w/-]+/(?P<name>cnsfails(?P<year>\d{4})(?P<month>\d{2})(?P<half>[ab]))(?:_\d+)?\.zip)"'
)
_HEADER = "SETTLEMENT DATE|CUSIP|SYMBOL|QUANTITY (FAILS)|DESCRIPTION|PRICE"
_TRAILER_COUNT = re.compile(r"Trailer record count (?P<count>\d+)")
_TRAILER = "Trailer "


class FailsToDeliver:
    """SEC Fails-to-Deliver 파일 (2009-07~, 반월마다 하나)"""

    def __init__(self, client: Client):
        self.client = client

    def files(self) -> List[FailsToDeliverFile]:
        """받을 수 있는 파일 목록 (최신순)."""
        html = self.client._get_bytes(LIST_URL).decode("utf-8", "replace")
        found = {}
        for match in _LINK.finditer(html):
            groups = match.groupdict()
            found[groups["name"]] = FailsToDeliverFile(
                name=groups["name"],
                year=int(groups["year"]),
                month=int(groups["month"]),
                half=groups["half"],
                path=groups["path"],
            )
        if not found:
            raise SecAPIError(f"Fails-to-Deliver 목록에 파일 링크가 없습니다: {LIST_URL}")
        return sorted(found.values(), key=lambda file: file.name, reverse=True)

    def records(self, file: FailsToDeliverFile) -> List[FailToDeliver]:
        """파일 하나의 행 (약 5–7만 행, zip 1–2MB).

        Raises:
            SecAPIError: zip 안 파일이 하나가 아니거나, 머리글·열 수가 예상과 다르거나, 끝의 레코드 수와 행 수가 다를 때
        """
        data = self.client._get_bytes(f"{WWW_BASE_URL}{file.path}")
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            members = archive.infolist()
            if len(members) != 1:
                raise SecAPIError(f"zip 안 파일이 하나가 아닙니다: {file.name} {[m.filename for m in members]}")
            text = archive.read(members[0]).decode("latin-1")
        return _parse(text, file.name)


def cusip_symbols(records: Iterable[FailToDeliver]) -> Dict[str, str]:
    """CUSIP → 티커. 한 CUSIP에 티커가 여럿이면(티커 변경) 결제일이 가장 늦은 것을 쓴다.

    결제일이 같으면 나중에 나온 행이 이긴다. 티커가 없는 행은 건너뛴다.
    """
    latest: Dict[str, FailToDeliver] = {}
    for record in records:
        if not record.symbol:
            continue
        current = latest.get(record.cusip)
        if current is None or record.settlement_date >= current.settlement_date:
            latest[record.cusip] = record
    return {cusip: record.symbol or "" for cusip, record in latest.items()}


def _parse(text: str, name: str) -> List[FailToDeliver]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != _HEADER:
        raise SecAPIError(f"Fails-to-Deliver 머리글이 다릅니다: {name} {lines[:1]!r}")
    rows: List[FailToDeliver] = []
    expected: Optional[int] = None
    for number, line in enumerate(lines[1:], start=2):
        if line.startswith(_TRAILER):
            count = _TRAILER_COUNT.fullmatch(line.strip())
            expected = int(count.group("count")) if count else expected
            continue
        if line.strip():
            rows.append(_row(line, f"{name}:{number}"))
    if expected is not None and expected != len(rows):
        raise SecAPIError(f"Fails-to-Deliver 레코드 수가 다릅니다: {name} 끝 표기 {expected}, 읽은 행 {len(rows)}")
    return rows


def _row(line: str, where: str) -> FailToDeliver:
    cells = [cell.strip() for cell in line.split("|")]
    if len(cells) != 6:
        raise SecAPIError(f"Fails-to-Deliver 열 수가 6이 아닙니다: {where} {line!r}")
    settlement, cusip, symbol, quantity, description, price = cells
    try:
        return FailToDeliver(
            settlement_date=datetime.strptime(settlement, "%Y%m%d").date(),
            cusip=cusip.upper(),
            symbol=symbol or None,
            quantity=int(quantity),
            description=description or None,
            price=_price(price),
        )
    except ValueError as error:
        raise SecAPIError(f"Fails-to-Deliver 행을 읽을 수 없습니다: {where} {line!r} ({error})") from None


def _price(raw: str) -> Optional[Decimal]:
    if raw in ("", "."):
        return None
    try:
        return Decimal(raw)
    except InvalidOperation:
        raise ValueError(f"가격이 아닙니다: {raw!r}") from None
