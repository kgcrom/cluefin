from cluefin_openapi.kis._client import Client


class OverseasAccount:
    """해외주식 주문/계좌"""

    def __init__(self, client: Client):
        self.client = client

url: /uapi/overseas-stock/v1/trading/order
tr_id: 실전[TTTT1002U (미국매수), TTTT1006U (미국매도, 아시아 국가 하단 규격서 참고)], 모의[VTTT1002U (미국매수), VTTT1001U (아시아 국가 하단 규격서 참고)]
arguments:
ORD_DVSN	주문구분	string	Y	2	<description>[Header tr_id TTTT1002U(미국 매수 주문)]
00 : 지정가
32 : LOO(장개시지정가)
34 : LOC(장마감지정가)
35 : TWAP (시간가중평균)
36 : VWAP (거래량가중평균)
* 모의투자 VTTT1002U(미국 매수 주문)로는 00:지정가만 가능
* TWAP, VWAP 주문은 분할시간 주문 입력 필수

[Header tr_id TTTT1006U(미국 매도 주문)]
00 : 지정가
31 : MOO(장개시시장가)
32 : LOO(장개시지정가)
33 : MOC(장마감시장가)
34 : LOC(장마감지정가)
35 : TWAP (시간가중평균)
36 : VWAP (거래량가중평균)
* 모의투자 VTTT1006U(미국 매도 주문)로는 00:지정가만 가능
* TWAP, VWAP 주문은 분할시간 주문 입력 필수

[Header tr_id TTTS1001U(홍콩 매도 주문)]
00 : 지정가
50 : 단주지정가
* 모의투자 VTTS1001U(홍콩 매도 주문)로는 00:지정가만 가능

[그외 tr_id]
제거

※ TWAP, VWAP 주문은 정정 불가</description>
START_TIME	시작시간	string	N	6	<description>※ TWAP, VWAP 주문유형이고 알고리즘주문시간구분코드가 00일때 사용
※ YYMMDD 형태로 입력
※ 시간 입력 시 정규장 종료 5분전까지 입력 가능</description>
END_TIME	종료시간	string	N	6	<description>※ TWAP, VWAP 주문유형이고 알고리즘주문시간구분코드가 00일때 사용
※ YYMMDD 형태로 입력
※ 시간 입력 시 정규장 종료 5분전까지 입력 가능</description>
ALGO_ORD_TMD_DVSN_CD	알고리즘주문시간구분코드	string	N	2	00 : 분할주문 시간 직접입력 , 02 : 정규장 종료시까지
    def request_stock_quote_current(self):
        """해외주식 주문
        
        """
        pass

url: /uapi/overseas-stock/v1/trading/order-rvsecncl
tr_id: 실전[TTTT1004U (미국 정정·취소, 아시아 국가 하단 규격서 참고)], 모의[VTTT1004U (미국 정정·취소, 아시아 국가 하단 규격서 참고)]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
OVRS_EXCG_CD	해외거래소코드	string	Y	4	<description>NASD : 나스닥 
NYSE : 뉴욕 
AMEX : 아멕스
SEHK : 홍콩
SHAA : 중국상해
SZAA : 중국심천
TKSE : 일본
HASE : 베트남 하노이
VNSE : 베트남 호치민</description>
PDNO	상품번호	string	Y	12	
ORGN_ODNO	원주문번호	string	Y	10	<description>정정 또는 취소할 원주문번호
(해외주식_주문 API ouput ODNO 
or 해외주식 미체결내역 API output ODNO 참고)</description>
RVSE_CNCL_DVSN_CD	정정취소구분코드	string	Y	2	01 : 정정, 02 : 취소
ORD_QTY	주문수량	string	Y	10	 
OVRS_ORD_UNPR	해외주문단가	string	Y	32	취소주문 시, "0" 입력
MGCO_APTM_ODNO	운용사지정주문번호	string	N	12	
ORD_SVR_DVSN_CD	주문서버구분코드	string	N	1	"0"(Default)
    def request_stock_quote_correction(self):
        """해외주식 정정취소주문

        """
        pass

