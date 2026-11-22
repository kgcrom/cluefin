from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from cluefin_openapi_cli.errors import EXIT_USAGE, CliError
from cluefin_openapi_cli.review import five_checks as fc
from cluefin_openapi_cli.review.cli import run_review

# Synthetic payloads (hand-computable, not from a real filer). Amounts in 억원, ratios in %.


def _quarters(revenues: list[float], yoys: list[Any]) -> list[dict[str, Any]]:
    return [
        {"period": f"Q{i}", "revenue": r, "yoy": None if y is None else {"revenue": y}}
        for i, (r, y) in enumerate(zip(revenues, yoys, strict=True))
    ]


def _fs(**over: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "as_of": "2026-11-11",
        # 4 quarters 440 vs prior 400 → +10%, last two quarterly YoY +10%.
        "quarters": _quarters([100] * 4 + [110] * 4, [None] * 4 + [10.0] * 4),
        "ttm": {"revenue": 440.0, "operating_income": 52.8, "net_income_owners": 40.0},  # OPM 12%
        "annual": [
            {"year": 2023, "opm": 11.0, "free_cash_flow": 5.0},
            {"year": 2024, "opm": 12.0, "free_cash_flow": 6.0},
            {"year": 2025, "opm": 13.0, "free_cash_flow": 7.0},
        ],
        "latest": {
            "period": "2026 3Q",
            "free_cash_flow": 3.0,
            "operating_cash_flow": 10.0,
            "net_debt": -20.0,
            "interest_coverage": None,
            "net_debt_ratio": -10.0,
        },
    }
    base.update(over)
    return base


def _folder(tmp_path: Path, fs: dict[str, Any] | None, per: float | None = 8.0, code: str = "005930") -> Path:
    folder = tmp_path / "run"
    (folder / "raw").mkdir(parents=True)
    (folder / "run.json").write_text(json.dumps({"stock_code": code, "peers": []}), encoding="utf-8")
    if fs is not None:
        (folder / "raw" / f"{code}__dart-financial-summary.json").write_text(json.dumps(fs), encoding="utf-8")
    if per is not None:
        valuation = {"as_of": "2026-11-11", "per_ttm": per}
        (folder / "raw" / f"{code}__kis-stock-valuation.json").write_text(json.dumps(valuation), encoding="utf-8")
    return folder


def _results(payload: dict[str, Any]) -> dict[str, str]:
    return {c["item"]: c["result"] for c in payload["checks"]}


def test_all_good_and_file_written(tmp_path: Path) -> None:
    folder = _folder(tmp_path, _fs())
    payload = fc.evaluate_five_checks(folder, "005930")
    assert _results(payload) == {
        "growth": "좋음",
        "profitability": "좋음",
        "cash": "좋음",
        "debt": "좋음",
        "price": "좋음",
    }
    assert json.loads((folder / fc.FIVE_CHECKS_FILE).read_text(encoding="utf-8")) == payload
    assert payload["missing_raw"] == []


def test_neutral_between_thresholds(tmp_path: Path) -> None:
    fs = _fs(
        quarters=_quarters([100] * 4 + [105] * 4, [None] * 4 + [5.0] * 4),  # +5%: below 10
        ttm={"revenue": 420.0, "operating_income": 33.6, "net_income_owners": 20.0},  # OPM 8%, prior 13% → drop
        latest={**_fs()["latest"], "net_debt": 30.0, "net_debt_ratio": 50.0, "interest_coverage": 8.0},
    )
    results = _results(fc.evaluate_five_checks(_folder(tmp_path, fs, per=15.0), "005930"))
    assert results["growth"] == "보통"
    assert results["profitability"] == "주의"  # 8% < 13% − 2%p
    assert results["debt"] == "보통"
    assert results["price"] == "보통"


@pytest.mark.parametrize(
    ("over", "item"),
    [
        ({"quarters": _quarters([110] * 4 + [100] * 4, [None] * 4 + [-9.0] * 4)}, "growth"),
        ({"quarters": _quarters([100] * 8, [None] * 6 + [-1.0, "적전"])}, "growth"),
        ({"ttm": {"revenue": 440.0, "operating_income": -1.0, "net_income_owners": 1.0}}, "profitability"),
        ({"latest": {**_fs()["latest"], "operating_cash_flow": -1.0}}, "cash"),
        ({"latest": {**_fs()["latest"], "interest_coverage": 2.5}}, "debt"),
        ({"latest": {**_fs()["latest"], "net_debt": 500.0, "net_debt_ratio": 250.0}}, "debt"),
        ({"ttm": {"revenue": 440.0, "operating_income": 52.8, "net_income_owners": -3.0}}, "price"),
    ],
)
def test_caution_conditions(tmp_path: Path, over: dict[str, Any], item: str) -> None:
    assert _results(fc.evaluate_five_checks(_folder(tmp_path, _fs(**over)), "005930"))[item] == "주의"


def test_cash_caution_needs_two_negative_fcf(tmp_path: Path) -> None:
    one_bad = _fs(latest={**_fs()["latest"], "free_cash_flow": -2.0})
    assert _results(fc.evaluate_five_checks(_folder(tmp_path, one_bad), "005930"))["cash"] == "보통"
    annual = [*_fs()["annual"][:2], {"year": 2025, "opm": 13.0, "free_cash_flow": -1.0}]
    both = _fs(annual=annual, latest={**_fs()["latest"], "free_cash_flow": -2.0})
    assert _results(fc.evaluate_five_checks(_folder(tmp_path / "b", both), "005930"))["cash"] == "주의"


def test_price_uses_per_bands(tmp_path: Path) -> None:
    assert _results(fc.evaluate_five_checks(_folder(tmp_path, _fs(), per=30.0), "005930"))["price"] == "주의"
    assert _results(fc.evaluate_five_checks(_folder(tmp_path / "n", _fs(), per=-4.0), "005930"))["price"] == "주의"


def test_missing_raw_is_pending_with_reason(tmp_path: Path) -> None:
    payload = fc.evaluate_five_checks(_folder(tmp_path, None, per=None), "005930")
    assert set(_results(payload).values()) == {"판정 보류"}
    assert all(c["reason"] for c in payload["checks"])
    assert payload["missing_raw"] == ["dart-financial-summary", "kis-stock-valuation"]
    assert payload["summary"]["판정 보류"] == 5


def test_caution_wins_over_missing_good_inputs(tmp_path: Path) -> None:
    fs = _fs(latest={**_fs()["latest"], "net_debt": None, "interest_coverage": 1.0})
    check = next(c for c in fc.evaluate_five_checks(_folder(tmp_path, fs), "005930")["checks"] if c["item"] == "debt")
    assert check["result"] == "주의"
    assert "reason" not in check


def test_cli_five_checks(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    folder = _folder(tmp_path, _fs())
    run_review(["five-checks", "--from", str(folder), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert out["stock_code"] == "005930"
    assert len(out["checks"]) == 5


def test_cli_five_checks_needs_folder(tmp_path: Path) -> None:
    with pytest.raises(CliError) as err:
        run_review(["five-checks", "--json"])
    assert err.value.exit_code == EXIT_USAGE
    with pytest.raises(CliError):
        run_review(["five-checks", "--from", str(tmp_path), "--json"])
