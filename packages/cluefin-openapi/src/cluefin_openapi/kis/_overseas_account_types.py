from pydantic import BaseModel
from pydantic import Field

from typing import Optional, Literal
from cluefin_openapi.kis._model import KisHttpBody

KRX_FWDG_ORD_ORGNO	한국거래소전송주문조직번호	string	Y	5	주문시 한국투자증권 시스템에서 지정된 영업점코드
ODNO	주문번호	string	Y	10	주문시 한국투자증권 시스템에서 채번된 주문번호
ORD_TMD	주문시각	string	Y	6	주문시각(시분초HHMMSS)
class StockQuoteCurrentItem(BaseModel):
    pass


class StockQuoteCurrent(BaseModel, KisHttpBody):
    """해외주식 주문"""

    output: StockQuoteCurrentItem = Field(title="응답상세")


KRX_FWDG_ORD_ORGNO	한국거래소전송주문조직번호	string	Y	5	주문시 한국투자증권 시스템에서 지정된 영업점코드
ODNO	주문번호	string	Y	10	주문시 한국투자증권 시스템에서 채번된 주문번호
ORD_TMD	주문시각	string	Y	6	주문시각(시분초HHMMSS)
class StockQuoteCorrectionItem(BaseModel):
    pass


class StockQuoteCorrection(BaseModel, KisHttpBody):
    """해외주식 정정취소주문"""

    output: StockQuoteCorrectionItem = Field(title="응답상세")

ODNO	한국거래소전송주문조직번호	string	Y	10	tr_id가 TTTT3016U(미국 예약 매도 주문) / TTTT3014U(미국 예약 매수 주문)인 경우만 출력
RSVN_ORD_RCIT_DT	예약주문접수일자	string	Y	8	tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 출력
OVRS_RSVN_ODNO	해외예약주문번호	string	Y	10	tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 출력
class StockReserveQuoteItem(BaseModel):
    pass


class StockReserveQuote(BaseModel, KisHttpBody):
    """해외주식 예약주문접수"""

    output: StockReserveQuoteItem = Field(title="응답상세")

OVRS_RSVN_ODNO	해외예약주문번호	string	Y	10
class StockReserveQuoteCorrectionItem(BaseModel):
    pass


class StockReserveQuoteCorrection(BaseModel, KisHttpBody):
    """해외주식 예약주문접수취소"""

    output: StockReserveQuoteCorrectionItem = Field(title="응답상세")

tr_crcy_cd	거래통화코드	string	N	3	18.2
ord_psbl_frcr_amt	주문가능외화금액	string	N	21	18.2
sll_ruse_psbl_amt	매도재사용가능금액	string	N	21	가능금액 산정 시 사용
ovrs_ord_psbl_amt	해외주문가능금액	string	N	21	- 한국투자 앱 해외주식 주문화면내 "외화" 인경우 주문가능금액
max_ord_psbl_qty	최대주문가능수량	string	N	19	<description>- 한국투자 앱 해외주식 주문화면내 "외화" 인경우 주문가능수량
- 매수 시 수량단위 절사해서 사용 
   예 : (100주단위) 545 주 -> 500 주 / (10주단위) 545 주 -> 540 주</description>
echm_af_ord_psbl_amt	환전이후주문가능금액	string	N	21	사용되지 않는 사항(0으로 출력)
echm_af_ord_psbl_qty	환전이후주문가능수량	string	N	19	사용되지 않는 사항(0으로 출력)
ord_psbl_qty	주문가능수량	string	N	10	22(20.1)
exrt	환율	string	N	22	25(18.6)
frcr_ord_psbl_amt1	외화주문가능금액1	string	N	25	- 한국투자 앱 해외주식 주문화면내 "통합" 인경우 주문가능금액
ovrs_max_ord_psbl_qty	해외최대주문가능수량	string	N	19	<description>- 한국투자 앱 해외주식 주문화면내 "통합" 인경우 주문가능수량
- 매수 시 수량단위 절사해서 사용 
   예 : (100주단위) 545 주 -> 500 주 / (10주단위) 545 주 -> 540 주</description>
class BuyTradableAmountItem(BaseModel):
    pass


class BuyTradableAmount(BaseModel, KisHttpBody):
    """해외주식 매수가능금액조회"""

    output: BuyTradableAmountItem = Field(title="응답상세")


