from typing import Sequence

from pydantic import BaseModel, Field

from cluefin_openapi.kis._model import KisHttpBody


class ProductBasicInfoItem(BaseModel):
    pdno: str = Field(title="상품번호")
    prdt_type_cd: str = Field(title="상품유형코드")
    prdt_name: str = Field(title="상품명")
    prdt_name120: str = Field(title="상품명120")
    prdt_abrv_name: str = Field(title="상품약어명")
    prdt_eng_name: str = Field(title="상품영문명")
    prdt_eng_name120: str = Field(title="상품영문명120")
    prdt_eng_abrv_name: str = Field(title="상품영문약어명")
    std_pdno: str = Field(title="표준상품번호")
    shtn_pdno: str = Field(title="단축상품번호")
    prdt_sale_stat_cd: str = Field(title="상품판매상태코드")
    prdt_risk_grad_cd: str = Field(title="상품위험등급코드")
    prdt_clsf_cd: str = Field(title="상품분류코드")
    prdt_clsf_name: str = Field(title="상품분류명")
    sale_strt_dt: str = Field(title="판매시작일자")
    sale_end_dt: str = Field(title="판매종료일자")
    wrap_asst_type_cd: str = Field(title="랩어카운트자산유형코드")
    ivst_prdt_type_cd: str = Field(title="투자상품유형코드")
    ivst_prdt_type_cd_name: str = Field(title="투자상품유형코드명")
    frst_erlm_dt: str = Field(title="최초등록일자")


class ProductBasicInfo(BaseModel, KisHttpBody):
    """상품기본조회"""

    output: ProductBasicInfoItem = Field(title="응답상세")


