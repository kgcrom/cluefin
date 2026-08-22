from dataclasses import dataclass
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T_NHPlugHttpBody = TypeVar("T_NHPlugHttpBody", bound="NHPlugHttpBody")


class NHPlugHttpBody(BaseModel):
    """공통 응답 봉투.

    모든 REST 응답은 `rsp_cd`/`rsp_msg` + `Output_0`(+`Output_1`…) 블록으로 구성된다.
    `Output_N` 블록은 API 마다 객체(집계값) 또는 배열(목록)로 타입이 다르므로
    각 API 응답 타입에서 하위 클래스로 정의한다. 블록은 데이터가 있을 때만
    내려오므로 하위 타입에서 Optional 로 선언할 것.
    """

    model_config = ConfigDict(extra="allow")

    rsp_cd: str = Field(description="응답코드 (00000: 성공)")
    rsp_msg: str = Field(description="응답메시지")


class NHPlugHttpHeader(BaseModel):
    """응답 헤더 중 클라이언트가 사용하는 값."""

    model_config = ConfigDict(extra="allow")

    cts: str | None = Field(default=None, description="연속거래키 (다음 페이지 요청 헤더에 그대로 전달)")
    cts_flag: Literal["Y", "N"] | None = Field(default=None, description="연속거래 여부 (Y: 연속거래 있음)")


@dataclass
class NHPlugHttpResponse(Generic[T_NHPlugHttpBody]):
    header: NHPlugHttpHeader
    body: T_NHPlugHttpBody