url: /uapi/overseas-stock/v1/trading/order-resv
tr_id: 실전[TTTT3014U (미국예약매수), TTTT3016U (중국/홍콩/일본/베트남 예약주문) TTTS3013U], 모의[VTTT3014U (미국예약매수), VTTT3016U (중국/홍콩/일본/베트남 예약주문) VTTS3013U]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
SLL_BUY_DVSN_CD	매도매수구분코드	string	N	2	<description>tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용
01 : 매도
02 : 매수</description>
RVSE_CNCL_DVSN_CD	정정취소구분코드	string	Y	2	<description>tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용
00 : "매도/매수 주문"시 필수 항목
02 : 취소</description>
PDNO	상품번호	string	Y	12	
PRDT_TYPE_CD	상품유형코드	string	Y	3	<description>tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용
515 : 일본
501 : 홍콩 / 543 : 홍콩CNY / 558 : 홍콩USD
507 : 베트남 하노이거래소 / 508 : 베트남 호치민거래소
551 : 중국 상해A / 552 : 중국 심천A</description>
OVRS_EXCG_CD	해외거래소코드	string	Y	4	<description>NASD : 나스닥
NYSE : 뉴욕
AMEX : 아멕스
SEHK : 홍콩
SHAA : 중국상해
SZAA : 중국심천
TKSE : 일본
HASE : 베트남 하노이
VNSE : 베트남 호치민</description>
FT_ORD_QTY	FT주문수량	string	Y	10	
FT_ORD_UNPR3	FT주문단가3	string	Y	27	
ORD_SVR_DVSN_CD	주문서버구분코드	string	N	1	"0"(Default)
RSVN_ORD_RCIT_DT	예약주문접수일자	string	N	8	tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용
ORD_DVSN	주문구분	string	N	20	<description>tr_id가 TTTT3014U(미국 예약 매수 주문)인 경우만 사용
00 : 지정가
35 : TWAP
36 : VWAP

tr_id가 TTTT3016U(미국 예약 매도 주문)인 경우만 사용
00 : 지정가
31 : MOO(장개시시장가)
35 : TWAP
36 : VWAP</description>
OVRS_RSVN_ODNO	해외예약주문번호	string	N	10	tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약 주문)인 경우만 사용
ALGO_ORD_TMD_DVSN_CD	알고리즘주문시간구분코드	string	N	2	<description>※ TWAP, VWAP 주문에서만 사용. 예약주문은 시간입력 불가하여 02로 값 고정
※ 정규장 종료 10분전까지 가능</description>
    def request_stock_reserve_quote(self):
        """해외주식 예약주문접수

        """
        pass

url: /uapi/overseas-stock/v1/trading/order-resv-ccnl
tr_id: 실전[TTTT3017U (미국 예약주문 취소·정정), VTTT3017U (아시아국가 미제외)], 모의[VTTT3017U (아시아국가 미제외)]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
RSYN_ORD_RCIT_DT	해외주문접수일자	string	Y	8	
OVRS_RSVN_ODNO	해외예약주문번호	string	Y	10	해외주식_예약주문접수 API Output ODNO(주문번호) 참고
    def request_stock_reserve_quote_correction(self):
        """해외주식 예약주문접수취소

        """
        pass

url: /uapi/overseas-stock/v1/trading/inquire-psamount
tr_id: 실전[TTTS3007R], 모의[VTTS3007R]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
OVRS_EXCG_CD	해외거래소코드	string	Y	4	<description>NASD : 나스닥 / NYSE : 뉴욕 / AMEX : 아멕스
SEHK : 홍콩 / SHAA : 중국상해 / SZAA : 중국심천
TKSE : 일본 / HASE : 하노이거래소 / VNSE : 호치민거래소</description>
OVRS_ORD_UNPR	해외주문단가	string	Y	27	해외주문단가 (23.8) 정수부분 23자리, 소수부분 8자리
ITEM_CD	종목코드	string	Y	12	종목코드
    def get_buy_tradable_amount(self):
        """해외주식 매수가능금액조회

        """
        pass