class StockBasicInfoItem(BaseModel):
    pdno: str = Field(title="상품번호")
    prdt_type_cd: str = Field(title="상품유형코드")
    mket_id_cd: str = Field(
        title="시장ID코드",
        description="AGR.농축산물파생\nBON.채권파생\nCMD.일반상품시장\nCUR.통화파생\nENG.에너지파생\nEQU.주식파생\nETF.ETF파생\nIRT.금리파생\nKNX.코넥스\nKSQ.코스닥\nMTL.금속파생\nSPI.주가지수파생\nSTK.유가증권",
    )
    scty_grp_id_cd: str = Field(
        title="증권그룹ID코드",
        description="BC.수익증권\nDR.주식예탁증서\nEF.ETF\nEN.ETN\nEW.ELW\nFE.해외ETF\nFO.선물옵션\nFS.외국주권\nFU.선물\nFX.플렉스 선물\nGD.금현물\nIC.투자계약증권\nIF.사회간접자본투융자회사\nKN.코넥스주권\nMF.투자회사\nOP.옵션\nRT.부동산투자회사\nSC.선박투자회사\nSR.신주인수권증서\nST.주권\nSW.신주인수권증권\nTC.신탁수익증권",
    )
    excg_dvsn_cd: str = Field(
        title="거래소구분코드",
        description="01.한국증권\n02.증권거래소\n03.코스닥\n04.K-OTC\n05.선물거래소\n06.CME\n07.EUREX\n21.금현물\n50.미국주간\n51.홍콩\n52.상해B\n53.심천\n54.홍콩거래소\n55.미국\n56.일본\n57.상해A\n58.심천A\n59.베트남\n61.장전시간외시장\n64.경쟁대량매매\n65.경매매시장\n81.시간외단일가시장",
    )
    setl_mmdd: str = Field(title="결산월일")
    lstg_stqt: str = Field(title="상장주수")
    lstg_cptl_amt: str = Field(title="상장자본금액")
    cpta: str = Field(title="자본금")
    papr: str = Field(title="액면가")
    issu_pric: str = Field(title="발행가격")
    kospi200_item_yn: str = Field(title="코스피200종목여부")
    scts_mket_lstg_dt: str = Field(title="유가증권시장상장일자")
    scts_mket_lstg_abol_dt: str = Field(title="유가증권시장상장폐지일자")
    kosdaq_mket_lstg_dt: str = Field(title="코스닥시장상장일자")
    kosdaq_mket_lstg_abol_dt: str = Field(title="코스닥시장상장폐지일자")
    frbd_mket_lstg_dt: str = Field(title="프리보드시장상장일자")
    frbd_mket_lstg_abol_dt: str = Field(title="프리보드시장상장폐지일자")
    reits_kind_cd: str = Field(title="리츠종류코드")
    etf_dvsn_cd: str = Field(title="ETF구분코드")
    oilf_fund_yn: str = Field(title="유전펀드여부")
    idx_bztp_lcls_cd: str = Field(title="지수업종대분류코드")
    idx_bztp_mcls_cd: str = Field(title="지수업종중분류코드")
    idx_bztp_scls_cd: str = Field(title="지수업종소분류코드")
    stck_kind_cd: str = Field(
        title="주식종류코드",
        description="000.해당사항없음\n101.보통주\n201.우선주\n202.2우선주\n203.3우선주\n204.4우선주\n205.5우선주\n206.6우선주\n207.7우선주\n208.8우선주\n209.9우선주\n210.10우선주\n211.11우선주\n212.12우선주\n213.13우선주\n214.14우선주\n215.15우선주\n216.16우선주\n217.17우선주\n218.18우선주\n219.19우선주\n220.20우선주\n301.후배주\n401.혼합주",
    )
    mfnd_opng_dt: str = Field(title="뮤추얼펀드개시일자")
    mfnd_end_dt: str = Field(title="뮤추얼펀드종료일자")
    dpsi_erlm_cncl_dt: str = Field(title="예탁등록취소일자")
    etf_cu_qty: str = Field(title="ETFCU수량")
    prdt_name: str = Field(title="상품명")
    prdt_name120: str = Field(title="상품명120")
    prdt_abrv_name: str = Field(title="상품약어명")
    std_pdno: str = Field(title="표준상품번호")
    prdt_eng_name: str = Field(title="상품영문명")
    prdt_eng_name120: str = Field(title="상품영문명120")
    prdt_eng_abrv_name: str = Field(title="상품영문약어명")
    dpsi_aptm_erlm_yn: str = Field(title="예탁지정등록여부")
    etf_txtn_type_cd: str = Field(title="ETF과세유형코드")
    etf_type_cd: str = Field(title="ETF유형코드")
    lstg_abol_dt: str = Field(title="상장폐지일자")
    nwst_odst_dvsn_cd: str = Field(title="신주구주구분코드")
    sbst_pric: str = Field(title="대용가격")
    thco_sbst_pric: str = Field(title="당사대용가격")
    thco_sbst_pric_chng_dt: str = Field(title="당사대용가격변경일자")
    tr_stop_yn: str = Field(title="거래정지여부")
    admn_item_yn: str = Field(title="관리종목여부")
    thdt_clpr: str = Field(title="당일종가")
    bfdy_clpr: str = Field(title="전일종가")
    clpr_chng_dt: str = Field(title="종가변경일자")
    std_idst_clsf_cd: str = Field(title="표준산업분류코드")
    std_idst_clsf_cd_name: str = Field(title="표준산업분류코드명", description="표준산업소분류코드")
    idx_bztp_lcls_cd_name: str = Field(
        title="지수업종대분류코드명",
        description="표준산업대분류코드\n00\t해당사항없음\n01\t농업, 임업 및 어업\n02\t광업\n03\t제조업\n04\t전기, 가스, 증기 및 수도사업\n05\t하수-폐기물 처리, 원료재생 및환경복원업\n06\t건설업\n07\t도매 및 소매업\n08\t운수업\n09\t숙박 및 음식점업\n10\t출판, 영상, 방송통신 및 정보서비스업\n11\t금융 및 보험업\n12\t부동산업 및 임대업\n13\t전문, 과학 및 기술 서비스업\n14\t사업시설관리 및 사업지원서비스업\n15\t공공행정, 국방 및 사회보장 행정\n16\t교육 서비스업\n17\t보건업 및 사회복지 서비스업\n18\t예술, 스포츠 및 여가관련 서비스업\n19\t협회 및 단체, 수리 및 기타 개인 서비스업\n20\t가구내 고용활동 및 달리 분류되지 않은 자가소비생산활동\n21\t국제 및 외국기관",
    )
    idx_bztp_mcls_cd_name: str = Field(
        title="지수업종중분류코드명",
        description="표준산업중분류코드\n0000\t해당사항없음\n0101\t농업\n0102\t임업\n0103\t어업\n0205\t석탄, 원유 및 천연가스 광업\n0206\t금속 광업\n0207\t비금속광물 광업; 연료용 제외\n0208\t광업 지원 서비스업\n0310\t식료품 제조업\n0311\t음료 제조업\n0312\t담배 제조업\n0313\t섬유제품 제조업; 의복제외\n0314\t의복, 의복액세서리 및 모피제품제조업\n0315\t가죽, 가방 및 신발 제조업\n0316\t목재 및 나무제품 제조업;가구제외\n0317\t펄프, 종이 및 종이제품 제조업\n0318\t인쇄 및 기록매체 복제업\n0319\t코크스, 연탄 및 석유정제품 제조업\n0320\t화학물질 및 화학제품 제조업;의약품 제외\n0321\t의료용 물질 및 의약품 제조업\n0322\t고무제품 및 플라스틱제품 제조업\n0323\t비금속 광물제품 제조업\n0324\t1차 금속 제조업\n0325\t금속가공제품 제조업;기계 및가구 제외\n0326\t전자부품, 컴퓨터, 영상, 음향 및 통신장비 제조업\n0327\t의료, 정밀, 광학기기 및 시계 제조업\n0328\t전기장비 제조업\n0329\t기타 기계 및 장비 제조업\n0330\t자동차 및 트레일러 제조업\n0331\t기타 운송장비 제조업\n0332\t가구 제조업\n0333\t기타 제품 제조업\n0435\t전기, 가스, 증기 및 공기조절 공급업\n0436\t수도사업\n0537\t하수, 폐수 및 분뇨 처리업\n0538\t폐기물 수집운반, 처리 및 원료재생업\n0539\t환경 정화 및 복원업\n0641\t종합 건설업\n0642\t전문직별 공사업\n0745\t자동차 및 부품 판매업\n0746\t도매 및 상품중개업\n0747\t소매업; 자동차 제외\n0849\t육상운송 및 파이프라인 운송업\n0850\t수상 운송업\n0851\t항공 운송업\n0852\t창고 및 운송관련 서비스업\n0955\t숙박업\n0956\t음식점 및 주점업\n1058\t출판업\n1059\t영상·오디오 기록물 제작 및 배급업\n1060\t방송업\n1061\t통신업\n1062\t컴퓨터 프로그래밍, 시스템 통합및 관리업\n1063\t정보서비스업\n1164\t금융업\n1165\t보험 및 연금업\n1166\t금융 및 보험 관련 서비스업\n1268\t부동산업\n1269\t임대업;부동산 제외\n1370\t연구개발업\n1371\t전문서비스업\n1372\t건축기술, 엔지니어링 및 기타과학기술 서비스업\n1373\t기타 전문, 과학 및 기술 서비스업\n1474\t사업시설 관리 및 조경 서비스업\n1475\t사업지원 서비스업\n1584\t공공행정, 국방 및 사회보장 행정\n1685\t교육 서비스업\n1786\t보건업\n1787\t사회복지 서비스업\n1890\t창작, 예술 및 여가관련 서비스업\n1891\t스포츠 및 오락관련 서비스업\n1994\t협회 및 단체\n1995\t수리업\n1996\t기타 개인 서비스업\n2097\t가구내 고용활동\n2098\t달리 분류되지 않은 자가소비를 위한가구의 재화 및 서비스 생산활동\n2199\t국제 및 외국기관",
    )
    idx_bztp_scls_cd_name: str = Field(title="지수업종소분류코드명")
    ocr_no: str = Field(title="OCR번호")
    crfd_item_yn: str = Field(title="크라우드펀딩종목여부")
    elec_scty_yn: str = Field(title="전자증권여부")
    issu_istt_cd: str = Field(title="발행기관코드")
    etf_chas_erng_rt_dbnb: str = Field(title="ETF추적수익율배수")
    etf_etn_ivst_heed_item_yn: str = Field(title="ETFETN투자유의종목여부")
    stln_int_rt_dvsn_cd: str = Field(title="대주이자율구분코드")
    frnr_psnl_lmt_rt: str = Field(title="외국인개인한도비율")
    lstg_rqsr_issu_istt_cd: str = Field(title="상장신청인발행기관코드")
    lstg_rqsr_item_cd: str = Field(title="상장신청인종목코드")
    trst_istt_issu_istt_cd: str = Field(title="신탁기관발행기관코드")
    cptt_trad_tr_psbl_yn: str = Field(title="NXT 거래종목여부", description="NXT 거래가능한 종목은 Y, 그 외 종목은 N")
    nxt_tr_stop_yn: str = Field(
        title="NXT 거래정지여부",
        description="NXT 거래종목 중 거래정지가 된 종목은 Y, 그 외 모든 종목은 N",
    )


