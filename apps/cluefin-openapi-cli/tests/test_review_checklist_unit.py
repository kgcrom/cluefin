from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
from cluefin_openapi_cli.review import checklist as ck
from cluefin_openapi_cli.review import metrics as rm
from cluefin_openapi_cli.review.cli import run_review

# --- synthetic raw payloads (hand-computable, not from a real filer) -------------------------------------------

_FS_PAYLOAD: dict[str, Any] = {
    "as_of": "2026-11-11",
    "quarters": [
        {"period": "2024Q3", "revenue": 100.0},
        {"period": "2024Q4", "revenue": 100.0},
        {"period": "2025Q1", "revenue": 100.0},
        {"period": "2025Q2", "revenue": 100.0},
        {"period": "2025Q3", "revenue": 110.0},
        {"period": "2025Q4", "revenue": 110.0},
        {"period": "2026Q1", "revenue": 110.0},
        {"period": "2026Q2", "revenue": 110.0},
    ],
    "ttm": {"revenue": 440.0, "operating_income": 44.0},
    "quality": {
        "years": [
            {"roic": {"value": 5.0}, "dupont": {"roe_reported": 10.0}, "altman_z_double_prime": {"value": 3.0}},
            {"roic": {"value": 8.0}, "dupont": {"roe_reported": 16.0}, "altman_z_double_prime": {"value": 4.5}},
        ],
        "f_score": {"total": 7, "incomplete": False},
    },
    "latest": {"net_debt_ratio": -12.5, "interest_coverage": None},
}

# A bank/insurer/securities filer: no classified current/noncurrent assets, so quality.py leaves ROIC's inputs
# null — the catalog must report `unknown` with a reason, never 0.
_FS_PAYLOAD_FINANCIAL: dict[str, Any] = {
    "as_of": "2026-11-11",
    "quarters": _FS_PAYLOAD["quarters"],
    "ttm": {"revenue": 0, "operating_income": None},
    "quality": {"years": [{"roic": {"value": None}, "dupont": {"roe_reported": None}}], "f_score": {}},
    "latest": {"net_debt_ratio": None, "interest_coverage": None},
}

_VALUATION = {"as_of": "2026-11-11", "per_ttm": 12.5, "pbr": 1.2}
_BAND = {"as_of": "2026-11-09", "per": {"current_percentile": 73.6}, "pbr": {"current_percentile": 85.7}}
_INVESTOR_METRICS = {
    "as_of": "2026-11-11",
    "fcf_yield": {"value": 3.1, "reason": None},
    "ev_ebit": {"value": 6.4, "reason": None},
    "shareholder_yield": {"value": 1.5, "reason": None},
}
_DILUTION = {
    "end_de": "20261111",
    "rows": [
        {"pct_of_shares": 0.02},
        {"pct_of_shares": -0.91},  # treasury acquisition: negative, not dilution
        {"pct_of_shares": 0.03},
    ],
}
_CACHE_RS = {"as_of": "2026-11-09", "rows": [{"code": "005930", "rs_1m": 20, "sector_rs": 8}]}
_TREND_SETUP = {"as_of": "20261111", "setup": {"status": "no_group"}}
_TECHNICAL = {
    "as_of": "20261111",
    "stop_sizing": {"levels": [{"horizon_days": 20, "width_pct": 8.4}, {"horizon_days": 60, "width_pct": 14.55}]},
}

_RAW = {
    "dart-financial-summary": _FS_PAYLOAD,
    "kis-stock-valuation": _VALUATION,
    "kis-stock-valuation-band": _BAND,
    "kis-stock-investor-metrics": _INVESTOR_METRICS,
    "dart-dilution-watch": _DILUTION,
    "cache-rs": _CACHE_RS,
    "kis-chart-trend-setup": _TREND_SETUP,
    "kis-chart-technical": _TECHNICAL,
}


def _write_folder(tmp_path: Path, code: str = "005930", raw: dict[str, Any] | None = None) -> Path:
    folder = tmp_path / "run"
    (folder / "raw").mkdir(parents=True)
    (folder / "run.json").write_text(json.dumps({"stock_code": code, "peers": []}), encoding="utf-8")
    for stem, payload in (raw if raw is not None else _RAW).items():
        (folder / "raw" / f"{code}__{stem}.json").write_text(json.dumps(payload), encoding="utf-8")
    return folder


