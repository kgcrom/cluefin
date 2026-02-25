"""해외주식 실시간시세 타입 정의.

WebSocket을 통해 수신되는 해외주식 실시간 시세 데이터의 Pydantic 모델을 정의합니다.

References:
- https://apiportal.koreainvestment.com/apiservice/apiservice-oversea-stock-real
"""

from pydantic import BaseModel, Field


class OverseasRealtimeOrderbookItem(BaseModel):
    """해외주식 실시간 호가 Item"""

    rsym: str = Field(title="실시간종목코드")
    symb: str = Field(title="종목코드")
    zdiv: str = Field(title="소숫점자리수")
    xymd: str = Field(title="현지일자")
    xhms: str = Field(title="현지시간")
    kymd: str = Field(title="한국일자")
    khms: str = Field(title="한국시간")
    bvol: str = Field(title="매수총잔량")
    avol: str = Field(title="매도총잔량")
    bdvl: str = Field(title="매수총잔량대비")
    advl: str = Field(title="매도총잔량대비")

    # 1호가
    pbid1: str = Field(title="매수호가1")
    pask1: str = Field(title="매도호가1")
    vbid1: str = Field(title="매수잔량1")
    vask1: str = Field(title="매도잔량1")
    dbid1: str = Field(title="매수잔량대비1")
    dask1: str = Field(title="매도잔량대비1")

    # 2호가
    pbid2: str = Field(title="매수호가2")
    pask2: str = Field(title="매도호가2")
    vbid2: str = Field(title="매수잔량2")
    vask2: str = Field(title="매도잔량2")
    dbid2: str = Field(title="매수잔량대비2")
    dask2: str = Field(title="매도잔량대비2")

    # 3호가
    pbid3: str = Field(title="매수호가3")
    pask3: str = Field(title="매도호가3")
    vbid3: str = Field(title="매수잔량3")
    vask3: str = Field(title="매도잔량3")
    dbid3: str = Field(title="매수잔량대비3")
    dask3: str = Field(title="매도잔량대비3")

    # 4호가
    pbid4: str = Field(title="매수호가4")
    pask4: str = Field(title="매도호가4")
    vbid4: str = Field(title="매수잔량4")
    vask4: str = Field(title="매도잔량4")
    dbid4: str = Field(title="매수잔량대비4")
    dask4: str = Field(title="매도잔량대비4")

    # 5호가
    pbid5: str = Field(title="매수호가5")
    pask5: str = Field(title="매도호가5")
    vbid5: str = Field(title="매수잔량5")
    vask5: str = Field(title="매도잔량5")
    dbid5: str = Field(title="매수잔량대비5")
    dask5: str = Field(title="매도잔량대비5")

    # 6호가
    pbid6: str = Field(title="매수호가6")
    pask6: str = Field(title="매도호가6")
    vbid6: str = Field(title="매수잔량6")
    vask6: str = Field(title="매도잔량6")
    dbid6: str = Field(title="매수잔량대비6")
    dask6: str = Field(title="매도잔량대비6")

    # 7호가
    pbid7: str = Field(title="매수호가7")
    pask7: str = Field(title="매도호가7")
    vbid7: str = Field(title="매수잔량7")
    vask7: str = Field(title="매도잔량7")
    dbid7: str = Field(title="매수잔량대비7")
    dask7: str = Field(title="매도잔량대비7")

    # 8호가
    pbid8: str = Field(title="매수호가8")
    pask8: str = Field(title="매도호가8")
    vbid8: str = Field(title="매수잔량8")
    vask8: str = Field(title="매도잔량8")
    dbid8: str = Field(title="매수잔량대비8")
    dask8: str = Field(title="매도잔량대비8")

    # 9호가
    pbid9: str = Field(title="매수호가9")
    pask9: str = Field(title="매도호가9")
    vbid9: str = Field(title="매수잔량9")
    vask9: str = Field(title="매도잔량9")
    dbid9: str = Field(title="매수잔량대비9")
    dask9: str = Field(title="매도잔량대비9")

    # 10호가
    pbid10: str = Field(title="매수호가10")
    pask10: str = Field(title="매도호가10")
    vbid10: str = Field(title="매수잔량10")
    vask10: str = Field(title="매도잔량10")
    dbid10: str = Field(title="매수잔량대비10")
    dask10: str = Field(title="매도잔량대비10")


