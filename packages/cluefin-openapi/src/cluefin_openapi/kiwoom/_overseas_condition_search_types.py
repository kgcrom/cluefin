"""미국주식 조건검색 (웹소켓) 요청/응답 모델.

웹소켓 프레임은 HTTP 응답이 아니므로 ``KiwoomHttpBody``를 상속하지 않고 순수
``BaseModel``로 정의한다. 응답 ``data`` List<Map> 요소 중 숫자 FID/camelCase 키를
사용하는 필드는 의미 있는 영어 필드명 + ``alias``로 매핑하고 ``populate_by_name=True``를
설정한다.

usa20281(요청 일반)과 usa20290(요청 실시간)은 동일한 ``trnm``(GCNSRREQ) 값을 공유하며
``search_type`` 값(0 vs 1)으로 구분된다.
"""

from typing import Literal

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

# ---------------------------------------------------------------------------
# usa20280 미국주식 조건검색 목록조회
# ---------------------------------------------------------------------------


class OverseasConditionSearchListRequest(BaseModel):
    """usa20280 미국주식 조건검색 목록조회 요청."""

    model_config = ConfigDict(title="미국주식 조건검색 목록조회 요청")

    trnm: Literal["GCNSRLST"] = Field(description="TR명. GCNSRLST 고정값")


class OverseasConditionSearchListItem(BaseModel):
    """조건검색식 목록 항목."""

    model_config = ConfigDict(title="조건검색식 목록 항목")

    seq: str = Field(default="", description="조건검색식 일련번호")
    name: str = Field(default="", description="조건검색식 명")


class OverseasConditionSearchListResponse(BaseModel):
    """usa20280 미국주식 조건검색 목록조회 응답."""

    model_config = ConfigDict(title="미국주식 조건검색 목록조회 응답")

    return_code: int | None = Field(default=None, description="결과코드. 정상:0")
    return_msg: str = Field(default="", description="결과메시지. 정상인 경우는 메시지 없음")
    trnm: str = Field(default="", description="서비스명. GCNSRLT고정값")
    data: list[OverseasConditionSearchListItem] = Field(default_factory=list, description="조건검색식 목록")


# ---------------------------------------------------------------------------
# usa20281 미국주식 조건검색 요청 일반
# ---------------------------------------------------------------------------


class OverseasConditionSearchRequest(BaseModel):
    """usa20281 미국주식 조건검색 요청 일반."""

    model_config = ConfigDict(title="미국주식 조건검색 요청 일반")

    trnm: Literal["GCNSRREQ"] = Field(description="서비스명. GCNSRREQ 고정값")
    seq: str = Field(description="조건검색식 일련번호")
    search_type: Literal["0"] = Field(description="조회타입. 0:조건검색")
    cont_yn: Literal["Y", "N"] = Field(default="N", description="연속조회여부. Y:연속조회요청, N:연속조회미요청")
    next_key: str = Field(default="", description="연속조회키")


class OverseasConditionSearchResultItem(BaseModel):
    """조건검색 결과 데이터 항목 (일반 조회)."""

    model_config = ConfigDict(populate_by_name=True, title="조건검색 결과 데이터 항목")

    stock_code: str = Field(default="", alias="9001", description="종목코드")
    stock_name: str = Field(default="", alias="302", description="종목명")
    current_price: str = Field(default="", alias="10", description="현재가")
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1:상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )
    prev_day_diff: str = Field(default="", alias="11", description="전일대비")
    fluctuation_rate: str = Field(default="", alias="12", description="등락률")
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량")
    open_price: str = Field(default="", alias="16", description="시가")
    high_price: str = Field(default="", alias="17", description="고가")
    low_price: str = Field(default="", alias="18", description="저가")
    sub_industry: str = Field(default="", alias="318", description="소업종")
    stex_tp: str = Field(default="", description="거래소구분. NA:AMEX, ND:NASDAQ, NY:NYSE")


