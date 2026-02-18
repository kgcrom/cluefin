from typing import Optional, Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class OnmarketBondAskingPriceItem(BaseModel):
    """장내채권현재가(호가) 응답 항목"""

    aspr_acpt_hour: str = Field(title="호가 접수 시간", max_length=6)
    bond_askp1: str = Field(title="채권 매도호가1", max_length=20)
    bond_askp2: str = Field(title="채권 매도호가2", max_length=20)
    bond_askp3: str = Field(title="채권 매도호가3", max_length=20)
    bond_askp4: str = Field(title="채권 매도호가4", max_length=20)
    bond_askp5: str = Field(title="채권 매도호가5", max_length=20)
    bond_bidp1: str = Field(title="채권 매수호가1", max_length=20)
    bond_bidp2: str = Field(title="채권 매수호가2", max_length=20)
    bond_bidp3: str = Field(title="채권 매수호가3", max_length=20)
    bond_bidp4: str = Field(title="채권 매수호가4", max_length=20)
    bond_bidp5: str = Field(title="채권 매수호가5", max_length=20)
    askp_rsqn1: str = Field(title="매도호가 잔량1", max_length=12)
    askp_rsqn2: str = Field(title="매도호가 잔량2", max_length=12)
    askp_rsqn3: str = Field(title="매도호가 잔량3", max_length=12)
    askp_rsqn4: str = Field(title="매도호가 잔량4", max_length=12)
    askp_rsqn5: str = Field(title="매도호가 잔량5", max_length=12)
    bidp_rsqn1: str = Field(title="매수호가 잔량1", max_length=12)
    bidp_rsqn2: str = Field(title="매수호가 잔량2", max_length=12)
    bidp_rsqn3: str = Field(title="매수호가 잔량3", max_length=12)
    bidp_rsqn4: str = Field(title="매수호가 잔량4", max_length=12)
    bidp_rsqn5: str = Field(title="매수호가 잔량5", max_length=12)
    total_askp_rsqn: str = Field(title="총 매도호가 잔량", max_length=12)
    total_bidp_rsqn: str = Field(title="총 매수호가 잔량", max_length=12)
    ntby_aspr_rsqn: str = Field(title="순매수 호가 잔량", max_length=12)
    seln_ernn_rate1: str = Field(title="매도 수익비율1", max_length=15)
    seln_ernn_rate2: str = Field(title="매도 수익비율2", max_length=15)
    seln_ernn_rate3: str = Field(title="매도 수익비율3", max_length=15)
    seln_ernn_rate4: str = Field(title="매도 수익비율4", max_length=15)
    seln_ernn_rate5: str = Field(title="매도 수익비율5", max_length=15)
    shnu_ernn_rate1: str = Field(title="매수 수익비율1", max_length=15)
    shnu_ernn_rate2: str = Field(title="매수 수익비율2", max_length=15)
    shnu_ernn_rate3: str = Field(title="매수 수익비율3", max_length=15)
    shnu_ernn_rate4: str = Field(title="매수 수익비율4", max_length=15)
    shnu_ernn_rate5: str = Field(title="매수 수익비율5", max_length=15)


class OnmarketBondAskingPrice(BaseModel, KisHttpBody):
    """장내채권현재가(호가)"""

    output: Optional[OnmarketBondAskingPriceItem] = Field(default=None, title="응답상세")


