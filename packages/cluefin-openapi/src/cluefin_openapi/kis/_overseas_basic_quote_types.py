from pydantic import BaseModel, Field
from typing import List, Optional, Sequence
from cluefin_openapi.kis._model import KisHttpBody


rsym	실시간조회종목코드	string	Y	16	 
pvol	전일거래량	string	Y	14	 
open	시가	string	Y	12	 
high	고가	string	Y	12	 
low	저가	string	Y	12	 
last	현재가	string	Y	12	 
base	전일종가	string	Y	12	 
tomv	시가총액	string	Y	16	 
pamt	전일거래대금	string	Y	14	 
uplp	상한가	string	Y	12	 
dnlp	하한가	string	Y	12	 
h52p	52주최고가	string	Y	12	 
h52d	52주최고일자	string	Y	8	 
l52p	52주최저가	string	Y	12	 
l52d	52주최저일자	string	Y	8	 
perx	PER	string	Y	10	 
pbrx	PBR	string	Y	10	 
epsx	EPS	string	Y	10	 
bpsx	BPS	string	Y	10	 
shar	상장주수	string	Y	16	 
mcap	자본금	string	Y	16	 
curr	통화	string	Y	4	 
zdiv	소수점자리수	string	Y	1	 
vnit	매매단위	string	Y	6	 
t_xprc	원환산당일가격	string	Y	12	 
t_xdif	원환산당일대비	string	Y	12	 
t_xrat	원환산당일등락	string	Y	12	 
p_xprc	원환산전일가격	string	Y	12	 
p_xdif	원환산전일대비	string	Y	12	 
p_xrat	원환산전일등락	string	Y	12	 
t_rate	당일환율	string	Y	12	 
p_rate	전일환율	string	Y	12	 
t_xsgn	원환산당일기호	string	Y	1	HTS 색상표시용
p_xsng	원환산전일기호	string	Y	1	HTS 색상표시용
e_ordyn	거래가능여부	string	Y	20	 
e_hogau	호가단위	string	Y	8	 
e_icod	업종(섹터)	string	Y	40	 
e_parp	액면가	string	Y	12	 
tvol	거래량	string	Y	14	 
tamt	거래대금	string	Y	14	 
etyp_nm	ETP 분류명	string	Y	20	 
class StockCurrentPriceDetailItem(BaseModel):
    pass


class StockCurrentPriceDetail(BaseModel, KisHttpBody):
    """해외주식 현재가상세"""

    output: StockCurrentPriceDetailItem = Field(title="응답상세")

rsym	실시간조회종목코드	string	Y	16	 
zdiv	소수점자리수	string	Y	1	 
curr	통화	string	Y	4	 
base	전일종가	string	Y	12	 
open	시가	string	Y	12	 
high	고가	string	Y	12	 
low	저가	string	Y	12	 
last	현재가	string	Y	12	 
dymd	호가일자	string	Y	8	 
dhms	호가시간	string	Y	6	 
bvol	매수호가총잔량	string	Y	10	 
avol	매도호가총잔량	string	Y	10	 
bdvl	매수호가총잔량대비	string	Y	10	 
advl	매도호가총잔량대비	string	Y	10	 
code	종목코드	string	Y	16	 
ropen	시가율	string	Y	12	 
rhigh	고가율	string	Y	12	 
rlow	저가율	string	Y	12	 
rclose	현재가율	string	Y	12	 
output2	응답상세	array	Y	100	 
pbid1	매수호가가격1	string	Y	12	 
pask1	매도호가가격1	string	Y	12	 
vbid1	매수호가잔량1	string	Y	10	 
vask1	매도호가잔량1	string	Y	10	 
dbid1	매수호가대비1	string	Y	10	 
dask1	매도호가대비1	string	Y	10	 
output3	응답상세	object array	Y	100	 
vstm	VCMStart시간	string	Y	6	데이터 없음
vetm	VCMEnd시간	string	Y	6	데이터 없음
csbp	CAS/VCM기준가	string	Y	12	데이터 없음
cshi	CAS/VCMHighprice	string	Y	12	데이터 없음
cslo	CAS/VCMLowprice	string	Y	12	데이터 없음
iep	IEP	string	Y	12	데이터 없음
iev	IEV	string	Y	12	데이터 없음
class CurrentPriceFirstQuoteItem(BaseModel):
    pass


