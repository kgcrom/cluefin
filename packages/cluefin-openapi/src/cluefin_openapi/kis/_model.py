from dataclasses import dataclass
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field

T_KisHttpBody = TypeVar("T_KisHttpBody", bound="KisHttpBody")


class KisHttpHeader(BaseModel):
    content_type: str = Field(alias="content-type", description="컨텐츠타입")
    tr_id: str = Field(title="거래ID", description="요청한 tr_id")
    tr_cont: Literal["F", "M", "D", "E", "", "0"] | None = Field(
        default=None,
        title="연속 거래 여부",
        description="F or M : 다음 데이터 있음, D or E : 마지막 데이터",
    )
    gt_uid: str | None = Field(
        default=None,
        title="Global UID",
        description="[법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함",
    )


@dataclass
class KisHttpBody:
    rt_cd: Literal["2", "1", "0", ""] = Field(
        description="성공 실패 여부, (0: 성공, '': 데이터가 존재하지 않음,0이 아닌숫자: 실패)"
    )
    msg_cd: str = Field(description="응답코드")
    msg1: str = Field(description="응답메세지")


@dataclass
class KisHttpResponse(Generic[T_KisHttpBody]):
    header: KisHttpHeader
    body: T_KisHttpBody
