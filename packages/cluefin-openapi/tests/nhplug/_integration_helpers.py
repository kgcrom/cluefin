"""NH PLUG 통합 테스트에서 "환경 때문에 검증 불가"를 구분해 skip 하는 헬퍼.

kiwoom 의 `tests/kiwoom/_integration_helpers.py` 와 같은 철학이다. 두 갈래로 나눈다.

- `real_account_only`: 모의투자에서 **영구적으로** 안 되는 API → 수집 시점 정적 skip.
- `skip_if_env_blocked`: 장 운영시간·영업일·계좌 상태처럼 **나중에 해소되는** 제약 →
  런타임 skip. 조건이 풀리면 코드 수정 없이 실제 검증이 재개된다.
"""

import os
from typing import NoReturn

import dotenv
import pytest

from cluefin_openapi.nhplug._exceptions import NO_DATA_RSP_CODES, NOT_BUSINESS_DAY_RSP_CODES, NHPlugAPIError

# 모듈 임포트(= 테스트 수집) 시점에 로드해야 모듈 레벨 skipif 가 NHPLUG_ENV 를 볼 수 있다.
dotenv.load_dotenv(dotenv_path=".env.test")


def nhplug_env() -> str:
    """테스트가 붙을 NH PLUG 환경. dev=모의투자(moapi), prod=운영(실제 체결)."""
    return os.getenv("NHPLUG_ENV", "dev").lower()


def mock_omits(*fields: str) -> tuple[str, ...]:
    """모의 서버가 보내지 않는 스펙 필드 — `assert_matches_spec(..., ignore=)` 에 넘긴다.

    모의(moapi)는 스펙에 있는 필드 일부를 키째 생략한다 (VENDOR_DOC_ERRATA.md). 운영에서
    보내는지는 확인하지 못했으므로 모델에서 지우지 않고, 운영(prod)에서는 그대로 검사한다.
    """
    return fields if nhplug_env() != "prod" else ()


def real_account_only(api: str, error: str) -> pytest.MarkDecorator:
    """모의투자에서 제공되지 않는 API 를 운영 전용으로 표시한다.

    Args:
        api: API 경로 또는 이름 (예: "/krstock/order/v1/creditBuy").
        error: 모의투자에서 실제로 돌아오는 오류 문자열. 왜 skip 인지 추적할 근거로 남긴다.
    """
    return pytest.mark.skipif(
        nhplug_env() != "prod",
        reason=f"{api}은 모의투자에서 제공되지 않는다 ({error}). 운영(NHPLUG_ENV=prod)에서만 검증 가능하다.",
    )


# 장 운영시간·영업일·계좌 상태 때문에 지금은 검증할 수 없다는 뜻의 rsp_cd.
# 입력 오류는 HTTP 400 + rsp_cd(IGW…)지만, 주문 거부는 HTTP 200 + rsp_cd 로 온다.
# 코드는 실측하며 채운다 — 클라이언트의 분류를 그대로 쓴다.
# - 영업일 아님(NOT_BUSINESS_DAY_RSP_CODES)
# - 빈 결과(NO_DATA_RSP_CODES): 잔고·내역이 없는 계좌에서는 응답 형태를 검증할 수 없다.
#   계좌에 데이터가 생기면 코드 수정 없이 검증이 재개된다.
ENV_BLOCKED_CODES: tuple[str, ...] = NOT_BUSINESS_DAY_RSP_CODES + NO_DATA_RSP_CODES


def skip_if_env_blocked(e: NHPlugAPIError) -> NoReturn:
    """환경 제약이면 skip, 그 외 오류는 그대로 올려 실패로 남긴다.

    `except NHPlugAPIError as e: skip_if_env_blocked(e)` 형태로 쓴다. 정상 반환하는
    경로가 없으므로(항상 skip 이거나 raise) 호출부에서 뒤따르는 코드는 실행되지 않는다.
    """
    data = e.response_data or {}
    rsp_cd = data.get("rsp_cd") or ""
    msg = data.get("rsp_msg") or e.message
    if rsp_cd in ENV_BLOCKED_CODES or any(code in msg for code in ENV_BLOCKED_CODES):
        pytest.skip(f"장 운영시간/계좌 상태(빈 결과 포함) 때문에 검증 불가: [{rsp_cd}] {msg}")
    raise e
