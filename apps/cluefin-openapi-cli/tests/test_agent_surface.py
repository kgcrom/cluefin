"""Agent-facing surface: broker roles, schema, dry-run, validation, field masks, error taxonomy."""

from __future__ import annotations

import json

import pytest

from cluefin_openapi_cli.errors import (
    EXIT_BROKER,
    EXIT_CREDENTIALS,
    EXIT_RATE_LIMIT,
    EXIT_UNEXPECTED,
    EXIT_USAGE,
    classify_exception,
)
from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.metadata import BROKER_ORDER, BROKER_ROLES, KIWOOM_KIS_ALTERNATIVES
from cluefin_openapi_cli.output import select_fields
from cluefin_openapi_cli.registry import EmptyRegistry, RpcRegistry, build_cli_registry, set_registry_provider
from cluefin_openapi_cli.validation import validate_params


@pytest.fixture(autouse=True)
def _real_registry():
    set_registry_provider(RpcRegistry)
    yield
    set_registry_provider(EmptyRegistry)


def _json(argv: list[str]) -> tuple[int, dict]:
    result = run_cli(argv)
    return result.exit_code, json.loads(result.stdout)


# --- broker roles ------------------------------------------------------------


def test_kis_is_primary_and_kiwoom_is_auxiliary() -> None:
    assert BROKER_ORDER[0] == "kis"
    assert BROKER_ROLES["kis"].role == "primary"
    assert BROKER_ROLES["kiwoom"].role == "auxiliary"
    assert BROKER_ROLES["dart"].role == "reference"


def test_every_kiwoom_alternative_points_at_a_real_command() -> None:
    registry = build_cli_registry()
    for source, targets in KIWOOM_KIS_ALTERNATIVES.items():
        assert tuple(source.split(".")) in registry, source
        for target in targets:
            assert target.startswith("kis."), target
            assert tuple(target.split(".")) in registry, target


def test_registry_commands_carry_role_and_alternatives() -> None:
    registry = build_cli_registry()
    assert registry[("kis", "stock", "current-price")].broker_role == "primary"
    theme = registry[("kiwoom", "theme", "group")]
    assert theme.broker_role == "auxiliary"
    assert theme.kis_alternatives == ()
    assert "no KIS equivalent" in (theme.agent_notes or "")
    daily = registry[("kiwoom", "stock", "daily-price")]
    assert "kis.chart.daily" in daily.kis_alternatives
    assert "Prefer the primary KIS command" in (daily.agent_notes or "")


def test_brokers_command_reports_roles_without_secrets(monkeypatch) -> None:
    monkeypatch.setenv("KIS_APP_KEY", "secret-app-key-value")
    monkeypatch.setenv("KIS_SECRET_KEY", "secret-secret-value")
    code, payload = _json(["brokers", "--json"])

    assert code == 0
    assert payload["order"][0] == "kis"
    kis = payload["brokers"][0]
    assert kis["role"] == "primary"
    assert kis["credentials"]["required"] == ["KIS_APP_KEY", "KIS_SECRET_KEY"]
    assert kis["credentials"]["configured"] is True
    kiwoom = next(row for row in payload["brokers"] if row["name"] == "kiwoom")
    assert kiwoom["role"] == "auxiliary"
    assert kiwoom["kiwoom_only_count"] == len(kiwoom["kiwoom_only_commands"]) > 0
    assert "kiwoom.theme.group" in kiwoom["kiwoom_only_commands"]
    assert "secret-app-key-value" not in json.dumps(payload)
    assert "secret-secret-value" not in json.dumps(payload)


def test_root_payload_lists_roles_workflow_and_exit_codes() -> None:
    code, payload = _json(["--json"])

    assert code == 0
    assert payload["brokers"][0] == {"name": "kis", "role": "primary"}
    assert "brokers" in payload["commands"] and "schema" in payload["commands"]
    assert payload["workflow"][0].endswith("brokers --json")
    assert set(payload["exit_codes"]) == {"0", "1", "2", "3", "4", "5"}


# --- list / schema -----------------------------------------------------------


def test_list_is_brief_by_default_and_kis_first() -> None:
    code, payload = _json(["list", "--json"])

    assert code == 0
    assert payload["detail"] == "brief"
    first = payload["commands"][0]
    assert first["broker"] == "kis"
    assert "parameters" not in first
    assert set(first) >= {"qualified_name", "broker_role", "required", "kis_alternatives"}
    brokers = [row["broker"] for row in payload["commands"]]
    assert brokers.index("kiwoom") > brokers.index("kis")
    assert brokers[-1] == "dart"


