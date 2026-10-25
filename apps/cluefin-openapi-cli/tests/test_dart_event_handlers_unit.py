"""dart major-event·report-item — 람다 표가 실제 라이브러리 메서드를 부르고, 그 메서드가 표에 적힌 엔드포인트로 가는지.

라이브러리 메서드 이름은 엔드포인트와 자주 다르다(`real_estate_development` → dfOcr, 부도발생). 표의 `endpoint`
가 진실의 원천이므로, 실제 DART client 의 `_get` 만 가로채 36종 전부를 대조한다. 계약 테스트
(`test_handler_client_contract_unit.py`)는 enum 첫 값 하나만 돌기 때문에 이 테스트가 필요하다.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from cluefin_openapi.dart import Client as DartClient

from cluefin_openapi_cli.errors import EXIT_RATE_LIMIT, EXIT_USAGE, CliError, classify_exception
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
    "changes, message",
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
    with pytest.raises(Exception) as exc_info:
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
    with pytest.raises(Exception) as exc_info:
        handlers.handle_report_item(_ITEM_PARAMS, _Session(_RecordingDart(status="020")))
    error = classify_exception(exc_info.value, command="dart.report-item", broker="dart")
    assert error.exit_code == EXIT_RATE_LIMIT
