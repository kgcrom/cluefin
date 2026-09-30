"""`dart financial-as-filed`: download -> parse -> rows, with the parser faked.

Arelle may fetch taxonomies over the network, so no real XBRL is parsed here. The numbers are
the Nodemason (01328170) FY2024 pair from the Phase 0 live check: original 20250318001317 vs
amendment 20250828000839, consolidated CIS `dart:OperatingIncomeLoss`.
"""

from __future__ import annotations

import itertools
import json
import random
from datetime import date
from decimal import Decimal
from pathlib import Path

import cluefin_xbrl
import pytest
from cluefin_xbrl import (
    FinancialStatement,
    ParsedFinancialStatements,
    PeriodType,
    StatementLineItem,
    StatementType,
    XbrlDocument,
    XbrlFact,
    XbrlParseError,
    XbrlPeriod,
)

from cluefin_openapi_cli import registry as registry_module
from cluefin_openapi_cli.errors import CliError
from cluefin_openapi_cli.handlers import dart as handlers
from cluefin_openapi_cli.main import run_cli
from cluefin_openapi_cli.registry import EmptyRegistry, RpcRegistry, set_registry_provider

CORP = "01328170"
ORIGINAL = "20250318001317"
AMENDED = "20250828000839"

CURRENT = XbrlPeriod(period_type=PeriodType.DURATION, start_date=date(2024, 1, 1), end_date=date(2024, 12, 31))
PRIOR = XbrlPeriod(period_type=PeriodType.DURATION, start_date=date(2023, 1, 1), end_date=date(2023, 12, 31))
PRIOR2 = XbrlPeriod(period_type=PeriodType.DURATION, start_date=date(2022, 1, 1), end_date=date(2022, 12, 31))
INSTANT = XbrlPeriod(period_type=PeriodType.INSTANT, instant=date(2024, 12, 31))


def _item(local, value, period, *, order=1.0, label="영업이익(손실)", abstract=False, dims=None, ns="dart"):
    return StatementLineItem(
        concept_local_name=local,
        concept_qname=f"{ns}:{local}",
        label_ko=label,
        label_en=local,
        value=None if value is None else Decimal(value),
        unit="iso4217:KRW" if value is not None else None,
        period=period,
        depth=1,
        order=order,
        is_abstract=abstract,
        dimensions=dims or {},
    )


def _statement(kind, items, *, consolidated=True):
    return FinancialStatement(
        statement_type=StatementType(kind),
        linkrole=f"http://dart.fss.or.kr/role/ifrs/dart_2024-06-30_role-{kind}",
        line_items=items,
        is_consolidated=consolidated,
    )


def _cis_items(current_value: str) -> list[StatementLineItem]:
    return [
        _item("StatementOfComprehensiveIncomeAbstract", None, None, order=0.0, label="포괄손익계산서", abstract=True),
        _item("Revenue", "21650735678", CURRENT, order=1.0, label="매출액", ns="ifrs-full"),
        _item("Revenue", "17000000000", PRIOR, order=1.0, label="매출액", ns="ifrs-full"),
        _item("OperatingIncomeLoss", current_value, CURRENT, order=2.0),
        _item("OperatingIncomeLoss", "-3588338302", PRIOR, order=2.0),
        _item("OperatingIncomeLoss", "-3299506436", PRIOR2, order=2.0),
    ]


def _parsed(current_value: str, *, consolidated=("CIS", "BS"), separate=("CIS",)) -> ParsedFinancialStatements:
    def build(kinds, is_consolidated):
        out = {}
        for kind in kinds:
            items = _cis_items(current_value) if kind == "CIS" else [_item("Assets", "100", INSTANT, label="자산총계")]
            out[kind] = _statement(kind, items, consolidated=is_consolidated)
        return out

    return ParsedFinancialStatements(
        source_file="x.xbrl",
        entity_id=CORP,
        statements=build(consolidated, True),
        separate_statements=build(separate, False),
    )


