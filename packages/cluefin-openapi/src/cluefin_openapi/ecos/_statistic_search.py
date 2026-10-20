"""통계 조회 (StatisticSearch)."""

from __future__ import annotations

from typing import Literal, Optional, Sequence, cast

from ._client import Client, Lang
from ._constants import EcosSeries
from ._model import EcosPage
from ._statistic_search_types import StatisticObservation

Cycle = Literal["A", "S", "Q", "M", "SM", "D"]

MAX_ITEM_CODES = 4


class StatisticSearch:
    """통계 조회 조건 설정 (OA-1040)"""

    def __init__(self, client: Client):
        self.client = client

    def search(
        self,
        stat_code: str,
        cycle: Cycle,
        start: str,
        end: str,
        item_codes: Sequence[str] = (),
        *,
        lang: Lang = "kr",
        start_row: Optional[int] = None,
        end_row: Optional[int] = None,
    ) -> EcosPage[StatisticObservation]:
        """통계표의 시계열 값을 받는다.

        Args:
            stat_code: 통계표코드 (예: `817Y002` 시장금리(일별))
            cycle: 주기 — A(년) S(반년) Q(분기) M(월) SM(반월) D(일)
            start: 검색시작일자. 주기 형식을 따른다 — 2015, 2015S1, 2015Q1, 201501, 201501S1, 20150101
            end: 검색종료일자 (형식은 start 와 같다)
            item_codes: 통계항목코드1~4. 생략하면 통계표의 모든 항목이 온다
            lang: kr(국문) / en(영문) 이름
            start_row, end_row: 한 쪽만 받을 때의 행 범위. 생략하면 전체를 쪽 넘김으로 받는다

        Returns:
            EcosPage[StatisticObservation]: 휴일에는 행이 없고, 데이터가 없으면 빈 rows
        """
        if len(item_codes) > MAX_ITEM_CODES:
            raise ValueError(f"항목코드는 {MAX_ITEM_CODES}개까지입니다. 받은 개수: {len(item_codes)}")
        segments = (stat_code, cycle, start, end, *item_codes)
        total, rows, row_count = self.client._get_rows("StatisticSearch", segments, lang, start_row, end_row)
        return EcosPage[StatisticObservation].model_validate(
            {"list_total_count": total, "row_count": row_count, "row": rows}
        )

    def search_series(
        self, series: EcosSeries, start: str, end: str, *, lang: Lang = "kr"
    ) -> EcosPage[StatisticObservation]:
        """`_constants` 의 계열 하나(예: `KTB_10Y`)를 기간으로 받는다."""
        return self.search(series.stat_code, cast(Cycle, series.cycle), start, end, (series.item_code,), lang=lang)
