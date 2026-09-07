from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.dart._model import DartHttpBody


class CapitalChangeStatusItem(BaseModel):
    model_config = ConfigDict(title="증자(감자) 현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    isu_dcrs_de: str = Field(description="주식발행 감소일자")
    isu_dcrs_stle: str = Field(description="발행 감소 형태")
    isu_dcrs_stock_knd: str = Field(description="발행 감소 주식 종류")
    isu_dcrs_qy: str = Field(description="발행 감소 수량")
    isu_dcrs_mstvdv_fval_amount: str = Field(description="발행 감소 주당 액면 가액")
    isu_dcrs_mstvdv_amount: str = Field(description="발행 감소 주당 가액")
    stlm_dt: str = Field(description="결산기준일")


class CapitalChangeStatus(BaseModel, DartHttpBody[CapitalChangeStatusItem]):
    model_config = ConfigDict(title="증자(감자) 현황 응답", populate_by_name=True)


class DividendInformationItem(BaseModel):
    model_config = ConfigDict(title="배당 관련 사항 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    se: str = Field(description="구분")
    stock_knd: Optional[str] = Field(description="주식 종류", default=None)
    thstrm: str = Field(description="당기")
    frmtrm: str = Field(description="전기")
    lwfr: str = Field(description="전전기")
    stlm_dt: str = Field(description="결산기준일")


class DividendInformation(BaseModel, DartHttpBody[DividendInformationItem]):
    model_config = ConfigDict(title="배당 관련 사항 응답", populate_by_name=True)


class TreasuryStockActivityItem(BaseModel):
    model_config = ConfigDict(title="자기주식 취득 및 처분 현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    acqs_mth1: str = Field(description="취득방법 대분류")
    acqs_mth2: str = Field(description="취득방법 중분류")
    acqs_mth3: str = Field(description="취득방법 소분류")
    stock_knd: str = Field(description="주식 종류")
    bsis_qy: str = Field(description="기초 수량")
    change_qy_acqs: str = Field(description="변동 수량 취득")
    change_qy_dsps: str = Field(description="변동 수량 처분")
    change_qy_incnr: str = Field(description="변동 수량 소각")
    trmend_qy: str = Field(description="기말 수량")
    rm: str = Field(description="비고")
    stlm_dt: str = Field(description="결산기준일")


class TreasuryStockActivity(BaseModel, DartHttpBody[TreasuryStockActivityItem]):
    model_config = ConfigDict(title="자기주식 취득 및 처분 현황 응답", populate_by_name=True)


class MajorShareholderStatusItem(BaseModel):
    model_config = ConfigDict(title="최대주주 현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    nm: str = Field(description="성명")
    relate: Optional[str] = Field(description="관계", default=None)
    stock_knd: str = Field(description="주식 종류")
    bsis_posesn_stock_co: str = Field(description="기초 소유 주식 수")
    bsis_posesn_stock_qota_rt: str = Field(description="기초 소유 주식 지분 율")
    trmend_posesn_stock_co: str = Field(description="기말 소유 주식 수")
    trmend_posesn_stock_qota_rt: str = Field(description="기말 소유 주식 지분 율")
    rm: str = Field(description="비고")
    stlm_dt: str = Field(description="결산기준일")


class MajorShareholderStatus(BaseModel, DartHttpBody[MajorShareholderStatusItem]):
    model_config = ConfigDict(title="최대주주 현황 응답", populate_by_name=True)


class MajorShareholderChangesItem(BaseModel):
    model_config = ConfigDict(title="최대주주 변동현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    change_on: str = Field(description="변동 일")
    mxmm_shrholdr_nm: str = Field(description="최대 주주 명")
    posesn_stock_co: str = Field(description="소유 주식 수")
    qota_rt: str = Field(description="지분 율")
    change_cause: str = Field(description="변동 원인")
    rm: str = Field(description="비고")
    stlm_dt: str = Field(description="결산기준일")


class MajorShareholderChanges(BaseModel, DartHttpBody[MajorShareholderChangesItem]):
    model_config = ConfigDict(title="최대주주 변동현황 응답", populate_by_name=True)


class MinorityShareholderStatusItem(BaseModel):
    model_config = ConfigDict(title="소액주주 현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    se: str = Field(description="구분")
    shrholdr_co: str = Field(description="주주수")
    shrholdr_tot_co: str = Field(description="전체 주주수")
    shrholdr_rate: str = Field(description="주주 비율")
    hold_stock_co: str = Field(description="보유 주식수")
    stock_tot_co: str = Field(description="총발행 주식수")
    hold_stock_rate: str = Field(description="보유 주식 비율")
    stlm_dt: str = Field(description="결산기준일")


class MinorityShareholderStatus(BaseModel, DartHttpBody[MinorityShareholderStatusItem]):
    model_config = ConfigDict(title="소액주주 현황 응답", populate_by_name=True)


class ExecutiveStatusItem(BaseModel):
    model_config = ConfigDict(title="임원 현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    nm: str = Field(description="성명")
    sexdstn: str = Field(description="성별")
    birth_ym: str = Field(description="출생 년월")
    ofcps: str = Field(description="직위")
    rgist_exctv_at: str = Field(description="등기 임원 여부")
    fte_at: str = Field(description="상근 여부")
    chrg_job: str = Field(description="담당 업무")
    main_career: str = Field(description="주요 경력")
    mxmm_shrholdr_relate: str = Field(description="최대 주주 관계")
    hffc_pd: str = Field(description="재직 기간")
    tenure_end_on: str = Field(description="임기 만료 일")
    stlm_dt: str = Field(description="결산기준일")


class ExecutiveStatus(BaseModel, DartHttpBody[ExecutiveStatusItem]):
    model_config = ConfigDict(title="임원 현황 응답", populate_by_name=True)


class EmployeeStatusItem(BaseModel):
    model_config = ConfigDict(title="직원 현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    fo_bbm: str = Field(description="사업부문")
    sexdstn: str = Field(description="성별")
    reform_bfe_emp_co_rgllbr: str = Field(description="개정 전 직원 수 정규직")
    reform_bfe_emp_co_cnttk: str = Field(description="개정 전 직원 수 계약직")
    reform_bfe_emp_co_etc: str = Field(description="개정 전 직원 수 기타")
    rgllbr_co: str = Field(description="정규직 수")
    rgllbr_abacpt_labrr_co: str = Field(description="정규직 단시간 근로자 수")
    cnttk_co: str = Field(description="계약직 수")
    cnttk_abacpt_labrr_co: str = Field(description="계약직 단시간 근로자 수")
    sm: str = Field(description="합계")
    avrg_cnwk_sdytrn: str = Field(description="평균 근속 연수")
    fyer_salary_totamt: str = Field(description="연간 급여 총액")
    jan_salary_am: str = Field(description="1인평균 급여 액")
    rm: str = Field(description="비고")
    stlm_dt: str = Field(description="결산기준일")


class EmployeeStatus(BaseModel, DartHttpBody[EmployeeStatusItem]):
    model_config = ConfigDict(title="직원 현황 응답", populate_by_name=True)


class BoardAndAuditCompensationAbove500mItem(BaseModel):
    model_config = ConfigDict(title="이사·감사 개별 보수현황(5억 이상) 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    nm: str = Field(description="이름")
    ofcps: str = Field(description="직위")
    mendng_totamt: str = Field(description="보수 총액")
    mendng_totamt_ct_incls_mendng: str = Field(description="보수 총액 비 포함 보수")
    stlm_dt: str = Field(description="결산기준일")


class BoardAndAuditCompensationAbove500m(BaseModel, DartHttpBody[BoardAndAuditCompensationAbove500mItem]):
    model_config = ConfigDict(title="이사·감사 개별 보수현황(5억 이상) 응답", populate_by_name=True)


class BoardAndAuditTotalCompensationItem(BaseModel):
    model_config = ConfigDict(title="이사·감사 전체 보수지급금액 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    nmpr: str = Field(description="인원수")
    mendng_totamt: str = Field(description="보수 총액")
    jan_avrg_mendng_am: str = Field(description="1인 평균 보수 액")
    rm: str = Field(description="비고")
    stlm_dt: str = Field(description="결산기준일")


class BoardAndAuditTotalCompensation(BaseModel, DartHttpBody[BoardAndAuditTotalCompensationItem]):
    model_config = ConfigDict(title="이사·감사 전체 보수지급금액 응답", populate_by_name=True)


class TopFiveIndividualCompensationItem(BaseModel):
    model_config = ConfigDict(title="개인별 보수지급 금액(5억 이상 상위 5인) 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="법인명")
    nm: str = Field(description="이름")
    ofcps: str = Field(description="직위")
    mendng_totamt: str = Field(description="보수 총액")
    mendng_totamt_ct_incls_mendng: str = Field(description="보수 총액 비 포함 보수")
    stlm_dt: str = Field(description="결산기준일")


class TopFiveIndividualCompensation(BaseModel, DartHttpBody[TopFiveIndividualCompensationItem]):
    model_config = ConfigDict(title="개인별 보수지급 금액(5억 이상 상위 5인) 응답", populate_by_name=True)


class OtherCorporationInvestmentsItem(BaseModel):
    model_config = ConfigDict(title="타법인 출자현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    inv_prm: str = Field(description="법인명")
    frst_acqs_de: str = Field(description="최초 취득 일자")
    invstmnt_purps: str = Field(description="출자 목적")
    frst_acqs_amount: str = Field(description="최초 취득 금액")
    bsis_blce_qy: str = Field(description="기초 잔액 수량")
    bsis_blce_qota_rt: str = Field(description="기초 잔액 지분 율")
    bsis_blce_acntbk_amount: str = Field(description="기초 잔액 장부 가액")
    incrs_dcrs_acqs_dsps_qy: str = Field(description="증가 감소 취득 처분 수량")
    incrs_dcrs_acqs_dsps_amount: str = Field(description="증가 감소 취득 처분 금액")
    incrs_dcrs_evl_lstmn: str = Field(description="증가 감소 평가 손액")
    trmend_blce_qy: str = Field(description="기말 잔액 수량")
    trmend_blce_qota_rt: str = Field(description="기말 잔액 지분 율")
    trmend_blce_acntbk_amount: str = Field(description="기말 잔액 장부 가액")
    recent_bsns_year_fnnr_sttus_tot_assets: str = Field(description="최근 사업 연도 재무 현황 총 자산")
    recent_bsns_year_fnnr_sttus_thstrm_ntpf: str = Field(description="최근 사업 연도 재무 현황 당기 순이익")
    stlm_dt: str = Field(description="결산기준일")


class OtherCorporationInvestments(BaseModel, DartHttpBody[OtherCorporationInvestmentsItem]):
    model_config = ConfigDict(title="타법인 출자현황 응답", populate_by_name=True)


class TotalNumberOfSharesItem(BaseModel):
    model_config = ConfigDict(title="주식의 총수 현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    se: str = Field(description="구분")
    isu_stock_totqy: str = Field(description="발행할 주식의 총수")
    now_to_isu_stock_totqy: str = Field(description="현재까지 발행한 주식의 총수")
    now_to_dcrs_stock_totqy: str = Field(description="현재까지 감소한 주식의 총수")
    redc: str = Field(description="감자")
    profit_incnr: str = Field(description="이익소각")
    rdmstk_repy: str = Field(description="상환주식의 상환")
    etc: str = Field(description="기타")
    istc_totqy: str = Field(description="발행주식의 총수")
    tesstk_co: str = Field(description="자기주식수")
    distb_stock_co: str = Field(description="유통주식수")
    stlm_dt: str = Field(description="결산기준일")


class TotalNumberOfShares(BaseModel, DartHttpBody[TotalNumberOfSharesItem]):
    model_config = ConfigDict(title="주식의 총수 현황 응답", populate_by_name=True)


class DebtSecuritiesIssuancePerformanceItem(BaseModel):
    model_config = ConfigDict(title="채무증권 발행실적 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    isu_cmpny: str = Field(description="발행회사")
    scrits_knd_nm: str = Field(description="증권종류")
    isu_mth_nm: str = Field(description="발행방법")
    isu_de: str = Field(description="발행일자(YYYYMMDD)")
    facvalu_totamt: str = Field(description="권면(전자등록)총액")
    intrt: str = Field(description="이자율")
    evl_grad_instt: str = Field(description="평가등급(평가기관)")
    mtd: str = Field(description="만기일(YYYYMMDD)")
    repy_at: str = Field(description="상환여부")
    mngt_cmpny: str = Field(description="주관회사")
    stlm_dt: str = Field(description="결산기준일")


class DebtSecuritiesIssuancePerformance(BaseModel, DartHttpBody[DebtSecuritiesIssuancePerformanceItem]):
    model_config = ConfigDict(title="채무증권 발행실적 응답", populate_by_name=True)


class OutstandingCommercialPaperBalanceItem(BaseModel):
    model_config = ConfigDict(title="기업어음증권 미상환 잔액 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="공시대상회사명")
    remndr_exprtn1: str = Field(description="잔여만기")
    remndr_exprtn2: str = Field(description="잔여만기")
    de10_below: str = Field(description="10일 이하")
    de10_excess_de30_below: str = Field(description="10일초과 30일이하")
    de30_excess_de90_below: str = Field(description="30일초과 90일이하")
    de90_excess_de180_below: str = Field(description="90일초과 180일이하")
    de180_excess_yy1_below: str = Field(description="180일초과 1년이하")
    yy1_excess_yy2_below: str = Field(description="1년초과 2년이하")
    yy2_excess_yy3_below: str = Field(description="2년초과 3년이하")
    yy3_excess: str = Field(description="3년 초과")
    sm: str = Field(description="합계")
    stlm_dt: str = Field(description="결산기준일")


class OutstandingCommercialPaperBalance(BaseModel, DartHttpBody[OutstandingCommercialPaperBalanceItem]):
    model_config = ConfigDict(title="기업어음증권 미상환 잔액 응답", populate_by_name=True)


class OutstandingShortTermBondsItem(BaseModel):
    model_config = ConfigDict(title="단기사채 미상환 잔액 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="공시대상회사명")
    remndr_exprtn1: str = Field(description="잔여만기")
    remndr_exprtn2: str = Field(description="잔여만기")
    de10_below: str = Field(description="10일 이하")
    de10_excess_de30_below: str = Field(description="10일초과 30일이하")
    de30_excess_de90_below: str = Field(description="30일초과 90일이하")
    de90_excess_de180_below: str = Field(description="90일초과 180일이하")
    de180_excess_yy1_below: str = Field(description="180일초과 1년이하")
    sm: str = Field(description="합계")
    isu_lmt: str = Field(description="발행 한도")
    remndr_lmt: str = Field(description="잔여 한도")
    stlm_dt: str = Field(description="결산기준일")


class OutstandingShortTermBonds(BaseModel, DartHttpBody[OutstandingShortTermBondsItem]):
    model_config = ConfigDict(title="단기사채 미상환 잔액 응답", populate_by_name=True)


class OutstandingCorporateBondsItem(BaseModel):
    model_config = ConfigDict(title="회사채 미상환 잔액 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="공시대상회사명")
    remndr_exprtn1: str = Field(description="잔여만기")
    remndr_exprtn2: str = Field(description="잔여만기")
    yy1_below: str = Field(description="1년 이하")
    yy1_excess_yy2_below: str = Field(description="1년초과 2년이하")
    yy2_excess_yy3_below: str = Field(description="2년초과 3년이하")
    yy3_excess_yy4_below: str = Field(description="3년초과 4년이하")
    yy4_excess_yy5_below: str = Field(description="4년초과 5년이하")
    yy5_excess_yy10_below: str = Field(description="5년초과 10년이하")
    yy10_excess: str = Field(description="10년초과")
    sm: str = Field(description="합계")
    stlm_dt: str = Field(description="결산기준일")


class OutstandingCorporateBonds(BaseModel, DartHttpBody[OutstandingCorporateBondsItem]):
    model_config = ConfigDict(title="회사채 미상환 잔액 응답", populate_by_name=True)


class OutstandingHybridCapitalSecuritiesItem(BaseModel):
    model_config = ConfigDict(title="신종자본증권 미상환 잔액 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="공시대상회사명")
    remndr_exprtn1: str = Field(description="잔여만기")
    remndr_exprtn2: str = Field(description="잔여만기")
    yy1_below: str = Field(description="1년 이하")
    yy1_excess_yy5_below: str = Field(description="1년초과 5년이하")
    yy5_excess_yy10_below: str = Field(description="5년초과 10년이하")
    yy10_excess_yy15_below: str = Field(description="10년초과 15년이하")
    yy15_excess_yy20_below: str = Field(description="15년초과 20년이하")
    yy20_excess_yy30_below: str = Field(description="20년초과 30년이하")
    yy30_excess: str = Field(description="30년초과")
    sm: str = Field(description="합계")
    stlm_dt: str = Field(description="결산기준일")


class OutstandingHybridCapitalSecurities(BaseModel, DartHttpBody[OutstandingHybridCapitalSecuritiesItem]):
    model_config = ConfigDict(title="신종자본증권 미상환 잔액 응답", populate_by_name=True)


class OutstandingContingentCapitalSecuritiesItem(BaseModel):
    model_config = ConfigDict(title="조건부 자본증권 미상환 잔액 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="공시대상회사명")
    remndr_exprtn1: str = Field(description="잔여만기")
    remndr_exprtn2: str = Field(description="잔여만기")
    yy1_below: str = Field(description="1년 이하")
    yy1_excess_yy2_below: str = Field(description="1년초과 2년이하")
    yy2_excess_yy3_below: str = Field(description="2년초과 3년이하")
    yy3_excess_yy4_below: str = Field(description="3년초과 4년이하")
    yy4_excess_yy5_below: str = Field(description="4년초과 5년이하")
    yy5_excess_yy10_below: str = Field(description="5년초과 10년이하")
    yy10_excess_yy20_below: str = Field(description="10년초과 20년이하")
    yy20_excess_yy30_below: str = Field(description="20년초과 30년이하")
    yy30_excess: str = Field(description="30년초과")
    sm: str = Field(description="합계")
    stlm_dt: str = Field(description="결산기준일")


class OutstandingContingentCapitalSecurities(BaseModel, DartHttpBody[OutstandingContingentCapitalSecuritiesItem]):
    model_config = ConfigDict(title="조건부 자본증권 미상환 잔액 응답", populate_by_name=True)


class AuditorNameAndOpinionItem(BaseModel):
    model_config = ConfigDict(title="회계감사인 명칭과 감사의견 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="공시대상회사명")
    bsns_year: str = Field(description="사업연도")
    adtor: str = Field(description="감사인")
    adt_opinion: str = Field(description="감사의견")
    adt_reprt_spcmnt_matter: str = Field(description="감사보고서 특기사항")
    emphs_matter: str = Field(description="강조사항 등")
    core_adt_matter: Optional[str] = Field(description="핵심감사사항")
    stlm_dt: str = Field(description="결산기준일")


class AuditorNameAndOpinion(BaseModel, DartHttpBody[AuditorNameAndOpinionItem]):
    model_config = ConfigDict(title="회계감사인 명칭과 감사의견 응답", populate_by_name=True)


class AuditServiceContractsItem(BaseModel):
    model_config = ConfigDict(title="감사용역 계약현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    bsns_year: str = Field(description="사업연도")
    adtor: str = Field(description="감사인")
    cn: str = Field(description="내용")
    mendng: str = Field(description="보수")
    tot_reqre_time: str = Field(description="총소요시간")
    adt_cntrct_dtls_mendng: str = Field(description="감사계약내역(보수)")
    adt_cntrct_dtls_time: str = Field(description="감사계약내역(시간)")
    real_exc_dtls_mendng: str = Field(description="실제수행내역(보수)")
    real_exc_dtls_time: str = Field(description="실제수행내역(시간)")
    stlm_dt: str = Field(description="결산기준일")


class AuditServiceContracts(BaseModel, DartHttpBody[AuditServiceContractsItem]):
    model_config = ConfigDict(title="감사용역 계약현황 응답", populate_by_name=True)


class NonAuditServiceContractsItem(BaseModel):
    model_config = ConfigDict(title="회계감사인과의 비감사용역 계약체결 현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="공시대상회사명")
    bsns_year: str = Field(description="사업연도")
    cntrct_cncls_de: str = Field(description="계약체결일")
    servc_cn: str = Field(description="용역내용")
    servc_exc_pd: str = Field(description="용역수행기간")
    servc_mendng: str = Field(description="용역보수")
    rm: str = Field(description="비고")
    stlm_dt: str = Field(description="결산기준일")


class NonAuditServiceContracts(BaseModel, DartHttpBody[NonAuditServiceContractsItem]):
    model_config = ConfigDict(title="회계감사인과의 비감사용역 계약체결 현황 응답", populate_by_name=True)


class OutsideDirectorStatusItem(BaseModel):
    model_config = ConfigDict(title="사외이사 및 변동현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    drctr_co: str = Field(description="이사의 수")
    otcmp_drctr_co: str = Field(description="사외이사 수")
    apnt: str = Field(description="사외이사 변동현황(선임)")
    rlsofc: str = Field(description="사외이사 변동현황(해임)")
    mdstrm_resig: str = Field(description="사외이사 변동현황(중도퇴임)")
    stlm_dt: str = Field(description="결산기준일")


class OutsideDirectorStatus(BaseModel, DartHttpBody[OutsideDirectorStatusItem]):
    model_config = ConfigDict(title="사외이사 및 변동현황 응답", populate_by_name=True)


class UnregisteredExecutiveCompensationItem(BaseModel):
    model_config = ConfigDict(title="미등기임원 보수현황 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    se: str = Field(description="구분(미등기임원)")
    nmpr: str = Field(description="9,999,999,999")
    fyer_salary_totamt: str = Field(description="연간급여 총액")
    jan_salary_am: str = Field(description="1인평균 급여액")
    rm: str = Field(description="비고")
    stlm_dt: str = Field(description="결산기준일")


class UnregisteredExecutiveCompensation(BaseModel, DartHttpBody[UnregisteredExecutiveCompensationItem]):
    model_config = ConfigDict(title="미등기임원 보수현황 응답", populate_by_name=True)


class BoardAndAuditCompensationShareholderApprovedItem(BaseModel):
    model_config = ConfigDict(title="이사·감사 전체 보수현황(주주총회 승인금액) 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    se: str = Field(description="구분")
    nmpr: str = Field(description="인원수")
    gmtsck_confm_amount: str = Field(description="주주총회 승인금액")
    rm: str = Field(description="비고")
    stlm_dt: str = Field(description="결산기준일")


class BoardAndAuditCompensationShareholderApproved(
    BaseModel, DartHttpBody[BoardAndAuditCompensationShareholderApprovedItem]
):
    model_config = ConfigDict(title="이사·감사 전체 보수현황(주주총회 승인금액) 응답", populate_by_name=True)


class BoardAndAuditCompensationByTypeItem(BaseModel):
    model_config = ConfigDict(title="이사·감사 전체 보수현황(보수지급금액 유형별) 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    se: str = Field(description="구분")
    nmpr: str = Field(description="인원수")
    pymnt_totamt: str = Field(description="보수총액")
    psn1_avrg_pymntamt: str = Field(description="1인 평균 보수액")
    rm: str = Field(description="비고")
    stlm_dt: str = Field(description="결산기준일")


class BoardAndAuditCompensationByType(BaseModel, DartHttpBody[BoardAndAuditCompensationByTypeItem]):
    model_config = ConfigDict(title="이사·감사 전체 보수현황(보수지급금액 유형별) 응답", populate_by_name=True)


class PublicOfferingFundUsageItem(BaseModel):
    model_config = ConfigDict(title="공모자금 사용내역 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    se_nm: str = Field(description="구분")
    tm: str = Field(description="회차")
    pay_de: str = Field(description="납입일")
    pay_amount: str = Field(description="납입금액")
    on_dclrt_cptal_use_plan: str = Field(description="신고서상 자금사용 계획")
    real_cptal_use_sttus: str = Field(description="실제 자금사용 현황")
    rs_cptal_use_plan_useprps: str = Field(description="증권신고서 등의 자금사용 계획(사용용도)")
    rs_cptal_use_plan_prcure_amount: str = Field(description="증권신고서 등의 자금사용 계획(조달금액)")
    real_cptal_use_dtls_cn: str = Field(description="실제 자금사용 내역(내용)")
    real_cptal_use_dtls_amount: str = Field(description="실제 자금사용 내역(금액)")
    dffrnc_occrrnc_resn: str = Field(description="차이발생 사유 등")
    stlm_dt: str = Field(description="결산기준일")


class PublicOfferingFundUsage(BaseModel, DartHttpBody[PublicOfferingFundUsageItem]):
    model_config = ConfigDict(title="공모자금 사용내역 응답", populate_by_name=True)


class PrivatePlacementFundUsageItem(BaseModel):
    model_config = ConfigDict(title="사모자금 사용내역 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)")
    corp_cls: str = Field(description="법인구분")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)")
    corp_name: str = Field(description="회사명")
    se_nm: str = Field(description="구분")
    tm: str = Field(description="회차")
    pay_de: str = Field(description="납입일")
    pay_amount: str = Field(description="납입금액")
    cptal_use_plan: str = Field(description="자금사용 계획")
    real_cptal_use_sttus: str = Field(description="실제 자금사용 현황")
    mtrpt_cptal_use_plan_useprps: str = Field(description="주요사항보고서의 자금사용 계획(사용용도)")
    mtrpt_cptal_use_plan_prcure_amount: str = Field(description="주요사항보고서의 자금사용 계획(조달금액)")
    real_cptal_use_dtls_cn: str = Field(description="실제 자금사용 내역(내용)")
    real_cptal_use_dtls_amount: str = Field(description="실제 자금사용 내역(금액)")
    dffrnc_occrrnc_resn: str = Field(description="차이발생 사유 등")
    stlm_dt: str = Field(description="결산기준일")


class PrivatePlacementFundUsage(BaseModel, DartHttpBody[PrivatePlacementFundUsageItem]):
    model_config = ConfigDict(title="사모자금 사용내역 응답", populate_by_name=True)
