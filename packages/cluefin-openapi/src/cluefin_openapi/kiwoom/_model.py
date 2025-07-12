from dataclasses import dataclass
from typing import Generic, Literal, Optional, TypeVar

from pydantic import BaseModel, Field

# Define a TypeVar for the body of the KiwoomHttpResponse
T_KiwoomHttpBody = TypeVar("T_KiwoomHttpBody", bound="KiwoomHttpBody")


class KiwoomHttpHeader(BaseModel):
    # 연속조회여부
    cont_yn: Literal["Y", "N"] = Field(..., alias="cont-yn")
    # 연속조회키
    next_key: str = Field(..., alias="next-key")
    # TR명
    api_id: str = Field(..., alias="api-id")


@dataclass
class KiwoomHttpBody:  # This can remain a base class or be used directly if no further specialization is needed often
    return_code: int
    return_msg: Optional[str] = None


@dataclass
class KiwoomHttpResponse(Generic[T_KiwoomHttpBody]):
    headers: KiwoomHttpHeader
    body: T_KiwoomHttpBody