def _doc(*, entity=CORP, period_end=date(2024, 12, 31), facts=1) -> XbrlDocument:
    fact = XbrlFact(concept_local_name="Assets", concept_qname="ifrs-full:Assets", namespace="ifrs-full")
    return XbrlDocument(
        source_file="x.xbrl",
        facts=[fact] * facts,
        entity_id=entity,
        reporting_period_end=period_end,
        taxonomy=cluefin_xbrl.TaxonomyInfo(),
    )


class _FakePeriodic:
    def __init__(self, error: Exception | None = None) -> None:
        self.destinations: list[Path] = []
        self.calls: list[tuple] = []
        self.error = error

    def download_financial_statement_xbrl(self, rcept_no, reprt_code, *, destination, overwrite=False):
        destination = Path(destination)
        self.destinations.append(destination)
        self.calls.append((rcept_no, reprt_code))
        (destination / "dummy.xbrl").write_text("<xbrl/>")
        if self.error is not None:
            raise self.error
        return destination


class _FakeDart:
    def __init__(self, error: Exception | None = None) -> None:
        self.periodic_report_financial_statement = _FakePeriodic(error)


class _Session:
    def __init__(self, dart: _FakeDart) -> None:
        self._dart = dart

    def get_dart(self) -> _FakeDart:
        return self._dart


@pytest.fixture
def install(monkeypatch):
    """Fake the parser seam: returns (doc, parsed) for the next call and records the parse directory."""

    seen: dict = {}

    def _install(doc: XbrlDocument, parsed: ParsedFinancialStatements):
        def fake_parse(directory, *, include_taxonomy=False):
            seen["directory"] = Path(directory)
            seen["include_taxonomy"] = include_taxonomy
            seen["files"] = sorted(p.name for p in Path(directory).iterdir())
            return doc

        monkeypatch.setattr(cluefin_xbrl, "parse_xbrl_directory", fake_parse)
        monkeypatch.setattr(cluefin_xbrl, "extract_financial_statements", lambda d: parsed)
        return seen

    return _install


def _run(params: dict | None = None, *, dart: _FakeDart | None = None) -> dict:
    base = {"rcept_no": ORIGINAL, "reprt_code": "11011", "corp_code": CORP}
    return handlers.handle_financial_as_filed({**base, **(params or {})}, _Session(dart or _FakeDart()))


def _operating_income(result: dict, basis="consolidated") -> list[dict]:
    return [r for r in result["statements"]["CIS"][basis] if r["concept"] == "OperatingIncomeLoss"]


def test_original_and_amended_operating_income_differ_as_decimal_strings(install) -> None:
    install(_doc(), _parsed("28915427"))
    original = _run({"rcept_no": ORIGINAL})
    install(_doc(), _parsed("-190143795"))
    amended = _run({"rcept_no": AMENDED})

    orig_rows = _operating_income(original)
    amend_rows = _operating_income(amended)
    assert orig_rows[0]["value"] == "28915427" and isinstance(orig_rows[0]["value"], str)
    assert amend_rows[0]["value"] == "-190143795"
    assert orig_rows[0]["label_ko"] == "영업이익(손실)"
    assert orig_rows[0]["end_date"] == "2024-12-31" and orig_rows[0]["start_date"] == "2024-01-01"
    # Prior-period comparative columns are kept and identical between the two filings.
    assert [r["value"] for r in orig_rows[1:]] == [r["value"] for r in amend_rows[1:]] == ["-3588338302", "-3299506436"]
    assert original["entity_id"] == CORP and original["reporting_period_end"] == "2024-12-31"
    assert original["rcept_no"] == ORIGINAL and amended["rcept_no"] == AMENDED
    json.dumps(original)  # JSON-serializable: no Decimal/date leaks


def test_download_and_parse_happen_in_the_same_temp_directory(install) -> None:
    seen = install(_doc(), _parsed("1"))
    dart = _FakeDart()
    _run(dart=dart)

    assert dart.periodic_report_financial_statement.calls == [(ORIGINAL, "11011")]
    assert seen["directory"] == dart.periodic_report_financial_statement.destinations[0]
    assert seen["include_taxonomy"] is True and seen["files"] == ["dummy.xbrl"]


