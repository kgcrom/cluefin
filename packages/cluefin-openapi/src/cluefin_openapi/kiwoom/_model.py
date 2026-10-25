from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

# Define a TypeVar for the body of the KiwoomHttpResponse
T_KiwoomHttpBody = TypeVar("T_KiwoomHttpBody", bound="KiwoomHttpBody")


class KiwoomHttpHeader(BaseModel):
    # 연속조회여부 (Kiwoom occasionally returns continuation keys here)
    cont_yn: str = Field(alias="cont-yn")
    # 연속조회키
    next_key: str = Field(alias="next-key")
    # TR명
    api_id: str = Field(alias="api-id")


# frozen·slots 없음: pydantic 응답 모델이 BaseModel 과 함께 상속하는 기반이라 둘 다 붙일 수 없다.
@dataclass
class KiwoomHttpBody:  # This can remain a base class or be used directly if no further specialization is needed often
    return_code: int
    return_msg: str | None = None


@dataclass(frozen=True, slots=True)
class KiwoomHttpResponse(Generic[T_KiwoomHttpBody]):
    headers: KiwoomHttpHeader
    body: T_KiwoomHttpBody
