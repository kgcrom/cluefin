"""NH PLUG 통합 테스트에서 "환경 때문에 검증 불가"를 구분해 skip 하는 헬퍼.

kiwoom 의 `tests/kiwoom/_integration_helpers.py` 와 같은 철학이다: 장 운영시간·
영업일·계좌 상태처럼 나중에 해소되는 제약으로 실패한 케이스를 실패로 남기면
실제 회귀를 가리므로 런타임 skip 으로 구분한다. 조건이 풀리면 코드 수정 없이
실제 검증이 재개된다.
"""

from typing import NoReturn

from cluefin_openapi.nhplug._exceptions import NHPlugAPIError

# 장 운영시간·영업일·계좌 상태 때문에 지금은 검증할 수 없다는 뜻의 rsp_cd.
# 입력 오류는 HTTP 400 + rsp_cd(IGW…)지만, 주문 거부는 HTTP 200 + rsp_cd 로 온다.
# 코드는 실측하며 채운다.
ENV_BLOCKED_CODES: tuple[str, ...] = (
    "14100",  # 모의투자 영업일이 아닙니다 (2026-08-22 토요일 실측)
)


def skip_if_env_blocked(e: NHPlugAPIError) -> NoReturn:
    """환경 제약이면 skip, 그 외 오류는 그대로 올려 실패로 남긴다.

    `except NHPlugAPIError as e: skip_if_env_blocked(e)` 형태로 쓴다. 정상 반환하는
    경로가 없으므로(항상 skip 이거나 raise) 호출부에서 뒤따르는 코드는 실행되지 않는다.
    """
    import pytest

    data = e.response_data or {}
    rsp_cd = data.get("rsp_cd") or ""
    msg = data.get("rsp_msg") or e.message
    if rsp_cd in ENV_BLOCKED_CODES or any(code in msg for code in ENV_BLOCKED_CODES):
        pytest.skip(f"장 운영시간/계좌 상태 때문에 검증 불가: [{rsp_cd}] {msg}")
    raise e