class OverseasConditionSearchResponse(BaseModel):
    """usa20281 미국주식 조건검색 요청 일반 응답."""

    model_config = ConfigDict(title="미국주식 조건검색 요청 일반 응답")

    return_code: int | None = Field(default=None, description="결과코드. 정상:0 나머지:에러")
    return_msg: str = Field(default="", description="결과메시지. 정상인 경우는 메시지 없음")
    trnm: str = Field(default="", description="서비스명. CNSRREQ")
    seq: str = Field(default="", description="조건검색식 일련번호")
    cont_yn: str = Field(default="", description="연속조회여부. 연속 데이터가 존재하는경우 Y, 없으면 N")
    next_key: str = Field(default="", description="연속조회키. 연속조회여부가 Y일경우 다음 조회시 필요한 조회값")
    data: list[OverseasConditionSearchResultItem] = Field(default_factory=list, description="검색결과데이터")


# ---------------------------------------------------------------------------
# usa20290 미국주식 조건검색 요청 실시간
# ---------------------------------------------------------------------------


class OverseasConditionSearchRealtimeRequest(BaseModel):
    """usa20290 미국주식 조건검색 요청 실시간."""

    model_config = ConfigDict(title="미국주식 조건검색 요청 실시간")

    trnm: Literal["GCNSRREQ"] = Field(description="서비스명. GCNSRREQ 고정값")
    seq: str = Field(description="조건검색식 일련번호")
    search_type: Literal["1"] = Field(description="조회타입. 1:조건검색+실시간조건검색")


class OverseasConditionSearchRealtimeResultItem(BaseModel):
    """조건검색 결과 데이터 항목 (실시간 조회)."""

    model_config = ConfigDict(populate_by_name=True, title="조건검색 결과 데이터 항목 (실시간)")

    jmcode: str = Field(default="", description="종목코드")
    stex_tp: str = Field(default="", alias="stexTp", description="거래소구분")


class OverseasConditionSearchRealtimeResponse(BaseModel):
    """usa20290 미국주식 조건검색 요청 실시간 응답."""

    model_config = ConfigDict(title="미국주식 조건검색 요청 실시간 응답")

    return_code: int | None = Field(default=None, description="결과코드. 정상:0 나머지:에러")
    return_msg: str = Field(default="", description="결과메시지. 정상인 경우는 메시지 없음")
    trnm: str = Field(default="", description="서비스명. GCNSRREQ")
    seq: str = Field(default="", description="조건검색식 일련번호")
    data: list[OverseasConditionSearchRealtimeResultItem] = Field(default_factory=list, description="검색결과데이터")


# ---------------------------------------------------------------------------
# usa20291 미국주식 조건검색 실시간 해제
# ---------------------------------------------------------------------------


class OverseasConditionSearchRealtimeCancelRequest(BaseModel):
    """usa20291 미국주식 조건검색 실시간 해제 요청."""

    model_config = ConfigDict(title="미국주식 조건검색 실시간 해제 요청")

    trnm: Literal["GCNSRCLR"] = Field(description="서비스명. GCNSRCLR 고정값")
    seq: str = Field(description="조건검색식 일련번호")


class OverseasConditionSearchRealtimeCancelResponse(BaseModel):
    """usa20291 미국주식 조건검색 실시간 해제 응답.

    스펙상 네 필드 모두 Required=Y(단순 ACK 프레임)이므로 다른 TR과 달리 기본값을
    부여하지 않는다.
    """

    model_config = ConfigDict(title="미국주식 조건검색 실시간 해제 응답")

    return_code: int = Field(description="결과코드. 정상:0 나머지:에러")
    return_msg: str = Field(description="결과메시지. 정상인 경우는 메시지 없음")
    trnm: Literal["GCNSRCLR"] = Field(description="서비스명. GCNSRCLR 고정값")
    seq: str = Field(description="조건검색식 일련번호")
