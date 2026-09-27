"""HTTP 200 + body rsp_cd 실패를 코드별 예외로 나누는지 확인한다."""

import pytest
import requests_mock

from cluefin_openapi.nhplug._exceptions import (
    NHPlugAPIError,
    NHPlugMockUnsupportedError,
    NHPlugNoDataError,
    NHPlugNotBusinessDayError,
    raise_for_rsp_cd,
)
from cluefin_openapi.nhplug._model import SUCCESS_RSP_CODES

from ._unit_helpers import make_client

BASE_PROD = "https://api.nhplug.com:8443"


@pytest.mark.parametrize("rsp_cd", SUCCESS_RSP_CODES)
def test_success_codes_do_not_raise(rsp_cd):
    raise_for_rsp_cd({"rsp_cd": rsp_cd, "rsp_msg": "조회가 완료되었습니다."})


def test_missing_rsp_cd_does_not_raise():
    raise_for_rsp_cd({"Output_0": []})


@pytest.mark.parametrize(
    "rsp_cd, rsp_msg, error_type",
    [
        ("13578", "조회할 내역이 없습니다.", NHPlugNoDataError),
        ("11512", "데이터가 존재하지 않습니다.", NHPlugNoDataError),
        ("16935", "해당 잔고가 없습니다.", NHPlugNoDataError),
        ("19999", "모의투자에서는 해당업무가 제공되지 않습니다.", NHPlugMockUnsupportedError),
        ("14100", "모의투자 영업일이 아닙니다.", NHPlugNotBusinessDayError),
    ],
)
def test_known_codes_raise_dedicated_error(rsp_cd, rsp_msg, error_type):
    with pytest.raises(error_type) as exc_info:
        raise_for_rsp_cd({"rsp_cd": rsp_cd, "rsp_msg": rsp_msg})

    error = exc_info.value
    # 전용 예외도 NHPlugAPIError 하위라 기존 `except NHPlugAPIError` 가 그대로 잡는다.
    assert isinstance(error, NHPlugAPIError)
    assert error.rsp_cd == rsp_cd
    assert error.status_code == 200
    assert str(error) == f"[200] API error {rsp_cd}: {rsp_msg}"


def test_unknown_code_raises_base_error():
    with pytest.raises(NHPlugAPIError) as exc_info:
        raise_for_rsp_cd({"rsp_cd": "40010", "rsp_msg": "계좌번호 오류"})

    assert type(exc_info.value) is NHPlugAPIError
    assert exc_info.value.rsp_cd == "40010"


def test_rsp_cd_is_none_without_response_data():
    assert NHPlugAPIError("network").rsp_cd is None


def test_client_raises_no_data_error_for_empty_result():
    client = make_client("prod")
    with requests_mock.Mocker() as m:
        m.post(
            f"{BASE_PROD}/krstock/inquiry/v1/sellableQuantity",
            json={"rsp_cd": "16935", "rsp_msg": "해당 잔고가 없습니다."},
        )
        with pytest.raises(NHPlugNoDataError):
            client.krstock_inquiry.sellable_quantity(act_no="50051036881", iem_cd="005930", cfd_lon_cd="00")
