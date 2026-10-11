"""Unit tests for SEC Fails-to-Deliver files: listing, parsing and the CUSIP → ticker map."""

import io
import zipfile
from datetime import date
from decimal import Decimal

import pytest
import requests_mock

from cluefin_openapi.sec import Client, FailsToDeliverFile, FailToDeliver, SecAPIError, cusip_symbols

USER_AGENT = "Cluefin Test test@example.com"
LIST_URL = "https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data"
HEADER = "SETTLEMENT DATE|CUSIP|SYMBOL|QUANTITY (FAILS)|DESCRIPTION|PRICE"

# The folder differs by period and two names carry a `_0` suffix (measured on the live page, 2026-10).
LIST_HTML = """
<ul>
<li><a href="/files/data/fails-deliver-data/cnsfails202609a.zip">September 2026, first half</a></li>
<li><a href="/files/data/other/fails-deliver-data/cnsfails202605b.zip">May 2026, second half</a></li>
<li><a href="/files/data/fails-deliver-data/cnsfails201910a_0.zip">October 2019, first half</a></li>
<li><a href="/files/node/add/data_distribution/cnsfails202002a.zip">February 2020, first half</a></li>
<li><a href="/files/data/frequently-requested-foia-document-fails-deliver-data/cnsfails200907a.zip">July 2009</a></li>
<li><a href="/files/other-report.pdf">unrelated</a></li>
</ul>
"""


@pytest.fixture
def client() -> Client:
    return Client(user_agent=USER_AGENT)


def _zip(text: str, name: str = "cnsfails202609a.txt") -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr(name, text)
    return buffer.getvalue()


def _file(path: str = "/files/data/fails-deliver-data/cnsfails202609a.zip") -> FailsToDeliverFile:
    return FailsToDeliverFile(name="cnsfails202609a", year=2026, month=9, half="a", path=path)


def _body(*rows: str, count: int | None = None) -> str:
    trailer = [f"Trailer record count {len(rows) if count is None else count}", "Trailer total quantity of shares 1"]
    return "\r\n".join([HEADER, *rows, *trailer]) + "\r\n"


def test_files_reads_links_from_the_list_page(client: Client):
    with requests_mock.Mocker() as m:
        m.get(LIST_URL, text=LIST_HTML)
        files = client.fails_to_deliver.files()

    assert [(f.name, f.year, f.month, f.half) for f in files] == [
        ("cnsfails202609a", 2026, 9, "a"),
        ("cnsfails202605b", 2026, 5, "b"),
        ("cnsfails202002a", 2020, 2, "a"),
        ("cnsfails201910a", 2019, 10, "a"),
        ("cnsfails200907a", 2009, 7, "a"),
    ]
    assert files[1].path == "/files/data/other/fails-deliver-data/cnsfails202605b.zip"
    assert files[3].path == "/files/data/fails-deliver-data/cnsfails201910a_0.zip"


def test_files_without_links_fails_loudly(client: Client):
    with requests_mock.Mocker() as m:
        m.get(LIST_URL, text="<html>moved</html>")
        with pytest.raises(SecAPIError, match="링크"):
            client.fails_to_deliver.files()


def test_records_parse_rows_and_check_the_trailer(client: Client):
    body = _body(
        "20260901|037833100|AAPL|1200|APPLE INC COM|255.46",
        "20260902|b6s7wd106|NYXH|2508|NYXOAH S A SHS (BMU)|.",
        "20260903|12345A109||10||",
    )
    with requests_mock.Mocker() as m:
        m.get("https://www.sec.gov/files/data/fails-deliver-data/cnsfails202609a.zip", content=_zip(body))
        records = client.fails_to_deliver.records(_file())

    assert records[0] == FailToDeliver(
        settlement_date=date(2026, 9, 1),
        cusip="037833100",
        symbol="AAPL",
        quantity=1200,
        description="APPLE INC COM",
        price=Decimal("255.46"),
    )
    assert (records[1].cusip, records[1].price) == ("B6S7WD106", None)
    assert (records[2].symbol, records[2].description, records[2].price) == (None, None, None)


@pytest.mark.parametrize(
    ("body", "message"),
    [
        (_body("20260901|037833100|AAPL|1200|APPLE INC COM|255.46", count=2), "레코드 수"),
        (_body("20260901|037833100|AAPL|1200|APPLE INC COM"), "열 수"),
        (_body("2026-09-01|037833100|AAPL|1200|APPLE INC COM|1"), "행을 읽을 수 없습니다"),
        (_body("20260901|037833100|AAPL|12.5|APPLE INC COM|1"), "행을 읽을 수 없습니다"),
        (_body("20260901|037833100|AAPL|1|APPLE INC COM|n/a"), "행을 읽을 수 없습니다"),
        ("DATE|CUSIP\r\n", "머리글"),
    ],
)
def test_records_reject_unexpected_files(client: Client, body: str, message: str):
    with requests_mock.Mocker() as m:
        m.get("https://www.sec.gov/files/data/fails-deliver-data/cnsfails202609a.zip", content=_zip(body))
        with pytest.raises(SecAPIError, match=message):
            client.fails_to_deliver.records(_file())


def test_records_reject_zip_with_several_members(client: Client):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("a.txt", _body())
        archive.writestr("b.txt", _body())
    with requests_mock.Mocker() as m:
        m.get("https://www.sec.gov/files/data/fails-deliver-data/cnsfails202609a.zip", content=buffer.getvalue())
        with pytest.raises(SecAPIError, match="하나가 아닙니다"):
            client.fails_to_deliver.records(_file())


def _record(day: int, cusip: str, symbol: str | None) -> FailToDeliver:
    return FailToDeliver(settlement_date=date(2026, 9, day), cusip=cusip, symbol=symbol, quantity=1)


def test_cusip_symbols_keeps_the_latest_ticker():
    records = [
        _record(10, "000000001", "NEW"),
        _record(2, "000000001", "OLD"),  # an older file read after a newer one
        _record(3, "000000002", "AAA"),
        _record(3, "000000002", "BBB"),  # same day: the later row wins
        _record(4, "000000003", None),
    ]

    assert cusip_symbols(records) == {"000000001": "NEW", "000000002": "BBB"}
