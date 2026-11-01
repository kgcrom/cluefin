from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from cluefin_openapi.ecos import (
    EcosPage,
    KeyStatistic,
    StatisticItem,
    StatisticObservation,
    StatisticTable,
    StatisticWord,
)

from cluefin_openapi_cli.errors import EXIT_BROKER, EXIT_CREDENTIALS, EXIT_USAGE, CliError, classify_exception
from cluefin_openapi_cli.handlers import ecos as handlers
from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.registry import EmptyRegistry, RpcRegistry, set_registry_provider

from ._handler_fakes import assert_registers_all


def _page(model, rows: list[dict]) -> EcosPage:
    return EcosPage[model].model_validate({"list_total_count": len(rows), "row": rows})


_TABLES = [
    {"P_STAT_CODE": "*", "STAT_CODE": "0000000001", "STAT_NAME": "1. 통화 및 금융", "CYCLE": None, "SRCH_YN": "N"},
    {"P_STAT_CODE": "0000000001", "STAT_CODE": "817Y002", "STAT_NAME": "1.3.2.1. 시장금리(일별)", "CYCLE": "D",
     "SRCH_YN": "Y", "ORG_NAME": "한국은행"},
    {"P_STAT_CODE": "0000000001", "STAT_CODE": "721Y001", "STAT_NAME": "1.3.2.2. 시장금리(월,분기,년)", "CYCLE": "M",
     "SRCH_YN": "Y"},
    {"P_STAT_CODE": "0000000008", "STAT_CODE": "901Y067", "STAT_NAME": "8.1.2. 경기종합지수", "CYCLE": "M",
     "SRCH_YN": "Y"},
]  # fmt: skip

_ITEMS = [
    {"STAT_CODE": "512Y014", "STAT_NAME": "기업경기조사(전망)", "GRP_CODE": "Group1", "GRP_NAME": "산업",
     "ITEM_CODE": "99988", "ITEM_NAME": "전 산 업", "CYCLE": "M", "START_TIME": "200302", "END_TIME": "202611"},
    {"STAT_CODE": "512Y014", "STAT_NAME": "기업경기조사(전망)", "GRP_CODE": "Group2", "GRP_NAME": "지표",
     "ITEM_CODE": "BA", "ITEM_NAME": "업황전망BSI", "CYCLE": "M", "START_TIME": "200302", "END_TIME": "202611"},
]  # fmt: skip


def _obs(time: str, value: str, item: str = "010200000", name: str = "국고채(3년)", unit: str = "연%") -> dict:
    return {
        "STAT_CODE": "817Y002",
        "STAT_NAME": "1.3.2.1. 시장금리(일별)",
        "ITEM_CODE1": item,
        "ITEM_NAME1": name,
        "UNIT_NAME": unit,
        "TIME": time,
        "DATA_VALUE": value,
    }


class _Session:
    def __init__(self, *, tables=(), items=(), observations=(), key_stats=(), words=()) -> None:
        self.calls: list[tuple] = []
        catalog = SimpleNamespace(
            table_list=self._recorded("table_list", _page(StatisticTable, list(tables))),
            item_list=self._recorded("item_list", _page(StatisticItem, list(items))),
            key_statistic_list=self._recorded("key_statistic_list", _page(KeyStatistic, list(key_stats))),
        )
        search = SimpleNamespace(search=self._recorded("search", _page(StatisticObservation, list(observations))))
        glossary = SimpleNamespace(word=self._recorded("word", _page(StatisticWord, list(words))))
        self._client = SimpleNamespace(statistic_catalog=catalog, statistic_search=search, statistic_glossary=glossary)

    def _recorded(self, name: str, value):
        def call(*args, **kwargs):
            self.calls.append((name, args))
            return value

        return call

    def get_ecos(self):
        return self._client


def test_register_ecos_handlers() -> None:
    assert_registers_all(handlers.register_ecos_handlers, handlers._ALL_HANDLERS, "ecos")


