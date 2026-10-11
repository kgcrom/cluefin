"""KIS 실시간(WebSocket) 통합 테스트가 함께 쓰는 실행 조건.

실시간 테스트는 장중에만 데이터가 오므로 `-m "integration and realtime"` 으로 명시했을 때, 그리고 해당
시장이 열려 있을 때만 돈다. 공휴일은 따지지 않는다.
"""

import re
from datetime import datetime, time
from zoneinfo import ZoneInfo

import pytest


def markexpr_includes(markexpr: str, name: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", markexpr) is not None


def require_integration_and_realtime(request: pytest.FixtureRequest) -> None:
    markexpr = request.config.option.markexpr or ""
    if not (markexpr_includes(markexpr, "integration") and markexpr_includes(markexpr, "realtime")):
        pytest.skip('Requires -m "integration and realtime"')


def _weekday_between(tz: str, open_: time, close: time) -> bool:
    now = datetime.now(ZoneInfo(tz))
    return now.weekday() < 5 and open_ <= now.time() <= close


def is_krx_continuous_hours() -> bool:
    """국내 주식 정규장 연속매매: 평일 09:00–15:20 KST. 15:20 이후는 종가 단일가라 체결이 오지 않는다."""
    return _weekday_between("Asia/Seoul", time(9, 0), time(15, 20))


def is_kst_market_hours() -> bool:
    """장내채권 등 국내 정규장: 평일 09:00–15:30 KST."""
    return _weekday_between("Asia/Seoul", time(9, 0), time(15, 30))


def is_us_market_hours() -> bool:
    """미국 정규장: 평일 09:30–16:00 America/New_York (서머타임 자동 반영)."""
    return _weekday_between("America/New_York", time(9, 30), time(16, 0))