ord_dt	주문일자	string	Y	8	주문접수 일자
ord_gno_brno	주문채번지점번호	string	Y	5	계좌 개설 시 관리점으로 선택한 영업점의 고유번호
odno	주문번호	string	Y	10	접수한 주문의 일련번호
orgn_odno	원주문번호	string	Y	10	정정 또는 취소 대상 주문의 일련번호
pdno	상품번호	string	Y	12	종목코드
prdt_name	상품명	string	Y	60	종목명
sll_buy_dvsn_cd	매도매수구분코드	string	Y	2	01 : 매도, 02 : 매수
sll_buy_dvsn_cd_name	매도매수구분코드명	string	Y	60	매수매도구분명
rvse_cncl_dvsn_cd	정정취소구분코드	string	Y	2	01 : 정정, 02 : 취소
rvse_cncl_dvsn_cd_name	정정취소구분코드명	string	Y	60	정정취소구분명
rjct_rson	거부사유	string	Y	60	정상 처리되지 못하고 거부된 주문의 사유
rjct_rson_name	거부사유명	string	Y	60	정상 처리되지 못하고 거부된 주문의 사유명
ord_tmd	주문시각	string	Y	6	주문 접수 시간 
tr_mket_name	거래시장명	string	Y	60	 
tr_crcy_cd	거래통화코드	string	Y	3	<description>USD : 미국달러
HKD : 홍콩달러
CNY : 중국위안화
JPY : 일본엔화
VND : 베트남동</description>
natn_cd	국가코드	string	Y	3	 
natn_kor_name	국가한글명	string	Y	60	 
ft_ord_qty	FT주문수량	string	Y	10	주문수량
ft_ccld_qty	FT체결수량	string	Y	10	체결된 수량
nccs_qty	미체결수량	string	Y	10	미체결수량
ft_ord_unpr3	FT주문단가3	string	Y	26	주문가격
ft_ccld_unpr3	FT체결단가3	string	Y	26	체결된 가격
ft_ccld_amt3	FT체결금액3	string	Y	23	체결된 금액
ovrs_excg_cd	해외거래소코드	string	Y	4	<description>NASD : 나스닥
NYSE : 뉴욕
AMEX : 아멕스
SEHK : 홍콩
SHAA : 중국상해
SZAA : 중국심천
TKSE : 일본
HASE : 베트남 하노이
VNSE : 베트남 호치민</description>
prcs_stat_name	처리상태명	string	Y	60	"" 공백 입력
loan_type_cd	대출유형코드	string	Y	2	<description>00 해당사항없음
01 자기융자일반형
03 자기융자투자형
05 유통융자일반형
06 유통융자투자형
07 자기대주
09 유통대주
10 현금
11 주식담보대출
12 수익증권담보대출
13 ELS담보대출
14 채권담보대출
15 해외주식담보대출
16 기업신용공여
31 소액자동담보대출
41 매도담보대출
42 환매자금대출
43 매입환매자금대출
44 대여매도담보대출
81 대차거래
82 법인CMA론
91 공모주청약자금대출
92 매입자금
93 미수론서비스
94 대여</description>
loan_dt	대출일자	string	Y	8	대출 실행일자
usa_amk_exts_rqst_yn	미국애프터마켓연장신청여부	string	Y	1	Y/N
splt_buy_attr_name	분할매수속성명	string	Y	60	정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시됨
class StockNotConclusionHistoryItem(BaseModel):
    pass


