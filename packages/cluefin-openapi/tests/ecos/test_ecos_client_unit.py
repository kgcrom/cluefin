"""ECOS 클라이언트: 키·URL·쪽 넘김·본문 RESULT 오류 매핑·키 가리기."""

import re
from unittest.mock import patch

import pytest
import requests
import requests_mock

from cluefin_openapi.ecos import (
    Client,
    EcosAPIError,
    EcosAuthenticationError,
    EcosNetworkError,
    EcosNotFoundError,
    EcosQueryTimeoutError,
    EcosRateLimitError,
    EcosRequestError,
    EcosSampleLimitError,
    EcosServerError,
)

from ._helpers import BASE, SAMPLE_LIMIT_MESSAGE, load, result, serve_rows

REAL_KEY = "REALKEY0123456789ABC"
ANY_ECOS = re.compile(rf"^{re.escape(BASE)}/")


@pytest.fixture
def sample() -> Client:
    return Client()


@pytest.fixture
def real() -> Client:
    return Client(auth_key=REAL_KEY, max_retries=0)


def _rows(n: int):
    return [
        {"STAT_CODE": "817Y002", "STAT_NAME": "시장금리", "TIME": f"{i:08d}", "DATA_VALUE": str(i)} for i in range(n)
    ]


class TestInit:
    def test_no_key_means_sample(self, sample: Client):
        assert sample.auth_key == "sample"
        assert sample.is_sample
        assert sample.page_size == 10

    @pytest.mark.parametrize("key", [None, ""])
    def test_empty_key_falls_back_to_sample(self, key):
        assert Client(auth_key=key).is_sample

    def test_default_timeout_outlasts_server_60s_cutoff(self, sample: Client):
        assert sample.timeout > 60

    def test_real_key_uses_1000_row_pages(self, real: Client):
        assert not real.is_sample
        assert real.page_size == 1000


class TestUrl:
    def test_path_carries_key_and_encoded_segments(self, real: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=load("statistic_word.json"))
            real.statistic_glossary.word("소비자동향지수")
            assert m.last_request.path == (
                f"/api/statisticword/{REAL_KEY.lower()}/json/kr/1/1000/"
                "%ec%86%8c%eb%b9%84%ec%9e%90%eb%8f%99%ed%96%a5%ec%a7%80%ec%88%98"
            )

    def test_slash_in_value_cannot_add_a_path_segment(self, real: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=load("statistic_word.json"))
            real.statistic_glossary.word("a/b")
            assert m.last_request.path.endswith("/a%2fb")

    def test_blank_segment_is_rejected(self, real: Client):
        with pytest.raises(ValueError, match="빈 값"):
            real.statistic_catalog.item_list("  ")

    def test_bad_row_range_is_rejected(self, real: Client):
        with pytest.raises(ValueError, match="행 범위"):
            real.statistic_catalog.key_statistic_list(start_row=10, end_row=1)