class OnmarketBondPriceItem(BaseModel):
    """장내채권현재가(시세) 응답 항목"""

    stnd_iscd: str = Field(title="표준종목코드", max_length=12)
    hts_kor_isnm: str = Field(title="HTS한글종목명", max_length=40)
    bond_prpr: str = Field(title="채권현재가", max_length=112)
    prdy_vrss_sign: str = Field(title="전일대비부호", max_length=1)
    bond_prdy_vrss: str = Field(title="채권전일대비", max_length=112)
    prdy_ctrt: str = Field(title="전일대비율", max_length=82)
    acml_vol: str = Field(title="누적거래량", max_length=18)
    bond_prdy_clpr: str = Field(title="채권전일종가", max_length=112)
    bond_oprc: str = Field(title="채권시가2", max_length=112)
    bond_hgpr: str = Field(title="채권고가", max_length=112)
    bond_lwpr: str = Field(title="채권저가", max_length=112)
    ernn_rate: str = Field(title="수익비율", max_length=84)
    oprc_ert: str = Field(title="시가2수익률", max_length=72)
    hgpr_ert: str = Field(title="최고가수익률", max_length=72)
    lwpr_ert: str = Field(title="최저가수익률", max_length=72)
    bond_mxpr: str = Field(title="채권상한가", max_length=112)
    bond_llam: str = Field(title="채권하한가", max_length=112)


class OnmarketBondPrice(BaseModel, KisHttpBody):
    """장내채권현재가(시세)"""

    output: Optional[OnmarketBondPriceItem] = Field(default=None, title="응답상세")


class OnmarketBondExecutionItem(BaseModel):
    """장내채권현재가(체결) 응답 항목"""

    stck_cntg_hour: str = Field(title="주식 체결 시간", max_length=6)
    bond_prpr: str = Field(title="채권 현재가", max_length=112)
    bond_prdy_vrss: str = Field(title="채권 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    cntg_vol: str = Field(title="체결 거래량", max_length=18)
    acml_vol: str = Field(title="누적 거래량", max_length=18)


class OnmarketBondExecution(BaseModel, KisHttpBody):
    """장내채권현재가(체결)"""

    output: Optional[OnmarketBondExecutionItem] = Field(default=None, title="응답상세")


class OnmarketBondDailyPriceItem(BaseModel):
    """장내채권현재가(일별) 응답 항목"""

    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8)
    bond_prpr: str = Field(title="채권 현재가", max_length=112)
    bond_prdy_vrss: str = Field(title="채권 전일 대비", max_length=112)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    bond_oprc: str = Field(title="채권 시가", max_length=112)
    bond_hgpr: str = Field(title="채권 고가", max_length=112)
    bond_lwpr: str = Field(title="채권 저가", max_length=112)


class OnmarketBondDailyPrice(BaseModel, KisHttpBody):
    """장내채권현재가(일별)"""

    output: Sequence[OnmarketBondDailyPriceItem] = Field(default_factory=list)


class OnmarketBondDailyChartPriceItem(BaseModel):
    """장내채권 기간별시세(일) 응답 항목"""

    stck_bsop_date: str = Field(title="주식영업일자", max_length=8)
    bond_oprc: str = Field(title="채권시가2", max_length=112)
    bond_hgpr: str = Field(title="채권고가", max_length=112)
    bond_lwpr: str = Field(title="채권저가", max_length=112)
    bond_prpr: str = Field(title="채권현재가", max_length=112)
    acml_vol: str = Field(title="누적거래량", max_length=18)


class OnmarketBondDailyChartPrice(BaseModel, KisHttpBody):
    """장내채권 기간별시세(일)"""

    output: list[OnmarketBondDailyChartPriceItem] = Field(default_factory=list, title="응답상세")


