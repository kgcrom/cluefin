"""키움 통합 테스트에서 "환경 때문에 검증 불가"를 구분해 skip 하는 헬퍼.

모의투자(KIWOOM_ENV=dev)는 상당수 API를 아예 제공하지 않는다. 그 실패는 라이브러리
버그가 아니므로 실패로 남겨두면 실제 회귀를 가린다. 두 갈래로 나눈다.

- `real_account_only`: 모의투자에서 **영구적으로** 안 되는 API → 수집 시점 정적 skip.
- `skip_if_env_blocked`: 계좌 상태·장 운영시간처럼 **나중에 해소되는** 제약 → 런타임 skip.
  조건이 풀리면 코드를 고치지 않아도 실제 검증이 재개된다.
"""

import os
import re
from typing import Callable, List, NoReturn, Optional

import dotenv
import pytest

from cluefin_openapi.kiwoom._exceptions import KiwoomAPIError

# 모듈 임포트(= 테스트 수집) 시점에 로드해야 모듈 레벨 skipif가 KIWOOM_ENV를 볼 수 있다.
# 픽스처 안에서만 로드하면 skipif는 셸 env(보통 미설정)만 읽고 기본값 "dev"로 떨어진다.
dotenv.load_dotenv(dotenv_path=".env.test")


def kiwoom_env() -> str:
    """테스트가 붙을 키움 환경. dev=모의투자, prod=실계좌."""
    return os.getenv("KIWOOM_ENV", "dev").lower()


def real_account_only(api_id: str, error: str) -> pytest.MarkDecorator:
    """모의투자에서 제공되지 않는 API를 실계좌 전용으로 표시한다.

    Args:
        api_id: 키움 api-id (예: "kt00002").
        error: 모의투자에서 실제로 돌아오는 오류 문자열. 왜 skip 인지 추적할 근거로 남긴다.
    """
    return pytest.mark.skipif(
        kiwoom_env() != "prod",
        reason=(f"{api_id}은 모의투자에서 제공되지 않는다 ({error}). 실계좌(KIWOOM_ENV=prod)에서만 검증 가능하다."),
    )


# 계좌 상태·장 운영시간 때문에 지금은 검증할 수 없다는 뜻의 응답 코드.
ENV_BLOCKED_CODES = (
    "RC4091",  # 모의투자 종료된 계좌입니다 — 해외 모의투자 계좌 재신청 필요
    "RC4061",  # 모의투자 주문번호를 확인하세요 — 만료 계좌라 주문 접수부터 실패할 때 동반된다
    "RC4032",  # 모의투자 원주문번호가 존재하지 않습니다
    "RC4058",  # 모의투자 장종료
    "RC4010",  # 모의투자 영업일이 아닙니다
)


def skip_if_env_blocked(e: KiwoomAPIError) -> NoReturn:
    """환경 제약이면 skip, 그 외 오류는 그대로 올려 실패로 남긴다.

    `except KiwoomAPIError as e: skip_if_env_blocked(e)` 형태로 쓴다. 정상 반환하는
    경로가 없으므로(항상 skip 이거나 raise) 호출부에서 뒤따르는 코드는 실행되지 않는다.
    """
    msg = (e.response_data or {}).get("return_msg") or e.message
    if any(code in msg for code in ENV_BLOCKED_CODES):
        pytest.skip(f"계좌 상태/장 운영시간 때문에 검증 불가: {msg}")
    raise e


# 실계좌(prod)에서 주문·환전 테스트를 허용하는 플래그. pyproject·.env 에 두지 않고, 실행하는 사람이
# 셸에서 직접 준다 — 설정 파일에 남으면 다음 실행이 모르는 사이에 실계좌로 주문을 낸다.
LIVE_MUTATION_FLAG = "CLUEFIN_TEST_LIVE_MUTATION"


def _markexpr_names(markexpr: str, name: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", markexpr) is not None


def mutation_skip_reason(markexpr: str, env: str) -> Optional[str]:
    """`mutation` 테스트(주문·환전 접수)를 지금 돌리면 안 되는 이유. 돌려도 되면 None.

    - `-m` 에 `mutation` 이 없으면 막는다: `-m integration` 만으로는 주문이 나가지 않게.
    - prod 는 `CLUEFIN_TEST_LIVE_MUTATION=1` 까지 있어야 한다.
    """
    if not _markexpr_names(markexpr, "mutation"):
        return '주문·환전을 실제로 접수한다 — -m 에 mutation 을 적어야 돈다 (예: -m "integration and mutation")'
    if env == "prod" and os.getenv(LIVE_MUTATION_FLAG) != "1":
        return f"KIWOOM_ENV=prod 는 실계좌다 — {LIVE_MUTATION_FLAG}=1 을 직접 줘야 돈다"
    return None


def cancel_leftover_orders(ord_nos: List[str], cancel: Callable[[str], object]) -> None:
    """테스트가 접수하고 남긴 미체결 주문을 취소한다 (주문 테스트 픽스처의 teardown 용).

    하나라도 취소하지 못하면 주문번호를 담아 실패시킨다 — 조용히 넘어가면 계좌에 주문이 남은 걸
    아무도 모른다. 이미 취소·정정된 주문은 호출부가 목록에서 빼 두어야 한다.
    """
    failed = []
    for ord_no in ord_nos:
        try:
            cancel(ord_no)
        except KiwoomAPIError as e:
            failed.append(f"{ord_no} ({e.message})")
    if failed:
        pytest.fail("미체결 주문을 취소하지 못했다 — 직접 취소해야 한다: " + ", ".join(failed))