def test_list_full_includes_parameters_and_query_filters() -> None:
    code, payload = _json(["list", "--full", "--query", "theme group", "--json"])

    assert code == 0
    assert payload["detail"] == "full"
    assert payload["count"] >= 1
    assert all("parameters" in row for row in payload["commands"])
    assert all("theme" in row["qualified_name"] for row in payload["commands"])


def test_list_rejects_unknown_broker() -> None:
    code, payload = _json(["list", "--broker", "nhplug", "--json"])

    assert code == EXIT_USAGE
    assert payload["error"]["data"]["allowed"] == ["kis", "kiwoom", "dart"]


def test_schema_exposes_json_schema_options_and_invocations() -> None:
    code, payload = _json(["schema", "kis", "stock", "current-price", "--json"])

    assert code == 0
    assert payload["command"] == "kis.stock.current-price"
    assert payload["parameters"]["additionalProperties"] is False
    assert payload["parameters"]["required"] == ["stock_code"]
    stock = next(option for option in payload["options"] if option["field"] == "stock_code")
    assert stock["flag"] == "--stock-code"
    assert stock["required"] is True
    assert stock["pattern"] == "^[0-9]{6}$"
    assert payload["invoke"]["dry_run"].endswith("--dry-run --json")
    assert any(option["flag"] == "--dry-run" for option in payload["global_options"])


def test_schema_for_dart_path() -> None:
    code, payload = _json(["schema", "dart", "company-overview", "--json"])

    assert code == 0
    assert payload["broker_role"] == "reference"


# --- dry run / validation ----------------------------------------------------


def test_dry_run_validates_and_never_calls_the_broker(monkeypatch) -> None:
    monkeypatch.setenv("KIS_APP_KEY", "k")
    monkeypatch.setenv("KIS_SECRET_KEY", "s")
    code, payload = _json(["kis", "stock", "current-price", "--stock-code", "005930", "--dry-run", "--json"])

    assert code == 0
    assert payload["dry_run"] is True
    assert payload["params"] == {"stock_code": "005930"}
    assert payload["validation"] == "ok"
    assert payload["credentials"]["configured"] is True
    assert "--params-json" in payload["execute"]


def test_dry_run_with_fields_and_inline_equals() -> None:
    code, payload = _json(["kis", "stock", "current-price", "--stock-code=005930", "--dry-run", "--fields", "params"])

    assert code == 0
    assert payload == {"params": {"stock_code": "005930"}}


def test_enum_and_pattern_violations_fail_locally_with_field_issues() -> None:
    code, payload = _json(["kis", "stock", "current-price", "--stock-code", "5930", "--market", "X", "--json"])

    assert code == EXIT_USAGE
    error = payload["error"]
    assert error["type"] == "ValidationError"
    assert error["retryable"] is False
    issues = {issue["field"]: issue for issue in error["data"]["issues"]}
    assert "pattern" in issues["stock_code"]["problem"]
    assert issues["market"]["allowed"] == ["J", "NX", "UN"]


def test_missing_required_lists_field_in_missing_and_issues() -> None:
    code, payload = _json(["kis", "stock", "current-price", "--json"])

    assert code == EXIT_USAGE
    assert payload["error"]["data"]["missing"] == ["stock_code"]


@pytest.mark.parametrize("bad", ["0059%30", "0059?0", "0059#0", "../etc", "0059\x0130"])
def test_hardening_rejects_injection_like_strings(bad: str) -> None:
    report = validate_params({"name": bad}, {"type": "object", "properties": {"name": {"type": "string"}}})

    assert not report.ok
    assert report.issues[0].field == "name"


def test_hardening_walks_nested_params_json() -> None:
    schema = {"type": "object", "properties": {"stocks": {"type": "array"}}}
    report = validate_params({"stocks": [{"code": "0059%30"}]}, schema)

    assert not report.ok
    assert report.issues[0].field == "stocks[0].code"


