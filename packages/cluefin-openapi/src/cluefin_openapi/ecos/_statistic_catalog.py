"""통계 목록 (StatisticTableList · StatisticItemList · KeyStatisticList)."""

from __future__ import annotations

from typing import Optional

from ._client import Client, Lang
from ._model import EcosPage
from ._statistic_catalog_types import KeyStatistic, StatisticItem, StatisticTable


class StatisticCatalog:
    """어떤 통계표·항목이 있는지 찾는 서비스들"""

    def __init__(self, client: Client):
        self.client = client

    def table_list(
        self,
        stat_code: Optional[str] = None,
        *,
        lang: Lang = "kr",
        start_row: Optional[int] = None,
        end_row: Optional[int] = None,
    ) -> EcosPage[StatisticTable]:
        """서비스 통계 목록 (OA-1020).

        Args:
            stat_code: 통계표코드. 생략하면 분류 행까지 포함한 전체 목록(2026-10 기준 844행)
        """
        segments = (stat_code,) if stat_code else ()
        total, rows, row_count = self.client._get_rows("StatisticTableList", segments, lang, start_row, end_row)
        return EcosPage[StatisticTable].model_validate({"list_total_count": total, "row_count": row_count, "row": rows})

    def item_list(
        self,
        stat_code: str,
        *,
        lang: Lang = "kr",
        start_row: Optional[int] = None,
        end_row: Optional[int] = None,
    ) -> EcosPage[StatisticItem]:
        """통계 세부항목 목록 (OA-1030). StatisticSearch 에 넣을 항목코드를 찾는 데 쓴다."""
        total, rows, row_count = self.client._get_rows("StatisticItemList", (stat_code,), lang, start_row, end_row)
        return EcosPage[StatisticItem].model_validate({"list_total_count": total, "row_count": row_count, "row": rows})

    def key_statistic_list(
        self,
        *,
        lang: Lang = "kr",
        start_row: Optional[int] = None,
        end_row: Optional[int] = None,
    ) -> EcosPage[KeyStatistic]:
        """100대 통계지표 (OA-1010) — 지표마다 최근 값 하나. 행 순서는 호출마다 같다는 보장이 없다."""
        total, rows, row_count = self.client._get_rows("KeyStatisticList", (), lang, start_row, end_row)
        return EcosPage[KeyStatistic].model_validate({"list_total_count": total, "row_count": row_count, "row": rows})