class CurrentPriceFirstQuote(BaseModel, KisHttpBody):
    """해외주식 현재가 1호가"""

    output: CurrentPriceFirstQuoteItem = Field(title="응답상세")

rsym	실시간조회종목코드	string	Y	16	<description>D+시장구분(3자리)+종목코드
예) DNASAAPL : D+NAS(나스닥)+AAPL(애플)
[시장구분]
NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 ,
TSE : 도쿄, HKS : 홍콩,
SHS : 상해, SZS : 심천
HSX : 호치민, HNX : 하노이</description>
zdiv	소수점자리수	string	Y	1	
base	전일종가	string	Y	12	전일의 종가
pvol	전일거래량	string	Y	14	전일의 거래량
last	현재가	string	Y	12	당일 조회시점의 현재 가격
sign	대비기호	string	Y	1	1 : 상한, 2 : 상승, 3 : 보합, 4 : 하한, 5 : 하락
diff	대비	string	Y	12	전일 종가와 당일 현재가의 차이 (당일 현재가-전일 종가)
rate	등락율	string	Y	12	전일 대비 / 당일 현재가 * 100
tvol	거래량	string	Y	14	당일 조회시점까지 전체 거래량
tamt	거래대금	string	Y	14	당일 조회시점까지 전체 거래금액
ordy	매수가능여부	string	Y	20	매수주문 가능 종목 여부
class StockCurrentPriceConclusionItem(BaseModel):
    pass


class StockCurrentPriceConclusion(BaseModel, KisHttpBody):
    """해외주식 현재체결가"""

    output: StockCurrentPriceConclusionItem = Field(title="응답상세")


khms	한국기준시간	string	Y	6	 
last	체결가	string	Y	12	
sign	기호	string	Y	1	
diff	대비	string	Y	12	
rate	등락율	string	Y	12	
evol	체결량	string	Y	10	
tvol	거래량	string	Y	14	 
mtyp	시장구분	string	Y	1	 0: 장중 1:장전 2:장후
pbid	매수호가	string	Y	12	 
pask	매도호가	string	Y	12	 
vpow	체결강도	string	Y	10	 
class ConclusionTrendItem(BaseModel):
    pass


class ConclusionTrend(BaseModel, KisHttpBody):
    """해외주식 체결추이"""

    output1: Sequence[ConclusionTrendItem] = Field(default_factory=list)

rsym	실시간종목코드	string	Y	16	 
zdiv	소수점자리수	string	Y	1	 
stim	장시작현지시간	string	Y	6	 
etim	장종료현지시간	string	Y	6	 
sktm	장시작한국시간	string	Y	6	 
ektm	장종료한국시간	string	Y	6	 
next	다음가능여부	string	Y	1	 
more	추가데이타여부	string	Y	1	 
nrec	레코드갯수	string	Y	4	 
class StockMinuteChartItem1(BaseModel):
    pass

tymd	현지영업일자	string	Y	8
xymd	현지기준일자	string	Y	8
xhms	현지기준시간	string	Y	6
kymd	한국기준일자	string	Y	8
khms	한국기준시간	string	Y	6
open	시가	string	Y	12
high	고가	string	Y	12
low	저가	string	Y	12
last	종가	string	Y	12
evol	체결량	string	Y	12
eamt	체결대금	string	Y	14
class StockMinuteChartItem2(BaseModel):
    pass


class StockMinuteChart(BaseModel, KisHttpBody):
    """해외주식분봉조회"""

    output1: Sequence[StockMinuteChartItem1] = Field(default_factory=list)
    output2: StockMinuteChartItem2 = Field(title="응답상세")


