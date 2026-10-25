"""Live check against home.treasury.gov (read-only, no key)."""

import datetime as dt

import pytest

from cluefin_feeds.treasury import Client

pytestmark = pytest.mark.integration


def test_par_yield_curve_recent_month():
    client = Client()
    today = dt.date.today()
    rows = client.par_yield_curve(today.strftime("%Y%m"))
    if not rows:  # 달 초에는 이번 달이 비어 있다
        last_month = today.replace(day=1) - dt.timedelta(days=1)
        rows = client.par_yield_curve(last_month.strftime("%Y%m"))
    assert rows
    latest = rows[-1]
    assert (today - latest.date).days < 45
    assert latest.year_10 is not None
    assert 0 < latest.year_10 < 20
    # 피드에 새 만기가 생기면 모델에 선언해야 한다.
    assert not latest.model_extra, f"선언 안 된 필드: {latest.model_extra}"


def test_whole_year():
    rows = Client().par_yield_curve("2025")
    assert 245 <= len(rows) <= 255
    assert rows[0].date == dt.date(2025, 1, 2)