class OnmarketBondAvgUnitPriceOutput1Item(BaseModel):
    """장내채권 평균단가조회 output1 항목 (단가/수익율)"""

    evlu_dt: str = Field(title="평가일자", max_length=8)
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    prdt_name: str = Field(title="상품명", max_length=60)
    kis_unpr: str = Field(title="KIS단가", max_length=24)
    kbp_unpr: str = Field(title="KBP단가", max_length=24)
    nice_evlu_unpr: str = Field(title="NICE평가단가", max_length=24)
    fnp_unpr: str = Field(title="FnP단가", max_length=24)
    avg_evlu_unpr: str = Field(title="평균평가단가", max_length=24)
    kis_crdt_grad_text: str = Field(title="KIS신용등급텍스트", max_length=40)
    kbp_crdt_grad_text: str = Field(title="KBP신용등급텍스트", max_length=40)
    nice_crdt_grad_text: str = Field(title="NICE신용등급텍스트", max_length=40)
    fnp_crdt_grad_text: str = Field(title="FnP신용등급텍스트", max_length=40)
    chng_yn: str = Field(title="변경여부", max_length=1)
    kis_erng_rt: str = Field(title="KIS수익률", max_length=24)
    kbp_erng_rt: str = Field(title="KBP수익률", max_length=24)
    nice_evlu_erng_rt: str = Field(title="NICE평가수익률", max_length=24)
    fnp_erng_rt: str = Field(title="FnP수익률", max_length=24)
    avg_evlu_erng_rt: str = Field(title="평균평가수익률", max_length=24)
    kis_rf_unpr: str = Field(title="KIS기준단가", max_length=24)
    kbp_rf_unpr: str = Field(title="KBP기준단가", max_length=24)
    nice_evlu_rf_unpr: str = Field(title="NICE평가기준단가", max_length=24)
    avg_evlu_rf_unpr: str = Field(title="평균평가기준단가", max_length=24)


class OnmarketBondAvgUnitPriceOutput2Item(BaseModel):
    """장내채권 평균단가조회 output2 항목 (평가금액)"""

    evlu_dt: str = Field(title="평가일자", max_length=8)
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    prdt_name: str = Field(title="상품명", max_length=60)
    kis_evlu_amt: str = Field(title="KIS평가금액", max_length=24)
    kbp_evlu_amt: str = Field(title="KBP평가금액", max_length=24)
    nice_evlu_amt: str = Field(title="NICE평가금액", max_length=24)
    fnp_evlu_amt: str = Field(title="FnP평가금액", max_length=24)
    avg_evlu_amt: str = Field(title="평균평가금액", max_length=24)
    chng_yn: str = Field(title="변경여부", max_length=1)


class OnmarketBondAvgUnitPriceOutput3Item(BaseModel):
    """장내채권 평균단가조회 output3 항목 (외화평가)"""

    evlu_dt: str = Field(title="평가일자", max_length=8)
    pdno: str = Field(title="상품번호", max_length=12)
    prdt_type_cd: str = Field(title="상품유형코드", max_length=3)
    prdt_name: str = Field(title="상품명", max_length=60)
    kis_crcy_cd: str = Field(title="KIS통화코드", max_length=3)
    kis_evlu_unit_pric: str = Field(title="KIS평가단위가격", max_length=24)
    kis_evlu_pric: str = Field(title="KIS평가가격", max_length=24)
    kbp_crcy_cd: str = Field(title="KBP통화코드", max_length=3)
    kbp_evlu_unit_pric: str = Field(title="KBP평가단위가격", max_length=24)
    kbp_evlu_pric: str = Field(title="KBP평가가격", max_length=24)
    nice_crcy_cd: str = Field(title="NICE통화코드", max_length=3)
    nice_evlu_unit_pric: str = Field(title="NICE평가단위가격", max_length=24)
    nice_evlu_pric: str = Field(title="NICE평가가격", max_length=24)
    avg_evlu_unit_pric: str = Field(title="평균평가단위가격", max_length=24)
    avg_evlu_pric: str = Field(title="평균평가가격", max_length=24)
    chng_yn: str = Field(title="변경여부", max_length=1)


class OnmarketBondAvgUnitPrice(BaseModel, KisHttpBody):
    """장내채권 평균단가조회"""

    output1: list[OnmarketBondAvgUnitPriceOutput1Item] = Field(default_factory=list, title="단가/수익율")
    output2: list[OnmarketBondAvgUnitPriceOutput2Item] = Field(default_factory=list, title="평가금액")
    output3: list[OnmarketBondAvgUnitPriceOutput3Item] = Field(default_factory=list, title="외화평가")
