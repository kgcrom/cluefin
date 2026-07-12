"""국내주식 조건검색 (웹소켓) 요청/응답 모델.

웹소켓 프레임은 HTTP 응답이 아니므로 ``KiwoomHttpBody``를 상속하지 않고 순수
``BaseModel``로 정의한다. 응답 ``data`` List<Map> 요소 중 숫자 FID 키를 사용하는
필드는 의미 있는 영어 필드명 + ``alias``로 매핑하고 ``populate_by_name=True``를
설정한다. (미국주식 ``_overseas_condition_search_types.py`` 와 대칭.)

- 운영: wss://api.kiwoom.com:10000/api/dostk/websocket
- 모의투자: wss://mockapi.kiwoom.com:10000/api/dostk/websocket (KRX만 지원)

TR/trnm: 목록조회 CNSRLST(ka10171), 요청 일반/실시간은 CNSRREQ(ka10172/ka10173)를
공유하며 ``search_type`` 0/1 로 구분, 실시간 해제 CNSRCLR(ka10174). 요청에는
``stex_tp``(거래소구분, 국내는 K:KRX)를 포함한다.

ka10173(실시간)은 응답이 두 종류다: 최초 조회 응답(trnm CNSRREQ, data=[{jmcode}])과
이후 실시간 편입/이탈 푸시(trnm REAL, data=[{type, name, values{...}}]). 각각
``DomesticConditionSearchRealtimeResponse`` / ``DomesticConditionSearchRealtimePush``.
"""

from typing import Literal

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

# ---------------------------------------------------------------------------
# ka10171 조건검색 목록조회
# ---------------------------------------------------------------------------


class DomesticConditionSearchListRequest(BaseModel):
    """ka10171 조건검색 목록조회 요청."""

    model_config = ConfigDict(title="국내주식 조건검색 목록조회 요청")

    trnm: Literal["CNSRLST"] = Field(description="TR명. CNSRLST 고정값")


class DomesticConditionSearchListItem(BaseModel):
    """조건검색식 목록 항목."""

    model_config = ConfigDict(title="조건검색식 목록 항목")

    seq: str = Field(default="", description="조건검색식 일련번호")
    name: str = Field(default="", description="조건검색식 명")


class DomesticConditionSearchListResponse(BaseModel):
    """ka10171 조건검색 목록조회 응답."""

    model_config = ConfigDict(title="국내주식 조건검색 목록조회 응답")

    return_code: int | None = Field(default=None, description="결과코드. 정상:0")
    return_msg: str = Field(default="", description="결과메시지. 정상인 경우는 메시지 없음")
    trnm: str = Field(default="", description="서비스명. CNSRLST 고정값")
    data: list[DomesticConditionSearchListItem] = Field(default_factory=list, description="조건검색식 목록")


# ---------------------------------------------------------------------------
# ka10172 조건검색 요청 일반
# ---------------------------------------------------------------------------


class DomesticConditionSearchRequest(BaseModel):
    """ka10172 조건검색 요청 일반."""

    model_config = ConfigDict(title="국내주식 조건검색 요청 일반")

    trnm: Literal["CNSRREQ"] = Field(description="서비스명. CNSRREQ 고정값")
    seq: str = Field(description="조건검색식 일련번호")
    search_type: Literal["0"] = Field(description="조회타입. 0:조건검색")
    stex_tp: Literal["K"] = Field(default="K", description="거래소구분. K:KRX")
    cont_yn: Literal["Y", "N"] = Field(default="N", description="연속조회여부. Y:연속조회요청, N:연속조회미요청")
    next_key: str = Field(default="", description="연속조회키")


class DomesticConditionSearchResultItem(BaseModel):
    """조건검색 결과 데이터 항목 (일반 조회).

    값은 좌측 0-padding + 부호 포함 문자열로 내려온다 (예: 등락율 '00001500'=+1.50%,
    '-0001500'=-1.50%). 파싱/부호 해석은 소비 측 책임.
    """

    model_config = ConfigDict(populate_by_name=True, title="조건검색 결과 데이터 항목")

    stock_code: str = Field(
        default="", alias="9001", description="종목코드. 접두어 1자리+종목코드 6자리 (A:주식/J:ELW/Q:ETN)"
    )
    stock_name: str = Field(default="", alias="302", description="종목명")
    current_price: str = Field(default="", alias="10", description="현재가. 단위:원, 0-padding 부호포함 9자리")
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1:상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )
    prev_day_diff: str = Field(default="", alias="11", description="전일대비. 단위:원, 0-padding 부호포함 9자리")
    fluctuation_rate: str = Field(
        default="", alias="12", description="등락율. 0-padding 부호포함 8자리 (예: 00001500=+1.50%)"
    )
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량. 단위:1주, 0-padding 부호포함 10자리")
    open_price: str = Field(default="", alias="16", description="시가. 단위:원, 0-padding 부호포함 9자리")
    high_price: str = Field(default="", alias="17", description="고가. 단위:원, 0-padding 부호포함 9자리")
    low_price: str = Field(default="", alias="18", description="저가. 단위:원, 0-padding 부호포함 9자리")


