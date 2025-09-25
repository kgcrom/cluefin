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
    stock_knd: Optional[str] = Field(default=None, description="주식 종류")
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
    relate: str = Field(description="관계")
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


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	법인명	법인명
# nm	성명	홍길동
# sexdstn	성별	남
# birth_ym	출생 년월	YYYY년 MM월
# ofcps	직위	회장, 사장, 사외이사 등
# rgist_exctv_at	등기 임원 여부	등기임원, 미등기임원 등
# fte_at	상근 여부	상근, 비상근
# chrg_job	담당 업무	대표이사, 이사, 사외이사 등
# main_career	주요 경력
# mxmm_shrholdr_relate	최대 주주 관계
# hffc_pd	재직 기간
# tenure_end_on	임기 만료 일
# stlm_dt	결산기준일	YYYY-MM-DD
class ExecutiveStatusItem(BaseModel):
    model_config = ConfigDict(title="임원 현황 항목", populate_by_name=True)


class ExecutiveStatus(BaseModel, DartHttpBody[ExecutiveStatusItem]):
    model_config = ConfigDict(title="임원 현황 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	법인명	법인명
# fo_bbm	사 업부문
# sexdstn	성별	남, 여
# reform_bfe_emp_co_rgllbr	개정 전 직원 수 정규직
# reform_bfe_emp_co_cnttk	개정 전 직원 수 계약직
# reform_bfe_emp_co_etc	개정 전 직원 수 기타
# rgllbr_co	정규직 수	상근, 비상근
# rgllbr_abacpt_labrr_co	정규직 단시간 근로자 수	대표이사, 이사, 사외이사 등
# cnttk_co	계약직 수	9,999,999,999
# cnttk_abacpt_labrr_co	계약직 단시간 근로자 수	9,999,999,999
# sm	합계	9,999,999,999
# avrg_cnwk_sdytrn	평균 근속 연수	9,999,999,999
# fyer_salary_totamt	연간 급여 총액	9,999,999,999
# jan_salary_am	1인평균 급여 액	9,999,999,999
# rm	비고
# stlm_dt	결산기준일	YYYY-MM-DD
class EmployeeStatusItem(BaseModel):
    model_config = ConfigDict(title="직원 현황 항목", populate_by_name=True)


class EmployeeStatus(BaseModel, DartHttpBody[EmployeeStatusItem]):
    model_config = ConfigDict(title="직원 현황 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	법인명	법인명
# nm	이름	홍길동
# ofcps	직위	이사, 대표이사 등
# mendng_totamt	보수 총액	9,999,999,999
# mendng_totamt_ct_incls_mendng	보수 총액 비 포함 보수	9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class BoardAndAuditCompensationAbove500mItem(BaseModel):
    model_config = ConfigDict(title="이사·감사 개별 보수현황(5억 이상) 항목", populate_by_name=True)


class BoardAndAuditCompensationAbove500m(BaseModel, DartHttpBody[BoardAndAuditCompensationAbove500mItem]):
    model_config = ConfigDict(title="이사·감사 개별 보수현황(5억 이상) 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	법인명	법인명
# nmpr	인원수	9,999,999,999
# mendng_totamt	보수 총액	9,999,999,999
# jan_avrg_mendng_am	1인 평균 보수 액	9,999,999,999
# rm	비고
# stlm_dt	결산기준일	YYYY-MM-DD
class BoardAndAuditTotalCompensationItem(BaseModel):
    model_config = ConfigDict(title="이사·감사 전체 보수지급금액 항목", populate_by_name=True)


class BoardAndAuditTotalCompensation(BaseModel, DartHttpBody[BoardAndAuditTotalCompensationItem]):
    model_config = ConfigDict(title="이사·감사 전체 보수지급금액 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	법인명	법인명
# nm	이름	홍길동
# ofcps	직위	대표이사 등
# mendng_totamt	보수 총액	9,999,999,999
# mendng_totamt_ct_incls_mendng	보수 총액 비 포함 보수	9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class TopFiveIndividualCompensationItem(BaseModel):
    model_config = ConfigDict(title="개인별 보수지급 금액(5억 이상 상위 5인) 항목", populate_by_name=True)


class TopFiveIndividualCompensation(BaseModel, DartHttpBody[TopFiveIndividualCompensationItem]):
    model_config = ConfigDict(title="개인별 보수지급 금액(5억 이상 상위 5인) 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# inv_prm	법인명	법인명
# frst_acqs_de	최초 취득 일자	최초취득일자(YYYYMMDD)
# invstmnt_purps	출자 목적	출자목적(자회사 등)
# frst_acqs_amount	최초 취득 금액	9,999,999,999
# bsis_blce_qy	기초 잔액 수량	9,999,999,999
# bsis_blce_qota_rt	기초 잔액 지분 율	0.00
# bsis_blce_acntbk_amount	기초 잔액 장부 가액	9,999,999,999
# incrs_dcrs_acqs_dsps_qy	증가 감소 취득 처분 수량	9,999,999,999
# incrs_dcrs_acqs_dsps_amount	증가 감소 취득 처분 금액	9,999,999,999
# incrs_dcrs_evl_lstmn	증가 감소 평가 손액	9,999,999,999
# trmend_blce_qy	기말 잔액 수량	9,999,999,999
# trmend_blce_qota_rt	기말 잔액 지분 율	0.00
# trmend_blce_acntbk_amount	기말 잔액 장부 가액	9,999,999,999
# recent_bsns_year_fnnr_sttus_tot_assets	최근 사업 연도 재무 현황 총 자산	9,999,999,999
# recent_bsns_year_fnnr_sttus_thstrm_ntpf	최근 사업 연도 재무 현황 당기 순이익	9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class OtherCorporationInvestmentsItem(BaseModel):
    model_config = ConfigDict(title="타법인 출자현황 항목", populate_by_name=True)


class OtherCorporationInvestments(BaseModel, DartHttpBody[OtherCorporationInvestmentsItem]):
    model_config = ConfigDict(title="타법인 출자현황 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# se	구분	구분(증권의종류, 합계, 비고)
# isu_stock_totqy	발행할 주식의 총수	Ⅰ. 발행할 주식의 총수, 9,999,999,999
# now_to_isu_stock_totqy	현재까지 발행한 주식의 총수	Ⅱ. 현재까지 발행한 주식의 총수, 9,999,999,999
# now_to_dcrs_stock_totqy	현재까지 감소한 주식의 총수	Ⅲ. 현재까지 감소한 주식의 총수, 9,999,999,999
# redc	감자	Ⅲ. 현재까지 감소한 주식의 총수(1. 감자), 9,999,999,999
# profit_incnr	이익소각	Ⅲ. 현재까지 감소한 주식의 총수(2. 이익소각), 9,999,999,999
# rdmstk_repy	상환주식의 상환	Ⅲ. 현재까지 감소한 주식의 총수(3. 상환주식의 상환), 9,999,999,999
# etc	기타	Ⅲ. 현재까지 감소한 주식의 총수(4. 기타), 9,999,999,999
# istc_totqy	발행주식의 총수	Ⅳ. 발행주식의 총수 (Ⅱ-Ⅲ), 9,999,999,999
# tesstk_co	자기주식수	Ⅴ. 자기주식수, 9,999,999,999
# distb_stock_co	유통주식수	Ⅵ. 유통주식수 (Ⅳ-Ⅴ), 9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class TotalNumberOfSharesItem(BaseModel):
    model_config = ConfigDict(title="주식의 총수 현황 항목", populate_by_name=True)


class TotalNumberOfShares(BaseModel, DartHttpBody[TotalNumberOfSharesItem]):
    model_config = ConfigDict(title="주식의 총수 현황 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# isu_cmpny	발행회사	발행회사
# scrits_knd_nm	증권종류	증권종류
# isu_mth_nm	발행방법	발행방법
# isu_de	발행일자	발행일자(YYYYMMDD)
# facvalu_totamt	권면(전자등록)총액	9,999,999,999
# intrt	이자율	0.00
# evl_grad_instt	평가등급(평가기관)	평가등급(평가기관)
# mtd	만기일	만기일(YYYYMMDD)
# repy_at	상환여부	상환여부
# mngt_cmpny	주관회사	주관회사
# stlm_dt	결산기준일	YYYY-MM-DD
class DebtSecuritiesIssuancePerformanceItem(BaseModel):
    model_config = ConfigDict(title="채무증권 발행실적 항목", populate_by_name=True)


class DebtSecuritiesIssuancePerformance(BaseModel, DartHttpBody[DebtSecuritiesIssuancePerformanceItem]):
    model_config = ConfigDict(title="채무증권 발행실적 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# remndr_exprtn1	잔여만기	잔여만기
# remndr_exprtn2	잔여만기	잔여만기
# de10_below	10일 이하	9,999,999,999
# de10_excess_de30_below	10일초과 30일이하	9,999,999,999
# de30_excess_de90_below	30일초과 90일이하	9,999,999,999
# de90_excess_de180_below	90일초과 180일이하	9,999,999,999
# de180_excess_yy1_below	180일초과 1년이하	9,999,999,999
# yy1_excess_yy2_below	1년초과 2년이하	9,999,999,999
# yy2_excess_yy3_below	2년초과 3년이하	9,999,999,999
# yy3_excess	3년 초과	9,999,999,999
# sm	합계	9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class OutstandingCommercialPaperBalanceItem(BaseModel):
    model_config = ConfigDict(title="기업어음증권 미상환 잔액 항목", populate_by_name=True)


class OutstandingCommercialPaperBalance(BaseModel, DartHttpBody[OutstandingCommercialPaperBalanceItem]):
    model_config = ConfigDict(title="기업어음증권 미상환 잔액 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# remndr_exprtn1	잔여만기	잔여만기
# remndr_exprtn2	잔여만기	잔여만기
# de10_below	10일 이하	9,999,999,999
# de10_excess_de30_below	10일초과 30일이하	9,999,999,999
# de30_excess_de90_below	30일초과 90일이하	9,999,999,999
# de90_excess_de180_below	90일초과 180일이하	9,999,999,999
# de180_excess_yy1_below	180일초과 1년이하	9,999,999,999
# sm	합계	9,999,999,999
# isu_lmt	발행 한도	9,999,999,999
# remndr_lmt	잔여 한도	9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class OutstandingShortTermBondsItem(BaseModel):
    model_config = ConfigDict(title="단기사채 미상환 잔액 항목", populate_by_name=True)


class OutstandingShortTermBonds(BaseModel, DartHttpBody[OutstandingShortTermBondsItem]):
    model_config = ConfigDict(title="단기사채 미상환 잔액 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# remndr_exprtn1	잔여만기	잔여만기
# remndr_exprtn2	잔여만기	잔여만기
# yy1_below	1년 이하	9,999,999,999
# yy1_excess_yy2_below	1년초과 2년이하	9,999,999,999
# yy2_excess_yy3_below	2년초과 3년이하	9,999,999,999
# yy3_excess_yy4_below	3년초과 4년이하	9,999,999,999
# yy4_excess_yy5_below	4년초과 5년이하	9,999,999,999
# yy5_excess_yy10_below	5년초과 10년이하	9,999,999,999
# yy10_excess	10년초과	9,999,999,999
# sm	합계	9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class OutstandingCorporateBondsItem(BaseModel):
    model_config = ConfigDict(title="회사채 미상환 잔액 항목", populate_by_name=True)


class OutstandingCorporateBonds(BaseModel, DartHttpBody[OutstandingCorporateBondsItem]):
    model_config = ConfigDict(title="회사채 미상환 잔액 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# remndr_exprtn1	잔여만기	잔여만기
# remndr_exprtn2	잔여만기	잔여만기
# yy1_below	1년 이하	9,999,999,999
# yy1_excess_yy5_below	1년초과 5년이하	9,999,999,999
# yy5_excess_yy10_below	5년초과 10년이하	9,999,999,999
# yy10_excess_yy15_below	10년초과 15년이하	9,999,999,999
# yy15_excess_yy20_below	15년초과 20년이하	9,999,999,999
# yy20_excess_yy30_below	20년초과 30년이하	9,999,999,999
# yy30_excess	30년초과	9,999,999,999
# sm	합계	9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class OutstandingHybridCapitalSecuritiesItem(BaseModel):
    model_config = ConfigDict(title="신종자본증권 미상환 잔액 항목", populate_by_name=True)


class OutstandingHybridCapitalSecurities(BaseModel, DartHttpBody[OutstandingHybridCapitalSecuritiesItem]):
    model_config = ConfigDict(title="신종자본증권 미상환 잔액 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# remndr_exprtn1	잔여만기	잔여만기
# remndr_exprtn2	잔여만기	잔여만기
# yy1_below	1년 이하	9,999,999,999
# yy1_excess_yy2_below	1년초과 2년이하	9,999,999,999
# yy2_excess_yy3_below	2년초과 3년이하	9,999,999,999
# yy3_excess_yy4_below	3년초과 4년이하	9,999,999,999
# yy4_excess_yy5_below	4년초과 5년이하	9,999,999,999
# yy5_excess_yy10_below	5년초과 10년이하	9,999,999,999
# yy10_excess_yy20_below	10년초과 20년이하	9,999,999,999
# yy20_excess_yy30_below	20년초과 30년이하	9,999,999,999
# yy30_excess	30년초과	9,999,999,999
# sm	합계	9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class OutstandingContingentCapitalSecuritiesItem(BaseModel):
    model_config = ConfigDict(title="조건부 자본증권 미상환 잔액 항목", populate_by_name=True)


class OutstandingContingentCapitalSecurities(BaseModel, DartHttpBody[OutstandingContingentCapitalSecuritiesItem]):
    model_config = ConfigDict(title="조건부 자본증권 미상환 잔액 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# bsns_year	사업연도	사업연도(당기, 전기, 전전기)
# adtor	감사인	감사인
# adt_opinion	감사의견	감사의견
# adt_reprt_spcmnt_matter	감사보고서 특기사항	감사보고서 특기사항 ① 2019년 12월 8일까지 사용됨
# emphs_matter	강조사항 등	강조사항 등 ② 2019년 12월 9일부터 추가됨
# core_adt_matter	핵심감사사항	핵심감사사항 ② 2019년 12월 9일부터 추가됨
# stlm_dt	결산기준일	YYYY-MM-DD
class AuditorNameAndOpinionItem(BaseModel):
    model_config = ConfigDict(title="회계감사인 명칭과 감사의견 항목", populate_by_name=True)


class AuditorNameAndOpinion(BaseModel, DartHttpBody[AuditorNameAndOpinionItem]):
    model_config = ConfigDict(title="회계감사인 명칭과 감사의견 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# bsns_year	사업연도	사업연도(당기, 전기, 전전기)
# adtor	감사인	감사인
# cn	내용	내용
# mendng	보수	보수 ① 2020년 7월 5일까지 사용됨
# tot_reqre_time	총소요시간	총소요시간 ① 2020년 7월 5일까지 사용됨
# adt_cntrct_dtls_mendng	감사계약내역(보수)	감사계약내역(보수) ② 2020년 7월 6일부터 추가됨
# adt_cntrct_dtls_time	감사계약내역(시간)	감사계약내역(시간) ② 2020년 7월 6일부터 추가됨
# real_exc_dtls_mendng	실제수행내역(보수)	실제수행내역(보수) ② 2020년 7월 6일부터 추가됨
# real_exc_dtls_time	실제수행내역(시간)	실제수행내역(시간) ② 2020년 7월 6일부터 추가됨
# ② 2020년 7월 6일부터 추가됨
# stlm_dt	결산기준일	YYYY-MM-DD
class AuditServiceContractsItem(BaseModel):
    model_config = ConfigDict(title="감사용역 계약현황 항목", populate_by_name=True)


class AuditServiceContracts(BaseModel, DartHttpBody[AuditServiceContractsItem]):
    model_config = ConfigDict(title="감사용역 계약현황 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# bsns_year	사업연도	사업연도(당기, 전기, 전전기)
# cntrct_cncls_de	계약체결일	계약체결일
# servc_cn	용역내용	용역내용
# servc_exc_pd	용역수행기간	용역수행기간
# servc_mendng	용역보수	용역보수
# rm	비고	비고
# stlm_dt	결산기준일	YYYY-MM-DD
class NonAuditServiceContractsItem(BaseModel):
    model_config = ConfigDict(title="회계감사인과의 비감사용역 계약체결 현황 항목", populate_by_name=True)


class NonAuditServiceContracts(BaseModel, DartHttpBody[NonAuditServiceContractsItem]):
    model_config = ConfigDict(title="회계감사인과의 비감사용역 계약체결 현황 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# drctr_co	이사의 수	9,999,999,999
# otcmp_drctr_co	사외이사 수	9,999,999,999
# apnt	사외이사 변동현황(선임)	9,999,999,999
# rlsofc	사외이사 변동현황(해임)	9,999,999,999
# mdstrm_resig	사외이사 변동현황(중도퇴임)	9,999,999,999
# stlm_dt	결산기준일	YYYY-MM-DD
class OutsideDirectorStatusItem(BaseModel):
    model_config = ConfigDict(title="사외이사 및 변동현황 항목", populate_by_name=True)


class OutsideDirectorStatus(BaseModel, DartHttpBody[OutsideDirectorStatusItem]):
    model_config = ConfigDict(title="사외이사 및 변동현황 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# se	구분	구분(미등기임원)
# nmpr	인원수	9,999,999,999
# fyer_salary_totamt	연간급여 총액	9,999,999,999
# jan_salary_am	1인평균 급여액	9,999,999,999
# rm	비고	비고
# stlm_dt	결산기준일	YYYY-MM-DD
class UnregisteredExecutiveCompensationItem(BaseModel):
    model_config = ConfigDict(title="미등기임원 보수현황 항목", populate_by_name=True)


class UnregisteredExecutiveCompensation(BaseModel, DartHttpBody[UnregisteredExecutiveCompensationItem]):
    model_config = ConfigDict(title="미등기임원 보수현황 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# se	구분	구분
# nmpr	인원수	인원수
# gmtsck_confm_amount	주주총회 승인금액	9,999,999,999
# rm	비고	비고
# stlm_dt	결산기준일	YYYY-MM-DD
class BoardAndAuditCompensationShareholderApprovedItem(BaseModel):
    model_config = ConfigDict(title="이사·감사 전체 보수현황(주주총회 승인금액) 항목", populate_by_name=True)


class BoardAndAuditCompensationShareholderApproved(
    BaseModel, DartHttpBody[BoardAndAuditCompensationShareholderApprovedItem]
):
    model_config = ConfigDict(title="이사·감사 전체 보수현황(주주총회 승인금액) 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# se	구분	구분
# nmpr	인원수	인원수
# gmtsck_confm_amount	주주총회 승인금액	9,999,999,999
# rm	비고	비고
# stlm_dt	결산기준일	YYYY-MM-DD
class BoardAndAuditCompensationByTypeItem(BaseModel):
    model_config = ConfigDict(title="이사·감사 전체 보수현황(보수지급금액 유형별) 항목", populate_by_name=True)


class BoardAndAuditCompensationByType(BaseModel, DartHttpBody[BoardAndAuditCompensationByTypeItem]):
    model_config = ConfigDict(title="이사·감사 전체 보수현황(보수지급금액 유형별) 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# se_nm	구분	구분
# tm	회차	회차 ③ 2019년 12월 9일부터 추가됨
# pay_de	납입일	납입일
# pay_amount	납입금액	9,999,999,999 ① 2018년 1월 18일까지 사용됨
# on_dclrt_cptal_use_plan	신고서상 자금사용 계획	신고서상 자금사용 계획 ① 2018년 1월 18일까지 사용됨
# real_cptal_use_sttus	실제 자금사용 현황	실제 자금사용 현황 ① 2018년 1월 18일까지 사용됨
# rs_cptal_use_plan_useprps	증권신고서 등의 자금사용 계획(사용용도)	증권신고서 등의 자금사용 계획(사용용도) ② 2018년 1월 19일부터 추가됨
# rs_cptal_use_plan_prcure_amount	증권신고서 등의 자금사용 계획(조달금액)	9,999,999,999 ② 2018년 1월 19일부터 추가됨
# real_cptal_use_dtls_cn	실제 자금사용 내역(내용)	실제 자금사용 내역(내용) ② 2018년 1월 19일부터 추가됨
# real_cptal_use_dtls_amount	실제 자금사용 내역(금액)	9,999,999,999 ② 2018년 1월 19일부터 추가됨
# dffrnc_occrrnc_resn	차이발생 사유 등	차이발생 사유 등
# stlm_dt	결산기준일	YYYY-MM-DD
class PublicOfferingFundUsageItem(BaseModel):
    model_config = ConfigDict(title="공모자금 사용내역 항목", populate_by_name=True)


class PublicOfferingFundUsage(BaseModel, DartHttpBody[PublicOfferingFundUsageItem]):
    model_config = ConfigDict(title="공모자금 사용내역 응답", populate_by_name=True)


# rcept_no	접수번호	접수번호(14자리)
# corp_cls	법인구분	법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
# corp_code	고유번호	공시대상회사의 고유번호(8자리)
# corp_name	회사명	공시대상회사명
# se_nm	구분	구분
# tm	회차	회차 ③ 2019년 12월 9일부터 추가됨
# pay_de	납입일	납입일
# pay_amount	납입금액	9,999,999,999 ① 2018년 1월 18일까지 사용됨
# cptal_use_plan	자금사용 계획	자금사용 계획 ① 2018년 1월 18일까지 사용됨
# real_cptal_use_sttus	실제 자금사용 현황	실제 자금사용 현황 ① 2018년 1월 18일까지 사용됨
# mtrpt_cptal_use_plan_useprps	주요사항보고서의 자금사용 계획(사용용도)	주요사항보고서의 자금사용 계획(사용용도) ② 2018년 1월 19일부터 추가됨
# mtrpt_cptal_use_plan_prcure_amount	주요사항보고서의 자금사용 계획(조달금액)	9,999,999,999 ② 2018년 1월 19일부터 추가됨
# real_cptal_use_dtls_cn	실제 자금사용 내역(내용)	실제 자금사용 내역(내용) ② 2018년 1월 19일부터 추가됨
# real_cptal_use_dtls_amount	실제 자금사용 내역(금액)	9,999,999,999 ② 2018년 1월 19일부터 추가됨
# dffrnc_occrrnc_resn	차이발생 사유 등	차이발생 사유 등
# stlm_dt	결산기준일	YYYY-MM-DD
class PrivatePlacementFundUsageItem(BaseModel):
    model_config = ConfigDict(title="사모자금 사용내역 항목", populate_by_name=True)


class PrivatePlacementFundUsage(BaseModel, DartHttpBody[PrivatePlacementFundUsageItem]):
    model_config = ConfigDict(title="사모자금 사용내역 응답", populate_by_name=True)
