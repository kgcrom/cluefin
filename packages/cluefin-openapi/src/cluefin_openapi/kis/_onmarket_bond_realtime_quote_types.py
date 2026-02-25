"""장내채권 실시간시세 타입 정의.

WebSocket을 통해 수신되는 실시간 채권 시세 데이터의 Pydantic 모델을 정의합니다.

References:
- https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-bond-real
"""

from pydantic import BaseModel, Field


class OnmarketBondRealtimeExecutionItem(BaseModel):
    """장내채권 실시간 체결가 - H0BJCNT0.

    WebSocket 메시지의 데이터 부분을 파싱한 모델입니다.
    데이터는 "^" 구분자로 19개 필드가 구분되어 전달됩니다.
    """

    stnd_iscd: str = Field(title="표준종목코드")
    bond_isnm: str = Field(title="채권종목명")
    stck_cntg_hour: str = Field(title="주식체결시간")
    prdy_vrss_sign: str = Field(title="전일대비부호")
    prdy_vrss: str = Field(title="전일대비")
    prdy_ctrt: str = Field(title="전일대비율")
    stck_prpr: str = Field(title="현재가")
    cntg_vol: str = Field(title="체결거래량")
    stck_oprc: str = Field(title="시가")
    stck_hgpr: str = Field(title="고가")
    stck_lwpr: str = Field(title="저가")
    stck_prdy_clpr: str = Field(title="전일종가")
    bond_cntg_ert: str = Field(title="현재수익률")
    oprc_ert: str = Field(title="시가수익률")
    hgpr_ert: str = Field(title="고가수익률")
    lwpr_ert: str = Field(title="저가수익률")
    acml_vol: str = Field(title="누적거래량")
    prdy_vol: str = Field(title="전일거래량")
    cntg_type_cls_code: str = Field(title="체결유형코드")


# 필드 순서 리스트 (WebSocket 데이터 파싱용) - 채권 체결가
BOND_EXECUTION_FIELD_NAMES: list[str] = [
    "stnd_iscd",
    "bond_isnm",
    "stck_cntg_hour",
    "prdy_vrss_sign",
    "prdy_vrss",
    "prdy_ctrt",
    "stck_prpr",
    "cntg_vol",
    "stck_oprc",
    "stck_hgpr",
    "stck_lwpr",
    "stck_prdy_clpr",
    "bond_cntg_ert",
    "oprc_ert",
    "hgpr_ert",
    "lwpr_ert",
    "acml_vol",
    "prdy_vol",
    "cntg_type_cls_code",
]


class OnmarketBondIndexRealtimeExecutionItem(BaseModel):
    """채권지수 실시간 체결가 - H0BICNT0.

    WebSocket 메시지의 데이터 부분을 파싱한 모델입니다.
    데이터는 "^" 구분자로 20개 필드가 구분되어 전달됩니다.
    """

    nmix_id: str = Field(title="지수ID")
    stnd_date1: str = Field(title="기준일자1")
    trnm_hour: str = Field(title="전송시간")
    totl_ernn_nmix_oprc: str = Field(title="총수익지수시가지수")
    totl_ernn_nmix_hgpr: str = Field(title="총수익지수최고가")
    totl_ernn_nmix_lwpr: str = Field(title="총수익지수최저가")
    totl_ernn_nmix: str = Field(title="총수익지수")
    prdy_totl_ernn_nmix: str = Field(title="전일총수익지수")
    totl_ernn_nmix_prdy_vrss: str = Field(title="총수익지수전일대비")
    totl_ernn_nmix_prdy_vrss_sign: str = Field(title="총수익지수전일대비부호")
    totl_ernn_nmix_prdy_ctrt: str = Field(title="총수익지수전일대비율")
    clen_prc_nmix: str = Field(title="순가격지수")
    mrkt_prc_nmix: str = Field(title="시장가격지수")
    bond_call_rnvs_nmix: str = Field(title="Call재투자지수")
    bond_zero_rnvs_nmix: str = Field(title="Zero재투자지수")
    bond_futs_thpr: str = Field(title="선물이론가격")
    bond_avrg_drtn_val: str = Field(title="평균듀레이션")
    bond_avrg_cnvx_val: str = Field(title="평균컨벡서티")
    bond_avrg_ytm_val: str = Field(title="평균YTM")
    bond_avrg_frdl_ytm_val: str = Field(title="평균선도YTM")