url: /uapi/overseas-stock/v1/trading/inquire-nccs
tr_id: 실전[TTTS3018R], 모의[모의투자 미지원]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
OVRS_EXCG_CD	해외거래소코드	string	Y	4	<description>NASD : 나스닥
NYSE : 뉴욕 
AMEX : 아멕스
SEHK : 홍콩
SHAA : 중국상해
SZAA : 중국심천
TKSE : 일본
HASE : 베트남 하노이
VNSE : 베트남 호치민

* NASD 인 경우만 미국전체로 조회되며 나머지 거래소 코드는 해당 거래소만 조회됨
* 공백 입력 시 다음조회가 불가능하므로, 반드시 거래소코드 입력해야 함</description>
SORT_SQN	정렬순서	string	Y	2	<description>DS : 정순
그외 : 역순

[header tr_id: TTTS3018R]
""(공란)</description>
CTX_AREA_FK200	연속조회검색조건200	string	Y	200	공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
CTX_AREA_NK200	연속조회키200	string	Y	200	공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)
    def get_stock_not_conclusion_history(self):
        """해외주식 미체결내역

        """
        pass

url: /uapi/overseas-stock/v1/trading/inquire-balance
tr_id: 실전[TTTS3012R], 모의[VTTS3012R]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
OVRS_EXCG_CD	해외거래소코드	string	Y	4	<description>[모의]
NASD : 나스닥
NYSE : 뉴욕 
AMEX : 아멕스

[실전]
NASD : 미국전체
NAS : 나스닥
NYSE : 뉴욕 
AMEX : 아멕스

[모의/실전 공통]
SEHK : 홍콩
SHAA : 중국상해
SZAA : 중국심천
TKSE : 일본
HASE : 베트남 하노이
VNSE : 베트남 호치민</description>
TR_CRCY_CD	거래통화코드	string	Y	3	<description>USD : 미국달러
HKD : 홍콩달러
CNY : 중국위안화
JPY : 일본엔화
VND : 베트남동</description>
CTX_AREA_FK200	연속조회검색조건200	string	Y	200	공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
CTX_AREA_NK200	연속조회키200	string	Y	200	공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)
    def get_stock_balance(self):
        """해외주식 잔고

        """
        pass

url: /uapi/overseas-stock/v1/trading/inquire-ccnl
tr_id: 실전[TTTS3035R], 모의[VTTS3035R]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
PDNO	상품번호	string	Y	12	전종목일 경우 "%" 입력 ※ 모의투자계좌의 경우 ""(전체 조회)만 가능
ORD_STRT_DT	주문시작일자	string	Y	8	 YYYYMMDD 형식 (현지시각 기준)
ORD_END_DT	주문종료일자	string	Y	8	 YYYYMMDD 형식 (현지시각 기준)
SLL_BUY_DVSN	매도매수구분	string	Y	2	00 : 전체 01 : 매도  02 : 매수 ※ 모의투자계좌의 경우 "00"(전체 조회)만 가능
CCLD_NCCS_DVSN	체결미체결구분	string	Y	2	00 : 전체  01 : 체결  02 : 미체결 ※ 모의투자계좌의 경우 "00"(전체 조회)만 가능
OVRS_EXCG_CD	해외거래소코드	string	Y	4	<description>전종목일 경우 "%" 입력
NASD : 미국시장 전체(나스닥, 뉴욕, 아멕스)
NYSE : 뉴욕
AMEX : 아멕스
SEHK : 홍콩 
SHAA : 중국상해
SZAA : 중국심천
TKSE : 일본
HASE : 베트남 하노이
VNSE : 베트남 호치민
※ 모의투자계좌의 경우 ""(전체 조회)만 가능</description>
SORT_SQN	정렬순서	string	Y	2	<description>DS : 정순
AS : 역순 
※ 모의투자계좌의 경우 정렬순서 사용불가(Default : DS(정순))</description>
ORD_DT	주문일자	string	Y	8	"" (Null 값 설정)
ORD_GNO_BRNO	주문채번지점번호	string	Y	5	"" (Null 값 설정)
ODNO	주문번호	string	Y	10	<description>"" (Null 값 설정)
※ 주문번호로 검색 불가능합니다. 반드시 ""(Null 값 설정) 바랍니다.</description>
CTX_AREA_NK200	연속조회키200	string	Y	200	공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)
CTX_AREA_FK200	연속조회검색조건200	string	Y	200	공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
    def get_stock_conclusion_history(self):
        """해외주식 주문체결내역

        """
        pass