class StockBasicInfo(BaseModel, KisHttpBody):
    """주식기본조회"""

    output: StockBasicInfoItem = Field(title="응답상세")


class BalanceSheetItem(BaseModel):
    stac_yymm: str = Field(title="결산 년월")
    cras: str = Field(title="유동자산")
    fxas: str = Field(title="고정자산")
    total_aset: str = Field(title="자산총계")
    flow_lblt: str = Field(title="유동부채")
    fix_lblt: str = Field(title="고정부채")
    total_lblt: str = Field(title="부채총계")
    cpfn: str = Field(title="자본금")
    cfp_surp: str = Field(title="자본 잉여금", description="출력되지 않는 데이터(99.99 로 표시)")
    prfi_surp: str = Field(title="이익 잉여금", description="출력되지 않는 데이터(99.99 로 표시)")
    total_cptl: str = Field(title="자본총계")


class BalanceSheet(BaseModel, KisHttpBody):
    """국내주식 대차대조표"""

    output: Sequence[BalanceSheetItem] = Field(default_factory=list)


class IncomeStatementItem(BaseModel):
    stac_yymm: str = Field(title="결산 년월")
    sale_account: str = Field(title="매출액")
    sale_cost: str = Field(title="매출 원가")
    sale_totl_prfi: str = Field(title="매출 총 이익")
    depr_cost: str = Field(title="감가상각비", description="출력되지 않는 데이터(99.99 로 표시)")
    sell_mang: str = Field(title="판매 및 관리비", description="출력되지 않는 데이터(99.99 로 표시)")
    bsop_prti: str = Field(title="영업 이익")
    bsop_non_ernn: str = Field(title="영업 외 수익", description="출력되지 않는 데이터(99.99 로 표시)")
    bsop_non_expn: str = Field(title="영업 외 비용", description="출력되지 않는 데이터(99.99 로 표시)")
    op_prfi: str = Field(title="경상 이익")
    spec_prfi: str = Field(title="특별 이익")
    spec_loss: str = Field(title="특별 손실")
    thtr_ntin: str = Field(title="당기순이익")