OVERSEAS_ORDERBOOK_FIELD_NAMES = [
    "rsym",
    "symb",
    "zdiv",
    "xymd",
    "xhms",
    "kymd",
    "khms",
    "bvol",
    "avol",
    "bdvl",
    "advl",
    "pbid1",
    "pask1",
    "vbid1",
    "vask1",
    "dbid1",
    "dask1",
    "pbid2",
    "pask2",
    "vbid2",
    "vask2",
    "dbid2",
    "dask2",
    "pbid3",
    "pask3",
    "vbid3",
    "vask3",
    "dbid3",
    "dask3",
    "pbid4",
    "pask4",
    "vbid4",
    "vask4",
    "dbid4",
    "dask4",
    "pbid5",
    "pask5",
    "vbid5",
    "vask5",
    "dbid5",
    "dask5",
    "pbid6",
    "pask6",
    "vbid6",
    "vask6",
    "dbid6",
    "dask6",
    "pbid7",
    "pask7",
    "vbid7",
    "vask7",
    "dbid7",
    "dask7",
    "pbid8",
    "pask8",
    "vbid8",
    "vask8",
    "dbid8",
    "dask8",
    "pbid9",
    "pask9",
    "vbid9",
    "vask9",
    "dbid9",
    "dask9",
    "pbid10",
    "pask10",
    "vbid10",
    "vask10",
    "dbid10",
    "dask10",
]


class OverseasRealtimeDelayedOrderbookItem(BaseModel):
    """해외주식 지연호가(아시아)[실시간-008] - HDFSASP1.

    WebSocket 메시지의 데이터 부분을 파싱한 모델입니다.
    데이터는 "^" 구분자로 17개 필드가 구분되어 전달됩니다.
    """

    rsym: str = Field(title="실시간종목코드")
    symb: str = Field(title="종목코드")
    zdiv: str = Field(title="소수점자리수")
    xymd: str = Field(title="현지일자")
    xhms: str = Field(title="현지시간")
    kymd: str = Field(title="한국일자")
    khms: str = Field(title="한국시간")
    bvol: str = Field(title="매수총잔량")
    avol: str = Field(title="매도총잔량")
    bdvl: str = Field(title="매수총잔량대비")
    advl: str = Field(title="매도총잔량대비")
    pbid1: str = Field(title="매수호가1")
    pask1: str = Field(title="매도호가1")
    vbid1: str = Field(title="매수잔량1")
    vask1: str = Field(title="매도잔량1")
    dbid1: str = Field(title="매수잔량대비1")
    dask1: str = Field(title="매도잔량대비1")


# 필드 순서 리스트 (WebSocket 데이터 파싱용) - 해외주식 지연호가(아시아)
OVERSEAS_DELAYED_ORDERBOOK_FIELD_NAMES: list[str] = [
    "rsym",
    "symb",
    "zdiv",
    "xymd",
    "xhms",
    "kymd",
    "khms",
    "bvol",
    "avol",
    "bdvl",
    "advl",
    "pbid1",
    "pask1",
    "vbid1",
    "vask1",
    "dbid1",
    "dask1",
]


