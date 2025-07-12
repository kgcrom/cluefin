class DometicCreditOrder:
    pass


# 신용 매수주문	kt10006	order_credit_buy
# dmst_stex_tp	국내거래소구분	String	Y	3	KRX,NXT,SOR
# stk_cd	종목코드	String	Y	12
# ord_qty	주문수량	String	Y	12
# ord_uv	주문단가	String	N	12
# trde_tp	매매구분	String	Y	2	0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)
# cond_uv	조건단가	String	N	12

# 신용 매도주문	kt10007	order_credit_sell
# dmst_stex_tp	국내거래소구분	String	Y	3	KRX,NXT,SOR
# stk_cd	종목코드	String	Y	12
# ord_qty	주문수량	String	Y	12
# ord_uv	주문단가	String	N	12
# trde_tp	매매구분	String	Y	2	0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)
# crd_deal_tp	신용거래구분	String	Y	2	33:융자 , 99:융자합
# crd_loan_dt	대출일	String	N	8	YYYYMMDD(융자일경우필수)
# cond_uv	조건단가	String	N	12

# 신용 정정주문	kt10008	modify_credit_order
# dmst_stex_tp	국내거래소구분	String	Y	3	KRX,NXT,SOR
# orig_ord_no	원주문번호	String	Y	7
# stk_cd	종목코드	String	Y	12
# mdfy_qty	정정수량	String	Y	12
# mdfy_uv	정정단가	String	Y	12
# mdfy_cond_uv	정정조건단가	String	N	12

# 신용 취소주문	kt10009	cancel_credit_order
# dmst_stex_tp	국내거래소구분	String	Y	3	KRX,NXT,SOR
# orig_ord_no	원주문번호	String	Y	7
# stk_cd	종목코드	String	Y	12
# cncl_qty	취소수량	String	Y	12	'0' 입력시 잔량 전부 취소
