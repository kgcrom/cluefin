from dataclasses import dataclass
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, Field

T_KisHttpBody = TypeVar("T_KisHttpBody", bound="KisHttpBody")


class KisHttpHeader(BaseModel):
    tr_id: str = Field(title="거래ID", description="요청한 tr_id", max_length=13)
    tr_cont: str | None = Field(title="연속 거래 여부", description="tr_cont를 이용한 다음조회 불가 API", max_length=1)
    gt_uid: str | None = Field(
        title="Global UID", description="[법인 전용] 거래고유번호로 사용하므로 거래별로 UNIQUE해야 함", max_length=32
    )


@dataclass
class KisHttpBody:
    rt_cd: Literal["Y", "N"] = Field(description="성공 실패 여부")
    msg_cd: str = Field(description="응답코드", max_length=8)
    msg1: str = Field(description="응답메세지", max_length=80)


@dataclass
class KisHttpResponse(Generic[T_KisHttpBody]):
    header: KisHttpHeader
    body: T_KisHttpBody
