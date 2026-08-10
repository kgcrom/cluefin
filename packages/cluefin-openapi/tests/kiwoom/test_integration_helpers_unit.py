"""`_integration_helpers`의 skip 판정 자체를 검증한다.

이 헬퍼가 잘못 넓게 잡으면 진짜 회귀가 조용히 skip 되어 통합 테스트가 무의미해진다.
"""

import pytest

from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

from ._integration_helpers import skip_if_env_blocked


def _error(return_msg: str) -> KiwoomAPIError:
    return KiwoomAPIError(
        message=f"[200] Kiwoom API error 20: {return_msg}",
        status_code=200,
        response_data={"return_code": 20, "return_msg": return_msg},
    )


@pytest.mark.parametrize(
    "return_msg",
    [
        "[2000](RC4091:모의투자 종료된 계좌입니다. 다시 신청해주시기 바랍니다.)",
        "[2000](RC4061:모의투자 주문번호를 확인하세요.)",
        "[2000](RC4032:모의투자 원주문번호가 존재하지 않습니다.)",
        "[2000](RC4058:모의투자 장종료)",
        "[2000](RC4010:모의투자 영업일이 아닙니다.)",
    ],
)
def test_skips_on_env_blocked_codes(return_msg: str):
    with pytest.raises(pytest.skip.Exception) as excinfo:
        skip_if_env_blocked(_error(return_msg))

    assert return_msg in str(excinfo.value)


@pytest.mark.parametrize(
    "return_msg",
    [
        # 모의 미지원은 런타임 skip 대상이 아니다 — real_account_only 로 정적 skip 한다.
        "[2000](RC9000:모의투자에서는 해당업무가 제공되지 않습니다.)",
        "입력 값 오류입니다[8104:모의투자에서 지원하지 않는 API 입니다.]",
        # 구현/파라미터 버그는 반드시 실패로 남아야 한다.
        "[2000](1511:입력값을 확인하세요.)",
        "[2000](8031:투자구분(실전/모의)이 달라서 Token를 사용할수가 없습니다.)",
    ],
)
def test_reraises_other_errors(return_msg: str):
    error = _error(return_msg)

    with pytest.raises(KiwoomAPIError) as excinfo:
        skip_if_env_blocked(error)

    assert excinfo.value is error


def test_falls_back_to_message_when_response_data_missing():
    error = KiwoomAPIError(message="[2000](RC4058:모의투자 장종료)", status_code=200)

    with pytest.raises(pytest.skip.Exception):
        skip_if_env_blocked(error)