ovrs_nmix_prdy_vrss	해외 지수 전일 대비	string	Y	114	 
prdy_vrss_sign	전일 대비 부호	string	Y	1	 
hts_kor_isnm	HTS 한글 종목명	string	Y	40	 
prdy_ctrt	전일 대비율	string	Y	82	 
ovrs_nmix_prdy_clpr	해외 지수 전일 종가	string	Y	114	 
acml_vol	누적 거래량	string	Y	18	 
ovrs_nmix_prpr	해외 지수 현재가	string	Y	114	 
stck_shrn_iscd	주식 단축 종목코드	string	Y	9	 
ovrs_prod_oprc	해외 상품 시가2	string	Y	114	 시가
ovrs_prod_hgpr	해외 상품 최고가	string	Y	114	 최고가
ovrs_prod_lwpr	해외 상품 최저가	string	Y	114	 최저가
class IndexMinuteChartItem1(BaseModel):
    pass

stck_bsop_date	주식 영업 일자	string	Y	8	 영업 일자
stck_cntg_hour	주식 체결 시간	string	Y	6	 체결 시간
optn_prpr	옵션 현재가	string	Y	112	 현재가
optn_oprc	옵션 시가2	string	Y	112	 시가
optn_hgpr	옵션 최고가	string	Y	112	 최고가
optn_lwpr	옵션 최저가	string	Y	112	 최저가
cntg_vol	체결 거래량	string	Y	18	 
class IndexMinuteChartItem2(BaseModel):
    pass


class IndexMinuteChart(BaseModel, KisHttpBody):
    """해외지수분봉조회"""

    output1: IndexMinuteChartItem1 = Field(title="응답상세")
    output2: Sequence[IndexMinuteChartItem2] = Field(default_factory=list)

rsym	실시간조회종목코드	string	Y	16	<description>D+시장구분(3자리)+종목코드
예) DNASAAPL : D+NAS(나스닥)+AAPL(애플)
[시장구분]
NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 ,
TSE : 도쿄, HKS : 홍콩,
SHS : 상해, SZS : 심천
HSX : 호치민, HNX : 하노이</description>
zdiv	소수점자리수	string	Y	1	
nrec	전일종가	string	Y	12	
class StockPeriodQuoteItem1(BaseModel):
    pass

xymd	일자(YYYYMMDD)	string	Y	8	 
clos	종가	string	Y	12	해당 일자의 종가
sign	대비기호	string	Y	1	1 : 상한, 2 : 상승, 3 : 보합, 4 : 하한, 5 : 하락
diff	대비	string	Y	12	해당 일자의 종가와 해당 전일 종가의 차이 (해당일 종가-해당 전일 종가)
rate	등락율	string	Y	12	해당 전일 대비 / 해당일 종가 * 100
open	시가	string	Y	12	해당일 최초 거래가격
high	고가	string	Y	12	해당일 가장 높은 거래가격
low	저가	string	Y	12	해당일 가장 낮은 거래가격
tvol	거래량	string	Y	14	해당일 거래량
tamt	거래대금	string	Y	14	해당일 거래대금
pbid	매수호가	string	Y	12	마지막 체결이 발생한 시점의 매수호가. * 해당 일자 거래량 0인 경우 값이 수신되지 않음
vbid	매수호가잔량	string	Y	10	* 해당 일자 거래량 0인 경우 값이 수신되지 않음
pask	매도호가	string	Y	12	마지막 체결이 발생한 시점의 매도호가. * 해당 일자 거래량 0인 경우 값이 수신되지 않음
vask	매도호가잔량	string	Y	10	* 해당 일자 거래량 0인 경우 값이 수신되지 않음
class StockPeriodQuoteItem2(BaseModel):
    pass


class StockPeriodQuote(BaseModel, KisHttpBody):
    """해외주식 기간별시세"""

    output1: StockPeriodQuoteItem1 = Field(title="응답상세")
    output2: Sequence[StockPeriodQuoteItem2] = Field(default_factory=list)