class StockNotConclusion(BaseModel, KisHttpBody):
    """해외주식 미체결내역"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output: Sequence[StockNotConclusionHistoryItem] = Field(default_factory=list)


cano	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
acnt_prdt_cd	계좌상품코드	string	Y	2	계좌상품코드
prdt_type_cd	상품유형코드	string	Y	3	
ovrs_pdno	해외상품번호	string	Y	12	
ovrs_item_name	해외종목명	string	Y	60	
frcr_evlu_pfls_amt	외화평가손익금액	string	Y	30	해당 종목의 매입금액과 평가금액의 외회기준 비교 손익
evlu_pfls_rt	평가손익율	string	Y	10	해당 종목의 평가손익을 기준으로 한 수익률
pchs_avg_pric	매입평균가격	string	Y	23	해당 종목의 매수 평균 단가
ovrs_cblc_qty	해외잔고수량	string	Y	19	
ord_psbl_qty	주문가능수량	string	Y	10	매도 가능한 주문 수량
frcr_pchs_amt1	외화매입금액1	string	Y	23	해당 종목의 외화 기준 매입금액
ovrs_stck_evlu_amt	해외주식평가금액	string	Y	32	해당 종목의 외화 기준 평가금액
now_pric2	현재가격2	string	Y	25	해당 종목의 현재가
tr_crcy_cd	거래통화코드	string	Y	3	<description>USD : 미국달러
HKD : 홍콩달러
CNY : 중국위안화
JPY : 일본엔화
VND : 베트남동</description>
ovrs_excg_cd	해외거래소코드	string	Y	4	<description>NASD : 나스닥
NYSE : 뉴욕
AMEX : 아멕스
SEHK : 홍콩
SHAA : 중국상해
SZAA : 중국심천
TKSE : 일본
HASE : 하노이거래소
VNSE : 호치민거래소</description>
loan_type_cd	대출유형코드	string	Y	2	<description>00 : 해당사항없음
01 : 자기융자일반형
03 : 자기융자투자형
05 : 유통융자일반형
06 : 유통융자투자형
07 : 자기대주
09 : 유통대주
10 : 현금
11 : 주식담보대출
12 : 수익증권담보대출
13 : ELS담보대출
14 : 채권담보대출
15 : 해외주식담보대출
16 : 기업신용공여
31 : 소액자동담보대출
41 : 매도담보대출
42 : 환매자금대출
43 : 매입환매자금대출
44 : 대여매도담보대출
81 : 대차거래
82 : 법인CMA론
91 : 공모주청약자금대출
92 : 매입자금
93 : 미수론서비스
94 : 대여</description>
loan_dt	대출일자	string	Y	8	대출 실행일자
expd_dt	만기일자	string	Y	8	대출 만기일자
class StockBalanceItem1(BaseModel):
    pass

frcr_pchs_amt1	외화매입금액1	string	Y	24	
ovrs_rlzt_pfls_amt	해외실현손익금액	string	Y	20	
ovrs_tot_pfls	해외총손익	string	Y	24	
rlzt_erng_rt	실현수익율	string	Y	32	
tot_evlu_pfls_amt	총평가손익금액	string	Y	32	
tot_pftrt	총수익률	string	Y	32	
frcr_buy_amt_smtl1	외화매수금액합계1	string	Y	25	
ovrs_rlzt_pfls_amt2	해외실현손익금액2	string	Y	24	
frcr_buy_amt_smtl2	외화매수금액합계2	string	Y	25	
class StockBalanceItem2(BaseModel):
    pass


class StockBalance(BaseModel, KisHttpBody):
    """해외주식 잔고"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output1: Sequence[StockBalanceItem1] = Field(default_factory=list)
    output2: StockBalanceItem2 = Field(title="응답상세2")