url: /uapi/overseas-stock/v1/trading/inquire-present-balance
tr_id: 실전[CTRP6504R], 모의[VTRP6504R]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
WCRC_FRCR_DVSN_CD	원화외화구분코드	string	Y	2	01 : 원화  02 : 외화
NATN_CD	국가코드	string	Y	3	<description>000 전체
840 미국
344 홍콩
156 중국
392 일본
704 베트남</description>
TR_MKET_CD	거래시장코드	string	Y	2	<description>[Request body NATN_CD 000 설정]
00 : 전체

[Request body NATN_CD 840 설정]
00 : 전체
01 : 나스닥(NASD)
02 : 뉴욕거래소(NYSE)
03 : 미국(PINK SHEETS)
04 : 미국(OTCBB)
05 : 아멕스(AMEX)

[Request body NATN_CD 156 설정]
00 : 전체
01 : 상해B
02 : 심천B
03 : 상해A
04 : 심천A

[Request body NATN_CD 392 설정]
01 : 일본

[Request body NATN_CD 704 설정]
01 : 하노이거래
02 : 호치민거래소

[Request body NATN_CD 344 설정]
01 : 홍콩
02 : 홍콩CNY
03 : 홍콩USD</description>
INQR_DVSN_CD	조회구분코드	string	Y	2	00 : 전체  01 : 일반해외주식  02 : 미니스탁
    def get_current_balance_by_conclusion(self):
        """해외주식 체결기준현재잔고

        """
        pass

url: /uapi/overseas-stock/v1/trading/order-resv-list
tr_id: 실전[(미국) TTTT3039R (일본/중국/홍콩/베트남) TTTS3014R], 모의[모의투자 미지원]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
INQR_STRT_DT	조회시작일자	string	Y	8	조회시작일자(YYYYMMDD)
INQR_END_DT	조회종료일자	string	Y	8	조회종료일자(YYYYMMDD)
INQR_DVSN_CD	조회구분코드	string	Y	2	00 : 전체 01 : 일반해외주식  02 : 미니스탁
PRDT_TYPE_CD	상품유형코드	string	Y	3	<description>[tr_id=TTTT3039R인 경우]
공백 입력 시 미국주식 전체조회
[tr_id=TTTS3014R인 경우]
공백 입력 시 아시아주식 전체조회

512 : 미국 나스닥 / 513 : 미국 뉴욕거래소 / 529 : 미국 아멕스 
515 : 일본
501 : 홍콩 / 543 : 홍콩CNY / 558 : 홍콩USD
507 : 베트남 하노이거래소 / 508 : 베트남 호치민거래소
551 : 중국 상해A / 552 : 중국 심천A</description>
OVRS_EXCG_CD	해외거래소코드	string	Y	4	<description>[tr_id=TTTT3039R인 경우]
공백 입력 시 미국주식 전체조회
[tr_id=TTTS3014R인 경우]
공백 입력 시 아시아주식 전체조회

NASD : 나스닥 / NYSE : 뉴욕 / AMEX : 아멕스
SEHK : 홍콩 / SHAA : 중국상해 / SZAA : 중국심천
TKSE : 일본 / HASE : 하노이거래소 / VNSE : 호치민거래소</description>
CTX_AREA_FK200	연속조회검색조건200	string	Y	200	공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
CTX_AREA_NK200	연속조회키200	string	Y	200	공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)
    def get_reserve_orders(self):
        """해외주식 예약주문조회

        """
        pass

