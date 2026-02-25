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