ord_dt	주문일자	string	Y	8	주문접수 일자 (현지시각 기준)
ord_gno_brno	주문채번지점번호	string	Y	5	계좌 개설 시 관리점으로 선택한 영업점의 고유번호
odno	주문번호	string	Y	10	접수한 주문의 일련번호 ※ 정정취소주문 시, 해당 값 odno(주문번호) 넣어서 사용
orgn_odno	원주문번호	string	Y	10	정정 또는 취소 대상 주문의 일련번호
sll_buy_dvsn_cd	매도매수구분코드	string	Y	2	01 : 매도  02 : 매수
sll_buy_dvsn_cd_name	매도매수구분코드명	string	Y	60	
rvse_cncl_dvsn	정정취소구분	string	Y	2	01 : 정정  02 : 취소
rvse_cncl_dvsn_name	정정취소구분명	string	Y	60	
pdno	상품번호	string	Y	12	
prdt_name	상품명	string	Y	60	
ft_ord_qty	FT주문수량	string	Y	10	주문수량
ft_ord_unpr3	FT주문단가3	string	Y	26	주문가격
ft_ccld_qty	FT체결수량	string	Y	10	체결된 수량
ft_ccld_unpr3	FT체결단가3	string	Y	26	체결된 가격
ft_ccld_amt3	FT체결금액3	string	Y	23	체결된 금액
nccs_qty	미체결수량	string	Y	10	미체결수량
prcs_stat_name	처리상태명	string	Y	60	완료, 거부, 전송
rjct_rson	거부사유	string	Y	60	정상 처리되지 못하고 거부된 주문의 사유
rjct_rson_name	거부사유명	string	Y	60	
ord_tmd	주문시각	string	Y	6	주문 접수 시간 
tr_mket_name	거래시장명	string	Y	60	 
tr_natn	거래국가	string	Y	3	 
tr_natn_name	거래국가명	string	Y	3	 
ovrs_excg_cd	해외거래소코드	string	Y	4	<description>NASD : 나스닥
NYSE : 뉴욕
AMEX : 아멕스
SEHK : 홍콩 
SHAA : 중국상해
SZAA : 중국심천
TKSE : 일본
HASE : 베트남 하노이
VNSE : 베트남 호치민</description>
tr_crcy_cd	거래통화코드	string	Y	60	 
dmst_ord_dt	국내주문일자	string	Y	8	
thco_ord_tmd	당사주문시각	string	Y	6	
loan_type_cd	대출유형코드	string	Y	2	<description>00 : 해당사항없음
01 : 자기융자일반형
03 : 자기융자투자형
05 : 유통융자일반형
06 : 유통융자투자형
07 : 자기대주
09 : 유통대주
10 : 현금
11 : 주식담보대출
12 : 수익증권담보대출
13 : ELS담보대출
14 : 채권담보대출
15 : 해외주식담보대출
16 : 기업신용공여
31 : 소액자동담보대출
41 : 매도담보대출
42 : 환매자금대출
43 : 매입환매자금대출
44 : 대여매도담보대출
81 : 대차거래
82 : 법인CMA론
91 : 공모주청약자금대출
92 : 매입자금
93 : 미수론서비스
94 : 대여</description>
loan_dt	대출일자	string	Y	8	
mdia_dvsn_name	매체구분명	string	Y	60	ex) OpenAPI, 모바일
usa_amk_exts_rqst_yn	미국애프터마켓연장신청여부	string	Y	1	Y/N
splt_buy_attr_name	분할매수/매도속성명	string	Y	60	정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시
class StockConclusionHistoryItem(BaseModel):
    pass