url: /uapi/overseas-stock/v1/trading/inquire-paymt-stdr-balance
tr_id: 실전[CTRP6010R], 모의[모의투자 미지원]
arguments:
CANO	종합계좌번호	string	Y	8	 
ACNT_PRDT_CD	계좌상품코드	string	Y	2	 
BASS_DT	기준일자	string	Y	8	 
WCRC_FRCR_DVSN_CD	원화외화구분코드	string	Y	2	01(원화기준),02(외화기준)
INQR_DVSN_CD	조회구분코드	string	Y	2	00(전체), 01(일반), 02(미니스탁)
    def get_balance_by_settlement(self):
        """해외주식 결제기준잔고

        """
        pass

url: /uapi/overseas-stock/v1/trading/inquire-period-trans
tr_id: 실전[CTOS4001R], 모의[모의투자 미지원]
arguments:
CANO	종합계좌번호	string	Y	8	 
ACNT_PRDT_CD	계좌상품코드	string	Y	2	 
ERLM_STRT_DT	등록시작일자	string	Y	8	입력날짜 ~ (ex) 20240420)
ERLM_END_DT	등록종료일자	string	Y	8	~입력날짜 (ex) 20240520)
OVRS_EXCG_CD	해외거래소코드	string	Y	4	공백
PDNO	상품번호	string	Y	12	공백 (전체조회), 개별종목 조회는 상품번호입력
SLL_BUY_DVSN_CD	매도매수구분코드	string	Y	2	00(전체), 01(매도), 02(매수)
LOAN_DVSN_CD	대출구분코드	string	Y	2	공백
CTX_AREA_FK100	연속조회검색조건100	string	Y	100	공백
CTX_AREA_NK100	연속조회키100	string	Y	100	공백
    def get_daily_transaction_history(self):
        """해외주식 일별거래내역

        """
        pass

url: /uapi/overseas-stock/v1/trading/inquire-period-profit
tr_id: 실전[TTTS3039R], 모의[모의투자 미지원]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
OVRS_EXCG_CD	해외거래소코드	string	Y	2	공란 : 전체,  NASD : 미국, SEHK : 홍콩, SHAA : 중국, TKSE : 일본, HASE : 베트남
NATN_CD	국가코드	string	Y	2	공란(Default)
CRCY_CD	통화코드	string	Y	2	공란 : 전체 USD : 미국달러, HKD : 홍콩달러, CNY : 중국위안화,  JPY : 일본엔화, VND : 베트남동
PDNO	상품번호	string	Y	2	공란 : 전체
INQR_STRT_DT	조회시작일자	string	Y	2	YYYYMMDD
INQR_END_DT	조회종료일자	string	Y	2	YYYYMMDD
WCRC_FRCR_DVSN_CD	원화외화구분코드	string	Y	2	01 : 외화, 02 : 원화
CTX_AREA_FK200	연속조회검색조건200	string	Y	2	 
CTX_AREA_NK200	연속조회키200	string	Y	2	 
    def get_period_profit_loss(self):
        """해외주식 기간손익

        """
        pass

url: /uapi/overseas-stock/v1/trading/foreign-margin
tr_id: 실전[TTTC2101R], 모의[모의투자 미지원]
arguments:
CANO	종합계좌번호	string	Y	8
ACNT_PRDT_CD	계좌상품코드 	string	Y	2
    def get_margin_aggregate(self):
        """
        해외증거금 통합변조회

        """
        pass