ovrs_nmix_prdy_vrss	 전일 대비	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
prdy_vrss_sign	전일 대비 부호	string	N	1	 
prdy_ctrt	전일 대비율	string	N	11	11(8.2) 정수부분 8자리, 소수부분 2자리
ovrs_nmix_prdy_clpr	전일 종가	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
acml_vol	누적 거래량	string	N	18	 
hts_kor_isnm	HTS 한글 종목명	string	N	40	 
ovrs_nmix_prpr	현재가	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
stck_shrn_iscd	단축 종목코드	string	N	9	 
prdy_vol	전일 거래량	string	N	18	 
ovrs_prod_oprc	시가	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
ovrs_prod_hgpr	최고가	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
ovrs_prod_lwpr	최저가	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
class ItemIndexExchangePeriodPriceItem1(BaseModel):
    pass

stck_bsop_date	영업 일자	string	N	8	 
ovrs_nmix_prpr	현재가	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
ovrs_nmix_oprc	시가	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
ovrs_nmix_hgpr	최고가	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
ovrs_nmix_lwpr	최저가	string	N	16	16(11.4) 정수부분 11자리, 소수부분 4자리
acml_vol	누적 거래량	string	N	18	 
mod_yn	변경 여부	string	N	1	 
class ItemIndexExchangePeriodPriceItem2(BaseModel):
    pass

class ItemIndexExchangePeriodPrice(BaseModel, KisHttpBody):
    """해외주식 종목/지수/환율기간별시세(일/주/월/년)"""

    output1: ItemIndexExchangePeriodPriceItem1 = Field(title="응답상세")
    output2: Sequence[ItemIndexExchangePeriodPriceItem2] = Field(default_factory=list)


zdiv	소수점자리수	string	Y	1	소수점자리수
stat	거래상태정보	string	Y	20	거래상태정보
crec	현재조회종목수	string	Y	6	현재조회종목수
trec	전체조회종목수	string	Y	6	전체조회종목수
nrec	Record Count	string	Y	4	Record Count
class SearchByConditionItem1(BaseModel):
    pass    

rsym	실시간조회심볼	string	N	32	<description>실시간조회심볼

D+시장구분(3자리)+종목코드
예) DNASAAPL : D+NAS(나스닥)+AAPL(애플)
[시장구분]
NYS : 뉴욕, NAS : 나스닥, AMS : 아멕스 ,
TSE : 도쿄, HKS : 홍콩,
SHS : 상해, SZS : 심천
HSX : 호치민, HNX : 하노이</description>
excd	거래소코드	string	N	4	거래소코드
name	종목명	string	N	48	종목명
symb	종목코드	string	N	16	종목코드
last	현재가	string	N	12	현재가
shar	발행주식	string	N	14	발행주식수(단위: 천)
valx	시가총액	string	N	14	시가총액(단위: 천)
plow	저가	string	N	12	저가
phigh	고가	string	N	12	고가
popen	시가	string	N	12	시가
tvol	거래량	string	N	14	거래량(단위: 주)
rate	등락율	string	N	12	등락율(%)
diff	대비	string	N	12	대비
sign	기호	string	N	1	기호
avol	거래대금	string	N	14	거래대금(단위: 천)
eps	EPS	string	N	14	EPS
per	PER	string	N	14	PER
rank	순위	string	N	6	순위
ename	영문종목명	string	N	48	영문종목명
e_ordyn	매매가능	string	N	2	가능 : O
class SearchByConditionItem2(BaseModel):
    pass


class SearchByCondition(BaseModel, KisHttpBody):
    """해외주식조건검색"""

    output1: SearchByConditionItem1 = Field(title="응답상세")
    output2: Sequence[SearchByConditionItem2] = Field(default_factory=list)