class OnmarketBondRealtimeOrderbookItem(BaseModel):
    """장내채권 실시간 호가 - H0BJASP0.

    WebSocket 메시지의 데이터 부분을 파싱한 모델입니다.
    데이터는 "^" 구분자로 34개 필드가 구분되어 전달됩니다.
    5단계 매도/매수 호가(수익률, 가격, 잔량) 및 총잔량을 포함합니다.
    """

    stnd_iscd: str = Field(title="표준종목코드")
    stck_cntg_hour: str = Field(title="주식체결시간")
    askp_ert1: str = Field(title="매도호가수익률1")
    bidp_ert1: str = Field(title="매수호가수익률1")
    askp1: str = Field(title="매도호가1")
    bidp1: str = Field(title="매수호가1")
    askp_rsqn1: str = Field(title="매도호가잔량1")
    bidp_rsqn1: str = Field(title="매수호가잔량1")
    askp_ert2: str = Field(title="매도호가수익률2")
    bidp_ert2: str = Field(title="매수호가수익률2")
    askp2: str = Field(title="매도호가2")
    bidp2: str = Field(title="매수호가2")
    askp_rsqn2: str = Field(title="매도호가잔량2")
    bidp_rsqn2: str = Field(title="매수호가잔량2")
    askp_ert3: str = Field(title="매도호가수익률3")
    bidp_ert3: str = Field(title="매수호가수익률3")
    askp3: str = Field(title="매도호가3")
    bidp3: str = Field(title="매수호가3")
    askp_rsqn3: str = Field(title="매도호가잔량3")
    bidp_rsqn3: str = Field(title="매수호가잔량3")
    askp_ert4: str = Field(title="매도호가수익률4")
    bidp_ert4: str = Field(title="매수호가수익률4")
    askp4: str = Field(title="매도호가4")
    bidp4: str = Field(title="매수호가4")
    askp_rsqn4: str = Field(title="매도호가잔량4")
    bidp_rsqn4: str = Field(title="매수호가잔량4")
    askp_ert5: str = Field(title="매도호가수익률5")
    bidp_ert5: str = Field(title="매수호가수익률5")
    askp5: str = Field(title="매도호가5")
    bidp5: str = Field(title="매수호가5")
    askp_rsqn5: str = Field(title="매도호가잔량5")
    bidp_rsqn5: str = Field(title="매수호가잔량5")
    total_askp_rsqn: str = Field(title="총매도호가잔량")
    total_bidp_rsqn: str = Field(title="총매수호가잔량")


# 필드 순서 리스트 (WebSocket 데이터 파싱용) - 채권 호가
BOND_ORDERBOOK_FIELD_NAMES: list[str] = [
    "stnd_iscd",
    "stck_cntg_hour",
    "askp_ert1",
    "bidp_ert1",
    "askp1",
    "bidp1",
    "askp_rsqn1",
    "bidp_rsqn1",
    "askp_ert2",
    "bidp_ert2",
    "askp2",
    "bidp2",
    "askp_rsqn2",
    "bidp_rsqn2",
    "askp_ert3",
    "bidp_ert3",
    "askp3",
    "bidp3",
    "askp_rsqn3",
    "bidp_rsqn3",
    "askp_ert4",
    "bidp_ert4",
    "askp4",
    "bidp4",
    "askp_rsqn4",
    "bidp_rsqn4",
    "askp_ert5",
    "bidp_ert5",
    "askp5",
    "bidp5",
    "askp_rsqn5",
    "bidp_rsqn5",
    "total_askp_rsqn",
    "total_bidp_rsqn",
]


# 필드 순서 리스트 (WebSocket 데이터 파싱용) - 채권지수 체결가
BOND_INDEX_EXECUTION_FIELD_NAMES: list[str] = [
    "nmix_id",
    "stnd_date1",
    "trnm_hour",
    "totl_ernn_nmix_oprc",
    "totl_ernn_nmix_hgpr",
    "totl_ernn_nmix_lwpr",
    "totl_ernn_nmix",
    "prdy_totl_ernn_nmix",
    "totl_ernn_nmix_prdy_vrss",
    "totl_ernn_nmix_prdy_vrss_sign",
    "totl_ernn_nmix_prdy_ctrt",
    "clen_prc_nmix",
    "mrkt_prc_nmix",
    "bond_call_rnvs_nmix",
    "bond_zero_rnvs_nmix",
    "bond_futs_thpr",
    "bond_avrg_drtn_val",
    "bond_avrg_cnvx_val",
    "bond_avrg_ytm_val",
    "bond_avrg_frdl_ytm_val",
]
