from __future__ import annotations

from types import SimpleNamespace

import pytest
from _handler_fakes import assert_calls_client_once, assert_registers_all

from cluefin_openapi_cli.handlers.kis import domestic_issue_other as handlers


@pytest.mark.parametrize("handler", handlers._ALL_HANDLERS, ids=lambda h: h._rpc_schema.name)
def test_handler_calls_underlying_client(handler) -> None:
    assert_calls_client_once(handler)


def test_register_kis_issue_other_handlers() -> None:
    assert_registers_all(handlers.register_kis_issue_other_handlers, handlers._ALL_HANDLERS, "kis")


class _Row:
    """KIS output 행 스텁 — extract_output 이 부르는 model_dump 만 있으면 된다."""

    def __init__(self, **fields: str) -> None:
        self._fields = fields

    def model_dump(self) -> dict[str, str]:
        return dict(self._fields)


class _InterestRateSession:
    """get_interest_rate_summary 호출 인자를 기록하고 주어진 output 을 돌려준다."""

    def __init__(self, output1: list[_Row], output2: list[_Row]) -> None:
        self.calls: list[tuple] = []
        self._body = SimpleNamespace(output1=output1, output2=output2)

    def get_kis(self):
        return SimpleNamespace(domestic_issue_other=self)

    def get_interest_rate_summary(self, *args):
        self.calls.append(args)
        return SimpleNamespace(body=self._body)


# 2026-09-20 실서버 원문에서 옮긴 행들.
_DOMESTIC_ROW = _Row(
    bcdt_code="Y0106",
    hts_kor_isnm="국고채 10년",
    bond_mnrt_prpr="4.4660",
    prdy_vrss_sign="5",
    bond_mnrt_prdy_vrss="-0.0400",
    prdy_ctrt="-0.89",
    stck_bsop_date="20260918",
)
_FOREIGN_ROW = _Row(
    bcdt_code="Y0202",
    hts_kor_isnm="미국 10년T-NOTE 수익률",
    bond_mnrt_prpr="5.0100",
    prdy_vrss_sign="2",
    bond_mnrt_prdy_vrss="0.0700",
    prdy_ctrt="1.42",
    stck_bsop_date="20260918",
)
# output2 는 전일대비율을 bstp_nmix_prdy_ctrt 로 싣는다.
_OUTPUT2_ROW = _Row(
    bcdt_code="Y0117",
    hts_kor_isnm="국고채 30년",
    bond_mnrt_prpr="4.5730",
    prdy_vrss_sign="5",
    bond_mnrt_prdy_vrss="-0.0340",
    bstp_nmix_prdy_ctrt="-0.74",
    stck_bsop_date="20260918",
)
# div_cls_code="1" 의 output2 앞부분 — 종목명 자리에 자료코드가 온 깨진 행.
_SHIFTED_ROW = _Row(
    bcdt_code="Y0101",
    hts_kor_isnm="Y0109",
    bond_mnrt_prpr="Y0117",
    prdy_vrss_sign="국고채 30년",
    bond_mnrt_prdy_vrss="4.5730",
    bstp_nmix_prdy_ctrt="5",
    stck_bsop_date="-0.0340",
)


def test_interest_rate_requests_domestic_and_foreign_by_default() -> None:
    """div_cls_code 기본값 1 은 국내 19종 중 8종만 돌려준다 — 2 로 전체를 받는다."""
    session = _InterestRateSession([_DOMESTIC_ROW], [])

    handlers.handle_kis_interest_rate_summary({}, session)

    assert session.calls == [("I", "20702", "2", "")]


def test_interest_rate_splits_by_data_code_not_array_name() -> None:
    session = _InterestRateSession([_DOMESTIC_ROW, _FOREIGN_ROW], [])

    result = handlers.handle_kis_interest_rate_summary({}, session)

    assert [row["bcdt_code"] for row in result["domestic"]] == ["Y0106"]
    assert [row["bcdt_code"] for row in result["foreign"]] == ["Y0202"]


def test_interest_rate_drops_shifted_rows() -> None:
    session = _InterestRateSession([], [_SHIFTED_ROW, _OUTPUT2_ROW])

    result = handlers.handle_kis_interest_rate_summary({"div_cls_code": "1"}, session)

    assert [row["bcdt_code"] for row in result["domestic"]] == ["Y0117"]
    assert result["foreign"] == []


def test_interest_rate_dedupes_output2_and_normalizes_change_rate() -> None:
    session = _InterestRateSession([_DOMESTIC_ROW], [_DOMESTIC_ROW, _OUTPUT2_ROW])

    result = handlers.handle_kis_interest_rate_summary({}, session)

    assert [row["bcdt_code"] for row in result["domestic"]] == ["Y0106", "Y0117"]
    assert result["domestic"][1]["prdy_ctrt"] == "-0.74"
    assert "bstp_nmix_prdy_ctrt" not in result["domestic"][1]