class StockConclusionHistory(BaseModel, KisHttpBody):
    """해외주식 주문체결내역"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output: Sequence[StockConclusionHistoryItem] = Field(default_factory=list)


prdt_name	상품명	string	Y	60	종목명
cblc_qty13	잔고수량13	string	Y	32	결제보유수량
thdt_buy_ccld_qty1	당일매수체결수량1	string	Y	32	당일 매수 체결 완료 수량
thdt_sll_ccld_qty1	당일매도체결수량1	string	Y	32	당일 매도 체결 완료 수량
ccld_qty_smtl1	체결수량합계1	string	Y	32	체결기준 현재 보유수량
ord_psbl_qty1	주문가능수량1	string	Y	32	주문 가능한 주문 수량
frcr_pchs_amt	외화매입금액	string	Y	29	해당 종목의 외화 기준 매입금액
frcr_evlu_amt2	외화평가금액2	string	Y	30	해당 종목의 외화 기준 평가금액
evlu_pfls_amt2	평가손익금액2	string	Y	31	해당 종목의 매입금액과 평가금액의 외회기준 비교 손익
evlu_pfls_rt1	평가손익율1	string	Y	32	해당 종목의 평가손익을 기준으로 한 수익률
pdno	상품번호	string	Y	12	종목코드
bass_exrt	기준환율	string	Y	31	원화 평가 시 적용 환율
buy_crcy_cd	매수통화코드	string	Y	3	<description>USD : 미국달러
HKD : 홍콩달러
CNY : 중국위안화
JPY : 일본엔화
VND : 베트남동</description>
ovrs_now_pric1	해외현재가격1	string	Y	29	해당 종목의 현재가
avg_unpr3	평균단가3	string	Y	29	해당 종목의 매수 평균 단가
tr_mket_name	거래시장명	string	Y	60	해당 종목의 거래시장명
natn_kor_name	국가한글명	string	Y	60	거래 국가명
pchs_rmnd_wcrc_amt	매입잔액원화금액	string	Y	19	
thdt_buy_ccld_frcr_amt	당일매수체결외화금액	object	Y	30	당일 매수 외화금액 (Type: Object X String O)
thdt_sll_ccld_frcr_amt	당일매도체결외화금액	string	Y	30	당일 매도 외화금액
unit_amt	단위금액	string	Y	19	
std_pdno	표준상품번호	string	Y	12	
prdt_type_cd	상품유형코드	string	Y	3	
scts_dvsn_name	유가증권구분명	string	Y	60	
loan_rmnd	대출잔액	string	Y	19	대출 미상환 금액
loan_dt	대출일자	string	Y	8	대출 실행일자
loan_expd_dt	대출만기일자	string	Y	8	대출 만기일자
ovrs_excg_cd	해외거래소코드	string	Y	4	<description>NASD : 나스닥
NYSE : 뉴욕
AMEX : 아멕스
SEHK : 홍콩
SHAA : 중국상해
SZAA : 중국심천
TKSE : 일본
HASE : 하노이거래소
VNSE : 호치민거래소</description>
item_lnkg_excg_cd	종목연동거래소코드	string	Y	4	prdt_dvsn(상품구분) : 직원용 데이터(Type: String, Length:2)
class CurrentBalanceByConclusionItem1(BaseModel):
    pass

crcy_cd	통화코드	string	Y	3	
crcy_cd_name	통화코드명	string	Y	60	
frcr_buy_amt_smtl	외화매수금액합계	string	Y	29	해당 통화로 매수한 종목 전체의 매수금액
frcr_sll_amt_smtl	외화매도금액합계	string	Y	29	해당 통화로 매도한 종목 전체의 매수금액
frcr_dncl_amt_2	외화예수금액2	string	Y	29	외화로 표시된 외화사용가능금액
frst_bltn_exrt	최초고시환율	string	Y	31	
frcr_buy_mgn_amt	외화매수증거금액	string	Y	31	매수증거금으로 사용된 외화금액
frcr_etc_mgna	외화기타증거금	string	Y	31	
frcr_drwg_psbl_amt_1	외화출금가능금액1	string	Y	29	출금가능한 외화금액
frcr_evlu_amt2	출금가능원화금액	string	Y	29	출금가능한 원화금액
acpl_cstd_crcy_yn	현지보관통화여부	string	Y	1	
nxdy_frcr_drwg_psbl_amt	익일외화출금가능금액	string	Y	31	
output3	응답상세3	object	Y		
pchs_amt_smtl	매입금액합계	string	Y	19	해외유가증권 매수금액의 원화 환산 금액
evlu_amt_smtl	평가금액합계	string	Y	19	해외유가증권 평가금액의 원화 환산 금액
evlu_pfls_amt_smtl	평가손익금액합계	string	Y	19	해외유가증권 평가손익의 원화 환산 금액
dncl_amt	예수금액	string	Y	19	
cma_evlu_amt	CMA평가금액	string	Y	19	
tot_dncl_amt	총예수금액	string	Y	19	
etc_mgna	기타증거금	string	Y	19	
wdrw_psbl_tot_amt	인출가능총금액	string	Y	19	
frcr_evlu_tota	외화평가총액	string	Y	19	
evlu_erng_rt1	평가수익율1	string	Y	31	
pchs_amt_smtl_amt	매입금액합계금액	string	Y	19	
evlu_amt_smtl_amt	평가금액합계금액	string	Y	19	
tot_evlu_pfls_amt	총평가손익금액	string	Y	31	
tot_asst_amt	총자산금액	string	Y	19	
buy_mgn_amt	매수증거금액	string	Y	19	
mgna_tota	증거금총액	string	Y	19	
frcr_use_psbl_amt	외화사용가능금액	string	Y	20	
ustl_sll_amt_smtl	미결제매도금액합계	string	Y	19	
ustl_buy_amt_smtl	미결제매수금액합계	string	Y	19	
tot_frcr_cblc_smtl	총외화잔고합계	string	Y	29	
tot_loan_amt	총대출금액	string	Y	19	
class CurrentBalanceByConclusionItem2(BaseModel):
    pass

class CurrentBalanceByConclusion(BaseModel, KisHttpBody):
    """해외주식 체결기준현재잔고"""

    output1: Sequence[CurrentBalanceByConclusionItem1] = Field(default_factory=list)
    output2: Sequence[CurrentBalanceByConclusionItem2] = Field(default_factory=list)

cncl_yn	취소여부	string	N	1	 
rsvn_ord_rcit_dt	예약주문접수일자	string	N	8	 
ovrs_rsvn_odno	해외예약주문번호	string	N	10	 
ord_dt	주문일자	string	N	8	 
ord_gno_brno	주문채번지점번호	string	N	5	 
odno	주문번호	string	N	10	 
sll_buy_dvsn_cd	매도매수구분코드	string	N	2	 
sll_buy_dvsn_name	매도매수구분명	string	N	4	 
ovrs_rsvn_ord_stat_cd	해외예약주문상태코드	string	N	2	 
ovrs_rsvn_ord_stat_cd_name	해외예약주문상태코드명	string	N	60	 
pdno	상품번호	string	N	12	 
prdt_type_cd	상품유형코드	string	N	3	 
prdt_name	상품명	string	N	60	 
ord_rcit_tmd	주문접수시각	string	N	6	 
ord_fwdg_tmd	주문전송시각	string	N	6	 
tr_dvsn_name	거래구분명	string	N	60	 
ovrs_excg_cd	해외거래소코드	string	N	4	 
tr_mket_name	거래시장명	string	N	60	 
ord_stfno	주문직원번호	string	N	6	 
ft_ord_qty	FT주문수량	string	N	10	 
ft_ord_unpr3	FT주문단가3	string	N	27	 
ft_ccld_qty	FT체결수량	string	N	10	 
nprc_rson_text	미처리사유내용	string	N	500	
splt_buy_attr_name	분할매수속성명	string	N	60	정규장 종료 주문 시에는 '정규장 종료', 시간 입력 시에는 from ~ to 시간 표시
class ReserveOrdersItem(BaseModel):
    pass


class ReserveOrders(BaseModel, KisHttpBody):
    """해외주식 예약주문조회"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output: ReserveOrdersItem = Field(title="응답상세")