def test_table_search_matches_every_term_and_skips_grouping_rows() -> None:
    session = _Session(tables=_TABLES)

    rates = handlers.handle_table_search({"query": "시장금리"}, session)
    assert [row["stat_code"] for row in rates["data"]] == ["817Y002", "721Y001"]

    daily = handlers.handle_table_search({"query": "시장금리 일별"}, session)
    assert [row["stat_code"] for row in daily["data"]] == ["817Y002"]
    assert daily["data"][0]["org_name"] == "한국은행"

    by_cycle = handlers.handle_table_search({"cycle": "M"}, session)
    assert [row["stat_code"] for row in by_cycle["data"]] == ["721Y001", "901Y067"]

    everything = handlers.handle_table_search({"searchable_only": False, "max_rows": 2}, session)
    assert (everything["total"], everything["returned"], everything["truncated"]) == (4, 2, True)


def test_items_filters_by_name_and_keeps_group_order() -> None:
    session = _Session(items=_ITEMS)

    result = handlers.handle_items({"stat_code": "512Y014"}, session)
    assert [(row["group_code"], row["item_code"]) for row in result["data"]] == [("Group1", "99988"), ("Group2", "BA")]
    assert result["data"][1]["end_time"] == "202611"
    assert session.calls == [("item_list", ("512Y014",))]

    only = handlers.handle_items({"stat_code": "512Y014", "query": "업황"}, session)
    assert [row["item_code"] for row in only["data"]] == ["BA"]


def test_items_on_an_unknown_table_hints_at_table_search() -> None:
    result = handlers.handle_items({"stat_code": "999Y999"}, _Session())
    assert result["total"] == 0
    assert "table-search" in result["hint"]


def test_series_parses_values_keeps_latest_rows_and_hoists_the_unit() -> None:
    observations = [_obs("20261028", "3.70"), _obs("20261029", ""), _obs("20261030", "3.715")]
    session = _Session(observations=observations)

    result = handlers.handle_series(
        {"stat_code": "817Y002", "cycle": "D", "start_date": "20261028", "end_date": "20261030",
         "item_codes": "010200000", "max_rows": 2},
        session,
    )  # fmt: skip

    assert session.calls == [("search", ("817Y002", "D", "20261028", "20261030", ("010200000",)))]
    assert (result["stat_name"], result["unit"]) == ("1.3.2.1. 시장금리(일별)", "연%")
    assert (result["total"], result["returned"], result["truncated"]) == (3, 2, True)
    assert result["data"] == [
        {"time": "20261029", "value": None, "item_code1": "010200000", "item_name1": "국고채(3년)"},
        {"time": "20261030", "value": 3.715, "item_code1": "010200000", "item_name1": "국고채(3년)"},
    ]


def test_series_with_mixed_units_labels_each_row() -> None:
    observations = [
        _obs("202609", "104.1", "I16E", "선행지수순환변동치", "2020=100"),
        _obs("202609", "3.0", unit="연%"),
    ]
    result = handlers.handle_series(
        {"stat_code": "901Y067", "cycle": "M", "start_date": "202609", "end_date": "202609"},
        _Session(observations=observations),
    )
    assert result["unit"] == ["2020=100", "연%"]
    assert [row["unit_name"] for row in result["data"]] == ["2020=100", "연%"]


def test_series_without_rows_explains_publication_lag() -> None:
    result = handlers.handle_series(
        {"stat_code": "901Y067", "cycle": "M", "start_date": "202612", "end_date": "202612"}, _Session()
    )
    assert result["total"] == 0
    assert "ecos items" in result["hint"]


@pytest.mark.parametrize(
    ("cycle", "start", "end"),
    [
        ("M", "20260101", "202609"),  # daily format on a monthly table
        ("D", "20260231", "20260301"),  # not a calendar date
        ("Q", "2026Q5", "2026Q1"),
        ("M", "202609", "202601"),  # start after end
    ],
)
def test_series_rejects_periods_before_calling_ecos(cycle: str, start: str, end: str) -> None:
    session = _Session()
    with pytest.raises(CliError) as caught:
        handlers.handle_series({"stat_code": "901Y067", "cycle": cycle, "start_date": start, "end_date": end}, session)
    assert caught.value.exit_code == EXIT_USAGE
    assert session.calls == []