def test_validate_params_accepts_clean_input_and_bounds() -> None:
    schema = {
        "type": "object",
        "properties": {
            "count": {"type": "integer", "minimum": 1, "maximum": 100},
            "code": {"type": "string", "pattern": "^[0-9]{6}$"},
            "flag": {"type": "boolean"},
        },
        "required": ["code"],
    }
    assert validate_params({"count": 50, "code": "005930", "flag": True}, schema).ok
    assert not validate_params({"count": 0, "code": "005930"}, schema).ok
    assert not validate_params({"count": "50", "code": "005930"}, schema).ok
    assert not validate_params({"code": "005930", "extra": 1}, schema).ok


def test_array_field_flag_accepts_inline_json() -> None:
    code, payload = _json(
        [
            "kis",
            "analysis",
            "watchlist-multi-quote",
            "--stocks",
            '[{"market":"J","stock_code":"005930"}]',
            "--dry-run",
            "--fields",
            "params",
        ]
    )

    assert code == 0
    assert payload["params"]["stocks"][0]["stock_code"] == "005930"


# --- output helpers ----------------------------------------------------------


def test_select_fields_masks_top_level_dotted_and_list_paths() -> None:
    data = {
        "a": 1,
        "b": {"c": 2, "d": 3},
        "rows": [{"x": 1, "y": 2}, {"x": 3, "y": 4}],
    }
    assert select_fields(data, ["a"]) == {"a": 1}
    assert select_fields(data, ["b.c"]) == {"b": {"c": 2}}
    assert select_fields(data, ["rows.x"]) == {"rows": [{"x": 1}, {"x": 3}]}
    assert select_fields(data, ["missing"]) == {}
    assert select_fields([{"x": 1, "y": 2}], ["y"]) == [{"y": 2}]


def test_compact_output_is_single_line() -> None:
    result = run_cli(["schema", "kis", "stock", "current-price", "--compact"])

    assert result.exit_code == 0
    assert result.stdout.count("\n") == 1


# --- error taxonomy ----------------------------------------------------------


class _RateLimitError(Exception):
    retry_after = 7


class _KISAuthenticationError(Exception):
    status_code = 401


class _KiwoomNetworkError(Exception):
    pass


class _KISAPIError(Exception):
    response_data = {"rt_cd": "1", "msg_cd": "EGW00123", "msg1": "token mismatch"}


@pytest.mark.parametrize(
    ("exc", "exit_code", "error_type", "retryable"),
    [
        (_RateLimitError("slow down"), EXIT_RATE_LIMIT, "RateLimitError", True),
        (_KISAuthenticationError("401"), EXIT_CREDENTIALS, "AuthenticationError", False),
        (
            ValueError("KIS credentials not configured (kis_app_key, kis_secret_key)"),
            EXIT_CREDENTIALS,
            "CredentialsMissing",
            False,
        ),
        (_KiwoomNetworkError("boom"), EXIT_BROKER, "BrokerUnavailable", True),
        (_KISAPIError("bad"), EXIT_BROKER, "BrokerApiError", False),
        (ValueError("KIS API Error [OPSQ0001]: no data (rt_cd=1)"), EXIT_BROKER, "BrokerApiError", False),
        (RuntimeError("weird"), EXIT_UNEXPECTED, "ExecutionError", False),
    ],
)
def test_classify_exception_maps_to_exit_codes(exc, exit_code, error_type, retryable) -> None:
    error = classify_exception(exc, command="kis.stock.current-price", broker="kis")

    assert error.exit_code == exit_code
    assert error.error_type == error_type
    assert error.retryable is retryable
    payload = error.to_payload()["error"]
    assert payload["exit_code"] == exit_code
    assert payload["data"]["command"] == "kis.stock.current-price"


def test_classify_rate_limit_and_api_error_carry_broker_detail() -> None:
    rate = classify_exception(_RateLimitError("slow"), command="c", broker="kis")
    assert rate.data["retry_after"] == 7
    api = classify_exception(_KISAPIError("bad"), command="c", broker="kis")
    assert api.data["msg_cd"] == "EGW00123"


def test_classify_pydantic_response_parse_error() -> None:
    from pydantic import BaseModel, ValidationError

    class Model(BaseModel):
        a: int
        b: str

    try:
        Model.model_validate({})
    except ValidationError as exc:
        error = classify_exception(exc, command="kis.stock.current-price", broker="kis")

    assert error.exit_code == EXIT_BROKER
    assert error.error_type == "ResponseParseError"
    assert error.data["fields"] == ["a", "b"]
    assert error.data["model"] == "Model"
    assert "field errors" in error.message
