"""관심종목 표의 "그룹" 열 — `cache/trend.py`의 추세 셋업 그룹(1·2·3그룹)을 읽어 붙인다.

KIS 를 부르지 않는다. `cluefin_openapi_cli.cache`의 로컬 DuckDB 캐시를 읽기 전용으로 열어
`scan(codes=...)`에 넘길 뿐이다(여러 종목을 한 번에 판정하므로 종목별 호출보다 싸다). 캐시 파일이
없거나(`cache load` 를 아직 안 돌렸거나), `cache load` 가 쓰는 중이라 잠겨 있거나, 판정 중 어떤
예외가 나도 빈 dict 를 돌려준다 — 호출부가 누락된 종목을 "-" 로 채운다. 그룹 열 하나가 비는 것이지
관심종목 화면 전체가 멎지는 않는다.
"""

from __future__ import annotations

import logging
from typing import Any

from cluefin_openapi_cli.cache import store
from cluefin_openapi_cli.cache.trend import latest_index_date, scan

logger = logging.getLogger(__name__)

__all__ = ["NO_GROUP", "lookup_trend_groups"]

NO_GROUP = "-"
_GROUP_ORDER = ("g1", "g2", "g3")


def _label(groups: dict[str, Any]) -> str:
    """``groups`` (``trend_setup.classify`` 의 ``{"g1": bool, "g2": bool, "g3": bool}``, 중복 가능)를
    "1"·"2,3" 같은 라벨로. 어느 그룹도 아니면 ``NO_GROUP``."""

    active = [name[-1] for name in _GROUP_ORDER if groups.get(name)]
    return ",".join(active) if active else NO_GROUP


def lookup_trend_groups(codes: list[str], *, cache_path: Any = None) -> dict[str, str]:
    """code -> 그룹 라벨. 캐시가 없거나 실패하면 빈 dict."""

    if not codes:
        return {}
    path = cache_path if cache_path is not None else store.cache_path()
    try:
        conn = store.open_store(path, read_only=True)
    except Exception as e:
        logger.warning(f"Trend-setup cache unavailable: {e}")
        return {}
    try:
        as_of = latest_index_date(conn)
        if as_of is None:
            return {}
        payload = scan(conn, as_of, codes=codes, include_excluded=True)
    except Exception as e:
        logger.warning(f"Trend-setup scan failed: {e}")
        return {}
    finally:
        conn.close()
    return {row["code"]: _label(row["groups"]) for row in payload["rows"]}
