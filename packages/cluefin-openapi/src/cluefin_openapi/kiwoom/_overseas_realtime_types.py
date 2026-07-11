"""미국주식 실시간 시세 (웹소켓) 요청/응답 모델.

웹소켓 프레임은 HTTP 응답이 아니므로 ``KiwoomHttpBody``를 상속하지 않고 순수
``BaseModel``로 정의한다. 응답 ``values`` Map은 숫자 FID 키를 사용하므로 의미 있는
영어 필드명 + ``alias``(FID)로 매핑하고 ``populate_by_name=True``를 설정한다.
"""

from typing import Literal

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

# ---------------------------------------------------------------------------
# 공통 요청 모델 (F4/F5/FE/FT 4개 TR의 등록/해지 프레임이 동일)
# ---------------------------------------------------------------------------


class OverseasRealtimeRegisterItem(BaseModel):
    """실시간 등록 요소. Map 구조 {종목코드, 거래소코드}."""

    model_config = ConfigDict(title="실시간 등록 요소")

    jmcode: str = Field(default="", description="종목코드. ex) NVDA")
    stex_tp: str = Field(default="", description="거래소코드. ND:NASDAQ, NY:NYSE, NA:AMEX")


class OverseasRealtimeRegisterData(BaseModel):
    """실시간 등록 리스트 항목."""

    model_config = ConfigDict(title="실시간 등록 리스트 항목")

    item: list[OverseasRealtimeRegisterItem] = Field(default_factory=list, description="실시간 등록 요소 리스트")
    type: list[str] = Field(default_factory=list, description="실시간 항목. TR 명 리스트 (F4, F5, FE, FT 등)")


class OverseasRealtimeRequest(BaseModel):
    """실시간 등록/해지 요청."""

    model_config = ConfigDict(title="미국주식 실시간 시세 등록/해지 요청")

    trnm: Literal["REG", "REMOVE"] = Field(description="서비스명. REG:등록, REMOVE:해지")
    grp_no: str = Field(description="그룹번호")
    refresh: Literal["0", "1"] = Field(
        description="기존등록유지여부. 등록(REG)시 0:기존등록 item/type 해지, 1:기존등록 유지(Default). 해지(REMOVE)시 값 불필요"
    )
    data: list[OverseasRealtimeRegisterData] = Field(default_factory=list, description="실시간 등록 리스트")


# ---------------------------------------------------------------------------
# TR별 values 모델
# ---------------------------------------------------------------------------


class OverseasRealtimeOrderConfirmationValues(BaseModel):
    """F4 미국주식 실시간 주문 확인 values."""

    model_config = ConfigDict(populate_by_name=True, title="미국주식 실시간 주문 확인 values")

    account_no: str = Field(default="", alias="9201", description="계좌번호")
    order_no: str = Field(default="", alias="9203", description="주문번호")
    stock_code: str = Field(default="", alias="9001", description="종목,업종코드")
    order_type: str = Field(default="", alias="905", description="주문구분. 10:원주문, 11:정정주문, 12:취소주문")
    sell_buy_type: str = Field(default="", alias="907", description="매도수구분. 01:매도, 02:매수")
    original_order_no: str = Field(default="", alias="904", description="원주문번호")
    order_quantity: str = Field(default="", alias="900", description="주문수량")
    order_price: str = Field(default="", alias="901", description="주문가격")
    trade_type: str = Field(default="", alias="906", description="매매구분")
    order_status: str = Field(default="", alias="913", description="주문상태")
    order_execution_time: str = Field(default="", alias="908", description="주문/체결시간")
    order_stop_price: str = Field(default="", alias="50810", description="주문STOP가격")
    currency_code: str = Field(default="", alias="8043", description="통화코드")
    reservation_type: str = Field(default="", alias="50841", description="예약구분")
    country_code: str = Field(default="", alias="55190", description="(재무)국가코드 사용")
    country_name: str = Field(default="", alias="1091", description="국가명")
    sell_buy_type_name: str = Field(default="", alias="50072", description="매도수구분명")
    stock_name: str = Field(default="", alias="302", description="종목명")
    trade_type_name: str = Field(default="", alias="50073", description="매매구분명")