# --- metrics.py --------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("metric", "expected"),
    [
        ("revenue_yoy_4q", round((440.0 / 400.0 - 1) * 100, 4)),
        ("opm_ttm", round(44.0 / 440.0 * 100, 4)),
        ("roe", 16.0),
        ("roic", 8.0),
        ("f_score", 7),
        ("altman_z2", 4.5),
        ("net_debt_ratio", -12.5),
        ("per_ttm", 12.5),
        ("pbr", 1.2),
        ("per_band_pct", 73.6),
        ("pbr_band_pct", 85.7),
        ("fcf_yield", 3.1),
        ("ev_ebit", 6.4),
        ("shareholder_yield", 1.5),
        ("dilution_3y_pct", round(0.02 + 0.03, 6)),
        ("rs_1m", 20),
        ("sector_rs", 8),
        ("setup_group", "none"),
        ("stop_width_pct", 8.4),
    ],
)
def test_metric_extracts_expected_value(tmp_path: Path, metric: str, expected: Any) -> None:
    folder = _write_folder(tmp_path)
    result = rm.compute(folder, "005930", metric)
    assert result.value == expected
    assert result.reason is None


def test_interest_coverage_is_unknown_when_filer_has_no_interest_expense(tmp_path: Path) -> None:
    folder = _write_folder(tmp_path)
    result = rm.compute(folder, "005930", "interest_coverage")
    assert result.value is None
    assert result.reason


def test_financial_filer_without_current_assets_is_unknown_not_zero(tmp_path: Path) -> None:
    raw = dict(_RAW)
    raw["dart-financial-summary"] = _FS_PAYLOAD_FINANCIAL
    folder = _write_folder(tmp_path, raw=raw)
    for metric in ("roe", "roic", "opm_ttm", "net_debt_ratio"):
        result = rm.compute(folder, "005930", metric)
        assert result.value is None, metric
        assert result.reason, metric


def test_missing_raw_file_is_unknown_with_reason(tmp_path: Path) -> None:
    folder = tmp_path / "run"
    (folder / "raw").mkdir(parents=True)
    (folder / "run.json").write_text(json.dumps({"stock_code": "005930", "peers": []}), encoding="utf-8")
    result = rm.compute(folder, "005930", "per_ttm")
    assert result.value is None
    assert "raw" in result.reason


def test_cache_rs_row_missing_for_code_is_unknown(tmp_path: Path) -> None:
    raw = dict(_RAW)
    raw["cache-rs"] = {"as_of": "2026-11-09", "rows": [{"code": "000660", "rs_1m": 1, "sector_rs": 1}]}
    folder = _write_folder(tmp_path, raw=raw)
    result = rm.compute(folder, "005930", "rs_1m")
    assert result.value is None


def test_catalog_rows_cover_every_metric() -> None:
    rows = rm.catalog_rows()
    assert {row["metric"] for row in rows} == set(rm.CATALOG)
    assert any(row["metric"] == "setup_group" and row["kind"] == "string" for row in rows)


# --- checklist.py: rule loading/validation ----------------------------------------------------------------------


