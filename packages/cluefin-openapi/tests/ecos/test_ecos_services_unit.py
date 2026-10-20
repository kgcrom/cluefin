"""ECOS 6개 서비스가 실제 응답(픽스처)을 모델로 읽는지."""

import re
from decimal import Decimal

import pytest
import requests_mock

from cluefin_openapi.ecos import CPI_TOTAL, KTB_10Y, Client, StatisticObservation

from ._helpers import BASE, load

ANY_ECOS = re.compile(rf"^{re.escape(BASE)}/")


@pytest.fixture
def client() -> Client:
    return Client(auth_key="REALKEY", max_retries=0)


def _declared(model) -> set:
    return {field.alias or name for name, field in model.model_fields.items()}


class TestStatisticSearch:
    def test_market_rates(self, client: Client):
        raw = load("statistic_search_817Y002.json")
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=raw)
            page = client.statistic_search.search("817Y002", "D", "20261005", "20261017")
        assert page.list_total_count == len(page.rows) == 81
        first = page.rows[0]
        assert (first.item_code1, first.item_name1, first.unit_name) == ("010190000", "국고채(1년)", "연%")
        assert (first.time, first.value) == ("20261006", Decimal("3.737"))
        # 응답의 모든 키가 모델에 선언돼 있어야 한다 (model_extra 로 새면 안 된다).
        assert set(raw["StatisticSearch"]["row"][0]) <= _declared(StatisticObservation)

    def test_series_constant_builds_the_item_path(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=load("statistic_search_817Y002.json"))
            client.statistic_search.search_series(KTB_10Y, "20261005", "20261017")
            assert m.last_request.path.endswith("/817y002/d/20261005/20261017/010210000")

    def test_cpi_weight_string_is_kept(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=load("statistic_search_901Y009.json"))
            page = client.statistic_search.search_series(CPI_TOTAL, "202509", "202609")
        assert page.rows[0].weight == "1000"
        assert page.rows[0].unit_name == "2020=100"

    def test_numeric_weight_becomes_text(self):
        row = StatisticObservation.model_validate(
            {"STAT_CODE": "901Y009", "STAT_NAME": "CPI", "WGT": 1000, "TIME": "202609", "DATA_VALUE": "117.06"}
        )
        assert row.weight == "1000"

    @pytest.mark.parametrize("raw", ["", None, "-"])
    def test_blank_value_is_none(self, raw):
        row = StatisticObservation.model_validate({"STAT_CODE": "x", "STAT_NAME": "x", "TIME": "1", "DATA_VALUE": raw})
        assert row.value is None


class TestCatalog:
    def test_table_list(self, client: Client):
        raw = load("statistic_table_list.json")
        # 픽스처는 844행 중 앞 3행(sample 로 받음) — 전체가 3행인 것처럼 줘야 쪽 넘김이 멈춘다.
        raw["StatisticTableList"]["list_total_count"] = len(raw["StatisticTableList"]["row"])
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=raw)
            page = client.statistic_catalog.table_list()
            assert m.last_request.path.endswith("/json/kr/1/1000")
        top = page.rows[0]
        assert (top.parent_stat_code, top.stat_code, top.cycle, top.searchable) == ("*", "0000000001", None, "N")

    def test_table_list_by_code(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=load("statistic_table_list.json"))
            client.statistic_catalog.table_list("102Y004", start_row=1, end_row=10)
            assert m.last_request.path.endswith("/json/kr/1/10/102y004")

    def test_item_list(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=load("statistic_item_list_817Y002.json"))
            page = client.statistic_catalog.item_list("817Y002", start_row=1, end_row=10)
        item = page.rows[0]
        assert (item.group_code, item.item_code, item.parent_item_code) == ("Group1", "010101000", "010100000")
        assert item.data_count == 8068
        assert page.list_total_count == 27

    def test_key_statistic_list_has_row_count(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=load("key_statistic_list.json"))
            page = client.statistic_catalog.key_statistic_list(start_row=1, end_row=10)
        assert page.row_count == 10
        assert page.list_total_count == 101
        assert page.rows[0].keystat_name


class TestGlossary:
    def test_word(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=load("statistic_word.json"))
            page = client.statistic_glossary.word("소비자동향지수")
        assert page.rows[0].word == "소비자동향지수"
        assert "미시간대학" in (page.rows[0].content or "")

    def test_meta(self, client: Client):
        with requests_mock.Mocker() as m:
            m.get(ANY_ECOS, json=load("statistic_meta.json"))
            page = client.statistic_glossary.meta("경제심리지수", start_row=1, end_row=10)
        names = {row.name: row.meta_data for row in page.rows}
        assert names["통계명"] == "경제심리지수"
        assert page.rows[0].level == "2"