prdt_type_cd	상품유형코드	string	Y	3	<description>512  미국 나스닥 / 513  미국 뉴욕거래소 / 529  미국 아멕스 
515  일본
501  홍콩 / 543  홍콩CNY / 558  홍콩USD
507  베트남 하노이거래소 / 508  베트남 호치민거래소
551  중국 상해A / 552  중국 심천A</description>
tr_natn_cd	거래국가코드	string	Y	3	840 미국 / 392 일본 / 344 홍콩 / 704 베트남 / 156 중국
tr_natn_name	거래국가명	string	Y	60	 
natn_eng_abrv_cd	국가영문약어코드	string	Y	2	US 미국 / JP 일본 / HK 홍콩 / VN 베트남 / CN 중국
tr_mket_cd	거래시장코드	string	Y	2	 
tr_mket_name	거래시장명	string	Y	60	 
acpl_sttl_dt	현지결제일자	string	Y	8	현지결제일자(YYYYMMDD)
dmst_sttl_dt	국내결제일자	string	Y	8	 국내결제일자(YYYYMMDD)
class SettlementDateItem(BaseModel):
    pass


class SettlementDate(BaseModel, KisHttpBody):
    """해외결제일자조회"""

    output: SettlementDateItem = Field(title="응답상세")

std_pdno	표준상품번호	string	Y	12	 
prdt_eng_name	상품영문명	string	Y	60	 
natn_cd	국가코드	string	Y	3	 
natn_name	국가명	string	Y	60	 
tr_mket_cd	거래시장코드	string	Y	2	 
tr_mket_name	거래시장명	string	Y	60	 
ovrs_excg_cd	해외거래소코드	string	Y	4	 
ovrs_excg_name	해외거래소명	string	Y	60	 
tr_crcy_cd	거래통화코드	string	Y	3	 
ovrs_papr	해외액면가	string	Y	195	 
crcy_name	통화명	string	Y	60	 
ovrs_stck_dvsn_cd	해외주식구분코드	string	Y	2	01.주식, 02.WARRANT, 03.ETF, 04.우선주
prdt_clsf_cd	상품분류코드	string	Y	6	 
prdt_clsf_name	상품분류명	string	Y	60	 
sll_unit_qty	매도단위수량	string	Y	10	 
buy_unit_qty	매수단위수량	string	Y	10	 
tr_unit_amt	거래단위금액	string	Y	238	 
lstg_stck_num	상장주식수	string	Y	19	 
lstg_dt	상장일자	string	Y	8	 
ovrs_stck_tr_stop_dvsn_cd	해외주식거래정지구분코드	string	Y	2	<description>※ 해당 값 지연 반영될 수 있는 점 유의 부탁드립니다.

