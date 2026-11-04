"""dart major-event·report-item — 람다 표가 실제 라이브러리 메서드를 부르고, 그 메서드가 표에 적힌 엔드포인트로 가는지.

라이브러리 메서드 이름은 엔드포인트와 자주 다르다(`real_estate_development` → dfOcr, 부도발생). 표의 `endpoint`
가 진실의 원천이므로, 실제 DART client 의 `_get` 만 가로채 36종 전부를 대조한다. 계약 테스트
(`test_handler_client_contract_unit.py`)는 enum 첫 값 하나만 돌기 때문에 이 테스트가 필요하다.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from cluefin_openapi.dart import Client as DartClient

from cluefin_openapi_cli.errors import (
    EXIT_RATE_LIMIT,
    EXIT_USAGE,
    CliError,
    DartQuotaExceededAPIError,
    classify_exception,
)
from cluefin_openapi_cli.handlers import dart as handlers
from cluefin_openapi_cli.validation import validate_params

_PARAMS = {"corp_code": "00126380", "event": "convertible-bond", "bgn_de": "20240101", "end_de": "20241231"}


class _RecordingDart:
    """Real DART client whose `_get` records the path and answers "no data" (013)."""

    def __init__(self, status: str = "013") -> None:
        self.client = DartClient(auth_key="test")
        self.paths: list[tuple[str, dict]] = []

        def fake_get(path, *, params=None):
            self.paths.append((path, params))
            return {"status": status, "message": "조회된 데이타가 없습니다."}

        self.client._get = fake_get

    @property
    def major_shareholder_disclosure(self):
        return self.client.major_shareholder_disclosure

    @property
    def periodic_report_key_information(self):
        return self.client.periodic_report_key_information


class _Session:
    def __init__(self, dart) -> None:
        self._dart = dart

    def get_dart(self):
        return self._dart


@pytest.mark.parametrize("event", list(handlers._MAJOR_EVENTS))
def test_every_event_calls_the_endpoint_in_the_table(event: str) -> None:
    dart = _RecordingDart()
    spec = handlers._MAJOR_EVENTS[event]

    result = handlers.handle_major_event({**_PARAMS, "event": event}, _Session(dart))

    assert dart.paths == [
        (f"/api/{spec.endpoint}.json", {"corp_code": "00126380", "bgn_de": "20240101", "end_de": "20241231"})
    ]
    assert result["event"] == event
    assert result["endpoint"] == spec.endpoint
    assert result["result"]["status"] == "013"  # no data passes through, not an error


def test_table_has_all_36_endpoints_once() -> None:
    endpoints = [spec.endpoint for spec in handlers._MAJOR_EVENTS.values()]
    assert len(endpoints) == 36
    assert len(set(endpoints)) == 36


def test_enum_is_the_table() -> None:
    schema = handlers.handle_major_event._rpc_schema.parameters
    assert schema["properties"]["event"]["enum"] == list(handlers._MAJOR_EVENTS)
    assert "dfOcr" not in schema["properties"]["event"]["description"]  # labels, not endpoint names
    assert "convertible-bond (전환사채권 발행결정)" in schema["properties"]["event"]["description"]


@pytest.mark.parametrize(
    "changes",
    [
        {"bgn_de": "2024-01-01"},
        {"end_de": "2024123"},
        {"event": "stock-split"},
    ],
)
def test_schema_rejects_bad_shapes(changes: dict) -> None:
    schema = handlers.handle_major_event._rpc_schema.parameters
    assert validate_params(_PARAMS, schema).ok
    assert not validate_params({**_PARAMS, **changes}, schema).ok


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"bgn_de": "20250101", "end_de": "20241231"}, "after"),
        ({"bgn_de": "20141231"}, "before 20150101"),
        ({"bgn_de": "20250230"}, "not a calendar date"),
        ({"end_de": "20251301"}, "not a calendar date"),
    ],
)
def test_bad_ranges_exit_2_before_calling_dart(changes: dict, message: str) -> None:
    dart = _RecordingDart()
    with pytest.raises(CliError) as exc_info:
        handlers.handle_major_event({**_PARAMS, **changes}, _Session(dart))
    assert exc_info.value.exit_code == EXIT_USAGE
    assert message in str(exc_info.value)
    assert dart.paths == []


def test_single_day_range_is_allowed() -> None:
    dart = _RecordingDart()
    handlers.handle_major_event({**_PARAMS, "bgn_de": "20240105", "end_de": "20240105"}, _Session(dart))
    assert len(dart.paths) == 1


def test_status_020_is_classified_as_rate_limit() -> None:
    with pytest.raises(DartQuotaExceededAPIError, match=r"조회된 데이타가 없습니다\.") as exc_info:
        handlers.handle_major_event(_PARAMS, _Session(_RecordingDart(status="020")))
    error = classify_exception(exc_info.value, command="dart.major-event", broker="dart")
    assert error.exit_code == EXIT_RATE_LIMIT


def test_rows_pass_through_unchanged() -> None:
    row = {"rcept_no": "20240105000001", "bd_fta": "10,000,000,000", "cv_prc": "-"}
    model = SimpleNamespace(model_dump=lambda **_: {"result": {"status": "000", "list": [row]}})
    spec = handlers._MAJOR_EVENTS["convertible-bond"]
    session = _Session(
        SimpleNamespace(
            major_shareholder_disclosure=SimpleNamespace(convertible_bond_issuance_decision=lambda **_: model)
        )
    )
    result = handlers.handle_major_event(_PARAMS, session)
    assert result == {
        "event": "convertible-bond",
        "endpoint": spec.endpoint,
        "result": {"status": "000", "list": [row]},
    }


# --- dart report-item -------------------------------------------------------------------------

_ITEM_PARAMS = {"corp_code": "00126380", "item": "dividend", "bsns_year": "2025", "reprt_code": "11011"}


@pytest.mark.parametrize("item", list(handlers._REPORT_ITEMS))
def test_every_item_calls_the_endpoint_in_the_table(item: str) -> None:
    dart = _RecordingDart()
    spec = handlers._REPORT_ITEMS[item]

    result = handlers.handle_report_item({**_ITEM_PARAMS, "item": item}, _Session(dart))

    assert dart.paths == [
        (f"/api/{spec.endpoint}.json", {"corp_code": "00126380", "bsns_year": "2025", "reprt_code": "11011"})
    ]
    assert (result["item"], result["endpoint"]) == (item, spec.endpoint)
    assert result["result"]["status"] == "013"


def test_item_table_has_26_endpoints_and_leaves_existing_commands_alone() -> None:
    endpoints = [spec.endpoint for spec in handlers._REPORT_ITEMS.values()]
    assert len(endpoints) == len(set(endpoints)) == 26
    # dart major-shareholder / share-count already serve these two
    assert not {"hyslrSttus", "stockTotqySttus"} & set(endpoints)


def test_item_schema() -> None:
    schema = handlers.handle_report_item._rpc_schema.parameters
    assert schema["properties"]["item"]["enum"] == list(handlers._REPORT_ITEMS)
    assert validate_params(_ITEM_PARAMS, schema).ok
    assert not validate_params({**_ITEM_PARAMS, "reprt_code": "99999"}, schema).ok
    assert not validate_params({**_ITEM_PARAMS, "item": "share-count"}, schema).ok


def test_item_status_020_is_classified_as_rate_limit() -> None:
    with pytest.raises(DartQuotaExceededAPIError, match=r"조회된 데이타가 없습니다\.") as exc_info:
        handlers.handle_report_item(_ITEM_PARAMS, _Session(_RecordingDart(status="020")))
    error = classify_exception(exc_info.value, command="dart.report-item", broker="dart")
    assert error.exit_code == EXIT_RATE_LIMIT


# --- dart dilution-watch ----------------------------------------------------------------------

_DILUTION_PARAMS = {"corp_code": "00126380", "bgn_de": "20220101", "end_de": "20241231"}
_DILUTION_EVENT_METHODS = {
    "convertible-bond": "convertible_bond_issuance_decision",
    "bond-with-warrant": "new_stock_warrant_bond_issuance_decision",
    "exchangeable-bond": "corporate_bond_issuance_decision",
    "rights-offering": "securities_granted_decision",
    "bonus-issue": "free_securities_decision",
    "rights-and-bonus-issue": "paid_in_capital_reduction_decision",
    "capital-reduction": "capital_reduction_decision",
    "treasury-stock-acquisition": "treasury_stock_acquisition_decision",
    "treasury-stock-disposal": "treasury_stock_disposal_decision",
    "treasury-trust-contract": "treasury_stock_trust_contract_decision",
    "treasury-trust-termination": "treasury_stock_trust_contract_termination_decision",
}


def test_dilution_watch_kind_table_matches_every_declared_slug() -> None:
    assert set(_DILUTION_EVENT_METHODS) == set(handlers.dilution.DILUTION_KINDS)


def test_dilution_watch_calls_every_kind_and_the_share_count_window_when_all_empty() -> None:
    dart = _RecordingDart()  # answers every call with status 013

    result = handlers.handle_dilution_watch(_DILUTION_PARAMS, _Session(dart))

    event_paths = {path for path, _ in dart.paths if path != "/api/stockTotqySttus.json"}
    assert len(event_paths) == len(handlers.dilution.DILUTION_KINDS)
    assert result["rows"] == []
    assert result["empty_kinds"] == list(handlers.dilution.DILUTION_KINDS)
    assert result["share_base"] == {"total_common_shares": None, "report": None}
    # 11 major-event kinds + the full (year, year-1) x 4-reprt-code share-count window, all 013.
    assert result["calls"] == len(handlers.dilution.DILUTION_KINDS) + 8
    assert {"kind": "treasury-stock-retirement"} | result["not_covered"][0].keys() == result["not_covered"][0].keys()
    assert result["not_covered"][0]["kind"] == "treasury-stock-retirement"


def _event_response(rows: list[dict], status: str = "000"):
    row_stubs = [SimpleNamespace(model_dump=lambda _row=row, **_: _row) for row in rows]
    return SimpleNamespace(status=None, result=SimpleNamespace(status=status, list=row_stubs))


def test_dilution_watch_normalizes_rows_and_computes_pct_of_shares() -> None:
    cb_row = {
        "rcept_no": "20240615000123",
        "corp_name": "테스트기업",
        "bd_fta": "10,000,000,000",
        "cv_prc": "5,000",
        "act_mktprcfl_cvprc_lwtrsprc": "3,500",
        "cvisstk_cnt": "1,000,000",
    }
    share_row = {"se": "보통주", "istc_totqy": "100,000,000", "rcept_no": "20240401000456"}

    def share_count(**kwargs):
        if kwargs["bsns_year"] == "2024" and kwargs["reprt_code"] == "11011":
            return _event_response([share_row])
        return _event_response([], status="013")

    event_methods = {
        method: (
            lambda _slug=slug, **_: (
                _event_response([cb_row]) if _slug == "convertible-bond" else _event_response([], status="013")
            )
        )
        for slug, method in _DILUTION_EVENT_METHODS.items()
    }
    dart = SimpleNamespace(
        major_shareholder_disclosure=SimpleNamespace(**event_methods),
        periodic_report_key_information=SimpleNamespace(get_total_number_of_shares=share_count),
    )

    result = handlers.handle_dilution_watch(_DILUTION_PARAMS, _Session(dart))

    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["kind"] == "convertible-bond"
    assert row["rcept_dt"] == "20240615"
    assert row["amount_won"] == 10_000_000_000
    assert row["conversion_price"] == 5_000
    assert row["refixing_floor"] == 3_500
    assert row["new_shares"] == 1_000_000
    assert row["pct_of_shares"] == pytest.approx(1.0)
    assert set(result["empty_kinds"]) == set(handlers.dilution.DILUTION_KINDS) - {"convertible-bond"}
    assert result["share_base"]["total_common_shares"] == 100_000_000
    assert result["share_base"]["report"] == {
        "bsns_year": "2024",
        "reprt_code": "11011",
        "rcept_no": "20240401000456",
    }
    # 11 event calls + 1 share-count call (the first candidate, 2024/11011, already matches).
    assert result["calls"] == len(handlers.dilution.DILUTION_KINDS) + 1


def test_dilution_watch_defaults_to_the_last_three_years_ending_today_kst(monkeypatch) -> None:
    monkeypatch.setattr(handlers, "_kst_today", lambda: "20261104")
    dart = _RecordingDart()

    result = handlers.handle_dilution_watch({"corp_code": "00126380"}, _Session(dart))

    assert result["end_de"] == "20261104"
    assert result["bgn_de"] == "20231104"


def test_dilution_watch_default_range_floors_at_min_date(monkeypatch) -> None:
    monkeypatch.setattr(handlers, "_kst_today", lambda: "20160101")
    dart = _RecordingDart()

    result = handlers.handle_dilution_watch({"corp_code": "00126380"}, _Session(dart))

    assert result["bgn_de"] == handlers._MAJOR_EVENT_MIN_DATE


def test_default_bgn_de_handles_leap_day() -> None:
    assert handlers._default_bgn_de("20240229") == "20210228"


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"bgn_de": "20250101", "end_de": "20241231"}, "after"),
        ({"bgn_de": "20141231"}, "before 20150101"),
    ],
)
def test_dilution_watch_rejects_bad_ranges_before_calling_dart(changes: dict, message: str) -> None:
    dart = _RecordingDart()
    with pytest.raises(CliError) as exc_info:
        handlers.handle_dilution_watch({**_DILUTION_PARAMS, **changes}, _Session(dart))
    assert exc_info.value.exit_code == EXIT_USAGE
    assert message in str(exc_info.value)
    assert dart.paths == []


def test_dilution_watch_status_020_is_classified_as_rate_limit() -> None:
    with pytest.raises(DartQuotaExceededAPIError, match=r"조회된 데이타가 없습니다\.") as exc_info:
        handlers.handle_dilution_watch(_DILUTION_PARAMS, _Session(_RecordingDart(status="020")))
    error = classify_exception(exc_info.value, command="dart.dilution-watch", broker="dart")
    assert error.exit_code == EXIT_RATE_LIMIT