class DomesticConditionSearchResponse(BaseModel):
    """ka10172 조건검색 요청 일반 응답."""

    model_config = ConfigDict(title="국내주식 조건검색 요청 일반 응답")

    return_code: int | None = Field(default=None, description="결과코드. 정상:0 나머지:에러")
    return_msg: str = Field(default="", description="결과메시지. 정상인 경우는 메시지 없음")
    trnm: str = Field(default="", description="서비스명. CNSRREQ")
    seq: str = Field(default="", description="조건검색식 일련번호")
    cont_yn: str = Field(default="", description="연속조회여부. 연속 데이터가 존재하는경우 Y, 없으면 N")
    next_key: str = Field(default="", description="연속조회키. 연속조회여부가 Y일경우 다음 조회시 필요한 조회값")
    data: list[DomesticConditionSearchResultItem] = Field(default_factory=list, description="검색결과데이터")


# ---------------------------------------------------------------------------
# ka10173 조건검색 요청 실시간
# ---------------------------------------------------------------------------


class DomesticConditionSearchRealtimeRequest(BaseModel):
    """ka10173 조건검색 요청 실시간."""

    model_config = ConfigDict(title="국내주식 조건검색 요청 실시간")

    trnm: Literal["CNSRREQ"] = Field(description="서비스명. CNSRREQ 고정값")
    seq: str = Field(description="조건검색식 일련번호")
    search_type: Literal["1"] = Field(description="조회타입. 1:조건검색+실시간조건검색")
    stex_tp: Literal["K"] = Field(default="K", description="거래소구분. K:KRX")


class DomesticConditionSearchRealtimeResultItem(BaseModel):
    """ka10173 최초 조회 응답 데이터 항목 (편입 종목 목록)."""

    model_config = ConfigDict(title="조건검색 실시간 조회 데이터 항목")

    jmcode: str = Field(default="", description="종목코드. 접두어 1자리+종목코드 6자리 (A:주식/J:ELW/Q:ETN)")


class DomesticConditionSearchRealtimeResponse(BaseModel):
    """ka10173 조건검색 요청 실시간 - 최초 조회 응답 (trnm=CNSRREQ)."""

    model_config = ConfigDict(title="국내주식 조건검색 요청 실시간 응답")

    return_code: int | None = Field(default=None, description="결과코드. 정상:0 나머지:에러")
    return_msg: str = Field(default="", description="결과메시지. 정상인 경우는 메시지 없음")
    trnm: str = Field(default="", description="서비스명. CNSRREQ")
    seq: str = Field(default="", description="조건검색식 일련번호")
    data: list[DomesticConditionSearchRealtimeResultItem] = Field(default_factory=list, description="검색결과데이터")


class DomesticConditionSearchRealtimeValues(BaseModel):
    """ka10173 실시간 푸시 프레임의 values 오브젝트 (FID 매핑)."""

    model_config = ConfigDict(populate_by_name=True, title="조건검색 실시간 수신 값")

    seq_no: str = Field(default="", alias="841", description="일련번호")
    stock_code: str = Field(default="", alias="9001", description="종목코드")
    insert_delete: str = Field(default="", alias="843", description="삽입삭제 구분. I:삽입, D:삭제")
    exec_time: str = Field(default="", alias="20", description="체결시간")
    buy_sell: str = Field(default="", alias="907", description="매도/수 구분")
    exchange: str = Field(default="", alias="9081", description="거래소 구분")


class DomesticConditionSearchRealtimeDataItem(BaseModel):
    """ka10173 실시간 푸시 프레임의 data 항목."""

    model_config = ConfigDict(title="조건검색 실시간 데이터 항목")

    type: str = Field(description="실시간 항목. TR명(0A,0B...)")
    name: str = Field(description="실시간 항목명")
    values: DomesticConditionSearchRealtimeValues = Field(description="실시간 수신 값")


class DomesticConditionSearchRealtimePush(BaseModel):
    """ka10173 조건검색 실시간 편입/이탈 푸시 프레임 (trnm=REAL).

    스펙상 data/trnm 모두 Required=Y 인 실시간 이벤트 프레임.
    """

    model_config = ConfigDict(title="국내주식 조건검색 실시간 푸시")

    trnm: Literal["REAL"] = Field(description="서비스명. REAL 고정값")
    data: list[DomesticConditionSearchRealtimeDataItem] = Field(description="검색결과데이터")


# ---------------------------------------------------------------------------
# ka10174 조건검색 실시간 해제
# ---------------------------------------------------------------------------


class DomesticConditionSearchRealtimeCancelRequest(BaseModel):
    """ka10174 조건검색 실시간 해제 요청."""

    model_config = ConfigDict(title="국내주식 조건검색 실시간 해제 요청")

    trnm: Literal["CNSRCLR"] = Field(description="서비스명. CNSRCLR 고정값")
    seq: str = Field(description="조건검색식 일련번호")


class DomesticConditionSearchRealtimeCancelResponse(BaseModel):
    """ka10174 조건검색 실시간 해제 응답.

    스펙상 네 필드 모두 Required=Y(단순 ACK 프레임)이므로 다른 TR과 달리 기본값을
    부여하지 않는다.
    """

    model_config = ConfigDict(title="국내주식 조건검색 실시간 해제 응답")

    return_code: int = Field(description="결과코드. 정상:0 나머지:에러")
    return_msg: str = Field(description="결과메시지. 정상인 경우는 메시지 없음")
    trnm: Literal["CNSRCLR"] = Field(description="서비스명. CNSRCLR 고정값")
    seq: str = Field(description="조건검색식 일련번호")