pdno	상품번호	string	Y	12
prdt_name	상품명	string	Y	60
cblc_qty13	잔고수량13	string	Y	238
ord_psbl_qty1	주문가능수량1	string	Y	238
avg_unpr3	평균단가3	string	Y	244
ovrs_now_pric1	해외현재가격1	string	Y	235
frcr_pchs_amt	외화매입금액	string	Y	235
frcr_evlu_amt2	외화평가금액2	string	Y	236
evlu_pfls_amt2	평가손익금액2	string	Y	255
bass_exrt	기준환율	string	Y	238
oprt_dtl_dtime	조작상세일시	string	Y	17
buy_crcy_cd	매수통화코드	string	Y	3
thdt_sll_ccld_qty1	당일매도체결수량1	string	Y	238
thdt_buy_ccld_qty1	당일매수체결수량1	string	Y	238
evlu_pfls_rt1	평가손익율1	string	Y	238
tr_mket_name	거래시장명	string	Y	60
natn_kor_name	국가한글명	string	Y	60
std_pdno	표준상품번호	string	Y	12
mgge_qty	담보수량	string	Y	19
loan_rmnd	대출잔액	string	Y	19
prdt_type_cd	상품유형코드	string	Y	3
ovrs_excg_cd	해외거래소코드	string	Y	4
scts_dvsn_name	유가증권구분명	string	Y	60
ldng_cblc_qty	대여잔고수량	string	Y	19
class BalanceBySettlementItem1(BaseModel):
    pass

crcy_cd	통화코드	string	Y	3
crcy_cd_name	통화코드명	string	Y	60
frcr_dncl_amt_2	외화예수금액2	string	Y	236
frst_bltn_exrt	최초고시환율	string	Y	238
frcr_evlu_amt2	외화평가금액2	string	Y	236
output3	응답상세	object	Y	 
pchs_amt_smtl_amt	매입금액합계금액	string	Y	19
tot_evlu_pfls_amt	총평가손익금액	string	Y	238
evlu_erng_rt1	평가수익율1	string	Y	201
tot_dncl_amt	총예수금액	string	Y	19
wcrc_evlu_amt_smtl	원화평가금액합계	string	Y	236
tot_asst_amt2	총자산금액2	string	Y	236
frcr_cblc_wcrc_evlu_amt_smtl	외화잔고원화평가금액합계	string	Y	236
tot_loan_amt	총대출금액	string	Y	19
tot_ldng_evlu_amt	총대여평가금액	string	Y	9
class BalanceBySettlementItem2(BaseModel):
    pass

class BalanceBySettlement(BaseModel, KisHttpBody):
    """해외주식 결제기준잔고"""

    output1: Sequence[BalanceBySettlementItem1] = Field(default_factory=list)
    output2: Sequence[BalanceBySettlementItem2] = Field(default_factory=list)

