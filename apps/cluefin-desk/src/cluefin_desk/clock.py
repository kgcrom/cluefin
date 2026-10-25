"""한국 시장 기준 시각. 실행 머신의 시간대와 상관없이 KST 로 '오늘'과 '지금'을 정한다."""

from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")


def today_kst() -> date:
    return datetime.now(KST).date()


def now_kst() -> datetime:
    """KST 벽시계 시각(naive). API 날짜 파라미터(YYYYMMDD)를 만들 때 쓴다."""
    return datetime.now(KST).replace(tzinfo=None)
