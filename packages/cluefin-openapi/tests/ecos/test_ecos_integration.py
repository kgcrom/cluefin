"""Live checks against ecos.bok.or.kr (read-only, no account involved).

`sample` 키 경로는 키 없이 늘 돌고, 실키 경로는 `.env.test` 의 ECOS_AUTH_KEY 가 있을 때만 돈다.
"""

import os
from datetime import date, timedelta
from pathlib import Path

import dotenv
import pytest

from cluefin_openapi.ecos import (
    KTB_10Y,
    USD_KRW,
    Client,
    EcosRequestError,
    EcosSampleLimitError,
    KeyStatistic,
    StatisticItem,
    StatisticObservation,
    StatisticTable,
)

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parents[4] / ".env.test")
ECOS_AUTH_KEY = os.getenv("ECOS_AUTH_KEY")

pytestmark = pytest.mark.integration
requires_key = pytest.mark.skipif(not ECOS_AUTH_KEY, reason="ECOS_AUTH_KEY 미설정 (.env.test)")

# 2주면 영업일이 10일 이하라 sample 로도 한 쪽, 휴일이 끼어도 값이 있다.
END = date.today()
START = END - timedelta(days=14)


def _ymd(d: date) -> str:
    return d.strftime("%Y%m%d")


def _declared(model) -> set:
    return {field.alias or name for name, field in model.model_fields.items()}


@pytest.fixture(scope="module")
def sample() -> Client:
    return Client()


@pytest.fixture(scope="module")
def real() -> Client:
    return Client(auth_key=ECOS_AUTH_KEY)


def test_sample_ktb_10y(sample: Client):
    page = sample.statistic_search.search_series(KTB_10Y, _ymd(START), _ymd(END))
    assert page.rows, "최근 2주 국고채 10년 값이 없다"
    row = page.rows[-1]
    assert (row.item_code1, row.unit_name) == ("010210000", "연%")
    assert row.value is not None
    assert 0 < row.value < 20
    assert not row.model_extra, f"선언 안 된 필드: {row.model_extra}"


def test_sample_pages_past_ten_rows(sample: Client):
    page = sample.statistic_search.search_series(USD_KRW, _ymd(END - timedelta(days=60)), _ymd(END))
    assert page.list_total_count > 10
    assert len(page.rows) == page.list_total_count


def test_sample_over_ten_rows_in_one_call(sample: Client):
    with pytest.raises(EcosSampleLimitError):
        sample.statistic_search.search("817Y002", "D", _ymd(START), _ymd(END), ["010210000"], start_row=1, end_row=11)


@requires_key
def test_real_whole_market_rate_table(real: Client):
    page = real.statistic_search.search("817Y002", "D", _ymd(START), _ymd(END))
    assert len(page.rows) == page.list_total_count > 100
    for raw_key in ("STAT_CODE", "ITEM_CODE1", "TIME", "DATA_VALUE"):
        assert raw_key in _declared(StatisticObservation)
    assert all(not row.model_extra for row in page.rows)


@requires_key
def test_real_errors_come_as_body_codes(real: Client):
    with pytest.raises(EcosRequestError) as info:
        real.statistic_search.search("817Y002", "D", "202610", "202610", ["010210000"])
    assert info.value.code == "ERROR-101"


@requires_key
def test_real_no_data_is_empty(real: Client):
    page = real.statistic_search.search("XXXXXXX", "D", _ymd(START), _ymd(END))
    assert page.rows == []


@requires_key
def test_real_catalog(real: Client):
    tables = real.statistic_catalog.table_list()
    assert len(tables.rows) == tables.list_total_count > 500
    assert any(t.stat_code == "817Y002" and t.searchable == "Y" for t in tables.rows)
    assert all(not t.model_extra for t in tables.rows), _declared(StatisticTable)

    items = real.statistic_catalog.item_list("817Y002")
    assert {"010210000", "010300000"} <= {i.item_code for i in items.rows}
    assert all(not i.model_extra for i in items.rows), _declared(StatisticItem)

    keys = real.statistic_catalog.key_statistic_list()
    assert len(keys.rows) == keys.list_total_count
    assert all(not k.model_extra for k in keys.rows), _declared(KeyStatistic)


@requires_key
def test_real_glossary(real: Client):
    words = real.statistic_glossary.word("소비자동향지수")
    assert words.rows
    assert words.rows[0].word == "소비자동향지수"
    meta = real.statistic_glossary.meta("경제심리지수")
    assert any(row.name == "통계명" for row in meta.rows)
