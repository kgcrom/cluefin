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


class DomesticRealtimeExecutionNotificationItem(BaseModel):
    """국내주식 실시간체결통보 - H0STCNI0(실전)/H0STCNI9(모의).

    WebSocket 메시지의 데이터 부분을 파싱한 모델입니다.
    데이터는 "^" 구분자로 26개 필드가 구분되어 전달됩니다.
    """

    cust_id: str = Field(title="고객 ID")
    acnt_no: str = Field(title="계좌번호")
    oder_no: str = Field(title="주문번호")
    ooder_no: str = Field(title="원주문번호")
    seln_byov_cls: str = Field(title="매도매수구분")  # 01:매도, 02:매수
    rctf_cls: str = Field(title="정정구분")  # 0:정상, 1:정정, 2:취소
    oder_kind: str = Field(title="주문종류")
    oder_cond: str = Field(title="주문조건")  # 0:없음, 1:IOC, 2:FOK
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드")
    cntg_qty: str = Field(title="체결 수량")
    cntg_unpr: str = Field(title="체결단가")
    stck_cntg_hour: str = Field(title="주식 체결 시간")
    rfus_yn: str = Field(title="거부여부")  # 0:승인, 1:거부
    cntg_yn: str = Field(title="체결여부")  # 1:주문/정정/취소/거부, 2:체결
    acpt_yn: str = Field(title="접수여부")  # 1:주문접수, 2:확인, 3:취소(FOK/IOC)
    brnc_no: str = Field(title="지점번호")
    oder_qty: str = Field(title="주문수량")
    acnt_name: str = Field(title="계좌명")
    ord_cond_prc: str = Field(title="호가조건가격")  # 스톱지정가 시 표시
    ord_exg_gb: str = Field(title="주문거래소 구분")  # 1:KRX, 2:NXT, 3:SOR-KRX, 4:SOR-NXT
    popup_yn: str = Field(title="실시간체결창 표시여부")  # Y/N
    filler: str = Field(title="필러")
    crdt_cls: str = Field(title="신용구분")
    crdt_loan_date: str = Field(title="신용대출일자")
    cntg_isnm40: str = Field(title="체결종목명")
    oder_prc: str = Field(title="주문가격")


class DomesticRealtimeOrderbookItem(BaseModel):
    """국내주식 실시간호가 (KRX) - H0STASP0.

    WebSocket 메시지의 데이터 부분을 파싱한 모델입니다.
    데이터는 "^" 구분자로 59개 필드가 구분되어 전달됩니다.
    """

    mksc_shrn_iscd: str = Field(title="유가증권 단축 종목코드")
    bsop_hour: str = Field(title="영업 시간")
    hour_cls_code: str = Field(title="시간 구분 코드")
    askp1: str = Field(title="매도호가1")
    askp2: str = Field(title="매도호가2")
    askp3: str = Field(title="매도호가3")
    askp4: str = Field(title="매도호가4")
    askp5: str = Field(title="매도호가5")
    askp6: str = Field(title="매도호가6")
    askp7: str = Field(title="매도호가7")
    askp8: str = Field(title="매도호가8")
    askp9: str = Field(title="매도호가9")
    askp10: str = Field(title="매도호가10")
    bidp1: str = Field(title="매수호가1")
    bidp2: str = Field(title="매수호가2")
    bidp3: str = Field(title="매수호가3")
    bidp4: str = Field(title="매수호가4")
    bidp5: str = Field(title="매수호가5")
    bidp6: str = Field(title="매수호가6")
    bidp7: str = Field(title="매수호가7")
    bidp8: str = Field(title="매수호가8")
    bidp9: str = Field(title="매수호가9")
    bidp10: str = Field(title="매수호가10")
    askp_rsqn1: str = Field(title="매도호가 잔량1")
    askp_rsqn2: str = Field(title="매도호가 잔량2")
    askp_rsqn3: str = Field(title="매도호가 잔량3")
    askp_rsqn4: str = Field(title="매도호가 잔량4")
    askp_rsqn5: str = Field(title="매도호가 잔량5")
    askp_rsqn6: str = Field(title="매도호가 잔량6")
    askp_rsqn7: str = Field(title="매도호가 잔량7")
    askp_rsqn8: str = Field(title="매도호가 잔량8")
    askp_rsqn9: str = Field(title="매도호가 잔량9")
    askp_rsqn10: str = Field(title="매도호가 잔량10")
    bidp_rsqn1: str = Field(title="매수호가 잔량1")
    bidp_rsqn2: str = Field(title="매수호가 잔량2")
    bidp_rsqn3: str = Field(title="매수호가 잔량3")
    bidp_rsqn4: str = Field(title="매수호가 잔량4")
    bidp_rsqn5: str = Field(title="매수호가 잔량5")
    bidp_rsqn6: str = Field(title="매수호가 잔량6")
    bidp_rsqn7: str = Field(title="매수호가 잔량7")
    bidp_rsqn8: str = Field(title="매수호가 잔량8")
    bidp_rsqn9: str = Field(title="매수호가 잔량9")
    bidp_rsqn10: str = Field(title="매수호가 잔량10")
    total_askp_rsqn: str = Field(title="총 매도호가 잔량")
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량")
    ovtm_total_askp_rsqn: str = Field(title="시간외 총 매도호가 잔량")
    ovtm_total_bidp_rsqn: str = Field(title="시간외 총 매수호가 잔량")
    antc_cnpr: str = Field(title="예상 체결가")
    antc_cnqn: str = Field(title="예상 체결량")
    antc_vol: str = Field(title="예상 거래량")
    antc_cntg_vrss: str = Field(title="예상 체결 대비")
    antc_cntg_vrss_sign: str = Field(title="예상 체결 대비 부호")
    antc_cntg_prdy_ctrt: str = Field(title="예상 체결 전일 대비율")
    acml_vol: str = Field(title="누적 거래량")
    total_askp_rsqn_icdc: str = Field(title="총 매도호가 잔량 증감")
    total_bidp_rsqn_icdc: str = Field(title="총 매수호가 잔량 증감")
    ovtm_total_askp_icdc: str = Field(title="시간외 총 매도호가 증감")
    ovtm_total_bidp_icdc: str = Field(title="시간외 총 매수호가 증감")
    stck_deal_cls_code: str = Field(title="주식 매매 구분 코드")