def test_temp_directory_is_removed_on_success(install) -> None:
    install(_doc(), _parsed("1"))
    dart = _FakeDart()
    _run(dart=dart)
    (destination,) = dart.periodic_report_financial_statement.destinations
    assert not destination.exists()


@pytest.mark.parametrize(
    "scenario",
    ["entity_mismatch", "empty_facts", "download_error", "parse_error"],
)
def test_temp_directory_is_removed_on_exception(install, monkeypatch, scenario) -> None:
    error = RuntimeError("boom") if scenario == "download_error" else None
    dart = _FakeDart(error)
    doc = {
        "entity_mismatch": _doc(entity="00163114"),
        "empty_facts": _doc(facts=0),
    }.get(scenario, _doc())
    install(doc, _parsed("1"))
    if scenario == "parse_error":

        def boom(directory, *, include_taxonomy=False):
            raise XbrlParseError("bad")

        monkeypatch.setattr(cluefin_xbrl, "parse_xbrl_directory", boom)

    with pytest.raises((CliError, RuntimeError)):
        _run(dart=dart)
    (destination,) = dart.periodic_report_financial_statement.destinations
    assert not destination.exists()


def test_entity_mismatch_is_exit_4_with_expected_and_actual(install) -> None:
    install(_doc(entity="00163114"), _parsed("1"))
    with pytest.raises(CliError) as excinfo:
        _run()
    err = excinfo.value
    assert err.exit_code == 4 and err.error_type == "ResponseParseError"
    assert err.data["expected"] == CORP and err.data["actual"] == "00163114"


def test_zero_facts_is_exit_4(install) -> None:
    install(_doc(facts=0), _parsed("1"))
    with pytest.raises(CliError) as excinfo:
        _run()
    assert excinfo.value.exit_code == 4 and excinfo.value.error_type == "ResponseParseError"
    assert "Arelle" in (excinfo.value.hint or "")


def test_missing_reporting_period_end_is_exit_4(install) -> None:
    install(_doc(period_end=None), _parsed("1"))
    with pytest.raises(CliError) as excinfo:
        _run()
    assert excinfo.value.exit_code == 4 and excinfo.value.error_type == "ResponseParseError"


def test_parser_errors_map_to_exit_4(monkeypatch) -> None:
    def parse_error(directory, *, include_taxonomy=False):
        raise XbrlParseError("no xbrl")

    monkeypatch.setattr(cluefin_xbrl, "parse_xbrl_directory", parse_error)
    with pytest.raises(CliError) as excinfo:
        _run()
    assert excinfo.value.exit_code == 4 and excinfo.value.error_type == "ResponseParseError"

    monkeypatch.setattr(cluefin_xbrl, "parse_xbrl_directory", lambda d, *, include_taxonomy=False: _doc())

    def no_taxonomy(doc):
        raise ValueError("Taxonomy 정보가 필요합니다")

    monkeypatch.setattr(cluefin_xbrl, "extract_financial_statements", no_taxonomy)
    with pytest.raises(CliError) as excinfo:
        _run()
    assert excinfo.value.exit_code == 4


def test_client_errors_propagate_for_classification(install) -> None:
    install(_doc(), _parsed("1"))
    with pytest.raises(RuntimeError, match="boom"):
        _run(dart=_FakeDart(RuntimeError("boom")))


@pytest.mark.parametrize("statements", ["", "XX", "BS,XX", "BS,", ",BS", "bs", "BS, IS"])
def test_invalid_statements_is_exit_2(install, statements) -> None:
    install(_doc(), _parsed("1"))
    dart = _FakeDart()
    with pytest.raises(CliError) as excinfo:
        _run({"statements": statements}, dart=dart)
    assert excinfo.value.exit_code == 2
    assert dart.periodic_report_financial_statement.calls == []  # rejected before any download