class IncomeStatement(BaseModel, KisHttpBody):
    """국내주식 손익계산서"""

    output: Sequence[IncomeStatementItem] = Field(default_factory=list)


class FinancialRatioItem(BaseModel):
    stac_yymm: str = Field(title="결산 년월")
    grs: str = Field(title="매출액 증가율")
    bsop_prfi_inrt: str = Field(title="영업 이익 증가율")
    ntin_inrt: str = Field(title="순이익 증가율")
    roe_val: str = Field(title="ROE 값")
    eps: str = Field(title="EPS")
    sps: str = Field(title="주당매출액")
    bps: str = Field(title="BPS")
    rsrv_rate: str = Field(title="유보 비율")
    lblt_rate: str = Field(title="부채 비율")


class FinancialRatio(BaseModel, KisHttpBody):
    """국내주식 재무비율"""

    output: Sequence[FinancialRatioItem] = Field(default_factory=list)


class ProfitabilityRatioItem(BaseModel):
    stac_yymm: str = Field(title="결산 년월")
    cptl_ntin_rate: str = Field(title="총자본 순이익율")
    self_cptl_ntin_inrt: str = Field(title="자기자본 순이익율")
    sale_ntin_rate: str = Field(title="매출액 순이익율")
    sale_totl_rate: str = Field(title="매출액 총이익율")