class OverseasRealtimeExecutionValues(BaseModel):
    """F5 미국주식 실시간 체결 values."""

    model_config = ConfigDict(populate_by_name=True, title="미국주식 실시간 체결 values")

    country_name: str = Field(default="", alias="1091", description="국가명")
    exchange_code: str = Field(default="", alias="8046", description="거래소코드")
    stock_code: str = Field(default="", alias="9001", description="종목코드")
    stock_name: str = Field(default="", alias="302", description="종목명")
    original_order_no: str = Field(default="", alias="904", description="원주문번호")
    order_no: str = Field(default="", alias="9203", description="주문번호")
    order_type: str = Field(default="", alias="905", description="주문구분. 10:원주문, 11:정정주문, 12:취소주문")
    sell_buy_type: str = Field(default="", alias="907", description="매도수구분. 01:매도, 02:매수")
    order_execution_time: str = Field(default="", alias="908", description="주문/체결시간")
    order_status: str = Field(
        default="", alias="913", description="주문상태. 텍스트값(주문전송, 무효주문, 부분체결, 체결완료 등)"
    )
    order_quantity: str = Field(default="", alias="900", description="주문수량")
    order_price: str = Field(default="", alias="901", description="주문가격")
    unexecuted_quantity: str = Field(default="", alias="902", description="미체결수량")
    execution_no: str = Field(default="", alias="909", description="체결번호")
    execution_price: str = Field(default="", alias="910", description="체결가")
    execution_quantity: str = Field(default="", alias="911", description="체결량")
    holding_quantity: str = Field(default="", alias="930", description="보유수량")
    purchase_unit_price: str = Field(default="", alias="931", description="매입단가")
    today_sell_quantity: str = Field(default="", alias="934", description="당일매도수량 사용")
    today_buy_quantity: str = Field(default="", alias="936", description="당일매수수량 사용")
    prev_sell_quantity: str = Field(default="", alias="8004", description="전일매도수량")
    prev_buy_quantity: str = Field(default="", alias="8005", description="전일매수수량")
    profit_loss_amount: str = Field(default="", alias="8018", description="손익금액")
    profit_loss_rate: str = Field(default="", alias="8019", description="손익율")
    currency_code: str = Field(default="", alias="8043", description="통화코드")
    tax: str = Field(default="", alias="8075", description="세금 사용")
    account_no: str = Field(default="", alias="9201", description="계좌번호")
    commission: str = Field(default="", alias="13006", description="수수료 사용")
    sell_buy_type_name: str = Field(default="", alias="50072", description="매도수구분명")
    trade_type_name: str = Field(default="", alias="50073", description="매매구분명. 텍스트값(지정가, 시장가 등)")
    realized_profit_loss_purchase_amount: str = Field(default="", alias="50724", description="실현손익매입금 사용")
    exchange_realized_profit_loss_purchase_amount: str = Field(
        default="", alias="50725", description="환전실현손익매입금액 사용"
    )
    order_stop_price: str = Field(default="", alias="50810", description="주문STOP가격")
    reservation_type: str = Field(default="", alias="50841", description="예약구분")
    exchange_realized_profit_loss_amount: str = Field(default="", alias="50844", description="환전실현손익금액 사용")
    country_code: str = Field(default="", alias="55190", description="(재무)국가코드 사용")


class OverseasRealtimeExecutionPriceValues(BaseModel):
    """FE 미국주식 실시간 체결가 values."""

    model_config = ConfigDict(populate_by_name=True, title="미국주식 실시간 체결가 values")

    current_price: str = Field(default="", alias="10", description="현재가")
    prev_day_diff: str = Field(default="", alias="11", description="전일대비")
    fluctuation_rate: str = Field(default="", alias="12", description="등락율")
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량")
    acc_trade_value: str = Field(default="", alias="14", description="누적거래대금")
    execution_volume: str = Field(default="", alias="15", description="체결량")
    open_price: str = Field(default="", alias="16", description="시가")
    high_price: str = Field(default="", alias="17", description="고가")
    low_price: str = Field(default="", alias="18", description="저가")
    time: str = Field(default="", alias="20", description="시간")
    execution_date: str = Field(default="", alias="22", description="체결일자")
    prev_day_diff_sign: str = Field(default="", alias="25", description="전일대비기호")
    best_ask_price: str = Field(default="", alias="27", description="(최우선)매도호가")
    best_bid_price: str = Field(default="", alias="28", description="(최우선)매수호가")
    prev_day_volume_ratio: str = Field(default="", alias="30", description="전일거래량대비(비율)")
    execution_strength: str = Field(default="", alias="228", description="체결강도")
    market_type: str = Field(default="", alias="290", description="장구분")
    local_execution_time: str = Field(default="", alias="51020", description="현지 체결시간")


