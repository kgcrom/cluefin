from dataclasses import dataclass
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

# 응답 body 는 NHPlugHttpBody(공통)·NHPlugAssetHttpBody(자산군)·AccountList 처럼
# 봉투 형태가 갈리므로 BaseModel 로 바운드한다.
T_NHPlugHttpBody = TypeVar("T_NHPlugHttpBody", bound=BaseModel)

# body rsp_cd 중 성공을 뜻하는 코드. 문서상 성공은 00000 뿐이지만, 모의투자 서버는
# 일부 조회 API 성공에 XA102("모의투자 조회가 완료되었습니다")를 반환한다
# (2026-08-22 dailyOrderExecution 실측). 새 성공 코드가 실측되면 여기에 추가한다.
SUCCESS_RSP_CODES: tuple[str, ...] = ("00000", "XA102")


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


class NHPlugMessage(BaseModel):
    """자산군 스펙(openapi.json)이 명세하는 `message` 봉투.

    실서버(모의, 2026-08-22 실측)는 이 블록을 null 로 내려주고 대신
    `rsp_cd`/`rsp_msg` 를 반환하지만, 스펙 정본이 명세하므로 함께 정의한다.
    """

    model_config = ConfigDict(extra="allow")

    msg_code: str | None = Field(default=None, description="메시지코드")
    usr_msg: str | None = Field(default=None, description="사용자메시지")
    msg_lv_code: str | None = Field(default=None, description="메시지레벨코드")
    dvlp_msg_yn: str | None = Field(default=None, description="개발메시지여부")
    svc_nm: str | None = Field(default=None, description="서비스명")
    func_nm: str | None = Field(default=None, description="함수명")
    line_no: str | None = Field(default=None, description="라인번호")
    dvlp_msg: str | None = Field(default=None, description="개발메시지")


class NHPlugAssetHttpBody(BaseModel):
    """자산군(krstock 등) API 공통 응답 봉투.

    스펙은 `Output_N` + `message` 구조로 명세하지만 실서버는 common 과 동일하게
    `rsp_cd`/`rsp_msg` 를 반환하고 `message` 는 null 이다(모의 실측 2026-08-22).
    둘 다 Optional 로 두고, `Output_N` 블록은 데이터가 있을 때만 내려오므로
    하위 타입에서 Optional 로 선언할 것 (객체/배열 여부는 API 마다 다름).
    """

    model_config = ConfigDict(extra="allow")

    rsp_cd: str | None = Field(default=None, description="응답코드 (00000: 성공)")
    rsp_msg: str | None = Field(default=None, description="응답메시지")
    message: NHPlugMessage | None = Field(default=None, description="스펙상 메시지 봉투 (실서버는 null)")


class NHPlugHttpHeader(BaseModel):
    """응답 헤더 중 클라이언트가 사용하는 값."""

    model_config = ConfigDict(extra="allow")

    cts: str | None = Field(default=None, description="연속거래키 (다음 페이지 요청 헤더에 그대로 전달)")
    cts_flag: Literal["Y", "N"] | None = Field(default=None, description="연속거래 여부 (Y: 연속거래 있음)")


@dataclass
class NHPlugHttpResponse(Generic[T_NHPlugHttpBody]):
    header: NHPlugHttpHeader
    body: T_NHPlugHttpBody