# 필드 순서 리스트 (WebSocket 데이터 파싱용) - 체결가
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

# 필드 순서 리스트 (WebSocket 데이터 파싱용) - 호가
ORDERBOOK_FIELD_NAMES: list[str] = [
    "mksc_shrn_iscd",
    "bsop_hour",
    "hour_cls_code",
    "askp1",
    "askp2",
    "askp3",
    "askp4",
    "askp5",
    "askp6",
    "askp7",
    "askp8",
    "askp9",
    "askp10",
    "bidp1",
    "bidp2",
    "bidp3",
    "bidp4",
    "bidp5",
    "bidp6",
    "bidp7",
    "bidp8",
    "bidp9",
    "bidp10",
    "askp_rsqn1",
    "askp_rsqn2",
    "askp_rsqn3",
    "askp_rsqn4",
    "askp_rsqn5",
    "askp_rsqn6",
    "askp_rsqn7",
    "askp_rsqn8",
    "askp_rsqn9",
    "askp_rsqn10",
    "bidp_rsqn1",
    "bidp_rsqn2",
    "bidp_rsqn3",
    "bidp_rsqn4",
    "bidp_rsqn5",
    "bidp_rsqn6",
    "bidp_rsqn7",
    "bidp_rsqn8",
    "bidp_rsqn9",
    "bidp_rsqn10",
    "total_askp_rsqn",
    "total_bidp_rsqn",
    "ovtm_total_askp_rsqn",
    "ovtm_total_bidp_rsqn",
    "antc_cnpr",
    "antc_cnqn",
    "antc_vol",
    "antc_cntg_vrss",
    "antc_cntg_vrss_sign",
    "antc_cntg_prdy_ctrt",
    "acml_vol",
    "total_askp_rsqn_icdc",
    "total_bidp_rsqn_icdc",
    "ovtm_total_askp_icdc",
    "ovtm_total_bidp_icdc",
    "stck_deal_cls_code",
]

# 필드 순서 리스트 (WebSocket 데이터 파싱용) - 실시간체결통보
EXECUTION_NOTIFICATION_FIELD_NAMES: list[str] = [
    "cust_id",
    "acnt_no",
    "oder_no",
    "ooder_no",
    "seln_byov_cls",
    "rctf_cls",
    "oder_kind",
    "oder_cond",
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
    "ord_cond_prc",
    "ord_exg_gb",
    "popup_yn",
    "filler",
    "crdt_cls",
    "crdt_loan_date",
    "cntg_isnm40",
    "oder_prc",
]