trad_dt	매매일자	string	Y	8
sttl_dt	결제일자	string	Y	8
sll_buy_dvsn_cd	매도매수구분코드	string	Y	2
sll_buy_dvsn_name	매도매수구분명	string	Y	4
pdno	상품번호	string	Y	12
ovrs_item_name	해외종목명	string	Y	60
ccld_qty	체결수량	string	Y	10
amt_unit_ccld_qty	금액단위체결수량	string	Y	188
ft_ccld_unpr2	FT체결단가2	string	Y	238
ovrs_stck_ccld_unpr	해외주식체결단가	string	Y	238
tr_frcr_amt2	거래외화금액2	string	Y	236
tr_amt	거래금액	string	Y	19
frcr_excc_amt_1	외화정산금액1	string	Y	236
wcrc_excc_amt	원화정산금액	string	Y	19
dmst_frcr_fee1	국내외화수수료1	string	Y	235
frcr_fee1	외화수수료1	string	Y	236
dmst_wcrc_fee	국내원화수수료	string	Y	19
ovrs_wcrc_fee	해외원화수수료	string	Y	19
crcy_cd	통화코드	string	Y	3
std_pdno	표준상품번호	string	Y	12
erlm_exrt	등록환율	string	Y	238
loan_dvsn_cd	대출구분코드	string	Y	2
loan_dvsn_name	대출구분명	string	Y	60
output2	응답상세	object	Y	 
frcr_buy_amt_smtl	외화매수금액합계	string	Y	236
frcr_sll_amt_smtl	외화매도금액합계	string	Y	236
dmst_fee_smtl	국내수수료합계	string	Y	256
ovrs_fee_smtl	해외수수료합계	string	Y	236
class DailyTransactionHistoryItem(BaseModel):
    pass


class DailyTransactionHistory(BaseModel, KisHttpBody):
    """해외주식 일별거래내역"""

    ctx_area_fk200: str = Field(title="연속조회검색조건200", max_length=200)
    ctx_area_nk200: str = Field(title="연속조회키200", max_length=200)
    output: Sequence[DailyTransactionHistoryItem] = Field(default_factory=list)

trad_day	매매일	string	Y	8
ovrs_pdno	해외상품번호	string	Y	12
ovrs_item_name	해외종목명	string	Y	60
slcl_qty	매도청산수량	string	Y	10
pchs_avg_pric	매입평균가격	string	Y	184
frcr_pchs_amt1	외화매입금액1	string	Y	185
avg_sll_unpr	평균매도단가	string	Y	238
frcr_sll_amt_smtl1	외화매도금액합계1	string	Y	186
stck_sll_tlex	주식매도제비용	string	Y	184
ovrs_rlzt_pfls_amt	해외실현손익금액	string	Y	145
pftrt	수익률	string	Y	238
exrt	환율	string	Y	201
ovrs_excg_cd	해외거래소코드	string	Y	4
frst_bltn_exrt	최초고시환율	string	Y	238
class PeriodProfitLossItem1(BaseModel):
    pass

stck_sll_amt_smtl	주식매도금액합계	string	Y	184	WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
stck_buy_amt_smtl	주식매수금액합계	string	Y	184	WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
smtl_fee1	합계수수료1	string	Y	138	WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
excc_dfrm_amt	정산지급금액	string	Y	205	WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
ovrs_rlzt_pfls_tot_amt	해외실현손익총금액	string	Y	145	WCRC_FRCR_DVSN_CD(원화외화구분코드)가 01(외화)이고 OVRS_EXCG_CD(해외거래소코드)가 공란(전체)인 경우 출력값 무시
tot_pftrt	총수익률	string	Y	238	 
bass_dt	기준일자	string	Y	8	 
exrt	환율	string	Y	201	 
class PeriodProfitLossItem2(BaseModel):
    pass

class PeriodProfitLoss(BaseModel, KisHttpBody):
    """해외주식 기간손익"""

    output: Sequence[PeriodProfitLossItem1] = Field(default_factory=list)
    output2: PeriodProfitLossItem2 = Field(title="응답상세2")

natn_name	국가명           	string	Y	60	 
crcy_cd	통화코드          	string	Y	3	 
frcr_dncl_amt1	외화예수금액       	string	Y	186	 
ustl_buy_amt	미결제매수금액      	string	Y	182	 
ustl_sll_amt	미결제매도금액      	string	Y	182	 
frcr_rcvb_amt	외화미수금액       	string	Y	182	 
frcr_mgn_amt	외화증거금액       	string	Y	186	 
frcr_gnrl_ord_psbl_amt	외화일반주문가능금액  	string	Y	182	 
frcr_ord_psbl_amt1	외화주문가능금액    	string	Y	186	 원화주문가능환산금액
itgr_ord_psbl_amt	통합주문가능금액    	string	Y	182	 
bass_exrt	기준환율          	string	Y	238	 
class MarginAggregateItem(BaseModel):
    pass


