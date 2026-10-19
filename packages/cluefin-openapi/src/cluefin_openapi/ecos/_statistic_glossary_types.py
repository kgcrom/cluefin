from typing import Optional

from pydantic import BaseModel, Field

from ._model import ECOS_ROW_CONFIG


class StatisticWord(BaseModel):
    """StatisticWord 한 행 — 통계용어사전 항목."""

    model_config = ECOS_ROW_CONFIG | {"title": "ECOS 통계용어사전 행"}

    word: str = Field(alias="WORD", description="용어")
    content: Optional[str] = Field(default=None, alias="CONTENT", description="용어설명")


class StatisticMetaItem(BaseModel):
    """StatisticMeta 한 행 — 통계메타DB 의 트리 노드 하나."""

    model_config = ECOS_ROW_CONFIG | {"title": "ECOS 통계메타DB 행"}

    level: Optional[str] = Field(default=None, alias="LVL", description="트리 깊이 (1부터)")
    parent_code: Optional[str] = Field(default=None, alias="P_CONT_CODE", description="상위통계항목코드")
    code: str = Field(alias="CONT_CODE", description="통계항목코드")
    name: str = Field(alias="CONT_NAME", description="통계항목명")
    meta_data: Optional[str] = Field(default=None, alias="META_DATA", description="메타데이터")
