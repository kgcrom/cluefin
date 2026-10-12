"""브로커 공용 실시간(WebSocket) 통합 테스트 실행 조건.

실시간 테스트는 장중에만 데이터가 오므로 `-m "integration and realtime"` 으로 명시했을 때, 그리고 해당
시장이 열려 있을 때만 돈다. 공휴일은 따지지 않는다.

브로커별 테스트 디렉터리는 서로 import 할 수 없는 별도 패키지라 헬퍼 모듈 대신 여기 fixture 로 둔다.
모듈에서 `pytest.mark.usefixtures("krx_continuous_hours", ...)` 로 쓴다 — 네트워크를 타는 fixture 는
그 뒤에 나열해야 장외에 인증부터 하지 않는다.
"""

import re
from datetime import datetime, time
from zoneinfo import ZoneInfo

import pytest


def _markexpr_includes(markexpr: str, name: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", markexpr) is not None


def _weekday_between(tz: str, open_: time, close: time) -> bool:
    now = datetime.now(ZoneInfo(tz))
    return now.weekday() < 5 and open_ <= now.time() <= close


@pytest.fixture(scope="module")
def realtime_selected(request: pytest.FixtureRequest) -> None:
    markexpr = request.config.option.markexpr or ""
    if not (_markexpr_includes(markexpr, "integration") and _markexpr_includes(markexpr, "realtime")):
        pytest.skip('Requires -m "integration and realtime"')


@pytest.fixture(scope="module")
def krx_continuous_hours(realtime_selected) -> None:
    """국내 주식 정규장 연속매매: 평일 09:00–15:20 KST. 15:20 이후는 종가 단일가라 체결이 오지 않는다."""
    if not _weekday_between("Asia/Seoul", time(9, 0), time(15, 20)):
        pytest.skip("Requires KRX continuous trading hours (Mon-Fri 09:00-15:20 KST)")


@pytest.fixture(scope="module")
def kst_market_hours(realtime_selected) -> None:
    """장내채권 등 국내 정규장: 평일 09:00–15:30 KST."""
    if not _weekday_between("Asia/Seoul", time(9, 0), time(15, 30)):
        pytest.skip("Requires KST market hours (Mon-Fri 09:00-15:30)")


@pytest.fixture(scope="module")
def us_market_hours(realtime_selected) -> None:
    """미국 정규장: 평일 09:30–16:00 America/New_York (서머타임 자동 반영)."""
    if not _weekday_between("America/New_York", time(9, 30), time(16, 0)):
        pytest.skip("Requires US market hours (Mon-Fri 09:30-16:00 America/New_York)")