def test_statements_subset_and_canonical_order(install) -> None:
    install(_doc(), _parsed("1", consolidated=("CIS", "BS", "CF"), separate=("CIS", "BS", "CF")))
    result = _run({"statements": "CF,BS"})
    assert list(result["statements"]) == ["BS", "CF"]
    assert result["missing"] == []


def test_fs_div_filters_bases(install) -> None:
    install(_doc(), _parsed("1"))
    cfs = _run({"statements": "CIS", "fs_div": "CFS"})
    assert list(cfs["statements"]["CIS"]) == ["consolidated"]
    ofs = _run({"statements": "CIS", "fs_div": "OFS"})
    assert list(ofs["statements"]["CIS"]) == ["separate"]
    both = _run({"statements": "CIS"})
    assert list(both["statements"]["CIS"]) == ["consolidated", "separate"]


def test_missing_lists_requested_but_absent_and_never_synthesizes_is_from_cis(install) -> None:
    # Nodemason-like: no IS key at all, income lives in CIS; no separate BS/CF either.
    install(_doc(), _parsed("1", consolidated=("CIS", "BS"), separate=("CIS",)))
    result = _run({"statements": "BS,IS,CIS"})
    assert "IS" not in result["statements"]
    assert result["missing"] == ["BS/separate", "IS/consolidated", "IS/separate"]
    assert set(result["statements"]) == {"BS", "CIS"}
    assert list(result["statements"]["BS"]) == ["consolidated"]


def test_company_without_consolidated_statements(install) -> None:
    install(_doc(), _parsed("1", consolidated=(), separate=("BS", "CIS")))
    result = _run({"statements": "BS,CIS", "fs_div": "CFS"})
    assert result["statements"] == {}
    assert result["missing"] == ["BS/consolidated", "CIS/consolidated"]


def test_period_columns_are_sorted_whatever_order_arelle_returns_them(install) -> None:
    base = _cis_items("28915427") + [
        _item("EquityComponent", "5", CURRENT, order=3.0, dims={"ComponentsOfEquityAxis": "B"}),
        _item("EquityComponent", "4", CURRENT, order=3.0, dims={"ComponentsOfEquityAxis": "A"}),
    ]
    expected = None
    for seed in range(6):
        # Node order is fixed by the presentation tree; only one node's facts come back shuffled.
        items = []
        for _, run in itertools.groupby(base, key=lambda i: i.concept_qname):
            run = list(run)
            random.Random(seed).shuffle(run)
            items.extend(run)
        parsed = ParsedFinancialStatements(
            source_file="x", entity_id=CORP, statements={"CIS": _statement("CIS", items)}
        )
        install(_doc(), parsed)
        rows = _run({"statements": "CIS", "fs_div": "CFS"})["statements"]["CIS"]["consolidated"]
        key = [(r["concept"], r["end_date"], r["value"]) for r in rows]
        if expected is None:
            expected = key
        assert key == expected

    assert [c for c, *_ in expected] == [
        "Revenue",
        "Revenue",
        "OperatingIncomeLoss",
        "OperatingIncomeLoss",
        "OperatingIncomeLoss",
        "EquityComponent",
        "EquityComponent",
    ]
    # Current period first, then older ones.
    assert [e for c, e, v in expected if c == "OperatingIncomeLoss"] == ["2024-12-31", "2023-12-31", "2022-12-31"]
    # Same period: dimensions break the tie (A before B).
    assert [v for c, e, v in expected if c == "EquityComponent"] == ["4", "5"]


