from __future__ import annotations

from types import SimpleNamespace

import pytest
from _handler_fakes import FakeSession, assert_calls_client_once, assert_registers_all

from cluefin_openapi_cli.handlers import dart as handlers


@pytest.mark.parametrize("handler", handlers._ALL_HANDLERS, ids=lambda h: h._rpc_schema.name)
def test_handler_calls_underlying_client(handler) -> None:
    assert_calls_client_once(handler)


def test_register_dart_handlers() -> None:
    assert_registers_all(handlers.register_dart_handlers, handlers._ALL_HANDLERS, "dart")


def test_disclosure_search_forwards_only_provided_params() -> None:
    session = FakeSession()
    handlers.handle_disclosure_search({"corp_code": "00126380", "bgn_de": "20240101", "unknown": "x"}, session)
    _, method, _, kwargs = session.calls[0]
    assert method == "public_disclosure_search"
    assert kwargs == {"corp_code": "00126380", "bgn_de": "20240101"}


def test_corp_code_lookup_reads_items_from_the_result_envelope() -> None:
    session = FakeSession()
    result = handlers.handle_corp_code_lookup({}, session)
    assert result["total"] == result["returned"] == len(result["data"]) == 2
    assert result["truncated"] is False


def test_corp_code_lookup_handles_empty_list() -> None:
    session = FakeSession(output_value=None)
    result = handlers.handle_corp_code_lookup({}, session)
    assert result == {"total": 0, "returned": 0, "truncated": False, "data": []}


def test_corp_code_lookup_limit_caps_rows_and_flags_truncation() -> None:
    session = FakeSession()
    capped = handlers.handle_corp_code_lookup({"max_rows": 1}, session)
    assert capped["total"] == 2 and capped["returned"] == 1 and capped["truncated"] is True

    uncapped = handlers.handle_corp_code_lookup({"max_rows": 0}, session)
    assert uncapped["returned"] == 2 and uncapped["truncated"] is False


# DART's corp-code XML pads unlisted stock codes with spaces; the rows below mirror that.
_HANSAE = SimpleNamespace(corp_code="00188089", corp_name="한섬", stock_code="020000")
_HANSAE_UNLISTED = SimpleNamespace(corp_code="00999999", corp_name="한섬물산", stock_code="      ")
_APPLE = SimpleNamespace(corp_code="01234567", corp_name="Apple Korea", stock_code="   ")
_CORP_ROWS = [_HANSAE, _HANSAE_UNLISTED, _APPLE]


def _names(rows) -> list[str]:
    return [row.corp_name for row in rows]


def test_filter_corp_codes_matches_codes_exactly_after_stripping_padding() -> None:
    assert handlers._filter_corp_codes(_CORP_ROWS, {"corp_code": "00188089"}) == [_HANSAE]
    assert handlers._filter_corp_codes(_CORP_ROWS, {"corp_code": " 00188089 "}) == [_HANSAE]
    assert handlers._filter_corp_codes(_CORP_ROWS, {"stock_code": "020000"}) == [_HANSAE]
    # A prefix of the code is not a match, and padding alone never matches anything.
    assert handlers._filter_corp_codes(_CORP_ROWS, {"stock_code": "0200"}) == []
    assert handlers._filter_corp_codes(_CORP_ROWS, {"stock_code": "  "}) == _CORP_ROWS


def test_filter_corp_codes_matches_name_as_case_insensitive_substring() -> None:
    assert _names(handlers._filter_corp_codes(_CORP_ROWS, {"corp_name": "한섬"})) == ["한섬", "한섬물산"]
    assert _names(handlers._filter_corp_codes(_CORP_ROWS, {"corp_name": "apple"})) == ["Apple Korea"]
    assert _names(handlers._filter_corp_codes(_CORP_ROWS, {"corp_name": "KOREA"})) == ["Apple Korea"]
    assert handlers._filter_corp_codes(_CORP_ROWS, {"corp_name": "삼성"}) == []


def test_filter_corp_codes_listed_only_drops_space_padded_stock_codes() -> None:
    assert handlers._filter_corp_codes(_CORP_ROWS, {"listed_only": True}) == [_HANSAE]
    assert handlers._filter_corp_codes(_CORP_ROWS, {"listed_only": False}) == _CORP_ROWS
    assert handlers._filter_corp_codes(_CORP_ROWS, {"corp_name": "한섬", "listed_only": True}) == [_HANSAE]


