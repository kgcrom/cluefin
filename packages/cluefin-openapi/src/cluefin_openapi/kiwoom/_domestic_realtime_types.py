"""국내주식 실시간 시세 (웹소켓) 요청/응답 모델.

웹소켓 프레임은 HTTP 응답이 아니므로 ``KiwoomHttpBody``를 상속하지 않고 순수
``BaseModel``로 정의한다. 응답 ``values`` Map은 숫자 FID 키를 사용하므로 의미 있는
영어 필드명 + ``alias``(FID)로 매핑하고 ``populate_by_name=True``를 설정한다.
(미국주식 ``_overseas_realtime_types.py`` 와 대칭.)

이 모듈은 openapi.kiwoom.com 실시간시세 가이드(jobTpCode=14)의 19개 TR 스펙에서
생성되었다. FID 매핑은 각 TR 응답표를 그대로 반영한다.
"""

from typing import Literal

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

# ---------------------------------------------------------------------------
# 공통 등록/해지 요청 모델 (전체 TR 공유, REG/REMOVE)
# ---------------------------------------------------------------------------


class DomesticRealtimeRegisterData(BaseModel):
    """실시간 등록 리스트 항목."""

    model_config = ConfigDict(title="실시간 등록 리스트 항목")

    item: list[str] = Field(
        default_factory=list,
        description="실시간 등록 요소. 거래소별 종목/업종코드 리스트 (KRX:039490, NXT:039490_NX, SOR:039490_AL)",
    )
    type: list[str] = Field(default_factory=list, description="실시간 항목. TR명 리스트 (0A, 0B ...)")


class DomesticRealtimeRequest(BaseModel):
    """실시간 등록/해지 요청 (REG/REMOVE)."""

    model_config = ConfigDict(title="국내주식 실시간 시세 등록/해지 요청")

    trnm: Literal["REG", "REMOVE"] = Field(description="서비스명. REG:등록, REMOVE:해지")
    grp_no: str = Field(description="그룹번호")
    refresh: Literal["0", "1"] = Field(
        description="기존등록유지여부. 등록(REG)시 0:기존등록 item/type 해지, 1:기존등록 유지(Default). 해지(REMOVE)시 값 불필요"
    )
    data: list[DomesticRealtimeRegisterData] = Field(default_factory=list, description="실시간 등록 리스트")


# ---------------------------------------------------------------------------
# TR별 values 모델
# ---------------------------------------------------------------------------


