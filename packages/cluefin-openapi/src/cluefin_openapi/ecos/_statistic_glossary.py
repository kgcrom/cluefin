"""통계 용어·메타 (StatisticWord · StatisticMeta)."""

from __future__ import annotations

from typing import Optional

from ._client import Client, Lang
from ._model import EcosPage
from ._statistic_glossary_types import StatisticMetaItem, StatisticWord


class StatisticGlossary:
    """통계용어사전과 통계메타DB"""

    def __init__(self, client: Client):
        self.client = client

    def word(
        self,
        term: str,
        *,
        lang: Lang = "kr",
        start_row: Optional[int] = None,
        end_row: Optional[int] = None,
    ) -> EcosPage[StatisticWord]:
        """통계용어사전 (OA-1060). 예: `소비자동향지수`"""
        total, rows, row_count = self.client._get_rows("StatisticWord", (term,), lang, start_row, end_row)
        return EcosPage[StatisticWord].model_validate({"list_total_count": total, "row_count": row_count, "row": rows})

    def meta(
        self,
        data_name: str,
        *,
        lang: Lang = "kr",
        start_row: Optional[int] = None,
        end_row: Optional[int] = None,
    ) -> EcosPage[StatisticMetaItem]:
        """통계메타DB (OA-1050). 데이터명은 부분 일치한다(`경제심리` = `경제심리지수`, 2026-10-19 실측)."""
        total, rows, row_count = self.client._get_rows("StatisticMeta", (data_name,), lang, start_row, end_row)
        return EcosPage[StatisticMetaItem].model_validate(
            {"list_total_count": total, "row_count": row_count, "row": rows}
        )