class OverseasRealtimeTenQuotesValues(BaseModel):
    """FT 미국주식 10호가 values."""

    model_config = ConfigDict(populate_by_name=True, title="미국주식 10호가 values")

    time: str = Field(default="", alias="21", description="시간")
    ask_price_1: str = Field(default="", alias="41", description="매도1호가")
    ask_volume_1: str = Field(default="", alias="61", description="매도1호가잔량")
    ask_prev_diff_1: str = Field(default="", alias="81", description="매도1호가직전대비")
    bid_price_1: str = Field(default="", alias="51", description="매수1호가")
    bid_volume_1: str = Field(default="", alias="71", description="매수1호가잔량")
    bid_prev_diff_1: str = Field(default="", alias="91", description="매수1호가직전대비")
    ask_price_2: str = Field(default="", alias="42", description="매도2호가")
    ask_volume_2: str = Field(default="", alias="62", description="매도2호가잔량")
    ask_prev_diff_2: str = Field(default="", alias="82", description="매도2호가직전대비")
    bid_price_2: str = Field(default="", alias="52", description="매수2호가")
    bid_volume_2: str = Field(default="", alias="72", description="매수2호가잔량")
    bid_prev_diff_2: str = Field(default="", alias="92", description="매수2호가직전대비")
    ask_price_3: str = Field(default="", alias="43", description="매도3호가")
    ask_volume_3: str = Field(default="", alias="63", description="매도3호가잔량")
    ask_prev_diff_3: str = Field(default="", alias="83", description="매도3호가직전대비")
    bid_price_3: str = Field(default="", alias="53", description="매수3호가")
    bid_volume_3: str = Field(default="", alias="73", description="매수3호가잔량")
    bid_prev_diff_3: str = Field(default="", alias="93", description="매수3호가직전대비")
    ask_price_4: str = Field(default="", alias="44", description="매도4호가")
    ask_volume_4: str = Field(default="", alias="64", description="매도4호가잔량")
    ask_prev_diff_4: str = Field(default="", alias="84", description="매도4호가직전대비")
    bid_price_4: str = Field(default="", alias="54", description="매수4호가")
    bid_volume_4: str = Field(default="", alias="74", description="매수4호가잔량")
    bid_prev_diff_4: str = Field(default="", alias="94", description="매수4호가직전대비")
    ask_price_5: str = Field(default="", alias="45", description="매도5호가")
    ask_volume_5: str = Field(default="", alias="65", description="매도5호가잔량")
    ask_prev_diff_5: str = Field(default="", alias="85", description="매도5호가직전대비")
    bid_price_5: str = Field(default="", alias="55", description="매수5호가")
    bid_volume_5: str = Field(default="", alias="75", description="매수5호가잔량")
    bid_prev_diff_5: str = Field(default="", alias="95", description="매수5호가직전대비")
    ask_price_6: str = Field(default="", alias="46", description="매도6호가")
    ask_volume_6: str = Field(default="", alias="66", description="매도6호가잔량")
    ask_prev_diff_6: str = Field(default="", alias="86", description="매도6호가직전대비")
    bid_price_6: str = Field(default="", alias="56", description="매수6호가")
    bid_volume_6: str = Field(default="", alias="76", description="매수6호가잔량")
    bid_prev_diff_6: str = Field(default="", alias="96", description="매수6호가직전대비")
    ask_price_7: str = Field(default="", alias="47", description="매도7호가")
    ask_volume_7: str = Field(default="", alias="67", description="매도7호가잔량")
    ask_prev_diff_7: str = Field(default="", alias="87", description="매도7호가직전대비")
    bid_price_7: str = Field(default="", alias="57", description="매수7호가")
    bid_volume_7: str = Field(default="", alias="77", description="매수7호가잔량")
    bid_prev_diff_7: str = Field(default="", alias="97", description="매수7호가직전대비")
    ask_price_8: str = Field(default="", alias="48", description="매도8호가")
    ask_volume_8: str = Field(default="", alias="68", description="매도8호가잔량")
    ask_prev_diff_8: str = Field(default="", alias="88", description="매도8호가직전대비")
    bid_price_8: str = Field(default="", alias="58", description="매수8호가")
    bid_volume_8: str = Field(default="", alias="78", description="매수8호가잔량")
    bid_prev_diff_8: str = Field(default="", alias="98", description="매수8호가직전대비")
    ask_price_9: str = Field(default="", alias="49", description="매도9호가")
    ask_volume_9: str = Field(default="", alias="69", description="매도9호가잔량")
    ask_prev_diff_9: str = Field(default="", alias="89", description="매도9호가직전대비")
    bid_price_9: str = Field(default="", alias="59", description="매수9호가")
    bid_volume_9: str = Field(default="", alias="79", description="매수9호가잔량")
    bid_prev_diff_9: str = Field(default="", alias="99", description="매수9호가직전대비")
    ask_price_10: str = Field(default="", alias="50", description="매도10호가")
    ask_volume_10: str = Field(default="", alias="70", description="매도10호가잔량")
    ask_prev_diff_10: str = Field(default="", alias="90", description="매도10호가직전대비")
    bid_price_10: str = Field(default="", alias="60", description="매수10호가")
    bid_volume_10: str = Field(default="", alias="80", description="매수10호가잔량")
    bid_prev_diff_10: str = Field(default="", alias="100", description="매수10호가직전대비")
    total_ask_volume: str = Field(default="", alias="121", description="매도호가총잔량")
    total_ask_volume_prev_diff: str = Field(default="", alias="122", description="매도호가총잔량직전대비")
    total_bid_volume: str = Field(default="", alias="125", description="매수호가총잔량")
    total_bid_volume_prev_diff: str = Field(default="", alias="126", description="매수호가총잔량직전대비")