class MarginAggregate(BaseModel, KisHttpBody):
    """해외증거금 통합변조회"""

    output: Sequence[MarginAggregateItem] = Field(default_factory=list)

KRX_FWDG_ORD_ORGNO	한국거래소전송주문조직번호	string	Y	5	주문시 한국투자증권 시스템에서 지정된 영업점코드
ODNO	주문번호	string	Y	10	주문시 한국투자증권 시스템에서 채번된 주문번호
ORD_TMD	주문시각	string	Y	6	주문시각(시분초HHMMSS)
class OrderAfterDayTimeItem(BaseModel):
    pass


class OrderAfterDayTime(BaseModel, KisHttpBody):
    """해외주식 미국주간주문"""

    output: OrderAfterDayTimeItem = Field(title="응답상세")


KRX_FWDG_ORD_ORGNO	한국거래소전송주문조직번호	string	Y	5	주문시 한국투자증권 시스템에서 지정된 영업점코드
ODNO	주문번호	string	Y	10	주문시 한국투자증권 시스템에서 채번된 주문번호
ORD_TMD	주문시각	string	Y	6	주문시각(시분초HHMMSS)
class CorrectCancelAfterDayTimeItem(BaseModel):
    pass


class CorrectCancelAfterDayTime(BaseModel, KisHttpBody):
    """해외주식 미국주간정정취소"""

    output: CorrectCancelAfterDayTimeItem = Field(title="응답상세")


odno	주문번호	string	Y	10	
trad_dvsn_name	매매구분명	string	Y	60	
pdno	상품번호	string	Y	12	
item_name	종목명	string	Y	60	
ft_ord_qty	FT주문수량	string	Y	4	
ft_ord_unpr3	FT주문단가	string	Y	8	
splt_buy_attr_name	분할매수속성명	string	Y	60	
ft_ccld_qty	FT체결수량	string	Y	4	
ord_gno_brno	주문채번지점번호	string	N	5	
rt_cd	성공 실패 여부	string	Y	1	0 : 성공 0 이외의 값 : 실패
msg_cd	응답코드	string	Y	8	
msg1	응답메세지	string	Y	80	
ctx_area_fk200	연속조회검색조건200	string	Y	200	
ctx_area_nk200	연속조회키200	string	Y	200	
class LimitOrderNumberItem(BaseModel):
    pass


class LimitOrderNumber(BaseModel, KisHttpBody):
    """해외주식 지정가주문번호조회"""

    output: Sequence[LimitOrderExecutionHistoryItem] = Field(default_factory=list)  

CCLD_SEQ	체결순번	string	Y	4	
CCLD_BTWN	체결시간	string	Y	6	HHMMSS
PDNO	상품번호	string	Y	12	
ITEM_NAME	종목명	string	Y	60	
FT_CCLD_QTY	FT체결수량	string	N	4	
FT_CCLD_UNPR3	FT체결단가	string	Y	8	
FT_CCLD_AMT3	FT체결금액	string	N	8	
class LimitOrderConclusionHistoryItem1(BaseModel):
    pass

ODNO	주문번호	string	Y	10	
TRAD_DVSN_NAME	매매구분명	string	Y	60	
PDNO	상품번호	string	Y	12	
ITEM_NAME	종목명	string	Y	60	
FT_ORD_QTY	FT주문수량	string	Y	4	
FT_ORD_UNPR3	FT주문단가	string	Y	8	
ORD_TMD	주문시각	string	Y	6	
SPLT_BUY_ATTR_NAME	분할매수속성명	string	Y	60	
FT_CCLD_QTY	FT체결수량	string	Y	4	
TR_CRCY	거래통화	string	Y	3	
FT_CCLD_UNPR3	FT체결단가	string	Y	8	
FT_CCLD_AMT3	FT체결금액	string	Y	8	
CCLD_CNT	체결건수	string	Y	4	
class LimitOrderConclusionHistoryItem2(BaseModel):
    pass


class LimitOrderExecutionHistory(BaseModel, KisHttpBody):
    """해외주식 지정가체결내역조회"""

    output1: Sequence[LimitOrderConclusionHistoryItem1] = Field(default_factory=list)
    output2: Sequence[LimitOrderConclusionHistoryItem2] = Field(alias="output3",default_factory=list)