class DomesticRealtimeOrderExecutionValues(BaseModel):
    """00 주문체결 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주문체결 values")

    account_no: str = Field(default="", alias="9201", description="계좌번호. 고유 계좌번호 10자리")
    order_no: str = Field(default="", alias="9203", description="주문번호. 주문번호 7자리")
    manager_id: str = Field(default="", alias="9205", description="관리자사번")
    stock_code: str = Field(default="", alias="9001", description="종목코드,업종코드")
    order_business_type: str = Field(default="", alias="912", description="주문업무분류")
    order_status: str = Field(default="", alias="913", description="주문상태. 접수, 체결, 확인, 취소, 거부")
    stock_name: str = Field(default="", alias="302", description="종목명")
    order_quantity: str = Field(default="", alias="900", description="주문수량. 단위: 1주")
    order_price: str = Field(default="", alias="901", description="주문가격. 단위: 원")
    unexecuted_quantity: str = Field(default="", alias="902", description="미체결수량. 단위: 1주")
    cumulative_execution_amount: str = Field(default="", alias="903", description="체결누계금액. 단위: 원")
    original_order_no: str = Field(
        default="", alias="904", description="원주문번호. 원 주문이 없는 경우 '0000000'으로 출력"
    )
    order_type: str = Field(
        default="",
        alias="905",
        description='주문구분. "+/-", 매도, 매수, 매도정정, 매수정정, 매수취소, 매도취소 / / ※ 영웅문4에서 적색으로 표기되어있으면 +가, 청색으로 표기되어있으면 -가 앞에 기재됩니다',
    )
    trade_type: str = Field(
        default="",
        alias="906",
        description="매매구분. 보통, 시장가, 조건부지정가, 최유리지정가, 최우선지정가, 보통(IOC), 시장가(IOC), 최유리(IOC), 보통(FOK), 시장가(FOK), 최유리(FOK), 스톰지정가, 중간가, 중간가(IOC), 중간가(FOK), 장전시간외, 장후시간외, 시간외대량, 시간외바스켓, 시간외자사주, 시간외단일가",
    )
    sell_buy_type: str = Field(default="", alias="907", description="매도수구분. 1:매도, 2:매수")
    order_execution_time: str = Field(default="", alias="908", description="주문/체결시간. HHmmss")
    execution_no: str = Field(default="", alias="909", description="체결번호")
    execution_price: str = Field(default="", alias="910", description="체결가")
    execution_quantity: str = Field(default="", alias="911", description="체결량")
    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    best_ask_price: str = Field(default="", alias="27", description="(최우선)매도호가. 단위: 원, 부호가 포함된 숫자")
    best_bid_price: str = Field(default="", alias="28", description="(최우선)매수호가. 단위: 원, 부호가 포함된 숫자")
    unit_execution_price: str = Field(default="", alias="914", description="단위체결가")
    unit_execution_quantity: str = Field(default="", alias="915", description="단위체결량")
    today_trade_commission: str = Field(default="", alias="938", description="당일매매수수료")
    today_trade_tax: str = Field(default="", alias="939", description="당일매매세금")
    rejection_reason: str = Field(default="", alias="919", description="거부사유")
    screen_no: str = Field(default="", alias="920", description="화면번호. HTS화면번호")
    terminal_no: str = Field(default="", alias="921", description="터미널번호")
    credit_type2: str = Field(default="", alias="922", description="신용구분. 실시간 체결용")
    loan_date2: str = Field(default="", alias="923", description="대출일. 실시간 체결용")
    after_hours_single_price_current_price: str = Field(default="", alias="10010", description="시간외단일가_현재가")
    exchange_type2: str = Field(default="", alias="2134", description="거래소구분. 0:통합,1:KRX,2:NXT")
    exchange_type_name: str = Field(default="", alias="2135", description="거래소구분명. 통합,KRX,NXT")
    sor_yn: str = Field(default="", alias="2136", description="SOR여부. Y,N")


class DomesticRealtimeBalanceValues(BaseModel):
    """04 잔고 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 잔고 values")

    account_no: str = Field(default="", alias="9201", description="계좌번호. 고유 계좌번호 10자리")
    stock_code: str = Field(default="", alias="9001", description="종목코드,업종코드")
    credit_type: str = Field(default="", alias="917", description="신용구분")
    loan_date: str = Field(default="", alias="916", description="대출일. YYYYMMDD")
    stock_name: str = Field(default="", alias="302", description="종목명")
    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    holding_quantity: str = Field(default="", alias="930", description="보유수량. 단위: 1주")
    purchase_unit_price: str = Field(default="", alias="931", description="매입단가. 단위: 원")
    total_purchase_price: str = Field(default="", alias="932", description="총매입가(당일누적). 단위: 원")
    orderable_quantity: str = Field(default="", alias="933", description="주문가능수량. 단위: 1주")
    today_net_buy_quantity: str = Field(default="", alias="945", description="당일순매수량. 단위: 1주")
    sell_buy_type2: str = Field(default="", alias="946", description="매도/매수구분. 계약,주")
    today_total_sell_profit_loss: str = Field(default="", alias="950", description="당일총매도손익")
    extra_item2: str = Field(default="", alias="951", description="Extra Item")
    best_ask_price: str = Field(default="", alias="27", description="(최우선)매도호가. 단위: 원, 부호가 포함된 숫자")
    best_bid_price: str = Field(default="", alias="28", description="(최우선)매수호가. 단위: 원, 부호가 포함된 숫자")
    base_price: str = Field(default="", alias="307", description="기준가. 단위: 원")
    profit_loss_rate: str = Field(
        default="", alias="8019", description="손익률(실현손익). 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    credit_amount: str = Field(default="", alias="957", description="신용금액")
    credit_interest: str = Field(default="", alias="958", description="신용이자")
    maturity_date: str = Field(default="", alias="918", description="만기일. YYYYMMDD")
    today_realized_profit_loss_securities: str = Field(default="", alias="990", description="당일실현손익(유가)")
    today_realized_profit_loss_rate_securities: str = Field(default="", alias="991", description="당일실현손익율(유가)")
    today_realized_profit_loss_credit: str = Field(default="", alias="992", description="당일실현손익(신용)")
    today_realized_profit_loss_rate_credit: str = Field(default="", alias="993", description="당일실현손익율(신용)")
    collateral_loan_quantity: str = Field(default="", alias="959", description="담보대출수량")
    extra_item: str = Field(default="", alias="924", description="Extra Item")


class DomesticRealtimeStockMomentumValues(BaseModel):
    """0A 주식기세 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식기세 values")

    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff: str = Field(default="", alias="11", description="전일대비. 단위: 원, 부호가 포함된 숫자")
    fluctuation_rate: str = Field(
        default="", alias="12", description="등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    best_ask_price: str = Field(default="", alias="27", description="(최우선)매도호가. 단위: 원, 부호가 포함된 숫자")
    best_bid_price: str = Field(default="", alias="28", description="(최우선)매수호가. 단위: 원, 부호가 포함된 숫자")
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량. 단위: 1주")
    acc_trade_value: str = Field(default="", alias="14", description="누적거래대금. 단위: 백만원")
    open_price: str = Field(default="", alias="16", description="시가. 단위: 원, 부호가 포함된 숫자")
    high_price: str = Field(default="", alias="17", description="고가. 단위: 원, 부호가 포함된 숫자")
    low_price: str = Field(default="", alias="18", description="저가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )
    prev_day_volume_diff: str = Field(
        default="", alias="26", description="전일거래량대비(계약,주). 단위: 1주, 부호가 포함된 숫자"
    )
    trade_value_change: str = Field(default="", alias="29", description="거래대금증감. 단위: 원, 부호가 포함된 숫자")
    prev_day_volume_ratio: str = Field(
        default="",
        alias="30",
        description="전일거래량대비(비율). 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율",
    )
    turnover_rate: str = Field(
        default="", alias="31", description="거래회전율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율"
    )
    trade_cost: str = Field(default="", alias="32", description="거래비용")
    market_cap: str = Field(default="", alias="311", description="시가총액(억). 단위: 억원")
    upper_limit_time: str = Field(default="", alias="567", description="상한가발생시간. HHmmss")
    lower_limit_time: str = Field(default="", alias="568", description="하한가발생시간. HHmmss")


class DomesticRealtimeStockExecutionValues(BaseModel):
    """0B 주식체결 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식체결 values")

    execution_time: str = Field(default="", alias="20", description="체결시간. HHmmss")
    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff: str = Field(default="", alias="11", description="전일대비. 단위: 원, 부호가 포함된 숫자")
    fluctuation_rate: str = Field(
        default="", alias="12", description="등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    best_ask_price: str = Field(default="", alias="27", description="(최우선)매도호가. 단위: 원, 부호가 포함된 숫자")
    best_bid_price: str = Field(default="", alias="28", description="(최우선)매수호가. 단위: 원, 부호가 포함된 숫자")
    trade_volume: str = Field(default="", alias="15", description="거래량. +는 매수체결,-는 매도체결")
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량. 단위: 1주")
    acc_trade_value: str = Field(default="", alias="14", description="누적거래대금. 단위: 백만원")
    open_price: str = Field(default="", alias="16", description="시가. 단위: 원, 부호가 포함된 숫자")
    high_price: str = Field(default="", alias="17", description="고가. 단위: 원, 부호가 포함된 숫자")
    low_price: str = Field(default="", alias="18", description="저가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )
    prev_day_volume_diff: str = Field(
        default="", alias="26", description="전일거래량대비(계약,주). 단위: 1주, 부호가 포함된 숫자"
    )
    trade_value_change: str = Field(default="", alias="29", description="거래대금증감. 단위: 원, 부호가 포함된 숫자")
    prev_day_volume_ratio: str = Field(
        default="",
        alias="30",
        description="전일거래량대비(비율). 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율",
    )
    turnover_rate: str = Field(
        default="", alias="31", description="거래회전율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율"
    )
    trade_cost: str = Field(default="", alias="32", description="거래비용")
    execution_strength: str = Field(
        default="", alias="228", description="체결강도. 단위: %, 소수점 둘째 자리까지 포맷된 백분율"
    )
    market_cap: str = Field(default="", alias="311", description="시가총액(억)")
    market_type: str = Field(default="", alias="290", description="장구분. 1: 장전 시간외 , 2: 장중 , 3: 장후 시간외")
    ko_approach: str = Field(default="", alias="691", description="K.O 접근도")
    upper_limit_time: str = Field(default="", alias="567", description="상한가발생시간. HHmmss")
    lower_limit_time: str = Field(default="", alias="568", description="하한가발생시간. HHmmss")
    prev_same_time_volume_ratio: str = Field(default="", alias="851", description="전일 동시간 거래량 비율")
    open_time: str = Field(default="", alias="1890", description="시가시간")
    high_time: str = Field(default="", alias="1891", description="고가시간")
    low_time: str = Field(default="", alias="1892", description="저가시간")
    sell_execution_volume: str = Field(default="", alias="1030", description="매도체결량")
    buy_execution_volume: str = Field(default="", alias="1031", description="매수체결량")
    buy_ratio2: str = Field(default="", alias="1032", description="매수비율")
    sell_execution_count: str = Field(default="", alias="1071", description="매도체결건수")
    buy_execution_count: str = Field(default="", alias="1072", description="매수체결건수")
    instant_trade_value: str = Field(default="", alias="1313", description="순간거래대금")
    sell_execution_volume_single: str = Field(default="", alias="1315", description="매도체결량_단건")
    buy_execution_volume_single: str = Field(default="", alias="1316", description="매수체결량_단건")
    net_buy_execution_volume: str = Field(default="", alias="1314", description="순매수체결량")
    cfd_margin: str = Field(default="", alias="1497", description="CFD증거금")
    maintenance_margin: str = Field(default="", alias="1498", description="유지증거금")
    today_avg_trade_price: str = Field(default="", alias="620", description="당일거래평균가")
    cfd_trade_cost: str = Field(default="", alias="732", description="CFD거래비용")
    short_sell_trade_cost: str = Field(default="", alias="852", description="대주거래비용")
    exchange_type3: str = Field(default="", alias="9081", description="거래소구분")


class DomesticRealtimeStockPriorityQuoteValues(BaseModel):
    """0C 주식우선호가 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식우선호가 values")

    best_ask_price: str = Field(default="", alias="27", description="(최우선)매도호가. 단위: 원, 부호가 포함된 숫자")
    best_bid_price: str = Field(default="", alias="28", description="(최우선)매수호가. 단위: 원, 부호가 포함된 숫자")


class DomesticRealtimeStockQuoteRemainingValues(BaseModel):
    """0D 주식호가잔량 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식호가잔량 values")

    quote_time: str = Field(default="", alias="21", description="호가시간. HHmmss")
    ask_price_1: str = Field(default="", alias="41", description="매도호가1. 단위: 원, 부호가 포함된 숫자")
    ask_volume_1: str = Field(default="", alias="61", description="매도호가수량1. 단위: 1주")
    ask_prev_diff_1: str = Field(default="", alias="81", description="매도호가직전대비1")
    bid_price_1: str = Field(default="", alias="51", description="매수호가1. 단위: 원, 부호가 포함된 숫자")
    bid_volume_1: str = Field(default="", alias="71", description="매수호가수량1. 단위: 1주")
    bid_prev_diff_1: str = Field(default="", alias="91", description="매수호가직전대비1")
    ask_price_2: str = Field(default="", alias="42", description="매도호가2. 단위: 원, 부호가 포함된 숫자")
    ask_volume_2: str = Field(default="", alias="62", description="매도호가수량2. 단위: 1주")
    ask_prev_diff_2: str = Field(default="", alias="82", description="매도호가직전대비2")
    bid_price_2: str = Field(default="", alias="52", description="매수호가2. 단위: 원, 부호가 포함된 숫자")
    bid_volume_2: str = Field(default="", alias="72", description="매수호가수량2. 단위: 1주")
    bid_prev_diff_2: str = Field(default="", alias="92", description="매수호가직전대비2")
    ask_price_3: str = Field(default="", alias="43", description="매도호가3. 단위: 원, 부호가 포함된 숫자")
    ask_volume_3: str = Field(default="", alias="63", description="매도호가수량3. 단위: 1주")
    ask_prev_diff_3: str = Field(default="", alias="83", description="매도호가직전대비3")
    bid_price_3: str = Field(default="", alias="53", description="매수호가3. 단위: 원, 부호가 포함된 숫자")
    bid_volume_3: str = Field(default="", alias="73", description="매수호가수량3. 단위: 1주")
    bid_prev_diff_3: str = Field(default="", alias="93", description="매수호가직전대비3")
    ask_price_4: str = Field(default="", alias="44", description="매도호가4. 단위: 원, 부호가 포함된 숫자")
    ask_volume_4: str = Field(default="", alias="64", description="매도호가수량4. 단위: 1주")
    ask_prev_diff_4: str = Field(default="", alias="84", description="매도호가직전대비4")
    bid_price_4: str = Field(default="", alias="54", description="매수호가4. 단위: 원, 부호가 포함된 숫자")
    bid_volume_4: str = Field(default="", alias="74", description="매수호가수량4. 단위: 1주")
    bid_prev_diff_4: str = Field(default="", alias="94", description="매수호가직전대비4")
    ask_price_5: str = Field(default="", alias="45", description="매도호가5. 단위: 원, 부호가 포함된 숫자")
    ask_volume_5: str = Field(default="", alias="65", description="매도호가수량5. 단위: 1주")
    ask_prev_diff_5: str = Field(default="", alias="85", description="매도호가직전대비5")
    bid_price_5: str = Field(default="", alias="55", description="매수호가5. 단위: 원, 부호가 포함된 숫자")
    bid_volume_5: str = Field(default="", alias="75", description="매수호가수량5. 단위: 1주")
    bid_prev_diff_5: str = Field(default="", alias="95", description="매수호가직전대비5")
    ask_price_6: str = Field(default="", alias="46", description="매도호가6. 단위: 원, 부호가 포함된 숫자")
    ask_volume_6: str = Field(default="", alias="66", description="매도호가수량6. 단위: 1주")
    ask_prev_diff_6: str = Field(default="", alias="86", description="매도호가직전대비6")
    bid_price_6: str = Field(default="", alias="56", description="매수호가6. 단위: 원, 부호가 포함된 숫자")
    bid_volume_6: str = Field(default="", alias="76", description="매수호가수량6. 단위: 1주")
    bid_prev_diff_6: str = Field(default="", alias="96", description="매수호가직전대비6")
    ask_price_7: str = Field(default="", alias="47", description="매도호가7. 단위: 원, 부호가 포함된 숫자")
    ask_volume_7: str = Field(default="", alias="67", description="매도호가수량7. 단위: 1주")
    ask_prev_diff_7: str = Field(default="", alias="87", description="매도호가직전대비7")
    bid_price_7: str = Field(default="", alias="57", description="매수호가7. 단위: 원, 부호가 포함된 숫자")
    bid_volume_7: str = Field(default="", alias="77", description="매수호가수량7. 단위: 1주")
    bid_prev_diff_7: str = Field(default="", alias="97", description="매수호가직전대비7")
    ask_price_8: str = Field(default="", alias="48", description="매도호가8. 단위: 원, 부호가 포함된 숫자")
    ask_volume_8: str = Field(default="", alias="68", description="매도호가수량8. 단위: 1주")
    ask_prev_diff_8: str = Field(default="", alias="88", description="매도호가직전대비8")
    bid_price_8: str = Field(default="", alias="58", description="매수호가8. 단위: 원, 부호가 포함된 숫자")
    bid_volume_8: str = Field(default="", alias="78", description="매수호가수량8. 단위: 1주")
    bid_prev_diff_8: str = Field(default="", alias="98", description="매수호가직전대비8")
    ask_price_9: str = Field(default="", alias="49", description="매도호가9. 단위: 원, 부호가 포함된 숫자")
    ask_volume_9: str = Field(default="", alias="69", description="매도호가수량9. 단위: 1주")
    ask_prev_diff_9: str = Field(default="", alias="89", description="매도호가직전대비9")
    bid_price_9: str = Field(default="", alias="59", description="매수호가9. 단위: 원, 부호가 포함된 숫자")
    bid_volume_9: str = Field(default="", alias="79", description="매수호가수량9. 단위: 1주")
    bid_prev_diff_9: str = Field(default="", alias="99", description="매수호가직전대비9")
    ask_price_10: str = Field(default="", alias="50", description="매도호가10. 단위: 원, 부호가 포함된 숫자")
    ask_volume_10: str = Field(default="", alias="70", description="매도호가수량10. 단위: 1주")
    bid_price_10: str = Field(default="", alias="60", description="매수호가10. 단위: 원, 부호가 포함된 숫자")
    ask_prev_diff_10: str = Field(default="", alias="90", description="매도호가직전대비10")
    bid_volume_10: str = Field(default="", alias="80", description="매수호가수량10. 단위: 1주")
    bid_prev_diff_10: str = Field(default="", alias="100", description="매수호가직전대비10")
    total_ask_volume: str = Field(default="", alias="121", description="매도호가총잔량. 단위: 1주")
    total_ask_volume_prev_diff: str = Field(default="", alias="122", description="매도호가총잔량직전대비")
    total_bid_volume: str = Field(default="", alias="125", description="매수호가총잔량. 단위: 1주")
    total_bid_volume_prev_diff: str = Field(default="", alias="126", description="매수호가총잔량직전대비")
    expected_execution_price: str = Field(default="", alias="23", description="예상체결가. 단위: 원")
    expected_execution_quantity: str = Field(default="", alias="24", description="예상체결수량. 단위: 1주")
    net_buy_remaining: str = Field(default="", alias="128", description="순매수잔량. 단위: 1주, 부호가 포함된 숫자")
    buy_ratio: str = Field(default="", alias="129", description="매수비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    net_sell_remaining: str = Field(default="", alias="138", description="순매도잔량. 단위: 1주, 부호가 포함된 숫자")
    sell_ratio: str = Field(
        default="", alias="139", description="매도비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율"
    )
    expected_execution_prev_close_diff: str = Field(default="", alias="200", description="예상체결가전일종가대비")
    expected_execution_prev_close_diff_rate: str = Field(
        default="", alias="201", description="예상체결가전일종가대비등락율"
    )
    expected_execution_prev_close_diff_sign: str = Field(
        default="", alias="238", description="예상체결가전일종가대비기호"
    )
    expected_execution_price2: str = Field(
        default="", alias="291", description="예상체결가. 예상체결 시간동안에만 유효한 값"
    )
    expected_execution_volume: str = Field(default="", alias="292", description="예상체결량")
    expected_execution_prev_diff_sign: str = Field(default="", alias="293", description="예상체결가전일대비기호")
    expected_execution_prev_diff: str = Field(default="", alias="294", description="예상체결가전일대비")
    expected_execution_prev_diff_rate: str = Field(default="", alias="295", description="예상체결가전일대비등락율")
    krx_ask_volume_1: str = Field(default="", alias="6044", description="KRX 매도호가잔량1")
    krx_ask_volume_2: str = Field(default="", alias="6045", description="KRX 매도호가잔량2")
    krx_ask_volume_3: str = Field(default="", alias="6046", description="KRX 매도호가잔량3")
    krx_ask_volume_4: str = Field(default="", alias="6047", description="KRX 매도호가잔량4")
    krx_ask_volume_5: str = Field(default="", alias="6048", description="KRX 매도호가잔량5")
    krx_ask_volume_6: str = Field(default="", alias="6049", description="KRX 매도호가잔량6")
    krx_ask_volume_7: str = Field(default="", alias="6050", description="KRX 매도호가잔량7")
    krx_ask_volume_8: str = Field(default="", alias="6051", description="KRX 매도호가잔량8")
    krx_ask_volume_9: str = Field(default="", alias="6052", description="KRX 매도호가잔량9")
    krx_ask_volume_10: str = Field(default="", alias="6053", description="KRX 매도호가잔량10")
    krx_bid_volume_1: str = Field(default="", alias="6054", description="KRX 매수호가잔량1")
    krx_bid_volume_2: str = Field(default="", alias="6055", description="KRX 매수호가잔량2")
    krx_bid_volume_3: str = Field(default="", alias="6056", description="KRX 매수호가잔량3")
    krx_bid_volume_4: str = Field(default="", alias="6057", description="KRX 매수호가잔량4")
    krx_bid_volume_5: str = Field(default="", alias="6058", description="KRX 매수호가잔량5")
    krx_bid_volume_6: str = Field(default="", alias="6059", description="KRX 매수호가잔량6")
    krx_bid_volume_7: str = Field(default="", alias="6060", description="KRX 매수호가잔량7")
    krx_bid_volume_8: str = Field(default="", alias="6061", description="KRX 매수호가잔량8")
    krx_bid_volume_9: str = Field(default="", alias="6062", description="KRX 매수호가잔량9")
    krx_bid_volume_10: str = Field(default="", alias="6063", description="KRX 매수호가잔량10")
    krx_total_ask_volume: str = Field(default="", alias="6064", description="KRX 매도호가총잔량")
    krx_total_bid_volume: str = Field(default="", alias="6065", description="KRX 매수호가총잔량")
    nxt_ask_volume_1: str = Field(default="", alias="6066", description="NXT 매도호가잔량1")
    nxt_ask_volume_2: str = Field(default="", alias="6067", description="NXT 매도호가잔량2")
    nxt_ask_volume_3: str = Field(default="", alias="6068", description="NXT 매도호가잔량3")
    nxt_ask_volume_4: str = Field(default="", alias="6069", description="NXT 매도호가잔량4")
    nxt_ask_volume_5: str = Field(default="", alias="6070", description="NXT 매도호가잔량5")
    nxt_ask_volume_6: str = Field(default="", alias="6071", description="NXT 매도호가잔량6")
    nxt_ask_volume_7: str = Field(default="", alias="6072", description="NXT 매도호가잔량7")
    nxt_ask_volume_8: str = Field(default="", alias="6073", description="NXT 매도호가잔량8")
    nxt_ask_volume_9: str = Field(default="", alias="6074", description="NXT 매도호가잔량9")
    nxt_ask_volume_10: str = Field(default="", alias="6075", description="NXT 매도호가잔량10")
    nxt_bid_volume_1: str = Field(default="", alias="6076", description="NXT 매수호가잔량1")
    nxt_bid_volume_2: str = Field(default="", alias="6077", description="NXT 매수호가잔량2")
    nxt_bid_volume_3: str = Field(default="", alias="6078", description="NXT 매수호가잔량3")
    nxt_bid_volume_4: str = Field(default="", alias="6079", description="NXT 매수호가잔량4")
    nxt_bid_volume_5: str = Field(default="", alias="6080", description="NXT 매수호가잔량5")
    nxt_bid_volume_6: str = Field(default="", alias="6081", description="NXT 매수호가잔량6")
    nxt_bid_volume_7: str = Field(default="", alias="6082", description="NXT 매수호가잔량7")
    nxt_bid_volume_8: str = Field(default="", alias="6083", description="NXT 매수호가잔량8")
    nxt_bid_volume_9: str = Field(default="", alias="6084", description="NXT 매수호가잔량9")
    nxt_bid_volume_10: str = Field(default="", alias="6085", description="NXT 매수호가잔량10")
    nxt_total_ask_volume: str = Field(default="", alias="6086", description="NXT 매도호가총잔량")
    nxt_total_bid_volume: str = Field(default="", alias="6087", description="NXT 매수호가총잔량")
    krx_mid_price_total_ask_volume_change: str = Field(
        default="", alias="6100", description="KRX 중간가 매도 총잔량 증감"
    )
    krx_mid_price_total_ask_volume: str = Field(default="", alias="6101", description="KRX 중간가 매도 총잔량")
    krx_mid_price: str = Field(default="", alias="6102", description="KRX 중간가")
    krx_mid_price_total_bid_volume: str = Field(default="", alias="6103", description="KRX 중간가 매수 총잔량")
    krx_mid_price_total_bid_volume_change: str = Field(
        default="", alias="6104", description="KRX 중간가 매수 총잔량 증감"
    )
    nxt_mid_price_total_ask_volume_change: str = Field(
        default="", alias="6105", description="NXT중간가 매도 총잔량 증감"
    )
    nxt_mid_price_total_ask_volume: str = Field(default="", alias="6106", description="NXT중간가 매도 총잔량")
    nxt_mid_price: str = Field(default="", alias="6107", description="NXT중간가")
    nxt_mid_price_total_bid_volume: str = Field(default="", alias="6108", description="NXT중간가 매수 총잔량")
    nxt_mid_price_total_bid_volume_change: str = Field(
        default="", alias="6109", description="NXT중간가 매수 총잔량 증감"
    )
    krx_mid_price_diff: str = Field(default="", alias="6110", description="KRX중간가대비. 기준가대비")
    krx_mid_price_diff_sign: str = Field(default="", alias="6111", description="KRX중간가대비 기호. 기준가대비")
    krx_mid_price_diff_rate: str = Field(default="", alias="6112", description="KRX중간가대비등락율. 기준가대비")
    nxt_mid_price_diff: str = Field(default="", alias="6113", description="NXT중간가대비. 기준가대비")
    nxt_mid_price_diff_sign: str = Field(default="", alias="6114", description="NXT중간가대비 기호. 기준가대비")
    nxt_mid_price_diff_rate: str = Field(default="", alias="6115", description="NXT중간가대비등락율. 기준가대비")


class DomesticRealtimeStockAfterHoursQuoteValues(BaseModel):
    """0E 주식시간외호가 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식시간외호가 values")

    quote_time: str = Field(default="", alias="21", description="호가시간. HHmmss")
    after_hours_total_ask_volume: str = Field(default="", alias="131", description="시간외매도호가총잔량. 단위: 1주")
    after_hours_total_ask_volume_prev_diff: str = Field(
        default="", alias="132", description="시간외매도호가총잔량직전대비. 단위: 1주, 부호가 포함된 숫자"
    )
    after_hours_total_bid_volume: str = Field(default="", alias="135", description="시간외매수호가총잔량. 단위: 1주")
    after_hours_total_bid_volume_prev_diff: str = Field(
        default="", alias="136", description="시간외매수호가총잔량직전대비. 단위: 1주, 부호가 포함된 숫자"
    )


class DomesticRealtimeStockCurrentDayTraderValues(BaseModel):
    """0F 주식당일거래원 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식당일거래원 values")

    ask_trader_name_1: str = Field(default="", alias="141", description="매도거래원1")
    ask_trader_volume_1: str = Field(default="", alias="161", description="매도거래원수량1. 단위: 1주")
    ask_trader_change_1: str = Field(
        default="", alias="166", description="매도거래원별증감1. 단위: 1주, 부호가 포함된 숫자"
    )
    ask_trader_code_1: str = Field(default="", alias="146", description="매도거래원코드1")
    ask_trader_color_1: str = Field(default="", alias="271", description="매도거래원색깔1")
    bid_trader_name_1: str = Field(default="", alias="151", description="매수거래원1")
    bid_trader_volume_1: str = Field(default="", alias="171", description="매수거래원수량1. 단위: 1주")
    bid_trader_change_1: str = Field(
        default="", alias="176", description="매수거래원별증감1. 단위: 1주, 부호가 포함된 숫자"
    )
    bid_trader_code_1: str = Field(default="", alias="156", description="매수거래원코드1")
    bid_trader_color_1: str = Field(default="", alias="281", description="매수거래원색깔1")
    ask_trader_name_2: str = Field(default="", alias="142", description="매도거래원2")
    ask_trader_volume_2: str = Field(default="", alias="162", description="매도거래원수량2. 단위: 1주")
    ask_trader_change_2: str = Field(
        default="", alias="167", description="매도거래원별증감2. 단위: 1주, 부호가 포함된 숫자"
    )
    ask_trader_code_2: str = Field(default="", alias="147", description="매도거래원코드2")
    ask_trader_color_2: str = Field(default="", alias="272", description="매도거래원색깔2")
    bid_trader_name_2: str = Field(default="", alias="152", description="매수거래원2")
    bid_trader_volume_2: str = Field(default="", alias="172", description="매수거래원수량2. 단위: 1주")
    bid_trader_change_2: str = Field(
        default="", alias="177", description="매수거래원별증감2. 단위: 1주, 부호가 포함된 숫자"
    )
    bid_trader_code_2: str = Field(default="", alias="157", description="매수거래원코드2")
    bid_trader_color_2: str = Field(default="", alias="282", description="매수거래원색깔2")
    ask_trader_name_3: str = Field(default="", alias="143", description="매도거래원3")
    ask_trader_volume_3: str = Field(default="", alias="163", description="매도거래원수량3. 단위: 1주")
    ask_trader_change_3: str = Field(
        default="", alias="168", description="매도거래원별증감3. 단위: 1주, 부호가 포함된 숫자"
    )
    ask_trader_code_3: str = Field(default="", alias="148", description="매도거래원코드3")
    ask_trader_color_3: str = Field(default="", alias="273", description="매도거래원색깔3")
    bid_trader_name_3: str = Field(default="", alias="153", description="매수거래원3")
    bid_trader_volume_3: str = Field(default="", alias="173", description="매수거래원수량3. 단위: 1주")
    bid_trader_change_3: str = Field(
        default="", alias="178", description="매수거래원별증감3. 단위: 1주, 부호가 포함된 숫자"
    )
    bid_trader_code_3: str = Field(default="", alias="158", description="매수거래원코드3")
    bid_trader_color_3: str = Field(default="", alias="283", description="매수거래원색깔3")
    ask_trader_name_4: str = Field(default="", alias="144", description="매도거래원4")
    ask_trader_volume_4: str = Field(default="", alias="164", description="매도거래원수량4. 단위: 1주")
    ask_trader_change_4: str = Field(
        default="", alias="169", description="매도거래원별증감4. 단위: 1주, 부호가 포함된 숫자"
    )
    ask_trader_code_4: str = Field(default="", alias="149", description="매도거래원코드4")
    ask_trader_color_4: str = Field(default="", alias="274", description="매도거래원색깔4")
    bid_trader_name_4: str = Field(default="", alias="154", description="매수거래원4")
    bid_trader_volume_4: str = Field(default="", alias="174", description="매수거래원수량4. 단위: 1주")
    bid_trader_change_4: str = Field(
        default="", alias="179", description="매수거래원별증감4. 단위: 1주, 부호가 포함된 숫자"
    )
    bid_trader_code_4: str = Field(default="", alias="159", description="매수거래원코드4")
    bid_trader_color_4: str = Field(default="", alias="284", description="매수거래원색깔4")
    ask_trader_name_5: str = Field(default="", alias="145", description="매도거래원5")
    ask_trader_volume_5: str = Field(default="", alias="165", description="매도거래원수량5. 단위: 1주")
    ask_trader_change_5: str = Field(
        default="", alias="170", description="매도거래원별증감5. 단위: 1주, 부호가 포함된 숫자"
    )
    ask_trader_code_5: str = Field(default="", alias="150", description="매도거래원코드5")
    ask_trader_color_5: str = Field(default="", alias="275", description="매도거래원색깔5")
    bid_trader_name_5: str = Field(default="", alias="155", description="매수거래원5")
    bid_trader_volume_5: str = Field(default="", alias="175", description="매수거래원수량5. 단위: 1주")
    bid_trader_change_5: str = Field(
        default="", alias="180", description="매수거래원별증감5. 단위: 1주, 부호가 포함된 숫자"
    )
    bid_trader_code_5: str = Field(default="", alias="160", description="매수거래원코드5")
    bid_trader_color_5: str = Field(default="", alias="285", description="매수거래원색깔5")
    foreign_est_sell_sum: str = Field(default="", alias="261", description="외국계매도추정합")
    foreign_est_sell_sum_change: str = Field(default="", alias="262", description="외국계매도추정합변동")
    foreign_est_buy_sum: str = Field(default="", alias="263", description="외국계매수추정합")
    foreign_est_buy_sum_change: str = Field(default="", alias="264", description="외국계매수추정합변동")
    foreign_est_net_buy_sum: str = Field(default="", alias="267", description="외국계순매수추정합")
    foreign_est_net_buy_change: str = Field(default="", alias="268", description="외국계순매수변동")
    exchange_type: str = Field(default="", alias="337", description="거래소구분")


class DomesticRealtimeEtfNavValues(BaseModel):
    """0G ETF NAV values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 ETF NAV values")

    nav: str = Field(default="", alias="36", description="NAV. 부호 포함 소수점 둘째 자리까지 포맷된 숫자")
    nav_prev_day_diff: str = Field(
        default="", alias="37", description="NAV전일대비. 부호 포함 소수점 둘째 자리까지 포맷된 숫자"
    )
    nav_fluctuation_rate: str = Field(
        default="", alias="38", description="NAV등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    tracking_error_rate: str = Field(
        default="", alias="39", description="추적오차율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율"
    )
    execution_time: str = Field(default="", alias="20", description="체결시간. HHmmss")
    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff: str = Field(default="", alias="11", description="전일대비. 단위: 원, 부호가 포함된 숫자")
    fluctuation_rate: str = Field(
        default="", alias="12", description="등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량. 단위: 1주")
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )
    elw_gearing_ratio: str = Field(default="", alias="667", description="ELW기어링비율")
    elw_breakeven_rate: str = Field(default="", alias="668", description="ELW손익분기율")
    elw_capital_support_point: str = Field(default="", alias="669", description="ELW자본지지점")
    nav_index_gap_rate: str = Field(default="", alias="265", description="NAV/지수괴리율")
    nav_etf_gap_rate: str = Field(default="", alias="266", description="NAV/ETF괴리율")


class DomesticRealtimeStockExpectedExecutionValues(BaseModel):
    """0H 주식예상체결 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식예상체결 values")

    execution_time: str = Field(default="", alias="20", description="체결시간. HHmmss")
    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff: str = Field(default="", alias="11", description="전일대비. 단위: 원, 부호가 포함된 숫자")
    fluctuation_rate: str = Field(
        default="", alias="12", description="등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    trade_volume: str = Field(default="", alias="15", description="거래량. +는 매수체결, -는 매도체결")
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량. 단위: 1주")
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )


class DomesticRealtimeIntlGoldPriceValues(BaseModel):
    """0I 국제금환산가격 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 국제금환산가격 values")

    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1:상한, 2:상승, 3:없음, 4:하한, 5:하락"
    )
    prev_day_diff: str = Field(default="", alias="11", description="전일대비. 단위: 원, 부호가 포함된 숫자")
    fluctuation_rate: str = Field(
        default="", alias="12", description="등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )


class DomesticRealtimeIndustryIndexValues(BaseModel):
    """0J 업종지수 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 업종지수 values")

    execution_time: str = Field(default="", alias="20", description="체결시간. HHmmss")
    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff: str = Field(default="", alias="11", description="전일대비. 단위: 원, 부호가 포함된 숫자")
    fluctuation_rate: str = Field(
        default="", alias="12", description="등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    trade_volume: str = Field(default="", alias="15", description="거래량. +는 매수체결,-는 매도체결")
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량. 단위: 1주")
    acc_trade_value: str = Field(default="", alias="14", description="누적거래대금. 단위: 백만원")
    open_price: str = Field(default="", alias="16", description="시가. 단위: 원, 부호가 포함된 숫자")
    high_price: str = Field(default="", alias="17", description="고가. 단위: 원, 부호가 포함된 숫자")
    low_price: str = Field(default="", alias="18", description="저가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )
    prev_day_volume_diff: str = Field(default="", alias="26", description="전일거래량대비. 계약,주")


class DomesticRealtimeIndustryFluctuationValues(BaseModel):
    """0U 업종등락 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 업종등락 values")

    execution_time: str = Field(default="", alias="20", description="체결시간. HHmmss")
    advancing_count: str = Field(default="", alias="252", description="상승종목수")
    upper_limit_count: str = Field(default="", alias="251", description="상한종목수")
    unchanged_count: str = Field(default="", alias="253", description="보합종목수")
    declining_count: str = Field(default="", alias="255", description="하락종목수")
    lower_limit_count: str = Field(default="", alias="254", description="하한종목수")
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량. 단위: 1주")
    acc_trade_value: str = Field(default="", alias="14", description="누적거래대금. 단위: 백만원")
    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff: str = Field(default="", alias="11", description="전일대비. 단위: 원, 부호가 포함된 숫자")
    fluctuation_rate: str = Field(
        default="", alias="12", description="등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    traded_stock_count: str = Field(default="", alias="256", description="거래형성종목수. 계약,주")
    traded_ratio: str = Field(
        default="", alias="257", description="거래형성비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율"
    )
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )


class DomesticRealtimeStockItemInfoValues(BaseModel):
    """0g 주식종목정보 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식종목정보 values")

    discretionary_extension: str = Field(default="", alias="297", description="임의연장")
    pre_market_extension: str = Field(default="", alias="592", description="장전임의연장")
    post_market_extension: str = Field(default="", alias="593", description="장후임의연장")
    upper_limit_price: str = Field(default="", alias="305", description="상한가. 단위: 원, 부호가 포함된 숫자")
    lower_limit_price: str = Field(default="", alias="306", description="하한가. 단위: 원, 부호가 포함된 숫자")
    base_price: str = Field(default="", alias="307", description="기준가. 단위: 원")
    early_termination_elw: str = Field(default="", alias="689", description="조기종료ELW발생")
    currency_unit: str = Field(default="", alias="594", description="통화단위")
    margin_rate_display: str = Field(default="", alias="382", description="증거금율표시")
    stock_info: str = Field(default="", alias="370", description="종목정보")


class DomesticRealtimeElwTheoreticalPriceValues(BaseModel):
    """0m ELW 이론가 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 ELW 이론가 values")

    execution_time: str = Field(default="", alias="20", description="체결시간. HHmmss")
    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    elw_theoretical_price: str = Field(default="", alias="670", description="ELW이론가")
    elw_implied_volatility: str = Field(default="", alias="671", description="ELW내재변동성")
    elw_delta: str = Field(default="", alias="672", description="ELW델타")
    elw_gamma: str = Field(default="", alias="673", description="ELW감마")
    elw_theta: str = Field(default="", alias="674", description="ELW쎄타")
    elw_vega: str = Field(default="", alias="675", description="ELW베가")
    elw_rho: str = Field(default="", alias="676", description="ELW로")
    lp_quote_implied_volatility: str = Field(default="", alias="706", description="LP호가내재변동성")


class DomesticRealtimeMarketStartTimeValues(BaseModel):
    """0s 장시작시간 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 장시작시간 values")

    market_operation_type: str = Field(
        default="",
        alias="215",
        description="장운영구분. 0 : 장시작전 알림(8:40~), 3 : 장시작(09:00), 2 : 장마감 알림(15:20~), 4 : 장마감(15:30), 8 : 정규장마감(거래소 수신시 15:30 이후), 9 : 전체장마감(거래소 수신시 18:00 이후), a : 시간외 종가매매 시작(15:40), b : 시간외 종가매매 종료(16:00), c : 시간외 단일가 시작(16:00), d : 시간외 단일가 종료(18:00), e : 선옵 장마감전 동시호가 종료, f : 선물옵션 장운영시간 알림(조기개장 상품), o : 선옵 장시작, s : 선옵 장마감전 동시호가 시작, P : NXT 프리마켓 시작 알림, Q : NXT 프리마켓 종료 알림, R : NXT 메인마켓 시작 알림, S : NXT 메인마켓 종료 알림, T : NXT 에프터마켓 단일가 시작 알림, U : NXT 에프터마켓 시작 알림, V : NXT 에프터마켓 종료 알림",
    )
    execution_time: str = Field(default="", alias="20", description="체결시간. HHmmss")
    market_start_remaining_time: str = Field(default="", alias="214", description="장시작예상잔여시간. HHmmss")


class DomesticRealtimeElwIndicatorValues(BaseModel):
    """0u ELW 지표 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 ELW 지표 values")

    execution_time: str = Field(default="", alias="20", description="체결시간. HHmmss")
    elw_parity: str = Field(default="", alias="666", description="ELW패리티")
    elw_premium: str = Field(default="", alias="1211", description="ELW프리미엄")
    elw_gearing_ratio: str = Field(default="", alias="667", description="ELW기어링비율")
    elw_breakeven_rate: str = Field(default="", alias="668", description="ELW손익분기율")
    elw_capital_support_point: str = Field(default="", alias="669", description="ELW자본지지점")


class DomesticRealtimeStockProgramTradingValues(BaseModel):
    """0w 종목프로그램매매 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 종목프로그램매매 values")

    execution_time: str = Field(default="", alias="20", description="체결시간. HHmmss")
    current_price: str = Field(default="", alias="10", description="현재가. 단위: 원, 부호가 포함된 숫자")
    prev_day_diff_sign: str = Field(
        default="", alias="25", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )
    prev_day_diff: str = Field(default="", alias="11", description="전일대비. 단위: 원, 부호가 포함된 숫자")
    fluctuation_rate: str = Field(
        default="", alias="12", description="등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량. 단위: 1주")
    sell_quantity: str = Field(default="", alias="202", description="매도수량. 단위: 1주")
    sell_amount: str = Field(default="", alias="204", description="매도금액. 단위: 원")
    buy_quantity: str = Field(default="", alias="206", description="매수수량. 단위: 1주")
    buy_amount: str = Field(default="", alias="208", description="매수금액")
    net_buy_quantity: str = Field(default="", alias="210", description="순매수수량")
    net_buy_quantity_change: str = Field(default="", alias="211", description="순매수수량증감. 계약,주")
    net_buy_amount: str = Field(default="", alias="212", description="순매수금액")
    net_buy_amount_change: str = Field(default="", alias="213", description="순매수금액증감")
    market_start_remaining_time: str = Field(default="", alias="214", description="장시작예상잔여시간")
    market_operation_type: str = Field(default="", alias="215", description="장운영구분")
    investor_ticker: str = Field(default="", alias="216", description="투자자별ticker")


class DomesticRealtimeViActivationValues(BaseModel):
    """1h VI발동/해제 values."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 VI발동/해제 values")

    stock_code: str = Field(default="", alias="9001", description="종목코드")
    stock_name: str = Field(default="", alias="302", description="종목명")
    acc_trade_volume: str = Field(default="", alias="13", description="누적거래량. 단위: 1주")
    acc_trade_value: str = Field(default="", alias="14", description="누적거래대금. 단위: 백만원")
    vi_activation_type: str = Field(default="", alias="9068", description="VI발동구분")
    kospi_kosdaq_type: str = Field(default="", alias="9008", description="KOSPI,KOSDAQ,전체구분")
    pre_market_type: str = Field(default="", alias="9075", description="장전구분")
    vi_activation_price: str = Field(default="", alias="1221", description="VI발동가격. 단위: 원")
    trade_execution_time: str = Field(default="", alias="1223", description="매매체결처리시각. HHmmss")
    vi_release_time: str = Field(default="", alias="1224", description="VI해제시각. HHmmss")
    vi_apply_type: str = Field(default="", alias="1225", description="VI적용구분. 정적/동적/동적+정적")
    base_price_static: str = Field(default="", alias="1236", description="기준가격 정적. 계약,주")
    base_price_dynamic: str = Field(default="", alias="1237", description="기준가격 동적")
    gap_rate_static: str = Field(default="", alias="1238", description="괴리율 정적")
    gap_rate_dynamic: str = Field(default="", alias="1239", description="괴리율 동적")
    vi_activation_fluctuation_rate: str = Field(default="", alias="1489", description="VI발동가 등락율")
    vi_activation_count: str = Field(default="", alias="1490", description="VI발동횟수")
    activation_direction_type: str = Field(default="", alias="9069", description="발동방향구분")
    extra_item3: str = Field(default="", alias="1279", description="Extra Item")


# ---------------------------------------------------------------------------
# TR별 응답 프레임 모델
# ---------------------------------------------------------------------------


class DomesticRealtimeOrderExecutionDataItem(BaseModel):
    """00 주문체결 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주문체결 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeOrderExecutionValues = Field(
        default_factory=DomesticRealtimeOrderExecutionValues, description="실시간 값 리스트"
    )


class DomesticRealtimeOrderExecution(BaseModel):
    """00 국내주식 실시간 주문체결 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 주문체결 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeOrderExecutionDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeBalanceDataItem(BaseModel):
    """04 잔고 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 잔고 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeBalanceValues = Field(
        default_factory=DomesticRealtimeBalanceValues, description="실시간 값 리스트"
    )


class DomesticRealtimeBalance(BaseModel):
    """04 국내주식 실시간 잔고 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 잔고 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeBalanceDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeStockMomentumDataItem(BaseModel):
    """0A 주식기세 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식기세 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeStockMomentumValues = Field(
        default_factory=DomesticRealtimeStockMomentumValues, description="실시간 값 리스트"
    )


class DomesticRealtimeStockMomentum(BaseModel):
    """0A 국내주식 실시간 주식기세 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 주식기세 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeStockMomentumDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeStockExecutionDataItem(BaseModel):
    """0B 주식체결 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식체결 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeStockExecutionValues = Field(
        default_factory=DomesticRealtimeStockExecutionValues, description="실시간 값 리스트"
    )


class DomesticRealtimeStockExecution(BaseModel):
    """0B 국내주식 실시간 주식체결 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 주식체결 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeStockExecutionDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeStockPriorityQuoteDataItem(BaseModel):
    """0C 주식우선호가 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식우선호가 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeStockPriorityQuoteValues = Field(
        default_factory=DomesticRealtimeStockPriorityQuoteValues, description="실시간 값 리스트"
    )


class DomesticRealtimeStockPriorityQuote(BaseModel):
    """0C 국내주식 실시간 주식우선호가 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 주식우선호가 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeStockPriorityQuoteDataItem] = Field(
        default_factory=list, description="실시간 등록리스트"
    )


class DomesticRealtimeStockQuoteRemainingDataItem(BaseModel):
    """0D 주식호가잔량 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식호가잔량 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeStockQuoteRemainingValues = Field(
        default_factory=DomesticRealtimeStockQuoteRemainingValues, description="실시간 값 리스트"
    )


class DomesticRealtimeStockQuoteRemaining(BaseModel):
    """0D 국내주식 실시간 주식호가잔량 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 주식호가잔량 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeStockQuoteRemainingDataItem] = Field(
        default_factory=list, description="실시간 등록리스트"
    )


class DomesticRealtimeStockAfterHoursQuoteDataItem(BaseModel):
    """0E 주식시간외호가 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식시간외호가 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeStockAfterHoursQuoteValues = Field(
        default_factory=DomesticRealtimeStockAfterHoursQuoteValues, description="실시간 값 리스트"
    )


class DomesticRealtimeStockAfterHoursQuote(BaseModel):
    """0E 국내주식 실시간 주식시간외호가 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 주식시간외호가 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeStockAfterHoursQuoteDataItem] = Field(
        default_factory=list, description="실시간 등록리스트"
    )


class DomesticRealtimeStockCurrentDayTraderDataItem(BaseModel):
    """0F 주식당일거래원 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식당일거래원 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeStockCurrentDayTraderValues = Field(
        default_factory=DomesticRealtimeStockCurrentDayTraderValues, description="실시간 값 리스트"
    )


class DomesticRealtimeStockCurrentDayTrader(BaseModel):
    """0F 국내주식 실시간 주식당일거래원 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 주식당일거래원 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeStockCurrentDayTraderDataItem] = Field(
        default_factory=list, description="실시간 등록리스트"
    )


class DomesticRealtimeEtfNavDataItem(BaseModel):
    """0G ETF NAV 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 ETF NAV data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeEtfNavValues = Field(
        default_factory=DomesticRealtimeEtfNavValues, description="실시간 값 리스트"
    )


class DomesticRealtimeEtfNav(BaseModel):
    """0G 국내주식 실시간 ETF NAV 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 ETF NAV 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeEtfNavDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeStockExpectedExecutionDataItem(BaseModel):
    """0H 주식예상체결 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식예상체결 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeStockExpectedExecutionValues = Field(
        default_factory=DomesticRealtimeStockExpectedExecutionValues, description="실시간 값 리스트"
    )


class DomesticRealtimeStockExpectedExecution(BaseModel):
    """0H 국내주식 실시간 주식예상체결 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 주식예상체결 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeStockExpectedExecutionDataItem] = Field(
        default_factory=list, description="실시간 등록리스트"
    )


class DomesticRealtimeIntlGoldPriceDataItem(BaseModel):
    """0I 국제금환산가격 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 국제금환산가격 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeIntlGoldPriceValues = Field(
        default_factory=DomesticRealtimeIntlGoldPriceValues, description="실시간 값 리스트"
    )


class DomesticRealtimeIntlGoldPrice(BaseModel):
    """0I 국내주식 실시간 국제금환산가격 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 국제금환산가격 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeIntlGoldPriceDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeIndustryIndexDataItem(BaseModel):
    """0J 업종지수 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 업종지수 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeIndustryIndexValues = Field(
        default_factory=DomesticRealtimeIndustryIndexValues, description="실시간 값 리스트"
    )


class DomesticRealtimeIndustryIndex(BaseModel):
    """0J 국내주식 실시간 업종지수 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 업종지수 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeIndustryIndexDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeIndustryFluctuationDataItem(BaseModel):
    """0U 업종등락 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 업종등락 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeIndustryFluctuationValues = Field(
        default_factory=DomesticRealtimeIndustryFluctuationValues, description="실시간 값 리스트"
    )


class DomesticRealtimeIndustryFluctuation(BaseModel):
    """0U 국내주식 실시간 업종등락 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 업종등락 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeIndustryFluctuationDataItem] = Field(
        default_factory=list, description="실시간 등록리스트"
    )


class DomesticRealtimeStockItemInfoDataItem(BaseModel):
    """0g 주식종목정보 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 주식종목정보 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeStockItemInfoValues = Field(
        default_factory=DomesticRealtimeStockItemInfoValues, description="실시간 값 리스트"
    )


class DomesticRealtimeStockItemInfo(BaseModel):
    """0g 국내주식 실시간 주식종목정보 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 주식종목정보 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeStockItemInfoDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeElwTheoreticalPriceDataItem(BaseModel):
    """0m ELW 이론가 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 ELW 이론가 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeElwTheoreticalPriceValues = Field(
        default_factory=DomesticRealtimeElwTheoreticalPriceValues, description="실시간 값 리스트"
    )


class DomesticRealtimeElwTheoreticalPrice(BaseModel):
    """0m 국내주식 실시간 ELW 이론가 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 ELW 이론가 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeElwTheoreticalPriceDataItem] = Field(
        default_factory=list, description="실시간 등록리스트"
    )


class DomesticRealtimeMarketStartTimeDataItem(BaseModel):
    """0s 장시작시간 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 장시작시간 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeMarketStartTimeValues = Field(
        default_factory=DomesticRealtimeMarketStartTimeValues, description="실시간 값 리스트"
    )


class DomesticRealtimeMarketStartTime(BaseModel):
    """0s 국내주식 실시간 장시작시간 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 장시작시간 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeMarketStartTimeDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeElwIndicatorDataItem(BaseModel):
    """0u ELW 지표 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 ELW 지표 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeElwIndicatorValues = Field(
        default_factory=DomesticRealtimeElwIndicatorValues, description="실시간 값 리스트"
    )


class DomesticRealtimeElwIndicator(BaseModel):
    """0u 국내주식 실시간 ELW 지표 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 ELW 지표 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeElwIndicatorDataItem] = Field(default_factory=list, description="실시간 등록리스트")


class DomesticRealtimeStockProgramTradingDataItem(BaseModel):
    """0w 종목프로그램매매 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 종목프로그램매매 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeStockProgramTradingValues = Field(
        default_factory=DomesticRealtimeStockProgramTradingValues, description="실시간 값 리스트"
    )


class DomesticRealtimeStockProgramTrading(BaseModel):
    """0w 국내주식 실시간 종목프로그램매매 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 종목프로그램매매 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeStockProgramTradingDataItem] = Field(
        default_factory=list, description="실시간 등록리스트"
    )


class DomesticRealtimeViActivationDataItem(BaseModel):
    """1h VI발동/해제 실시간 등록리스트 항목."""

    model_config = ConfigDict(populate_by_name=True, title="국내주식 실시간 VI발동/해제 data 항목")

    type: str = Field(default="", description="실시간항목. TR명")
    name: str = Field(default="", description="실시간 항목명")
    item: str = Field(default="", description="실시간 등록 요소. 종목코드")
    values: DomesticRealtimeViActivationValues = Field(
        default_factory=DomesticRealtimeViActivationValues, description="실시간 값 리스트"
    )


class DomesticRealtimeViActivation(BaseModel):
    """1h 국내주식 실시간 VI발동/해제 응답 프레임."""

    model_config = ConfigDict(title="국내주식 실시간 VI발동/해제 응답")

    return_code: int | None = Field(
        default=None, description="결과코드. 등록/해지요청시에만 전송 0:정상,1:오류, 실시간 수신시 미전송"
    )
    return_msg: str = Field(default="", description="결과메시지")
    trnm: str = Field(default="", description="서비스명. 등록/해지요청시 요청값 반환, 실시간수신시 REAL 반환")
    data: list[DomesticRealtimeViActivationDataItem] = Field(default_factory=list, description="실시간 등록리스트")
