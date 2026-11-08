"""`today_kst`/`now_kst` follow Seoul time whatever the machine's zone is."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from cluefin_openapi_cli import clock


class _FrozenDatetime(datetime):
    """`datetime.now(tz)` pinned to 2026-11-08 15:30 UTC — already 11-09 00:30 in Seoul."""

    @classmethod
    def now(cls, tz=None):  # noqa: ANN001, ANN206 - mirrors datetime.now
        instant = datetime(2026, 11, 8, 15, 30, tzinfo=UTC)
        return instant.astimezone(tz) if tz else instant.replace(tzinfo=None)


@pytest.fixture
def frozen(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(clock, "datetime", _FrozenDatetime)


def test_today_is_the_seoul_date(frozen: None) -> None:
    assert clock.today_kst().isoformat() == "2026-11-09"


def test_now_is_naive_seoul_wall_time(frozen: None) -> None:
    now = clock.now_kst()
    assert now.tzinfo is None
    assert now == datetime(2026, 11, 9, 0, 30)