class ProfitabilityRatio(BaseModel, KisHttpBody):
    """국내주식 수익성비율"""

    output: Sequence[ProfitabilityRatioItem] = Field(default_factory=list)


class OtherKeyRatioItem(BaseModel):
    stac_yymm: str = Field(title="결산 년월")
    payout_rate: str = Field(title="배당 성향")
    eva: str = Field(title="EVA")
    ebitda: str = Field(title="EBITDA")
    ev_ebitda: str = Field(title="EV_EBITDA")


class OtherKeyRatio(BaseModel, KisHttpBody):
    """국내주식 기타주요비율"""

    output: Sequence[OtherKeyRatioItem] = Field(default_factory=list)


class StabilityRatioItem(BaseModel):
    stac_yymm: str = Field(title="결산 년월")
    lblt_rate: str = Field(title="부채 비율")
    bram_depn: str = Field(title="차입금 의존도")
    crnt_rate: str = Field(title="유동 비율")
    quck_rate: str = Field(title="당좌 비율")


class StabilityRatio(BaseModel, KisHttpBody):
    """국내주식 안정성비율"""

    output: Sequence[StabilityRatioItem] = Field(default_factory=list)


class GrowthRatioItem(BaseModel):
    stac_yymm: str = Field(title="결산 년월")
    grs: str = Field(title="매출액 증가율")
    bsop_prfi_inrt: str = Field(title="영업 이익 증가율")
    equt_inrt: str = Field(title="자기자본 증가율")
    totl_aset_inrt: str = Field(title="총자산 증가율")


class GrowthRatio(BaseModel, KisHttpBody):
    """국내주식 성장성비율"""

    output: Sequence[GrowthRatioItem] = Field(default_factory=list)


class MarginTradableStocksItem(BaseModel):
    stck_shrn_iscd: str = Field(title="주식 단축 종목코드")
    hts_kor_isnm: str = Field(title="HTS 한글 종목명")
    crdt_rate: str = Field(title="신용 비율")


class MarginTradableStocks(BaseModel, KisHttpBody):
    """국내주식 당사 신용가능종목"""

    output: Sequence[MarginTradableStocksItem] = Field(default_factory=list)


class KsdDividendDecisionItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    divi_kind: str = Field(title="배당종류")
    face_val: str = Field(title="액면가")
    per_sto_divi_amt: str = Field(title="현금배당금")
    divi_rate: str = Field(title="현금배당률(%)")
    stk_divi_rate: str = Field(title="주식배당률(%)")
    divi_pay_dt: str = Field(title="배당금지급일")
    stk_div_pay_dt: str = Field(title="주식배당지급일")
    odd_pay_dt: str = Field(title="단주대금지급일")
    stk_kind: str = Field(title="주식종류")
    high_divi_gb: str = Field(title="고배당종목여부")


class KsdDividendDecision(BaseModel, KisHttpBody):
    """예탁원정보(배당결정)"""

    output1: Sequence[KsdDividendDecisionItem] = Field(default_factory=list)


class KsdStockDividendDecisionItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    stk_kind: str = Field(title="주식종류")
    opp_opi_rcpt_term: str = Field(title="반대의사접수시한")
    buy_req_rcpt_term: str = Field(title="매수청구접수시한")
    buy_req_price: str = Field(title="매수청구가격")
    buy_amt_pay_dt: str = Field(title="매수대금지급일")
    get_meet_dt: str = Field(title="주총일")


class KsdStockDividendDecision(BaseModel, KisHttpBody):
    """예탁원정보(주식배수청구결정)"""

    output1: Sequence[KsdStockDividendDecisionItem] = Field(default_factory=list)


class KsdMergerSplitDecisionItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    opp_cust_cd: str = Field(title="피합병(피분할)회사코드")
    opp_cust_nm: str = Field(title="피합병(피분할)회사명")
    cust_cd: str = Field(title="합병(분할)회사코드")
    cust_nm: str = Field(title="합병(분할)회사명")
    merge_type: str = Field(title="합병사유")
    merge_rate: str = Field(title="비율")
    td_stop_dt: str = Field(title="매매거래정지기간")
    list_dt: str = Field(title="상장/등록일")
    odd_amt_pay_dt: str = Field(title="단주대금지급일")
    tot_issue_stk_qty: str = Field(title="발행주식")
    issue_stk_qty: str = Field(title="발행할주식")
    seq: str = Field(title="연번")


class KsdMergerSplitDecision(BaseModel, KisHttpBody):
    """예탁원정보(합병/분할결정)"""

    output1: Sequence[KsdMergerSplitDecisionItem] = Field(default_factory=list)


class KsdParValueChangeDecisionItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    inter_bf_face_amt: str = Field(title="변경전액면가")
    inter_af_face_amt: str = Field(title="변경후액면가")
    td_stop_dt: str = Field(title="매매거래정지기간")
    list_dt: str = Field(title="상장/등록일")


class KsdParValueChangeDecision(BaseModel, KisHttpBody):
    """예탁원정보(액면교체결정)"""

    output1: Sequence[KsdParValueChangeDecisionItem] = Field(default_factory=list)


class KsdCapitalReductionScheduleItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    stk_kind: str = Field(title="주식종류")
    reduce_cap_type: str = Field(title="감자구분")
    reduce_cap_rate: str = Field(title="감자배정율")
    comp_way: str = Field(title="계산방법")
    td_stop_dt: str = Field(title="매매거래정지기간")
    list_dt: str = Field(title="상장/등록일")


class KsdCapitalReductionSchedule(BaseModel, KisHttpBody):
    """예탁원정보(자본감소일정)"""

    output1: Sequence[KsdCapitalReductionScheduleItem] = Field(default_factory=list)


