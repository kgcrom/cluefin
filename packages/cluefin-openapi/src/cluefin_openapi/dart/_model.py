"""DART OpenAPI response models."""

from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, Mapping, Optional, Type, TypeVar

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Self


class DartStatusCode(str, Enum):
    """DART API 응답 상태 코드.

    Reference: https://opendart.fss.or.kr/intro/main.do (OpenDART 개발가이드 > 에러 및 메시지 설명)
    """

    SUCCESS = "000"
    """정상"""

    UNREGISTERED_KEY = "010"
    """등록되지 않은 키입니다."""

    DISABLED_KEY = "011"
    """사용할 수 없는 키입니다. 오픈API에 등록되었으나, 일시적으로 사용 중지된 키를 통하여 검색하는 경우 발생합니다."""

    INACCESSIBLE_IP = "012"
    """접근할 수 없는 IP입니다."""

    NO_DATA = "013"
    """조회된 데이타가 없습니다."""

    FILE_NOT_FOUND = "014"
    """파일이 존재하지 않습니다."""

    REQUEST_LIMIT_EXCEEDED = "020"
    """요청 제한을 초과하였습니다. 일반적으로는 20,000건 이상의 요청에 대하여 이 에러 메시지가 발생되나, 요청 제한이 다르게 설정된 경우에는 이에 준하여 발생됩니다."""

    COMPANY_LIMIT_EXCEEDED = "021"
    """조회 가능한 회사 개수가 초과하였습니다.(최대 100건)"""

    INVALID_FIELD_VALUE = "100"
    """필드의 부적절한 값입니다. 필드 설명에 없는 값을 사용한 경우에 발생하는 메시지입니다."""

    INVALID_ACCESS = "101"
    """부적절한 접근입니다."""

    SERVICE_MAINTENANCE = "800"
    """시스템 점검으로 인한 서비스가 중지 중입니다."""

    UNDEFINED_ERROR = "900"
    """정의되지 않은 오류가 발생하였습니다."""

    EXPIRED_ACCOUNT = "901"
    """사용자 계정의 개인정보 보유기간이 만료되어 사용할 수 없는 키입니다. 관리자 이메일(opendart@fss.or.kr)로 문의하시기 바랍니다."""


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