01.정상
02.거래정지(ALL)
03.거래중단
04.매도정지
05.거래정지(위탁)
06.매수정지</description>
lstg_abol_item_yn	상장폐지종목여부	string	Y	1	 
ovrs_stck_prdt_grp_no	해외주식상품그룹번호	string	Y	20	 
lstg_yn	상장여부	string	Y	1	 
tax_levy_yn	세금징수여부	string	Y	1	 
ovrs_stck_erlm_rosn_cd	해외주식등록사유코드	string	Y	2	 
ovrs_stck_hist_rght_dvsn_cd	해외주식이력권리구분코드	string	Y	2	 
chng_bf_pdno	변경전상품번호	string	Y	12	 
prdt_type_cd_2	상품유형코드2	string	Y	3	 
ovrs_item_name	해외종목명	string	Y	60	 
sedol_no	SEDOL번호	string	Y	15	 
blbg_tckr_text	블름버그티커내용	string	Y	100	 
ovrs_stck_etf_risk_drtp_cd	해외주식ETF위험지표코드	string	Y	3	<description>001.ETF
002.ETN
003.ETC(Exchage Traded Commodity)
004.Others(REIT's, Mutual Fund)
005.VIX Underlying ETF
006.VIX Underlying ETN</description>
etp_chas_erng_rt_dbnb	ETP추적수익율배수	string	Y	236	 
istt_usge_isin_cd	기관용도ISIN코드	string	Y	12	 
mint_svc_yn	MINT서비스여부	string	Y	1	 
mint_svc_yn_chng_dt	MINT서비스여부변경일자	string	Y	8	 
prdt_name	상품명	string	Y	60	 
lei_cd	LEI코드	string	Y	20	 
ovrs_stck_stop_rson_cd	해외주식정지사유코드	string	Y	2	<description>01.권리발생
02.ISIN상이
03.기타
04.급등락종목
05.상장폐지(예정)
06.종목코드,거래소변경
07.PTP종목</description>
lstg_abol_dt	상장폐지일자	string	Y	8	 
mini_stk_tr_stat_dvsn_cd	미니스탁거래상태구분코드	string	Y	2	<description>01.정상
02.매매 불가
03.매수 불가
04.매도 불가</description>
mint_frst_svc_erlm_dt	MINT최초서비스등록일자	string	Y	8	 
mint_dcpt_trad_psbl_yn	MINT소수점매매가능여부	string	Y	1	 
mint_fnum_trad_psbl_yn	MINT정수매매가능여부	string	Y	1	 
mint_cblc_cvsn_ipsb_yn	MINT잔고전환불가여부	string	Y	1	 
ptp_item_yn	PTP종목여부	string	Y	1	 
ptp_item_trfx_exmt_yn	PTP종목양도세면제여부	string	Y	1	 
ptp_item_trfx_exmt_strt_dt	PTP종목양도세면제시작일자	string	Y	8	 
ptp_item_trfx_exmt_end_dt	PTP종목양도세면제종료일자	string	Y	8	 
dtm_tr_psbl_yn	주간거래가능여부	string	Y	1	 
sdrf_stop_ecls_yn	급등락정지제외여부	string	Y	1	 
sdrf_stop_ecls_erlm_dt	급등락정지제외등록일자	string	Y	8	
memo_text1	메모내용1	string	Y	500	
ovrs_now_pric1	해외현재가격1	string	Y	23	23.5
last_rcvg_dtime	최종수신일시	string	Y	14	 
class ProductBaseInfoItem(BaseModel):
    pass


class ProductBaseInfo(BaseModel, KisHttpBody):
    """해외주식 상품기본정보"""

    output: ProductBaseInfoItem = Field(title="응답상세")

zdiv	소수점자리수	string	Y	1
stat	거래상태정보	string	Y	20
crec	현재조회종목수	string	Y	6
trec	전체조회종목수	string	Y	6
nrec	RecordCount	string	Y	4
class SectorPriceItem1(BaseModel):
    pass

rsym	실시간조회심볼	string	Y	16
excd	거래소코드	string	Y	4
symb	종목코드	string	Y	1
name	종목명	string	Y	48
last	현재가	string	Y	16
sign	기호	string	Y	1
diff	대비	string	Y	12
rate	등락율	string	Y	12
tvol	거래량	string	Y	14
vask	매도잔량	string	Y	10
pask	매도호가	string	Y	12
pbid	매수호가	string	Y	12
vbid	매수잔량	string	Y	10
seqn	순위	string	Y	6
ename	영문종목명	string	Y	48
e_ordyn	매매가능	string	Y	2
class SectorPriceItem2(BaseModel):
    pass

class SectorPrice(BaseModel, KisHttpBody):
    """해외주식 업종별시세"""

    output1: SectorPriceItem1 = Field(title="응답상세")
    output2: Sequence[SectorPriceItem2] = Field(default_factory=list)


nrec	RecordCount	string	Y	4
class SectorCodesItem1(BaseModel):
    pass
    
icod	업종코드	string	Y	4	 
name	업종명	string	Y	32	 
class SectorCodesItem2(BaseModel):
    pass


class SectorCodes(BaseModel, KisHttpBody):
    """해외주식 업종별코드조회"""

    output1: SectorCodesItem1 = Field(title="응답상세")
    output2: Sequence[SectorCodesItem2] = Field(default_factory=list)