class OverseasRealtimeExecutionItem(BaseModel):
    """해외주식 실시간지연체결가[실시간-007] - HDFSCNT0.

    WebSocket 메시지의 데이터 부분을 파싱한 모델입니다.
    데이터는 "^" 구분자로 26개 필드가 구분되어 전달됩니다.
    """

    rsym: str = Field(title="실시간종목코드")
    symb: str = Field(title="종목코드")
    zdiv: str = Field(title="소수점자리수")
    tymd: str = Field(title="현지영업일자")
    xymd: str = Field(title="현지일자")
    xhms: str = Field(title="현지시간")
    kymd: str = Field(title="한국일자")
    khms: str = Field(title="한국시간")
    open: str = Field(title="시가")
    high: str = Field(title="고가")
    low: str = Field(title="저가")
    last: str = Field(title="현재가")
    sign: str = Field(title="대비구분")
    diff: str = Field(title="전일대비")
    rate: str = Field(title="등락율")
    pbid: str = Field(title="매수호가")
    pask: str = Field(title="매도호가")
    vbid: str = Field(title="매수잔량")
    vask: str = Field(title="매도잔량")
    evol: str = Field(title="체결량")
    tvol: str = Field(title="거래량")
    tamt: str = Field(title="거래대금")
    bivl: str = Field(title="매도체결량")
    asvl: str = Field(title="매수체결량")
    strn: str = Field(title="체결강도")
    mtyp: str = Field(title="시장구분")


# 필드 순서 리스트 (WebSocket 데이터 파싱용) - 해외주식 실시간지연체결가
OVERSEAS_EXECUTION_FIELD_NAMES: list[str] = [
    "rsym",
    "symb",
    "zdiv",
    "tymd",
    "xymd",
    "xhms",
    "kymd",
    "khms",
    "open",
    "high",
    "low",
    "last",
    "sign",
    "diff",
    "rate",
    "pbid",
    "pask",
    "vbid",
    "vask",
    "evol",
    "tvol",
    "tamt",
    "bivl",
    "asvl",
    "strn",
    "mtyp",
]


class OverseasRealtimeExecutionNotificationItem(BaseModel):
    """해외주식 실시간체결통보[실시간-009] - H0GSCNI0.

    WebSocket 메시지의 데이터 부분을 파싱한 모델입니다.
    데이터는 "^" 구분자로 25개 필드가 구분되어 전달됩니다.
    """

    cust_id: str = Field(title="고객ID")
    acnt_no: str = Field(title="계좌번호")
    oder_no: str = Field(title="주문번호")
    ooder_no: str = Field(title="원주문번호")
    seln_byov_cls: str = Field(title="매도매수구분")
    rctf_cls: str = Field(title="정정구분")
    oder_kind2: str = Field(title="주문종류2")
    stck_shrn_iscd: str = Field(title="주식단축종목코드")
    cntg_qty: str = Field(title="체결수량")
    cntg_unpr: str = Field(title="체결단가")
    stck_cntg_hour: str = Field(title="주식체결시간")
    rfus_yn: str = Field(title="거부여부")
    cntg_yn: str = Field(title="체결여부")
    acpt_yn: str = Field(title="접수여부")
    brnc_no: str = Field(title="지점번호")
    oder_qty: str = Field(title="주문수량")
    acnt_name: str = Field(title="계좌명")
    cntg_isnm: str = Field(title="체결종목명")
    oder_cond: str = Field(title="해외종목구분")
    debt_gb: str = Field(title="담보유형코드")
    debt_date: str = Field(title="담보대출일자")
    start_tm: str = Field(title="분할매수매도시작시간")
    end_tm: str = Field(title="분할매수매도종료시간")
    tm_div_tp: str = Field(title="시간분할타입유형")
    cntg_unpr12: str = Field(title="체결단가12")


# 필드 순서 리스트 (WebSocket 데이터 파싱용) - 해외주식 실시간체결통보
OVERSEAS_EXECUTION_NOTIFICATION_FIELD_NAMES: list[str] = [
    "cust_id",
    "acnt_no",
    "oder_no",
    "ooder_no",
    "seln_byov_cls",
    "rctf_cls",
    "oder_kind2",
    "stck_shrn_iscd",
    "cntg_qty",
    "cntg_unpr",
    "stck_cntg_hour",
    "rfus_yn",
    "cntg_yn",
    "acpt_yn",
    "brnc_no",
    "oder_qty",
    "acnt_name",
    "cntg_isnm",
    "oder_cond",
    "debt_gb",
    "debt_date",
    "start_tm",
    "end_tm",
    "tm_div_tp",
    "cntg_unpr12",
]