def test_presentation_order_is_kept_across_parents(install) -> None:
    # `order` is sibling-relative: both parents' first child has order 1.0. Sorting on it would
    # pull CashAndCashEquivalents and PropertyPlantAndEquipment together.
    items = [
        _item("CurrentAssets", "10", CURRENT, order=1.0, label="유동자산"),
        _item("CashAndCashEquivalents", "3", CURRENT, order=1.0, label="현금및현금성자산"),
        _item("Inventories", "7", CURRENT, order=2.0, label="재고자산"),
        _item("NoncurrentAssets", "20", CURRENT, order=2.0, label="비유동자산"),
        _item("PropertyPlantAndEquipment", "20", CURRENT, order=1.0, label="유형자산"),
    ]
    parsed = ParsedFinancialStatements(source_file="x", entity_id=CORP, statements={"BS": _statement("BS", items)})
    install(_doc(), parsed)

    rows = _run({"statements": "BS", "fs_div": "CFS"})["statements"]["BS"]["consolidated"]

    assert [r["concept"] for r in rows] == [
        "CurrentAssets",
        "CashAndCashEquivalents",
        "Inventories",
        "NoncurrentAssets",
        "PropertyPlantAndEquipment",
    ]


def test_abstract_rows_are_skipped_and_none_value_stays_none(install) -> None:
    items = _cis_items("1") + [_item("Note", None, CURRENT, order=9.0, label="주석")]
    parsed = ParsedFinancialStatements(source_file="x", entity_id=CORP, statements={"CIS": _statement("CIS", items)})
    install(_doc(), parsed)
    rows = _run({"statements": "CIS", "fs_div": "CFS"})["statements"]["CIS"]["consolidated"]
    assert all(not r["concept"].endswith("Abstract") for r in rows)
    note = next(r for r in rows if r["concept"] == "Note")
    assert note["value"] is None and note["unit"] is None
    row = rows[0]
    assert set(row) == {
        "concept_qname",
        "concept",
        "label_ko",
        "label_en",
        "value",
        "unit",
        "period_type",
        "instant",
        "start_date",
        "end_date",
        "dimensions",
        "depth",
        "order",
    }
    assert row["period_type"] == "duration" and row["unit"] == "iso4217:KRW"


def test_instant_rows_carry_instant_only(install) -> None:
    install(_doc(), _parsed("1"))
    row = _run({"statements": "BS", "fs_div": "CFS"})["statements"]["BS"]["consolidated"][0]
    assert row["period_type"] == "instant" and row["instant"] == "2024-12-31"
    assert row["start_date"] is None and row["end_date"] is None


# --- through the CLI ---------------------------------------------------------


class _ExplodingFactory:
    def create(self, broker: str):
        raise AssertionError(f"broker client for `{broker}` must not be created here")


@pytest.fixture
def cli(monkeypatch):
    monkeypatch.setattr(registry_module, "BrokerClientFactory", _ExplodingFactory)
    set_registry_provider(lambda: RpcRegistry(client_factory=_ExplodingFactory()))
    yield
    set_registry_provider(EmptyRegistry)


def _argv(**params) -> list[str]:
    body = {"rcept_no": ORIGINAL, "reprt_code": "11011", "corp_code": CORP, **params}
    return ["dart", "financial-as-filed", "--params-json", json.dumps(body), "--json"]


def test_dry_run_never_touches_network_or_parser(cli, monkeypatch) -> None:
    def fail(*args, **kwargs):
        raise AssertionError("dry-run must not download or parse")

    monkeypatch.setattr(cluefin_xbrl, "parse_xbrl_directory", fail)
    result = run_cli([*_argv(), "--dry-run"])
    assert result.exit_code == 0, result.stdout
    assert json.loads(result.stdout)["dry_run"] is True


@pytest.mark.parametrize(
    "bad",
    [
        {"statements": "BS,XX"},
        {"statements": ""},
        {"rcept_no": "123"},
        {"corp_code": "1328170"},
        {"fs_div": "all"},
    ],
)
def test_cli_rejects_bad_params_with_exit_2_before_any_client(cli, bad) -> None:
    result = run_cli(_argv(**bad))
    assert result.exit_code == 2, result.stdout


def test_cli_requires_corp_code(cli) -> None:
    result = run_cli(
        [
            "dart",
            "financial-as-filed",
            "--params-json",
            json.dumps({"rcept_no": ORIGINAL, "reprt_code": "11011"}),
            "--json",
        ]
    )
    assert result.exit_code == 2
