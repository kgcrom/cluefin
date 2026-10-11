"""`_integration_helpers`의 skip 판정 자체를 검증한다.

이 헬퍼가 잘못 넓게 잡으면 진짜 회귀가 조용히 skip 되어 통합 테스트가 무의미해진다.
"""

import pytest

from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

from ._integration_helpers import LIVE_MUTATION_FLAG, mutation_skip_reason, skip_if_env_blocked


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


# --- mutation_skip_reason: 주문·환전 테스트가 명시 없이 도는 일이 없어야 한다 ---


@pytest.mark.parametrize("markexpr", ["", "integration", "integration and realtime", "mutations", "not_mutation"])
@pytest.mark.parametrize("env", ["dev", "prod"])
def test_mutation_blocked_unless_markexpr_names_it(monkeypatch, markexpr: str, env: str):
    monkeypatch.setenv(LIVE_MUTATION_FLAG, "1")  # 플래그가 있어도 -m 명시가 먼저다

    assert mutation_skip_reason(markexpr, env) is not None


def test_mutation_runs_on_dev_when_markexpr_names_it(monkeypatch):
    monkeypatch.delenv(LIVE_MUTATION_FLAG, raising=False)

    assert mutation_skip_reason("integration and mutation", "dev") is None


@pytest.mark.parametrize("flag", [None, "", "0", "true", "yes"])
def test_mutation_on_prod_needs_flag_exactly_one(monkeypatch, flag):
    if flag is None:
        monkeypatch.delenv(LIVE_MUTATION_FLAG, raising=False)
    else:
        monkeypatch.setenv(LIVE_MUTATION_FLAG, flag)

    reason = mutation_skip_reason("integration and mutation", "prod")

    assert reason is not None
    assert LIVE_MUTATION_FLAG in reason


def test_mutation_runs_on_prod_with_flag(monkeypatch):
    monkeypatch.setenv(LIVE_MUTATION_FLAG, "1")

    assert mutation_skip_reason("integration and mutation", "prod") is None