@pytest.mark.parametrize("bad", ["abc", -1, None, 2.5j], ids=["str", "negative", "none", "complex"])
def test_max_rows_falls_back_to_default_on_unusable_values(bad) -> None:
    assert handlers._max_rows({"max_rows": bad}) == handlers._DEFAULT_MAX_ROWS


def test_max_rows_reads_zero_and_positive_values_as_given() -> None:
    assert handlers._max_rows({}) == handlers._DEFAULT_MAX_ROWS == 100
    assert handlers._max_rows({"max_rows": 0}) == 0
    assert handlers._max_rows({"max_rows": "7"}) == 7


def test_share_disclosure_handlers_use_the_share_disclosure_client() -> None:
    session = FakeSession()
    handlers.handle_large_holding_report({"corp_code": "00188089"}, session)
    handlers.handle_executive_ownership_report({"corp_code": "00188089"}, session)
    subs = [sub for sub, _, _, _ in session.calls]
    methods = [method for _, method, _, _ in session.calls]
    assert subs == ["share_disclosure_comprehensive"] * 2
    assert methods == ["large_holding_report", "executive_major_shareholder_ownership_report"]


# DART returns rcept_dt as `2026-09-09` on these endpoints; rows arrive in no fixed order.
_OLD = SimpleNamespace(rcept_dt="2024-03-01", repror="국민연금공단")
_MID = SimpleNamespace(rcept_dt="2025-06-15", repror="Hansae Holdings")
_NEW = SimpleNamespace(rcept_dt="2026-09-09", repror="국민연금공단")
_UNDATED = SimpleNamespace(rcept_dt=None, repror="김대표")
_SHARE_ROWS = [_MID, _OLD, _NEW]


def test_filter_share_rows_sorts_newest_first() -> None:
    assert handlers._filter_share_rows(_SHARE_ROWS, {}) == [_NEW, _MID, _OLD]


def test_filter_share_rows_date_bounds_are_inclusive_and_ignore_separators() -> None:
    since_only = handlers._filter_share_rows(_SHARE_ROWS, {"since": "20250615"})
    assert since_only == [_NEW, _MID]
    until_only = handlers._filter_share_rows(_SHARE_ROWS, {"until": "2025-06-15"})
    assert until_only == [_MID, _OLD]
    both = handlers._filter_share_rows(_SHARE_ROWS, {"since": "20240302", "until": "20260908"})
    assert both == [_MID]


def test_filter_share_rows_keeps_undated_rows_under_date_bounds() -> None:
    rows = handlers._filter_share_rows([_OLD, _UNDATED], {"since": "20250101"})
    assert rows == [_UNDATED]


def test_filter_share_rows_matches_reporter_as_case_insensitive_substring() -> None:
    assert handlers._filter_share_rows(_SHARE_ROWS, {"reporter": "국민연금"}) == [_NEW, _OLD]
    assert handlers._filter_share_rows(_SHARE_ROWS, {"reporter": "hansae"}) == [_MID]
    assert handlers._filter_share_rows(_SHARE_ROWS, {"reporter": "삼성"}) == []


def test_share_disclosure_handles_empty_list() -> None:
    session = FakeSession(output_value=None)
    result = handlers.handle_executive_ownership_report({"corp_code": "x"}, session)
    assert result == {"total": 0, "returned": 0, "truncated": False, "data": []}


def test_share_disclosure_max_rows_caps_rows_and_flags_truncation() -> None:
    session = FakeSession()
    capped = handlers.handle_large_holding_report({"corp_code": "x", "max_rows": 1}, session)
    assert capped["total"] == 2 and capped["returned"] == 1 and capped["truncated"] is True


def test_financial_statement_handlers_forward_the_report_key() -> None:
    session = FakeSession()
    key = {"corp_code": "00381756", "bsns_year": "2026", "reprt_code": "11012"}
    handlers.handle_financial_major_accounts(key, session)
    handlers.handle_financial_full_statements(key, session)
    handlers.handle_financial_major_indicators({**key, "idx_cl_code": "M210000"}, session)

    assert [sub for sub, _, _, _ in session.calls] == ["periodic_report_financial_statement"] * 3
    assert [method for _, method, _, _ in session.calls] == [
        "get_single_company_major_accounts",
        "get_single_company_full_statements",
        "get_single_company_major_indicators",
    ]
    assert session.calls[0][3] == key
    # fs_div defaults to consolidated so the agent never has to know the DART code.
    assert session.calls[1][3] == {**key, "fs_div": "CFS"}
    assert session.calls[2][3] == {**key, "idx_cl_code": "M210000"}