def test_series_rejects_more_than_four_item_codes() -> None:
    with pytest.raises(CliError) as caught:
        handlers.handle_series(
            {"stat_code": "512Y014", "cycle": "M", "start_date": "202601", "end_date": "202609",
             "item_codes": "a,b,c,d,e"},
            _Session(),
        )  # fmt: skip
    assert caught.value.error_type == "TooManyItemCodes"


def test_key_stats_sorts_filters_and_parses_values() -> None:
    rows = [
        {"CLASS_NAME": "환율", "KEYSTAT_NAME": "원/달러 환율(종가)", "DATA_VALUE": "1,385.2", "CYCLE": "20261030"},
        {"CLASS_NAME": "시장금리", "KEYSTAT_NAME": "한국은행 기준금리", "DATA_VALUE": "3", "CYCLE": "20261030",
         "UNIT_NAME": "%"},
    ]  # fmt: skip
    session = _Session(key_stats=rows)

    result = handlers.handle_key_stats({}, session)
    assert [row["class_name"] for row in result["data"]] == ["시장금리", "환율"]
    assert result["data"][1]["value"] == 1385.2

    rates = handlers.handle_key_stats({"query": "기준금리"}, session)
    assert [row["name"] for row in rates["data"]] == ["한국은행 기준금리"]


def test_word_returns_definitions() -> None:
    result = handlers.handle_word(
        {"term": "경제심리지수"}, _Session(words=[{"WORD": "경제심리지수", "CONTENT": "기업과 소비자 모두를 포함한…"}])
    )
    assert result["data"] == [{"word": "경제심리지수", "content": "기업과 소비자 모두를 포함한…"}]


def test_classify_ecos_errors_keep_the_client_hint() -> None:
    from cluefin_openapi.ecos import EcosAuthenticationError, EcosQueryTimeoutError, EcosRequestError

    too_big = classify_exception(
        EcosQueryTimeoutError("60초 초과", code="ERROR-400", hint="기간을 나눠"), command="ecos.series", broker="ecos"
    )
    assert (too_big.exit_code, too_big.error_type, too_big.retryable) == (EXIT_BROKER, "QueryTooLarge", False)
    assert too_big.hint == "기간을 나눠"

    bad_key = classify_exception(
        EcosAuthenticationError("인증키", code="INFO-100"), command="ecos.series", broker="ecos"
    )
    assert bad_key.exit_code == EXIT_CREDENTIALS
    assert "ECOS_AUTH_KEY" in (bad_key.hint or "")

    rejected = classify_exception(
        EcosRequestError("날짜", code="ERROR-101", hint="A=2024"), command="ecos.series", broker="ecos"
    )
    assert (rejected.exit_code, rejected.error_type, rejected.hint) == (EXIT_BROKER, "BrokerRejectedRequest", "A=2024")


@pytest.fixture
def real_registry():
    # Another test file may leave EmptyRegistry installed; run_cli reads whatever provider is current.
    set_registry_provider(RpcRegistry)
    yield
    set_registry_provider(EmptyRegistry)


@pytest.mark.usefixtures("real_registry")
def test_brokers_reports_ecos_key_without_echoing_it(monkeypatch) -> None:
    key = "ecos-test-key-not-real"
    monkeypatch.setenv("ECOS_AUTH_KEY", key)
    result = run_cli(["brokers", "--json"])
    payload = json.loads(result.stdout)

    ecos = next(row for row in payload["brokers"] if row["name"] == "ecos")
    assert ecos["role"] == "reference"
    assert ecos["credentials"]["configured"] is True
    assert key not in result.stdout


@pytest.mark.usefixtures("real_registry")
def test_ecos_paths_have_no_category_segment() -> None:
    result = run_cli(["schema", "ecos", "series", "--json"])
    assert result.exit_code == 0
    assert json.loads(result.stdout)["command"] == "ecos.series"