# ---------------------------------------------------------------------------
# TR별 응답 프레임 모델
# ---------------------------------------------------------------------------


class OverseasRealtimeOrderConfirmationDataItem(BaseModel):
    """F4 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="미국주식 실시간 주문 확인 data 항목")

    type: str = Field(default="", description="실시간항목. TR 명")
    name: str = Field(default="", description="실시간 항목명")
    stex_tp: str = Field(default="", alias="stexTp", description="거래소구분")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: OverseasRealtimeOrderConfirmationValues = Field(
        default_factory=OverseasRealtimeOrderConfirmationValues, description="실시간 값 리스트"
    )


class OverseasRealtimeOrderConfirmation(BaseModel):
    """F4 미국주식 실시간 주문 확인 응답 프레임."""

    model_config = ConfigDict(title="미국주식 실시간 주문 확인 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[OverseasRealtimeOrderConfirmationDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class OverseasRealtimeExecutionDataItem(BaseModel):
    """F5 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="미국주식 실시간 체결 data 항목")

    type: str = Field(default="", description="실시간항목. TR 명")
    name: str = Field(default="", description="실시간 항목명")
    stex_tp: str = Field(default="", alias="stexTp", description="거래소구분")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: OverseasRealtimeExecutionValues = Field(
        default_factory=OverseasRealtimeExecutionValues, description="실시간 값 리스트"
    )


class OverseasRealtimeExecution(BaseModel):
    """F5 미국주식 실시간 체결 응답 프레임."""

    model_config = ConfigDict(title="미국주식 실시간 체결 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[OverseasRealtimeExecutionDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class OverseasRealtimeExecutionPriceDataItem(BaseModel):
    """FE 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="미국주식 실시간 체결가 data 항목")

    type: str = Field(default="", description="실시간항목. TR 명")
    name: str = Field(default="", description="실시간 항목명")
    stex_tp: str = Field(default="", alias="stexTp", description="거래소구분")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: OverseasRealtimeExecutionPriceValues = Field(
        default_factory=OverseasRealtimeExecutionPriceValues, description="실시간 값 리스트"
    )


class OverseasRealtimeExecutionPrice(BaseModel):
    """FE 미국주식 실시간 체결가 응답 프레임."""

    model_config = ConfigDict(title="미국주식 실시간 체결가 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[OverseasRealtimeExecutionPriceDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class OverseasRealtimeTenQuotesDataItem(BaseModel):
    """FT 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="미국주식 10호가 data 항목")

    type: str = Field(default="", description="실시간항목. TR 명")
    name: str = Field(default="", description="실시간 항목명")
    stex_tp: str = Field(default="", alias="stexTp", description="거래소구분")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: OverseasRealtimeTenQuotesValues = Field(
        default_factory=OverseasRealtimeTenQuotesValues, description="실시간 값 리스트"
    )


class OverseasRealtimeTenQuotes(BaseModel):
    """FT 미국주식 10호가 응답 프레임."""

    model_config = ConfigDict(title="미국주식 10호가 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[OverseasRealtimeTenQuotesDataItem] = Field(default_factory=list, description="실시간 등록리스트")
