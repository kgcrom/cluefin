"""DART OpenAPI response models."""

from dataclasses import dataclass
from typing import Generic, List, Literal, Mapping, Optional, Type, TypeVar

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Self

DartStatusCode = Literal[
    "000",
    "010",
    "011",
    "012",
    "013",
    "014",
    "020",
    "021",
    "100",
    "101",
    "800",
    "900",
    "901",
]

T_DartListItem = TypeVar("T_DartListItem", bound=BaseModel)


class DartResult(BaseModel, Generic[T_DartListItem]):
    """Common envelope returned by DART APIs.

    The ``list`` field is optional because a handful of endpoints only return
    data about the request itself (for example, usage quotas).
    """

    status: DartStatusCode = Field(description="에러 및 정보 코드")
    message: str = Field(description="에러 및 정보 메시지")
    page_no: Optional[int] = Field(default=None, description="페이지 번호")
    page_count: Optional[int] = Field(default=None, description="페이지 별 건수")
    total_count: Optional[int] = Field(default=None, description="총 건수")
    total_page: Optional[int] = Field(default=None, description="총 페이지 수")
    list: Optional[List[T_DartListItem]] = Field(
        default=None,
        description="요청 결과 목록 (엔드포인트에 따라 미제공)",
    )

    @field_validator("page_no", "page_count", "total_count", "total_page", mode="before")
    @classmethod
    def _coerce_numeric(cls, value):
        """DART sometimes serialises pagination numbers as strings."""
        if value is None or value == "":
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None
            try:
                return int(stripped, 10)
            except ValueError as exc:  # pragma: no cover - defensive guard
                raise ValueError(f"Cannot convert '{value}' to int") from exc
        return int(value)


@dataclass
class DartHttpBody(Generic[T_DartListItem]):
    """Typed representation of a DART response payload."""

    result: DartResult[T_DartListItem]

    @classmethod
    def parse(
        cls,
        payload: Mapping[str, object],
        *,
        list_model: Type[T_DartListItem],
        result_key: str = "result",
    ) -> Self:
        """Parse raw payload into a structured response.

        Parameters
        ----------
        payload:
            Raw JSON dictionary returned by :meth:`Client._get`.
        list_model:
            Pydantic model describing each entry in ``result.list``.
        result_key:
            Some endpoints already return the result object at the top level.
            For most endpoints the useful content is under ``result``. This
            parameter lets callers handle both shapes without additional glue.
        """

        if result_key in payload:
            raw_result = payload[result_key]
        else:
            raw_result = payload

        if not isinstance(raw_result, Mapping):
            raise TypeError(
                "DART response does not contain a mapping under the expected result key. "
                f"Got type: {type(raw_result)!r}"
            )

        result_type = DartResult[list_model]
        return cls(result=result_type.model_validate(raw_result))
