from __future__ import annotations

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


def test_corp_code_lookup_filters_drop_non_matching_rows() -> None:
    session = FakeSession()
    # Faked rows answer "1" to every field, so any other value must filter them out.
    assert handlers.handle_corp_code_lookup({"stock_code": "020000"}, session)["total"] == 0
    assert handlers.handle_corp_code_lookup({"corp_code": "00188089"}, session)["total"] == 0
    assert handlers.handle_corp_code_lookup({"corp_name": "한섬"}, session)["total"] == 0
    assert handlers.handle_corp_code_lookup({"stock_code": "1"}, session)["total"] == 2


def test_corp_code_lookup_limit_caps_rows_and_flags_truncation() -> None:
    session = FakeSession()
    capped = handlers.handle_corp_code_lookup({"max_rows": 1}, session)
    assert capped["total"] == 2 and capped["returned"] == 1 and capped["truncated"] is True

    uncapped = handlers.handle_corp_code_lookup({"max_rows": 0}, session)
    assert uncapped["returned"] == 2 and uncapped["truncated"] is False


def test_share_disclosure_handlers_use_the_share_disclosure_client() -> None:
    session = FakeSession()
    handlers.handle_large_holding_report({"corp_code": "00188089"}, session)
    handlers.handle_executive_ownership_report({"corp_code": "00188089"}, session)
    subs = [sub for sub, _, _, _ in session.calls]
    methods = [method for _, method, _, _ in session.calls]
    assert subs == ["share_disclosure_comprehensive"] * 2
    assert methods == ["large_holding_report", "executive_major_shareholder_ownership_report"]


def test_share_disclosure_date_filters_drop_out_of_range_rows() -> None:
    session = FakeSession()
    # Faked rows report rcept_dt "1", so any real date bound filters them out.
    assert handlers.handle_large_holding_report({"corp_code": "x", "since": "20260101"}, session)["total"] == 0
    assert handlers.handle_large_holding_report({"corp_code": "x", "until": "20200101"}, session)["total"] == 2
    assert handlers.handle_large_holding_report({"corp_code": "x", "reporter": "국민연금"}, session)["total"] == 0
    assert handlers.handle_large_holding_report({"corp_code": "x"}, session)["total"] == 2


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