def _write_rules(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "principles.toml"
    path.write_text(text, encoding="utf-8")
    return path


def test_load_rules_missing_file_is_usage_error(tmp_path: Path) -> None:
    with pytest.raises(CliError) as exc:
        ck.load_rules(tmp_path / "nope.toml")
    assert exc.value.exit_code == EXIT_USAGE


def test_init_rules_file_only_when_missing(tmp_path: Path) -> None:
    path = tmp_path / "principles.toml"
    ck.init_rules_file(path)
    assert path.is_file()
    rules = ck.load_rules(path)
    assert rules
    with pytest.raises(CliError) as exc:
        ck.init_rules_file(path)
    assert exc.value.exit_code == EXIT_USAGE


def test_unknown_metric_and_bad_op_collected_together(tmp_path: Path) -> None:
    path = _write_rules(
        tmp_path,
        """
        [[rule]]
        id = "a"
        label = "unknown metric"
        metric = "not_a_metric"
        op = ">="
        value = 1

        [[rule]]
        id = "b"
        label = "bad op for string metric"
        metric = "setup_group"
        op = "<"
        value = "g1"
        """,
    )
    with pytest.raises(CliError) as exc:
        ck.load_rules(path)
    issues = exc.value.data["issues"]
    assert len(issues) == 2
    assert any("not_a_metric" in i for i in issues)
    assert any("string metric" in i for i in issues)


def test_wrong_value_type_is_an_issue(tmp_path: Path) -> None:
    path = _write_rules(
        tmp_path,
        """
        [[rule]]
        id = "a"
        label = "value should be a number"
        metric = "roe"
        op = ">="
        value = "fifteen"
        """,
    )
    with pytest.raises(CliError) as exc:
        ck.load_rules(path)
    assert "must be a number" in exc.value.data["issues"][0]


def test_empty_rule_list_is_usage_error(tmp_path: Path) -> None:
    path = _write_rules(tmp_path, "")
    with pytest.raises(CliError):
        ck.load_rules(path)


# --- checklist.py: evaluate --------------------------------------------------------------------------------------


def test_evaluate_pass_fail_unknown_and_must_failed(tmp_path: Path) -> None:
    folder = _write_folder(tmp_path)
    rules = [
        {"id": "r1", "label": "ROE >= 15", "metric": "roe", "op": ">=", "value": 15.0, "must": False},
        {"id": "r2", "label": "PER <= 10", "metric": "per_ttm", "op": "<=", "value": 10.0, "must": True},
        {"id": "r3", "label": "interest coverage known", "metric": "interest_coverage", "op": ">=", "value": 3.0},
        {"id": "r4", "label": "setup not none", "metric": "setup_group", "op": "!=", "value": "none"},
    ]
    payload = ck.evaluate(folder, "005930", rules)
    by_id = {row["id"]: row for row in payload["rules"]}
    assert by_id["r1"]["result"] == "pass"
    assert by_id["r1"]["value"] == 16.0
    assert by_id["r2"]["result"] == "fail"
    assert by_id["r3"]["result"] == "unknown"
    assert by_id["r3"]["reason"]
    assert by_id["r4"]["result"] == "fail"  # setup_group is "none" here
    assert payload["summary"]["passed"] == 1
    assert payload["summary"]["failed"] == 2
    assert payload["summary"]["unknown"] == 1
    assert payload["summary"]["must_failed"] == ["r2"]
    written = json.loads((folder / ck.CHECKLIST_FILE).read_text(encoding="utf-8"))
    assert written == payload


# --- CLI -----------------------------------------------------------------------------------------------------


def test_cli_checklist_dry_run_never_touches_disk(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    missing_rules = tmp_path / "would-not-be-created.toml"
    run_review(
        ["checklist", "--init", "--rules", str(missing_rules), "--from", str(tmp_path / "nope"), "--dry-run", "--json"]
    )
    out = json.loads(capsys.readouterr().out)
    assert out["dry_run"] is True
    assert not missing_rules.exists()


def test_cli_checklist_metrics_true(capsys: pytest.CaptureFixture[str]) -> None:
    run_review(["checklist", "--metrics", "true", "--json"])
    out = json.loads(capsys.readouterr().out)
    assert {row["metric"] for row in out["metrics"]} == set(rm.CATALOG)


def test_cli_checklist_init_without_from_reports_created_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rules_path = tmp_path / "principles.toml"
    run_review(["checklist", "--init", "--rules", str(rules_path), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert out["created"] == str(rules_path)
    assert rules_path.is_file()


def test_cli_checklist_needs_from_init_or_metrics() -> None:
    with pytest.raises(CliError) as exc:
        run_review(["checklist", "--json"])
    assert exc.value.exit_code == EXIT_USAGE


def test_cli_checklist_from_unknown_folder_is_usage_error(tmp_path: Path) -> None:
    with pytest.raises(CliError):
        run_review(["checklist", "--from", str(tmp_path / "nope"), "--rules", str(tmp_path / "r.toml"), "--json"])


def test_cli_checklist_end_to_end(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    folder = _write_folder(tmp_path)
    rules_path = tmp_path / "principles.toml"
    ck.init_rules_file(rules_path)
    run_review(["checklist", "--from", str(folder), "--rules", str(rules_path), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert out["stock_code"] == "005930"
    assert out["rules"]
    assert (folder / ck.CHECKLIST_FILE).is_file()
