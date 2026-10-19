from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

RowT = TypeVar("RowT")

# ECOS 는 같은 필드를 문자열("1000")로도 숫자(1000)로도 준다(WGT 실측). 문자열 필드는 숫자도 받아 문자열로 둔다.
ECOS_ROW_CONFIG = ConfigDict(populate_by_name=True, extra="allow", coerce_numbers_to_str=True)


class EcosPage(BaseModel, Generic[RowT]):
    """ECOS 서비스 공통 응답 `{"<서비스명>": {"list_total_count": N, "row": [...]}}` 의 안쪽."""

    model_config = ConfigDict(title="ECOS 응답", populate_by_name=True, extra="allow")

    list_total_count: int = Field(default=0, description="조건에 맞는 전체 행 수 (받은 행 수가 아님)")
    row_count: Optional[int] = Field(default=None, description="이번 쪽 행 수. KeyStatisticList 만 준다(명세에 없음)")
    rows: List[RowT] = Field(
        default_factory=list, alias="row", description="행 목록. 데이터 없음(INFO-200)이면 빈 목록"
    )