url: /uapi/overseas-stock/v1/trading/daytime-order
tr_id: 실전[(주간매수) TTTS6036U (주간매도) TTTS6037U], 모의[모의투자 미지원]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
OVRS_EXCG_CD	해외거래소코드	string	Y	4	NASD:나스닥 / NYSE:뉴욕 / AMEX:아멕스
PDNO	상품번호	string	Y	12	종목코드
ORD_QTY	주문수량	string	Y	10	해외거래소 별 최소 주문수량 및 주문단위 확인 필요
OVRS_ORD_UNPR	해외주문단가	string	Y	32	소수점 포함, 1주당 가격 * 시장가의 경우 1주당 가격을 공란으로 비우지 않음 "0"으로 입력
CTAC_TLNO	연락전화번호	string	N	20	" "
MGCO_APTM_ODNO	운용사지정주문번호	string	N	12	" "
ORD_SVR_DVSN_CD	주문서버구분코드	string	Y	1	"0"
ORD_DVSN	주문구분	string	Y	2	[미국 매수/매도 주문]  00 : 지정가  * 주간거래는 지정가만 가능
    def request_order_after_day_time(self):
        """
        해외주식 미국주간주문

        """
        pass

url: /uapi/overseas-stock/v1/trading/daytime-order-rvsecncl
tr_id: 실전[TTTS6038U], 모의[모의투자 미지원]
arguments:
CANO	종합계좌번호	string	Y	8	계좌번호 체계(8-2)의 앞 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	계좌번호 체계(8-2)의 뒤 2자리
OVRS_EXCG_CD	해외거래소코드	string	Y	4	NASD:나스닥 / NYSE:뉴욕 / AMEX:아멕스
PDNO	상품번호	string	Y	12	종목코드
ORGN_ODNO	원주문번호	string	Y	10	'정정 또는 취소할 원주문번호(매매 TR의 주문번호) - 해외주식 주문체결내역api (/uapi/overseas-stock/v1/trading/inquire-nccs)에서 odno(주문번호) 참조'
RVSE_CNCL_DVSN_CD	정정취소구분코드	string	Y	2	'01 : 정정  02 : 취소'
ORD_QTY	주문수량	string	Y	10	 
OVRS_ORD_UNPR	해외주문단가	string	Y	32	소수점 포함, 1주당 가격
CTAC_TLNO	연락전화번호	string	Y	20	" "
MGCO_APTM_ODNO	운용사지정주문번호	string	Y	12	" "
ORD_SVR_DVSN_CD	주문서버구분코드	string	Y	1	"0"
    def correct_cancel_after_day_time(self):
        """
        해외주식 미국주간정정취소

        """
        pass

url: /uapi/overseas-stock/v1/trading/algo-ordno
tr_id: 실전[TTTS6058R], 모의[모의투자 미지원]
arguments:
TRAD_DT	거래일자	string	Y	8	YYYYMMDD
CANO	계좌번호	string	Y	8	종합계좌번호 (8자리)
ACNO_PRDT_CD	계좌상품코드	string	Y	2	계좌상품코드 (2자리) : 주식계좌는 01
CTX_AREA_NK200	연속조회키200	string	N	200	
CTX_AREA_FK200	연속조회조건200	string	N	200	
    def get_limit_order_number(self):
        """
        해외주식 지정가주문번호조회

        """
        pass

url: /uapi/overseas-stock/v1/trading/inquire-algo-ccnl
tr_id: 실전[TTTS6059R], 모의[모의투자 미지원]
arguments:
CANO	계좌번호	string	Y	8	종합계좌번호 8자리
ACNT_PRDT_CD	계좌상품코드	string	Y	2	상품코드 2자리 (주식계좌 : 01)
ORD_DT	주문일자	string	Y	8	주문일자 (YYYYMMDD)
ORD_GNO_BRNO	주문채번지점번호	string	N	5	
ODNO	주문번호	string	Y	10	지정가주문번호 (TTTC6058R)에서 조회된 주문번호 입력
TTLZ_ICLD_YN	집계포함여부	string	N	1	
CTX_AREA_NK200	연속조회키200	string	N	200	연속조회 시 사용
CTX_AREA_FK200	연속조회조건200	string	N	200	연속조회 시 사용
    def get_limit_order_execution_history(self):
        """
        해외주식 지정가체결내역조회

        """
        pass