class TestPaging:
    def test_sample_walks_pages_of_ten(self, sample: Client):
        with requests_mock.Mocker() as m:
            route = serve_rows(m, "StatisticSearch", _rows(25))
            page = sample.statistic_search.search("817Y002", "D", "20260101", "20261017", ["010210000"])
        assert page.list_total_count == 25
        assert [row.data_value for row in page.rows] == [str(i) for i in range(25)]
        assert [r.path.split("/json/kr/")[1].split("/")[:2] for r in route.request_history] == [
            ["1", "10"],
            ["11", "20"],
            ["21", "30"],
        ]

    def test_real_key_gets_everything_in_one_call(self, real: Client):
        with requests_mock.Mocker() as m:
            route = serve_rows(m, "StatisticSearch", _rows(216))
            page = real.statistic_search.search("817Y002", "D", "20261005", "20261017")
        assert len(page.rows) == 216
        assert route.call_count == 1

    def test_explicit_range_is_a_single_page(self, sample: Client):
        with requests_mock.Mocker() as m:
            route = serve_rows(m, "StatisticSearch", _rows(25))
            page = sample.statistic_search.search("817Y002", "D", "20260101", "20261017", start_row=11, end_row=20)
        assert page.list_total_count == 25
        assert [row.data_value for row in page.rows] == [str(i) for i in range(10, 20)]
        assert route.call_count == 1

    def test_sample_over_ten_rows_is_a_sample_limit_error(self, sample: Client):
        with requests_mock.Mocker() as m:
            serve_rows(m, "StatisticSearch", _rows(25))
            with pytest.raises(EcosSampleLimitError):
                sample.statistic_search.search("817Y002", "D", "20260101", "20261017", start_row=1, end_row=11)

    def test_page_cap_raises_instead_of_truncating(self):
        client = Client(max_pages=2)
        with requests_mock.Mocker() as m:
            serve_rows(m, "StatisticSearch", _rows(25))
            with pytest.raises(EcosAPIError, match="쪽 넘김 상한"):
                client.statistic_search.search("817Y002", "D", "20260101", "20261017")

    def test_no_data_is_an_empty_page(self, sample: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=result("INFO-200", "해당하는 데이터가 없습니다."))
            page = sample.statistic_search.search("817Y002", "D", "20261018", "20261018", ["010210000"])
        assert page.list_total_count == 0
        assert page.rows == []

    def test_more_than_four_item_codes_is_rejected(self, sample: Client):
        with pytest.raises(ValueError, match="4개"):
            sample.statistic_search.search("817Y002", "D", "20261005", "20261017", ["1", "2", "3", "4", "5"])


class TestBodyResult:
    """ECOS 는 오류도 HTTP 200 + 본문 RESULT 로 준다 (sample·실키 모두, 2026-10-19 실측)."""

    @pytest.mark.parametrize(
        ("code", "message", "expected"),
        [
            ("INFO-100", "인증키가 유효하지 않습니다.", EcosAuthenticationError),
            ("ERROR-100", "필수 값이 누락되어 있습니다.", EcosRequestError),
            ("ERROR-101", "주기와 다른 형식의 날짜 형식입니다.", EcosRequestError),
            ("ERROR-200", "요청타입 값이 누락 혹은 유효하지 않습니다.", EcosRequestError),
            ("ERROR-300", "조회건수 값이 누락되어 있습니다.", EcosRequestError),
            ("ERROR-301", "조회건수 값의 타입이 유효하지 않습니다.\n 요청시작건수가 더 큽니다.", EcosRequestError),
            ("ERROR-301", SAMPLE_LIMIT_MESSAGE, EcosSampleLimitError),
            ("ERROR-400", "60초 TIMEOUT이 발생하였습니다.", EcosQueryTimeoutError),
            ("ERROR-500", "서버 오류입니다.", EcosServerError),
            ("ERROR-600", "DB Connection 오류입니다.", EcosServerError),
            ("ERROR-601", "SQL 오류입니다.", EcosServerError),
            ("ERROR-602", "과도한 OpenAPI호출로 이용이 제한되었습니다.", EcosRateLimitError),
            ("ERROR-999", "처음 보는 코드", EcosAPIError),
        ],
    )
    def test_result_code_maps_to_exception(self, real: Client, code, message, expected):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=result(code, message))
            with pytest.raises(expected) as info:
                real.statistic_catalog.key_statistic_list()
        assert type(info.value) is expected
        assert info.value.code == code
        assert info.value.status_code is None or info.value.status_code == 200

    def test_query_timeout_is_a_server_error(self, real: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=result("ERROR-400", "60초 TIMEOUT"))
            with pytest.raises(EcosServerError):
                real.statistic_catalog.key_statistic_list()

    @pytest.mark.parametrize(
        ("code", "message", "needle"),
        [
            ("ERROR-101", "주기와 다른 형식의 날짜 형식입니다.", "D=20240101"),
            ("ERROR-301", SAMPLE_LIMIT_MESSAGE, "10행"),
            ("ERROR-400", "60초 TIMEOUT", "기간을 나눠"),
        ],
    )
    def test_error_carries_action_hint(self, real: Client, code, message, needle):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=result(code, message))
            with pytest.raises(EcosAPIError) as info:
                real.statistic_catalog.key_statistic_list()
        assert needle in info.value.hint
        assert f"(조치: {info.value.hint})" in str(info.value)

    def test_unknown_code_has_no_hint(self, real: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=result("ERROR-999", "처음 보는 코드"))
            with pytest.raises(EcosAPIError) as info:
                real.statistic_catalog.key_statistic_list()
        assert info.value.hint is None
        assert str(info.value) == "ECOS API Error [ERROR-999]: 처음 보는 코드"

    @pytest.mark.parametrize("code", ["ERROR-600", "ERROR-602"])
    def test_transient_body_error_is_retried(self, code):
        client = Client(auth_key=REAL_KEY, max_retries=2)
        with requests_mock.Mocker() as m, patch("time.sleep") as sleep:
            m.get(ANY_ECOS, [{"json": result(code, "일시 오류")}, {"json": load("key_statistic_list.json")}])
            page = client.statistic_catalog.key_statistic_list(start_row=1, end_row=10)
        assert page.rows
        assert m.call_count == 2
        sleep.assert_called_once_with(1)

    def test_transient_body_error_gives_up_after_retries(self):
        client = Client(auth_key=REAL_KEY, max_retries=2)
        with requests_mock.Mocker() as m, patch("time.sleep"):
            m.get(ANY_ECOS, json=result("ERROR-602", "과도한 OpenAPI호출로 이용이 제한되었습니다."))
            with pytest.raises(EcosRateLimitError):
                client.statistic_catalog.key_statistic_list()
        assert m.call_count == 3

    def test_query_timeout_is_not_retried(self):
        client = Client(auth_key=REAL_KEY, max_retries=2)
        with requests_mock.Mocker() as m, patch("time.sleep"):
            m.get(ANY_ECOS, json=result("ERROR-400", "60초 TIMEOUT"))
            with pytest.raises(EcosQueryTimeoutError):
                client.statistic_catalog.key_statistic_list()
        assert m.call_count == 1

    def test_plain_request_error_is_not_a_sample_limit(self, real: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=result("ERROR-301", "요청시작건수가 더 큽니다."))
            with pytest.raises(EcosRequestError) as info:
                real.statistic_catalog.key_statistic_list()
        assert not isinstance(info.value, EcosSampleLimitError)

    def test_missing_service_block_is_an_error(self, real: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json={"Other": {}})
            with pytest.raises(EcosAPIError, match="블록이 없습니다"):
                real.statistic_catalog.key_statistic_list()

    def test_html_body_is_an_error(self, real: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, text="<html></html>")
            with pytest.raises(EcosAPIError, match="JSON"):
                real.statistic_catalog.key_statistic_list()


