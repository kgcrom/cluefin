from pydantic import BaseModel, Field
from typing import List, Optional, Sequence
from cluefin_openapi.kis._model import KisHttpBody


class StockCurrentPriceDetailItem(BaseModel):
    rsym: str = Field(title="실시간조회종목코드", max_length=16)
    pvol: str = Field(title="전일거래량", max_length=14)
    open: str = Field(title="시가", max_length=12)
    high: str = Field(title="고가", max_length=12)
    low: str = Field(title="저가", max_length=12)
    last: str = Field(title="현재가", max_length=12)
    base: str = Field(title="전일종가", max_length=12)
    tomv: str = Field(title="시가총액", max_length=16)
    pamt: str = Field(title="전일거래대금", max_length=14)
    uplp: str = Field(title="상한가", max_length=12)
    dnlp: str = Field(title="하한가", max_length=12)
    h52p: str = Field(title="52주최고가", max_length=12)
    h52d: str = Field(title="52주최고일자", max_length=8)
    l52p: str = Field(title="52주최저가", max_length=12)
    l52d: str = Field(title="52주최저일자", max_length=8)
    perx: str = Field(title="PER", max_length=10)
    pbrx: str = Field(title="PBR", max_length=10)
    epsx: str = Field(title="EPS", max_length=10)
    bpsx: str = Field(title="BPS", max_length=10)
    shar: str = Field(title="상장주수", max_length=16)
    mcap: str = Field(title="자본금", max_length=16)
    curr: str = Field(title="통화", max_length=4)
    zdiv: str = Field(title="소수점자리수", max_length=1)
    vnit: str = Field(title="매매단위", max_length=6)
    t_xprc: str = Field(title="원환산당일가격", max_length=12)
    t_xdif: str = Field(title="원환산당일대비", max_length=12)
    t_xrat: str = Field(title="원환산당일등락", max_length=12)
    p_xprc: str = Field(title="원환산전일가격", max_length=12)
    p_xdif: str = Field(title="원환산전일대비", max_length=12)
    p_xrat: str = Field(title="원환산전일등락", max_length=12)
    t_rate: str = Field(title="당일환율", max_length=12)
    p_rate: str = Field(title="전일환율", max_length=12)
    t_xsgn: str = Field(title="원환산당일기호", max_length=1, description="HTS 색상표시용")
    p_xsng: str = Field(title="원환산전일기호", max_length=1, description="HTS 색상표시용")
    e_ordyn: str = Field(title="거래가능여부", max_length=20)
    e_hogau: str = Field(title="호가단위", max_length=8)
    e_icod: str = Field(title="업종(섹터)", max_length=40)
    e_parp: str = Field(title="액면가", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    tamt: str = Field(title="거래대금", max_length=14)
    etyp_nm: str = Field(title="ETP 분류명", max_length=20)


class StockCurrentPriceDetail(BaseModel, KisHttpBody):
    """해외주식 현재가상세"""

    output: StockCurrentPriceDetailItem = Field(title="응답상세")

class CurrentPriceFirstQuoteItem1(BaseModel):
    rsym: str = Field(title="실시간조회종목코드", max_length=16)
    zdiv: str = Field(title="소수점자리수", max_length=1)
    curr: str = Field(title="통화", max_length=4)
    base: str = Field(title="전일종가", max_length=12)
    open: str = Field(title="시가", max_length=12)
    high: str = Field(title="고가", max_length=12)
    low: str = Field(title="저가", max_length=12)
    last: str = Field(title="현재가", max_length=12)
    dymd: str = Field(title="호가일자", max_length=8)
    dhms: str = Field(title="호가시간", max_length=6)
    bvol: str = Field(title="매수호가총잔량", max_length=10)
    avol: str = Field(title="매도호가총잔량", max_length=10)
    bdvl: str = Field(title="매수호가총잔량대비", max_length=10)
    advl: str = Field(title="매도호가총잔량대비", max_length=10)
    code: str = Field(title="종목코드", max_length=16)
    ropen: str = Field(title="시가율", max_length=12)
    rhigh: str = Field(title="고가율", max_length=12)
    rlow: str = Field(title="저가율", max_length=12)
    rclose: str = Field(title="현재가율", max_length=12)
    
class CurrentPriceFirstQuoteItem2(BaseModel):
    pbid1: str = Field(title="매수호가가격1", max_length=12)
    pask1: str = Field(title="매도호가가격1", max_length=12)
    vbid1: str = Field(title="매수호가잔량1", max_length=10)
    vask1: str = Field(title="매도호가잔량1", max_length=10)
    dbid1: str = Field(title="매수호가대비1", max_length=10)
    dask1: str = Field(title="매도호가대비1", max_length=10)
    
class CurrentPriceFirstQuoteItem3(BaseModel):
    vstm: Optional[str] = Field(title="VCMStart시간", max_length=6, description="데이터 없음")
    vetm: Optional[str] = Field(title="VCMEnd시간", max_length=6, description="데이터 없음")
    csbp: Optional[str] = Field(title="CAS/VCM기준가", max_length=12, description="데이터 없음")
    cshi: Optional[str] = Field(title="CAS/VCMHighprice", max_length=12, description="데이터 없음")
    cslo: Optional[str] = Field(title="CAS/VCMLowprice", max_length=12, description="데이터 없음")
    iep: Optional[str] = Field(title="IEP", max_length=12, description="데이터 없음")
    iev: Optional[str] = Field(title="IEV", max_length=12, description="데이터 없음")


class CurrentPriceFirstQuote(BaseModel, KisHttpBody):
    """해외주식 현재가 1호가"""

    output1: CurrentPriceFirstQuoteItem1 = Field(title="응답상세1")
    # TODO(typo): 문서는 list지만 실제로는 object
    output2: CurrentPriceFirstQuoteItem2 = Field(title="응답상세2")
    output3: CurrentPriceFirstQuoteItem3 = Field(title="응답상세3")

class StockCurrentPriceConclusionItem(BaseModel):
    rsym: str = Field(title="실시간조회종목코드", max_length=16)
    zdiv: str = Field(title="소수점자리수", max_length=1)
    base: str = Field(title="전일종가", max_length=12, description="전일의 종가")
    pvol: str = Field(title="전일거래량", max_length=14, description="전일의 거래량")
    last: str = Field(title="현재가", max_length=12, description="당일 조회시점의 현재 가격")
    sign: str = Field(title="대비기호", max_length=1, description="1 : 상한, 2 : 상승, 3 : 보합, 4 : 하한, 5 : 하락")
    diff: str = Field(title="대비", max_length=12, description="전일 종가와 당일 현재가의 차이 (당일 현재가-전일 종가)")
    rate: str = Field(title="등락율", max_length=12, description="전일 대비 / 당일 현재가 * 100")
    tvol: str = Field(title="거래량", max_length=14, description="당일 조회시점까지 전체 거래량")
    tamt: str = Field(title="거래대금", max_length=14, description="당일 조회시점까지 전체 거래금액")
    ordy: str = Field(title="매수가능여부", max_length=20, description="매수주문 가능 종목 여부")


class StockCurrentPriceConclusion(BaseModel, KisHttpBody):
    """해외주식 현재체결가"""

    output: StockCurrentPriceConclusionItem = Field(title="응답상세")


class ConclusionTrendItem(BaseModel):
    khms: str = Field(title="한국기준시간", max_length=6)
    last: str = Field(title="체결가", max_length=12)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    evol: str = Field(title="체결량", max_length=10)
    tvol: str = Field(title="거래량", max_length=14)
    mtyp: str = Field(title="시장구분", max_length=1, description="0: 장중 1:장전 2:장후")
    pbid: str = Field(title="매수호가", max_length=12)
    pask: str = Field(title="매도호가", max_length=12)
    vpow: str = Field(title="체결강도", max_length=10)


class ConclusionTrend(BaseModel, KisHttpBody):
    """해외주식 체결추이"""

    output1: Sequence[ConclusionTrendItem] = Field(default_factory=list)

class StockMinuteChartItem1(BaseModel):
    rsym: str = Field(title="실시간종목코드", max_length=16)
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stim: str = Field(title="장시작현지시간", max_length=6)
    etim: str = Field(title="장종료현지시간", max_length=6)
    sktm: str = Field(title="장시작한국시간", max_length=6)
    ektm: str = Field(title="장종료한국시간", max_length=6)
    next: str = Field(title="다음가능여부", max_length=1)
    more: str = Field(title="추가데이타여부", max_length=1)
    nrec: str = Field(title="레코드갯수", max_length=4)

class StockMinuteChartItem2(BaseModel):
    tymd: str = Field(title="현지영업일자", max_length=8)
    xymd: str = Field(title="현지기준일자", max_length=8)
    xhms: str = Field(title="현지기준시간", max_length=6)
    kymd: str = Field(title="한국기준일자", max_length=8)
    khms: str = Field(title="한국기준시간", max_length=6)
    open: str = Field(title="시가", max_length=12)
    high: str = Field(title="고가", max_length=12)
    low: str = Field(title="저가", max_length=12)
    last: str = Field(title="종가", max_length=12)
    evol: str = Field(title="체결량", max_length=12)
    eamt: str = Field(title="체결대금", max_length=14)


class StockMinuteChart(BaseModel, KisHttpBody):
    """해외주식분봉조회"""

    output1: StockMinuteChartItem1 = Field(title="응답상세1")
    output2: Sequence[StockMinuteChartItem2] = Field(default_factory=list)


class IndexMinuteChartItem1(BaseModel):
    ovrs_nmix_prdy_vrss: str = Field(title="해외 지수 전일 대비", max_length=114)
    prdy_vrss_sign: str = Field(title="전일 대비 부호", max_length=1)
    hts_kor_isnm: str = Field(title="HTS 한글 종목명", max_length=40)
    prdy_ctrt: str = Field(title="전일 대비율", max_length=82)
    ovrs_nmix_prdy_clpr: str = Field(title="해외 지수 전일 종가", max_length=114)
    acml_vol: str = Field(title="누적 거래량", max_length=18)
    ovrs_nmix_prpr: str = Field(title="해외 지수 현재가", max_length=114)
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드", max_length=9)
    ovrs_prod_oprc: str = Field(title="해외 상품 시가2", max_length=114, description="시가")
    ovrs_prod_hgpr: str = Field(title="해외 상품 최고가", max_length=114, description="최고가")
    ovrs_prod_lwpr: str = Field(title="해외 상품 최저가", max_length=114, description="최저가")

class IndexMinuteChartItem2(BaseModel):
    stck_bsop_date: str = Field(title="주식 영업 일자", max_length=8, description="영업 일자")
    stck_cntg_hour: str = Field(title="주식 체결 시간", max_length=6, description="체결 시간")
    optn_prpr: str = Field(title="옵션 현재가", max_length=112, description="현재가")
    optn_oprc: str = Field(title="옵션 시가2", max_length=112, description="시가")
    optn_hgpr: str = Field(title="옵션 최고가", max_length=112, description="최고가")
    optn_lwpr: str = Field(title="옵션 최저가", max_length=112, description="최저가")
    cntg_vol: str = Field(title="체결 거래량", max_length=18)


class IndexMinuteChart(BaseModel, KisHttpBody):
    """해외지수분봉조회"""

    output1: IndexMinuteChartItem1 = Field(title="응답상세")
    output2: Sequence[IndexMinuteChartItem2] = Field(default_factory=list)

class StockPeriodQuoteItem1(BaseModel):
    rsym: str = Field(title="실시간조회종목코드", max_length=16, description="D+시장구분(3자리)+종목코드 예) DNASAAPL : D+NAS(나스닥)+AAPL(애플) [시장구분] NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 , TSE : 도쿄, HKS : 홍콩, SHS : 상해, SZS : 심천 HSX : 호치민, HNX : 하노이")
    zdiv: str = Field(title="소수점자리수", max_length=1)
    nrec: str = Field(title="전일종가", max_length=12)

class StockPeriodQuoteItem2(BaseModel):
    xymd: str = Field(title="일자(YYYYMMDD)", max_length=8)
    clos: str = Field(title="종가", max_length=12, description="해당 일자의 종가")
    sign: str = Field(title="대비기호", max_length=1, description="1 : 상한, 2 : 상승, 3 : 보합, 4 : 하한, 5 : 하락")
    diff: str = Field(title="대비", max_length=12, description="해당 일자의 종가와 해당 전일 종가의 차이 (해당일 종가-해당 전일 종가)")
    rate: str = Field(title="등락율", max_length=12, description="해당 전일 대비 / 해당일 종가 * 100")
    open: str = Field(title="시가", max_length=12, description="해당일 최초 거래가격")
    high: str = Field(title="고가", max_length=12, description="해당일 가장 높은 거래가격")
    low: str = Field(title="저가", max_length=12, description="해당일 가장 낮은 거래가격")
    tvol: str = Field(title="거래량", max_length=14, description="해당일 거래량")
    tamt: str = Field(title="거래대금", max_length=14, description="해당일 거래대금")
    pbid: Optional[str] = Field(title="매수호가", max_length=12, description="마지막 체결이 발생한 시점의 매수호가. * 해당 일자 거래량 0인 경우 값이 수신되지 않음")
    vbid: Optional[str] = Field(title="매수호가잔량", max_length=10, description="* 해당 일자 거래량 0인 경우 값이 수신되지 않음")
    pask: Optional[str] = Field(title="매도호가", max_length=12, description="마지막 체결이 발생한 시점의 매도호가. * 해당 일자 거래량 0인 경우 값이 수신되지 않음")
    vask: Optional[str] = Field(title="매도호가잔량", max_length=10, description="* 해당 일자 거래량 0인 경우 값이 수신되지 않음")


class StockPeriodQuote(BaseModel, KisHttpBody):
    """해외주식 기간별시세"""

    output1: StockPeriodQuoteItem1 = Field(title="응답상세")
    output2: Sequence[StockPeriodQuoteItem2] = Field(default_factory=list)


class ItemIndexExchangePeriodPriceItem1(BaseModel):
    ovrs_nmix_prdy_vrss: Optional[str] = Field(title="전일 대비", max_length=16, default=None)
    prdy_vrss_sign: Optional[str] = Field(title="전일 대비 부호", max_length=1, default=None)
    prdy_ctrt: Optional[str] = Field(title="전일 대비율", max_length=11, default=None)
    ovrs_nmix_prdy_clpr: Optional[str] = Field(title="전일 종가", max_length=16, default=None)
    acml_vol: Optional[str] = Field(title="누적 거래량", max_length=18, default=None)
    hts_kor_isnm: Optional[str] = Field(title="HTS 한글 종목명", max_length=40, default=None)
    ovrs_nmix_prpr: Optional[str] = Field(title="현재가", max_length=16, default=None)
    stck_shrn_iscd: Optional[str] = Field(title="단축 종목코드", max_length=9, default=None)
    prdy_vol: Optional[str] = Field(title="전일 거래량", max_length=18, default=None)
    ovrs_prod_oprc: Optional[str] = Field(title="시가", max_length=16, default=None)
    ovrs_prod_hgpr: Optional[str] = Field(title="최고가", max_length=16, default=None)
    ovrs_prod_lwpr: Optional[str] = Field(title="최저가", max_length=16, default=None)

class ItemIndexExchangePeriodPriceItem2(BaseModel):
    stck_bsop_date: Optional[str] = Field(title="영업 일자", max_length=8, default=None)
    ovrs_nmix_prpr: Optional[str] = Field(title="현재가", max_length=16, default=None)
    ovrs_nmix_oprc: Optional[str] = Field(title="시가", max_length=16, default=None)
    ovrs_nmix_hgpr: Optional[str] = Field(title="최고가", max_length=16, default=None)
    ovrs_nmix_lwpr: Optional[str] = Field(title="최저가", max_length=16, default=None)
    acml_vol: Optional[str] = Field(title="누적 거래량", max_length=18, default=None)
    mod_yn: Optional[str] = Field(title="변경 여부", max_length=1, default=None)

class ItemIndexExchangePeriodPrice(BaseModel, KisHttpBody):
    """해외주식 종목/지수/환율기간별시세(일/주/월/년)"""

    output1: ItemIndexExchangePeriodPriceItem1 = Field(title="응답상세")
    output2: Sequence[ItemIndexExchangePeriodPriceItem2] = Field(default_factory=list)


class SearchByConditionItem1(BaseModel):
    zdiv: Optional[str] = Field(title="소수점자리수", max_length=1)
    stat: Optional[str] = Field(title="거래상태정보", max_length=20)
    crec: Optional[str] = Field(title="현재조회종목수", max_length=6)
    trec: Optional[str] = Field(title="전체조회종목수", max_length=6)
    nrec: Optional[str] = Field(title="Record Count", max_length=4)
    
class SearchByConditionItem2(BaseModel):
    rsym: Optional[str] = Field(
        title="실시간조회심볼",
        description="실시간조회심볼\n\nD+시장구분(3자리)+종목코드\n예) DNASAAPL : D+NAS(나스닥)+AAPL(애플)\n[시장구분]\nNYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 ,\nTSE : 도쿄, HKS : 홍콩,\nSHS : 상해, SZS : 심천\nHSX : 호치민, HNX : 하노이",
        max_length=32
    )
    excd: Optional[str] = Field(title="거래소코드", max_length=4)
    name: Optional[str] = Field(title="종목명", max_length=48)
    symb: Optional[str] = Field(title="종목코드", max_length=16)
    last: Optional[str] = Field(title="현재가", max_length=12)
    shar: Optional[str] = Field(title="발행주식", description="발행주식수(단위: 천)", max_length=14)
    valx: Optional[str] = Field(title="시가총액", description="시가총액(단위: 천)", max_length=14)
    plow: Optional[str] = Field(title="저가", max_length=12)
    phigh: Optional[str] = Field(title="고가", max_length=12)
    popen: Optional[str] = Field(title="시가", max_length=12)
    tvol: Optional[str] = Field(title="거래량", description="거래량(단위: 주)", max_length=14)
    rate: Optional[str] = Field(title="등락율", description="등락율(%)", max_length=12)
    diff: Optional[str] = Field(title="대비", max_length=12)
    sign: Optional[str] = Field(title="기호", max_length=1)
    avol: Optional[str] = Field(title="거래대금", description="거래대금(단위: 천)", max_length=14)
    eps: Optional[str] = Field(title="EPS", max_length=14)
    per: Optional[str] = Field(title="PER", max_length=14)
    rank: Optional[str] = Field(title="순위", max_length=6)
    ename: Optional[str] = Field(title="영문종목명", max_length=48)
    e_ordyn: Optional[str] = Field(title="매매가능", description="가능 : O", max_length=2)


class SearchByCondition(BaseModel, KisHttpBody):
    """해외주식조건검색"""

    output1: SearchByConditionItem1 = Field(title="응답상세")
    output2: Sequence[SearchByConditionItem2] = Field(default_factory=list)


class SettlementDateItem(BaseModel):
    prdt_type_cd: str = Field(
        title="상품유형코드",
        max_length=3,
        description="512  미국 나스닥 / 513  미국 뉴욕거래소 / 529  미국 아멕스 \n515  일본\n501  홍콩 / 543  홍콩CNY / 558  홍콩USD\n507  베트남 하노이거래소 / 508  베트남 호치민거래소\n551  중국 상해A / 552  중국 심천A"
    )
    tr_natn_cd: str = Field(
        title="거래국가코드",
        max_length=3,
        description="840 미국 / 392 일본 / 344 홍콩 / 704 베트남 / 156 중국"
    )
    tr_natn_name: str = Field(
        title="거래국가명",
        max_length=60
    )
    natn_eng_abrv_cd: str = Field(
        title="국가영문약어코드",
        max_length=2,
        description="US 미국 / JP 일본 / HK 홍콩 / VN 베트남 / CN 중국"
    )
    tr_mket_cd: str = Field(
        title="거래시장코드",
        max_length=2
    )
    tr_mket_name: str = Field(
        title="거래시장명",
        max_length=60
    )
    acpl_sttl_dt: str = Field(
        title="현지결제일자",
        max_length=8,
        description="현지결제일자(YYYYMMDD)"
    )
    dmst_sttl_dt: str = Field(
        title="국내결제일자",
        max_length=8,
        description="국내결제일자(YYYYMMDD)"
    )


class SettlementDate(BaseModel, KisHttpBody):
    """해외결제일자조회"""

    # TODO(typo): 문서는 object지만 실제로는 list
    output: Sequence[SettlementDateItem] = Field(default_factory=list)

class ProductBaseInfoItem(BaseModel):
    std_pdno: str = Field(title="표준상품번호", max_length=12)
    prdt_eng_name: str = Field(title="상품영문명", max_length=60)
    natn_cd: str = Field(title="국가코드", max_length=3)
    natn_name: str = Field(title="국가명", max_length=60)
    tr_mket_cd: str = Field(title="거래시장코드", max_length=2)
    tr_mket_name: str = Field(title="거래시장명", max_length=60)
    ovrs_excg_cd: str = Field(title="해외거래소코드", max_length=4)
    ovrs_excg_name: str = Field(title="해외거래소명", max_length=60)
    tr_crcy_cd: str = Field(title="거래통화코드", max_length=3)
    ovrs_papr: str = Field(title="해외액면가", max_length=195)
    crcy_name: str = Field(title="통화명", max_length=60)
    ovrs_stck_dvsn_cd: str = Field(title="해외주식구분코드", max_length=2)
    prdt_clsf_cd: str = Field(title="상품분류코드", max_length=6)
    prdt_clsf_name: str = Field(title="상품분류명", max_length=60)
    sll_unit_qty: str = Field(title="매도단위수량", max_length=10)
    buy_unit_qty: str = Field(title="매수단위수량", max_length=10)
    tr_unit_amt: str = Field(title="거래단위금액", max_length=238)
    lstg_stck_num: str = Field(title="상장주식수", max_length=19)
    lstg_dt: str = Field(title="상장일자", max_length=8)
    ovrs_stck_tr_stop_dvsn_cd: str = Field(
        title="해외주식거래정지구분코드",
        max_length=2,
        description="※ 해당 값 지연 반영될 수 있는 점 유의 부탁드립니다.\n\n01.정상\n02.거래정지(ALL)\n03.거래중단\n04.매도정지\n05.거래정지(위탁)\n06.매수정지"
    )
    lstg_abol_item_yn: str = Field(title="상장폐지종목여부", max_length=1)
    ovrs_stck_prdt_grp_no: str = Field(title="해외주식상품그룹번호", max_length=20)
    lstg_yn: str = Field(title="상장여부", max_length=1)
    tax_levy_yn: str = Field(title="세금징수여부", max_length=1)
    ovrs_stck_erlm_rosn_cd: str = Field(title="해외주식등록사유코드", max_length=2)
    ovrs_stck_hist_rght_dvsn_cd: str = Field(title="해외주식이력권리구분코드", max_length=2)
    chng_bf_pdno: str = Field(title="변경전상품번호", max_length=12)
    prdt_type_cd_2: str = Field(title="상품유형코드2", max_length=3)
    ovrs_item_name: str = Field(title="해외종목명", max_length=60)
    sedol_no: str = Field(title="SEDOL번호", max_length=15)
    blbg_tckr_text: str = Field(title="블름버그티커내용", max_length=100)
    ovrs_stck_etf_risk_drtp_cd: str = Field(
        title="해외주식ETF위험지표코드",
        max_length=3,
        description="001.ETF\n002.ETN\n003.ETC(Exchage Traded Commodity)\n004.Others(REIT's, Mutual Fund)\n005.VIX Underlying ETF\n006.VIX Underlying ETN"
    )
    etp_chas_erng_rt_dbnb: str = Field(title="ETP추적수익율배수", max_length=236)
    istt_usge_isin_cd: str = Field(title="기관용도ISIN코드", max_length=12)
    mint_svc_yn: str = Field(title="MINT서비스여부", max_length=1)
    mint_svc_yn_chng_dt: str = Field(title="MINT서비스여부변경일자", max_length=8)
    prdt_name: str = Field(title="상품명", max_length=60)
    lei_cd: str = Field(title="LEI코드", max_length=20)
    ovrs_stck_stop_rson_cd: str = Field(
        title="해외주식정지사유코드",
        max_length=2,
        description="01.권리발생\n02.ISIN상이\n03.기타\n04.급등락종목\n05.상장폐지(예정)\n06.종목코드,거래소변경\n07.PTP종목"
    )
    lstg_abol_dt: str = Field(title="상장폐지일자", max_length=8)
    mini_stk_tr_stat_dvsn_cd: str = Field(
        title="미니스탁거래상태구분코드",
        max_length=2,
        description="01.정상\n02.매매 불가\n03.매수 불가\n04.매도 불가"
    )
    mint_frst_svc_erlm_dt: str = Field(title="MINT최초서비스등록일자", max_length=8)
    mint_dcpt_trad_psbl_yn: str = Field(title="MINT소수점매매가능여부", max_length=1)
    mint_fnum_trad_psbl_yn: str = Field(title="MINT정수매매가능여부", max_length=1)
    mint_cblc_cvsn_ipsb_yn: str = Field(title="MINT잔고전환불가여부", max_length=1)
    ptp_item_yn: str = Field(title="PTP종목여부", max_length=1)
    ptp_item_trfx_exmt_yn: str = Field(title="PTP종목양도세면제여부", max_length=1)
    ptp_item_trfx_exmt_strt_dt: str = Field(title="PTP종목양도세면제시작일자", max_length=8)
    ptp_item_trfx_exmt_end_dt: str = Field(title="PTP종목양도세면제종료일자", max_length=8)
    dtm_tr_psbl_yn: str = Field(title="주간거래가능여부", max_length=1)
    sdrf_stop_ecls_yn: str = Field(title="급등락정지제외여부", max_length=1)
    sdrf_stop_ecls_erlm_dt: str = Field(title="급등락정지제외등록일자", max_length=8)
    memo_text1: str = Field(title="메모내용1", max_length=500)
    ovrs_now_pric1: str = Field(title="해외현재가격1", max_length=23)
    last_rcvg_dtime: str = Field(title="최종수신일시", max_length=14)


class ProductBaseInfo(BaseModel, KisHttpBody):
    """해외주식 상품기본정보"""

    output: ProductBaseInfoItem = Field(title="응답상세")


class SectorPriceItem1(BaseModel):
    zdiv: str = Field(title="소수점자리수", max_length=1)
    stat: str = Field(title="거래상태정보", max_length=20)
    crec: str = Field(title="현재조회종목수", max_length=6)
    trec: str = Field(title="전체조회종목수", max_length=6)
    nrec: str = Field(title="RecordCount", max_length=4)

class SectorPriceItem2(BaseModel):
    rsym: str = Field(title="실시간조회심볼", max_length=16)
    excd: str = Field(title="거래소코드", max_length=4)
    symb: str = Field(title="종목코드", max_length=1)
    name: str = Field(title="종목명", max_length=48)
    last: str = Field(title="현재가", max_length=16)
    sign: str = Field(title="기호", max_length=1)
    diff: str = Field(title="대비", max_length=12)
    rate: str = Field(title="등락율", max_length=12)
    tvol: str = Field(title="거래량", max_length=14)
    vask: str = Field(title="매도잔량", max_length=10)
    pask: str = Field(title="매도호가", max_length=12)
    pbid: str = Field(title="매수호가", max_length=12)
    vbid: str = Field(title="매수잔량", max_length=10)
    seqn: str = Field(title="순위", max_length=6)
    ename: str = Field(title="영문종목명", max_length=48)
    e_ordyn: str = Field(title="매매가능", max_length=2)

class SectorPrice(BaseModel, KisHttpBody):
    """해외주식 업종별시세"""

    output1: SectorPriceItem1 = Field(title="응답상세")
    output2: Sequence[SectorPriceItem2] = Field(default_factory=list)


class SectorCodesItem1(BaseModel):
    nrec: str = Field(title="RecordCount", max_length=4)

class SectorCodesItem2(BaseModel):
    icod: str = Field(title="업종코드", max_length=4)
    name: str = Field(title="업종명", max_length=32)


class SectorCodes(BaseModel, KisHttpBody):
    """해외주식 업종별코드조회"""

    output1: SectorCodesItem1 = Field(title="응답상세")
    output2: Sequence[SectorCodesItem2] = Field(default_factory=list)