class KsdListingInfoScheduleItem(BaseModel):
    list_dt: str = Field(title="상장/등록일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    stk_kind: str = Field(title="주식종류")
    issue_type: str = Field(title="사유")
    issue_stk_qty: str = Field(title="상장주식수")
    tot_issue_stk_qty: str = Field(title="총발행주식수")
    issue_price: str = Field(title="발행가")


class KsdListingInfoSchedule(BaseModel, KisHttpBody):
    """예탁원정보(상장정보일정)"""

    output1: Sequence[KsdListingInfoScheduleItem] = Field(default_factory=list)


class KsdIpoSubscriptionScheduleItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    fix_subscr_pri: str = Field(title="공모가")
    face_value: str = Field(title="액면가")
    subscr_dt: str = Field(title="청약기간")
    pay_dt: str = Field(title="납입일")
    refund_dt: str = Field(title="환불일")
    list_dt: str = Field(title="상장/등록일")
    lead_mgr: str = Field(title="주간사")
    pub_bf_cap: str = Field(title="공모전자본금")
    pub_af_cap: str = Field(title="공모후자본금")
    assign_stk_qty: str = Field(title="당사배정물량")


class KsdIpoSubscriptionSchedule(BaseModel, KisHttpBody):
    """예탁원정보(공모주청약일정)"""

    output1: Sequence[KsdIpoSubscriptionScheduleItem] = Field(default_factory=list)


class KsdForfeitedShareScheduleItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    subscr_dt: str = Field(title="청약일")
    subscr_price: str = Field(title="공모가")
    subscr_stk_qty: str = Field(title="공모주식수")
    refund_dt: str = Field(title="환불일")
    list_dt: str = Field(title="상장/등록일")
    lead_mgr: str = Field(title="주간사")


class KsdForfeitedShareSchedule(BaseModel, KisHttpBody):
    """예탁원정보(실권주일정)"""

    output1: Sequence[KsdForfeitedShareScheduleItem] = Field(default_factory=list)


class KsdDepositScheduleItem(BaseModel):
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    stk_qty: str = Field(title="주식수")
    depo_date: str = Field(title="예치일")
    depo_reason: str = Field(title="사유")
    tot_issue_qty_per_rate: str = Field(title="총발행주식수대비비율(%)")


class KsdDepositSchedule(BaseModel, KisHttpBody):
    """예탁원정보(입무예치일정)"""

    output1: Sequence[KsdDepositScheduleItem] = Field(default_factory=list)


class KsdPaidInCapitalIncreaseScheduleItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    tot_issue_stk_qty: str = Field(title="발행주식")
    issue_stk_qty: str = Field(title="발행할주식")
    fix_rate: str = Field(title="확정배정율")
    disc_rate: str = Field(title="할인율")
    fix_price: str = Field(title="발행예정가")
    right_dt: str = Field(title="권리락일")
    sub_term_ft: str = Field(title="청약기간")
    sub_term: str = Field(title="청약기간")
    list_date: str = Field(title="상장/등록일")
    stk_kind: str = Field(title="주식종류")


class KsdPaidInCapitalIncreaseSchedule(BaseModel, KisHttpBody):
    """예탁원정보(유상증자일정)"""

    # 공식 문서는 output이지만 실서버는 output1로 응답한다(실측).
    output1: Sequence[KsdPaidInCapitalIncreaseScheduleItem] = Field(default_factory=list)


class KsdStockDividendScheduleItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    fix_rate: str = Field(title="확정배정율")
    odd_rec_price: str = Field(title="단주기준가")
    right_dt: str = Field(title="권리락일")
    odd_pay_dt: str = Field(title="단주대금지급일")
    list_date: str = Field(title="상장/등록일")
    tot_issue_stk_qty: str = Field(title="발행주식")
    issue_stk_qty: str = Field(title="발행할주식")
    stk_kind: str = Field(title="주식종류")


class KsdStockDividendSchedule(BaseModel, KisHttpBody):
    """예탁원정보(무상증자일정)"""

    output1: Sequence[KsdStockDividendScheduleItem] = Field(default_factory=list)


class KsdShareholderMeetingScheduleItem(BaseModel):
    record_date: str = Field(title="기준일")
    sht_cd: str = Field(title="종목코드")
    isin_name: str = Field(title="종목명")
    gen_meet_dt: str = Field(title="주총일자")
    gen_meet_type: str = Field(title="주총사유")
    agenda: str = Field(title="주총의안")
    vote_tot_qty: str = Field(title="의결권주식총수")


class KsdShareholderMeetingSchedule(BaseModel, KisHttpBody):
    """예탁원정보(주주총회일정)"""

    output1: Sequence[KsdShareholderMeetingScheduleItem] = Field(default_factory=list)


class EstimatedEarningsItem1(BaseModel):
    sht_cd: str = Field(title="ELW단축종목코드")
    item_kor_nm: str = Field(title="HTS한글종목명")
    name1: str = Field(title="ELW현재가")
    name2: str = Field(title="전일대비")
    estdate: str = Field(title="전일대비부호")
    rcmd_name: str = Field(title="전일대비율")
    capital: str = Field(title="누적거래량")
    forn_item_lmtrt: str = Field(title="행사가")


class EstimatedEarningsItem2(BaseModel):
    data1: str = Field(title="DATA1")
    data2: str = Field(title="DATA2")
    data3: str = Field(title="DATA3")
    data4: str = Field(title="DATA4")
    data5: str = Field(title="DATA5")


class EstimatedEarningsItem3(BaseModel):
    data1: str = Field(title="DATA1", description="결산연월(outblock4) 참조")
    data2: str = Field(title="DATA2", description="결산연월(outblock4) 참조")
    data3: str = Field(title="DATA3", description="결산연월(outblock4) 참조")
    data4: str = Field(title="DATA4", description="결산연월(outblock4) 참조")
    data5: str = Field(title="DATA5", description="결산연월(outblock4) 참조")


class EstimatedEarningsItem4(BaseModel):
    dt: str = Field(title="결산년월")


class EstimatedEarnings(BaseModel, KisHttpBody):
    """국내주식 종목추정실적"""

    output1: EstimatedEarningsItem1 = Field(title="응답상세1")
    output2: Sequence[EstimatedEarningsItem2] = Field(default_factory=list)
    output3: Sequence[EstimatedEarningsItem3] = Field(default_factory=list)
    output4: Sequence[EstimatedEarningsItem4] = Field(default_factory=list)


class StockLoanableListItem1(BaseModel):
    pdno: str = Field(title="상품번호")
    prdt_name: str = Field(title="상품명")
    papr: str = Field(title="액면가")
    bfdy_clpr: str = Field(title="전일종가", description="전일종가")
    sbst_prvs: str = Field(title="대용가")
    tr_stop_dvsn_name: str = Field(title="거래정지구분명")
    psbl_yn_name: str = Field(title="가능여부명")
    lmt_qty1: str = Field(title="한도수량1")
    use_qty1: str = Field(title="사용수량1")
    trad_psbl_qty2: str = Field(title="매매가능수량2", description="가능수량")
    rght_type_cd: str = Field(title="권리유형코드")
    bass_dt: str = Field(title="기준일자")
    psbl_yn: str = Field(title="가능여부")


class StockLoanableListItem2(BaseModel):
    tot_stup_lmt_qty: str = Field(title="총설정한도수량")
    brch_lmt_qty: str = Field(title="지점한도수량")
    rqst_psbl_qty: str = Field(title="신청가능수량")


class StockLoanableList(BaseModel, KisHttpBody):
    """당사 대주가능 종목"""

    ctx_area_fk200: str = Field(default="", title="연속조회검색조건200")
    ctx_area_nk100: str = Field(default="", title="연속조회키100")
    output1: Sequence[StockLoanableListItem1] = Field(default_factory=list)
    output2: StockLoanableListItem2 = Field(title="응답상세2")


class InvestmentOpinionItem(BaseModel):
    stck_bsop_date: str = Field(title="주식영업일자")
    invt_opnn: str = Field(title="투자의견")
    invt_opnn_cls_code: str = Field(title="투자의견구분코드")
    rgbf_invt_opnn: str = Field(title="직전투자의견")
    rgbf_invt_opnn_cls_code: str = Field(title="직전투자의견구분코드")
    mbcr_name: str = Field(title="회원사명")
    hts_goal_prc: str = Field(title="HTS목표가격")
    stck_prdy_clpr: str = Field(title="주식전일종가")
    stck_nday_esdg: str = Field(title="주식N일괴리도")
    nday_dprt: str = Field(title="N일괴리율")
    stft_esdg: str = Field(title="주식선물괴리도")
    dprt: str = Field(title="괴리율")


class InvestmentOpinion(BaseModel, KisHttpBody):
    """국내주식 종목투자의견"""

    output: Sequence[InvestmentOpinionItem] = Field(default_factory=list)


class InvestmentOpinionByBrokerageItem(BaseModel):
    stck_bsop_date: str = Field(title="주식영업일자")
    stck_shrn_iscd: str = Field(title="주식단축종목코드")
    hts_kor_isnm: str = Field(title="HTS한글종목명")
    invt_opnn: str = Field(title="투자의견")
    invt_opnn_cls_code: str = Field(title="투자의견구분코드")
    rgbf_invt_opnn: str = Field(title="직전투자의견")
    rgbf_invt_opnn_cls_code: str = Field(title="직전투자의견구분코드")
    mbcr_name: str = Field(title="회원사명")
    stck_prpr: str = Field(title="주식현재가")
    prdy_vrss: str = Field(title="전일대비")
    prdy_vrss_sign: str = Field(title="전일대비부호")
    prdy_ctrt: str = Field(title="전일대비율")
    hts_goal_prc: str = Field(title="HTS목표가격")
    stck_prdy_clpr: str = Field(title="주식전일종가")
    stft_esdg: str = Field(title="주식선물괴리도")
    dprt: str = Field(title="괴리율")


class InvestmentOpinionByBrokerage(BaseModel, KisHttpBody):
    """국내주식 증권사별 투자의견"""

    output: Sequence[InvestmentOpinionByBrokerageItem] = Field(default_factory=list)