class TestHttpAndKeyRedaction:
    def test_http_404_is_not_found(self, real: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, status_code=404, text="<HTML>503 - Service Unavailable</HTML>")
            with pytest.raises(EcosNotFoundError):
                real.statistic_catalog.key_statistic_list()

    def test_server_error_after_retries(self):
        client = Client(auth_key=REAL_KEY, max_retries=1)
        with requests_mock.Mocker() as m, patch("time.sleep"):
            m.get(ANY_ECOS, status_code=503)
            with pytest.raises(EcosServerError):
                client.statistic_catalog.key_statistic_list()
            assert m.call_count == 2

    def test_context_hides_key(self, real: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=result("ERROR-101", "날짜 형식"))
            with pytest.raises(EcosRequestError) as info:
                real.statistic_search.search("817Y002", "D", "202610", "202610")
        assert REAL_KEY not in repr(info.value.request_context)
        assert info.value.request_context["path"].startswith("/StatisticSearch/***/json/kr/1/1000/817Y002")

    def test_network_error_message_hides_key(self, real: Client):
        leaked = requests.exceptions.ConnectionError(
            f"HTTPSConnectionPool(host='ecos.bok.or.kr'): Max retries exceeded with url: /api/KeyStatisticList/{REAL_KEY}/json"
        )
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, exc=leaked)
            with pytest.raises(EcosNetworkError) as info:
                real.statistic_catalog.key_statistic_list()
        assert REAL_KEY not in str(info.value)
        assert "***" in str(info.value)
        assert info.value.__cause__ is None
        assert info.value.__suppress_context__
