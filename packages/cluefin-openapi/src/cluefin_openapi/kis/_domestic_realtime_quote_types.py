"""국내주식 실시간시세 타입 정의.

WebSocket을 통해 수신되는 실시간 시세 데이터의 Pydantic 모델을 정의합니다.

References:
- https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock-real2
"""

from pydantic import BaseModel, Field


class DomesticRealtimeExecutionItem(BaseModel):
    """국내주식 실시간 체결가 (통합) - H0UNCNT0.

    WebSocket 메시지의 데이터 부분을 파싱한 모델입니다.
    데이터는 "^" 구분자로 46개 필드가 구분되어 전달됩니다.
    """

    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    stck_cntg_hour: str = Field(title="주식 체결 시간")
    stck_prpr: str = Field(title="주식 현재가")
    prdy_vrss_sign: str = Field(title="전일 대비 부호")
    prdy_vrss: str = Field(title="전일 대비")
    prdy_ctrt: str = Field(title="전일 대비율")
    wghn_avrg_stck_prc: str = Field(title="가중 평균 주식 가격")
    stck_oprc: str = Field(title="주식 시가")
    stck_hgpr: str = Field(title="주식 최고가")
    stck_lwpr: str = Field(title="주식 최저가")
    askp1: str = Field(title="매도호가1")
    bidp1: str = Field(title="매수호가1")
    cntg_vol: str = Field(title="체결 거래량")
    acml_vol: str = Field(title="누적 거래량")
    acml_tr_pbmn: str = Field(title="누적 거래 대금")
    seln_cntg_csnu: str = Field(title="매도 체결 건수")
    shnu_cntg_csnu: str = Field(title="매수 체결 건수")
    ntby_cntg_csnu: str = Field(title="순매수 체결 건수")
    cttr: str = Field(title="체결강도")
    seln_cntg_smtn: str = Field(title="총 매도 수량")
    shnu_cntg_smtn: str = Field(title="총 매수 수량")
    cntg_cls_code: str = Field(title="체결구분")
    shnu_rate: str = Field(title="매수비율")
    prdy_vol_vrss_acml_vol_rate: str = Field(title="전일 거래량 대비 등락율")
    oprc_hour: str = Field(title="시가 시간")
    oprc_vrss_prpr_sign: str = Field(title="시가대비구분")
    oprc_vrss_prpr: str = Field(title="시가대비")
    hgpr_hour: str = Field(title="최고가 시간")
    hgpr_vrss_prpr_sign: str = Field(title="고가대비구분")
    hgpr_vrss_prpr: str = Field(title="고가대비")
    lwpr_hour: str = Field(title="최저가 시간")
    lwpr_vrss_prpr_sign: str = Field(title="저가대비구분")
    lwpr_vrss_prpr: str = Field(title="저가대비")
    bsop_date: str = Field(title="영업 일자")
    new_mkop_cls_code: str = Field(title="신 장운영 구분 코드")
    trht_yn: str = Field(title="거래정지 여부")
    askp_rsqn1: str = Field(title="매도호가 잔량1")
    bidp_rsqn1: str = Field(title="매수호가 잔량1")
    total_askp_rsqn: str = Field(title="총 매도호가 잔량")
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량")
    vol_tnrt: str = Field(title="거래량 회전율")
    prdy_smns_hour_acml_vol: str = Field(title="전일 동시간 누적 거래량")
    prdy_smns_hour_acml_vol_rate: str = Field(title="전일 동시간 누적 거래량 비율")
    hour_cls_code: str = Field(title="시간 구분 코드")
    mrkt_trtm_cls_code: str = Field(title="임의종료구분코드")
    vi_stnd_prc: str = Field(title="정적VI발동기준가")


# 필드 순서 리스트 (WebSocket 데이터 파싱용)
EXECUTION_FIELD_NAMES: list[str] = [
    "mksc_shrn_iscd",
    "stck_cntg_hour",
    "stck_prpr",
    "prdy_vrss_sign",
    "prdy_vrss",
    "prdy_ctrt",
    "wghn_avrg_stck_prc",
    "stck_oprc",
    "stck_hgpr",
    "stck_lwpr",
    "askp1",
    "bidp1",
    "cntg_vol",
    "acml_vol",
    "acml_tr_pbmn",
    "seln_cntg_csnu",
    "shnu_cntg_csnu",
    "ntby_cntg_csnu",
    "cttr",
    "seln_cntg_smtn",
    "shnu_cntg_smtn",
    "cntg_cls_code",
    "shnu_rate",
    "prdy_vol_vrss_acml_vol_rate",
    "oprc_hour",
    "oprc_vrss_prpr_sign",
    "oprc_vrss_prpr",
    "hgpr_hour",
    "hgpr_vrss_prpr_sign",
    "hgpr_vrss_prpr",
    "lwpr_hour",
    "lwpr_vrss_prpr_sign",
    "lwpr_vrss_prpr",
    "bsop_date",
    "new_mkop_cls_code",
    "trht_yn",
    "askp_rsqn1",
    "bidp_rsqn1",
    "total_askp_rsqn",
    "total_bidp_rsqn",
    "vol_tnrt",
    "prdy_smns_hour_acml_vol",
    "prdy_smns_hour_acml_vol_rate",
    "hour_cls_code",
    "mrkt_trtm_cls_code",
    "vi_stnd_prc",
]
