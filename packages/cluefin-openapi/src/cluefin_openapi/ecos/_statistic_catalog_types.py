from pydantic import BaseModel, Field

from ._model import ECOS_ROW_CONFIG


class StatisticTable(BaseModel):
    """StatisticTableList 한 행 — 통계표 또는 그 상위 분류."""

    model_config = ECOS_ROW_CONFIG | {"title": "ECOS 서비스 통계 목록 행"}

    parent_stat_code: str | None = Field(default=None, alias="P_STAT_CODE", description="상위통계표코드. 최상위는 '*'")
    stat_code: str = Field(alias="STAT_CODE", description="통계표코드 (분류 행은 10자리 숫자)")
    stat_name: str = Field(alias="STAT_NAME", description="통계명")
    cycle: str | None = Field(default=None, alias="CYCLE", description="주기 (A·S·Q·M·SM·D). 분류 행은 None")
    searchable: str | None = Field(default=None, alias="SRCH_YN", description="StatisticSearch 로 조회 가능 여부 Y/N")
    org_name: str | None = Field(default=None, alias="ORG_NAME", description="출처")


class StatisticItem(BaseModel):
    """StatisticItemList 한 행 — 통계표의 세부 항목."""

    model_config = ECOS_ROW_CONFIG | {"title": "ECOS 통계 세부항목 목록 행"}

    stat_code: str = Field(alias="STAT_CODE", description="통계표코드")
    stat_name: str = Field(alias="STAT_NAME", description="통계명")
    group_code: str | None = Field(
        default=None, alias="GRP_CODE", description="항목그룹코드 (Group1 → ITEM_CODE1 자리)"
    )
    group_name: str | None = Field(default=None, alias="GRP_NAME", description="항목그룹명")
    item_code: str = Field(alias="ITEM_CODE", description="통계항목코드")
    item_name: str = Field(alias="ITEM_NAME", description="통계항목명")
    parent_item_code: str | None = Field(default=None, alias="P_ITEM_CODE", description="상위통계항목코드")
    parent_item_name: str | None = Field(default=None, alias="P_ITEM_NAME", description="상위통계항목명")
    cycle: str | None = Field(default=None, alias="CYCLE", description="주기")
    start_time: str | None = Field(default=None, alias="START_TIME", description="수록시작일자")
    end_time: str | None = Field(default=None, alias="END_TIME", description="수록종료일자")
    data_count: int | None = Field(default=None, alias="DATA_CNT", description="자료수")
    unit_name: str | None = Field(default=None, alias="UNIT_NAME", description="단위")
    weight: str | None = Field(default=None, alias="WEIGHT", description="가중치")


class KeyStatistic(BaseModel):
    """KeyStatisticList 한 행 — 100대 통계지표의 최근 값."""

    model_config = ECOS_ROW_CONFIG | {"title": "ECOS 100대 통계지표 행"}

    class_name: str = Field(alias="CLASS_NAME", description="통계그룹명")
    keystat_name: str = Field(alias="KEYSTAT_NAME", description="통계명")
    data_value: str | None = Field(default=None, alias="DATA_VALUE", description="값 원문")
    cycle: str | None = Field(default=None, alias="CYCLE", description="최근 수록 시점 (202608, 20261019 …)")
    unit_name: str | None = Field(default=None, alias="UNIT_NAME", description="단위")
