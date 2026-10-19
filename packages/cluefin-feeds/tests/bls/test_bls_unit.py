"""BLS 시계열: v1/v2 선택, 연도·시리즈 쪼개기, 본문 status 오류, 결측값."""

import json
from decimal import Decimal
from pathlib import Path

import pytest
import requests_mock

from cluefin_feeds import FeedParseError, HttpClient
from cluefin_feeds.bls import CPI_U_ALL_ITEMS, BlsAPIError, BlsDailyLimitError, Client

FIXTURES = Path(__file__).parent / "fixtures"
V1 = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
V2 = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


def _fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def _client(key=None) -> Client:
    return Client(registration_key=key, http=HttpClient(max_retries=0, min_interval=0))


def _echo(request, context):
    """요청한 시리즈·연도마다 1월 값 하나씩 돌려주는 가짜 BLS."""
    body = request.json()
    years = range(int(body["startyear"]), int(body["endyear"]) + 1) if "startyear" in body else [2026]
    return {
        "status": "REQUEST_SUCCEEDED",
        "message": [],
        "Results": {
            "series": [
                {
                    "seriesID": sid,
                    "data": [
                        {"year": str(y), "period": "M01", "periodName": "January", "value": str(y), "footnotes": [{}]}
                        for y in reversed(years)
                    ],
                }
                for sid in body["seriesid"]
            ]
        },
    }


class TestRequest:
    def test_without_key_uses_v1_and_no_key_field(self):
        with requests_mock.Mocker() as m:
            m.post(V1, json=_fixture("cpi_2015.json"))
            _client().timeseries([CPI_U_ALL_ITEMS], 2015, 2015)
            assert m.last_request.json() == {"seriesid": ["CUUR0000SA0"], "startyear": "2015", "endyear": "2015"}

    def test_with_key_uses_v2_and_sends_key(self):
        with requests_mock.Mocker() as m:
            m.post(V2, json=_fixture("cpi_2015.json"))
            _client("k-123").timeseries([CPI_U_ALL_ITEMS], 2015, 2015, annual_average=True)
            body = m.last_request.json()
        assert body["registrationkey"] == "k-123"
        assert body["annualaverage"] is True

    def test_no_years_lets_server_pick_recent(self):
        with requests_mock.Mocker() as m:
            m.post(V1, json=_echo)
            _client().timeseries([CPI_U_ALL_ITEMS])
            assert "startyear" not in m.last_request.json()

    @pytest.mark.parametrize(
        ("ids", "start", "end", "match"),
        [([], 2020, 2021, "비었"), (["X"], 2020, None, "함께"), (["X"], 2026, 2020, "큽니다")],
    )
    def test_bad_arguments(self, ids, start, end, match):
        with pytest.raises(ValueError, match=match):
            _client().timeseries(ids, start, end)


class TestSplitting:
    def test_long_range_is_split_into_ten_year_windows_without_key(self):
        with requests_mock.Mocker() as m:
            m.post(V1, json=_echo)
            result = _client().timeseries(["A"], 2000, 2026)
            windows = [(r.json()["startyear"], r.json()["endyear"]) for r in m.request_history]
        assert windows == [("2000", "2009"), ("2010", "2019"), ("2020", "2026")]
        assert [row.year for row in result.get("A").data] == list(range(2000, 2027))

    def test_key_allows_twenty_years(self):
        with requests_mock.Mocker() as m:
            m.post(V2, json=_echo)
            _client("k").timeseries(["A"], 2000, 2026)
            assert m.call_count == 2

    def test_many_series_are_batched(self):
        ids = [f"S{i:02d}" for i in range(30)]
        with requests_mock.Mocker() as m:
            m.post(V1, json=_echo)
            result = _client().timeseries(ids, 2026, 2026)
            batches = [len(r.json()["seriesid"]) for r in m.request_history]
        assert batches == [25, 5]
        assert [s.series_id for s in result.series] == ids


class TestResponse:
    def test_rows_are_ascending_and_typed(self):
        with requests_mock.Mocker() as m:
            m.post(V1, json=_fixture("cpi_2015.json"))
            series = _client().timeseries([CPI_U_ALL_ITEMS], 2015, 2015).get(CPI_U_ALL_ITEMS)
        assert [row.month for row in series.data] == list(range(1, 13))
        assert series.data[-1].value == Decimal("236.525")
        assert not series.data[0].model_extra

    def test_missing_value_and_invalid_series(self):
        with requests_mock.Mocker() as m:
            m.post(V1, json=_fixture("cpi_2025_2026_with_invalid.json"))
            result = _client().timeseries([CPI_U_ALL_ITEMS, "NOPE123"], 2025, 2026)
        assert result.messages == ["Invalid Series for Series NOPE123"]
        assert result.get("NOPE123").data == []
        october = next(r for r in result.get(CPI_U_ALL_ITEMS).data if (r.year, r.month) == (2025, 10))
        assert october.raw_value == "-"
        assert october.value is None
        assert october.footnotes[0].code == "X"

    def test_annual_average_row_has_no_month(self):
        row = {"year": "2015", "period": "M13", "periodName": "Annual", "value": "237.017", "footnotes": [{}]}
        payload = {
            "status": "REQUEST_SUCCEEDED",
            "message": [],
            "Results": {"series": [{"seriesID": "A", "data": [row]}]},
        }
        with requests_mock.Mocker() as m:
            m.post(V1, json=payload)
            data = _client().timeseries(["A"], 2015, 2015, annual_average=True).get("A").data
        assert data[0].month is None
        assert data[0].value == Decimal("237.017")


class TestErrors:
    def test_invalid_parameters_status(self):
        payload = {"status": "REQUEST_FAILED_INVALID_PARAMETERS", "message": ["startyear is invalid."], "Results": {}}
        with requests_mock.Mocker() as m:
            m.post(V1, json=payload)
            with pytest.raises(BlsAPIError) as info:
                _client().timeseries(["A"], 2030, 2030)
        assert info.value.status == "REQUEST_FAILED_INVALID_PARAMETERS"
        assert info.value.messages == ["startyear is invalid."]

    def test_daily_limit(self):
        payload = {"status": "REQUEST_NOT_PROCESSED", "message": ["daily threshold reached"], "Results": {}}
        with requests_mock.Mocker() as m:
            m.post(V1, json=payload)
            with pytest.raises(BlsDailyLimitError):
                _client().timeseries(["A"], 2026, 2026)

    def test_non_json(self):
        with requests_mock.Mocker() as m:
            m.post(V1, text="<html>")
            with pytest.raises(FeedParseError):
                _client().timeseries(["A"], 2026, 2026)

    def test_key_is_not_in_error(self):
        payload = {"status": "REQUEST_FAILED", "message": ["boom"], "Results": {}}
        with requests_mock.Mocker() as m:
            m.post(V2, json=payload)
            with pytest.raises(BlsAPIError) as info:
                _client("secret-registration-key").timeseries(["A"], 2026, 2026)
        assert "secret-registration-key" not in str(info.value) + repr(vars(info.value))
