"""미 재무부 수익률 곡선: 요청 파라미터, XML 파싱, 빈 달, HTTP 오류."""

import datetime as dt
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import pytest
import requests_mock

from cluefin_feeds import FeedClientError, FeedParseError, FeedServerError, HttpClient
from cluefin_feeds.treasury import Client

FIXTURES = Path(__file__).parent / "fixtures"
URL = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml"
EMPTY_FEED = b"""<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<feed xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices"
      xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" xmlns="http://www.w3.org/2005/Atom">
<title type="text">DailyTreasuryYieldCurveRateData</title></feed>"""


@pytest.fixture
def client() -> Client:
    return Client(HttpClient(max_retries=0, min_interval=0))


def _fixture(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


class TestParYieldCurve:
    def test_month_query_and_parse(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(URL, content=_fixture("par_yield_curve_202610.xml"))
            rows = client.par_yield_curve("202610")
            assert m.last_request.qs == {
                "data": ["daily_treasury_yield_curve"],
                "field_tdr_date_value_month": ["202610"],
            }
        assert [row.date for row in rows] == sorted(row.date for row in rows)
        first = rows[0]
        assert first.date == dt.date(2026, 10, 14)
        assert (first.month_1, first.month_1_5, first.year_10, first.year_30) == (
            Decimal("4.11"),
            Decimal("4.15"),
            Decimal("5.19"),
            Decimal("5.52"),
        )
        assert not first.model_extra

    def test_year_query(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(URL, content=EMPTY_FEED)
            client.par_yield_curve("2025")
            assert m.last_request.qs["field_tdr_date_value"] == ["2025"]

    def test_tenors_not_yet_issued_are_none(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(URL, content=_fixture("par_yield_curve_201501.xml"))
            rows = client.par_yield_curve("201501")
        assert len(rows) == 20
        assert rows[0].date == dt.date(2015, 1, 2)
        assert rows[0].year_10 == Decimal("2.12")
        assert (rows[0].month_1_5, rows[0].month_2, rows[0].month_4) == (None, None, None)

    def test_empty_month_is_empty_list(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(URL, content=EMPTY_FEED)
            assert client.par_yield_curve("203001") == []

    @pytest.mark.parametrize("period", ["2026-10", "26", "2026101", "abcdef", ""])
    def test_bad_period_is_rejected(self, client: Client, period):
        with pytest.raises(ValueError, match="YYYY"):
            client.par_yield_curve(period)

    def test_broken_xml_is_an_error(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(URL, content=b"<html><body>maintenance")
            with pytest.raises(FeedParseError, match="XML"):
                client.par_yield_curve("202610")

    def test_entity_declarations_are_refused(self, client: Client):
        bomb = b'<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "aaaa">]><feed>&a;</feed>'
        with requests_mock.Mocker() as m:
            m.get(URL, content=bomb)
            with pytest.raises(Exception, match="(?i)entit"):
                client.par_yield_curve("202610")


class TestHttpErrors:
    def test_404_is_client_error(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(URL, status_code=404)
            with pytest.raises(FeedClientError):
                client.par_yield_curve("202610")

    def test_5xx_is_retried_then_server_error(self):
        client = Client(HttpClient(max_retries=1, min_interval=0))
        with requests_mock.Mocker() as m, patch("time.sleep"):
            m.get(URL, status_code=502)
            with pytest.raises(FeedServerError):
                client.par_yield_curve("202610")
            assert m.call_count == 2
