from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.dart._model import DartHttpBody


class SingleCompanyMajorAccountItem(BaseModel):
    model_config = ConfigDict(title="단일회사 주요계정 현황", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)", max_length=14)
    bsns_year: str = Field(description="사업 연도 (YYYY)")
    stock_code: str = Field(description="종목 코드 (상장회사의 종목코드 6자리)")
    reprt_code: str = Field(
        description="보고서 코드 (1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서:11011)"
    )
    account_nm: str = Field(description="계정명 (ex: 자본총계)")
    fs_div: str = Field(description="개별/연결구분 (OFS:재무제표, CFS:연결재무제표)")
    fs_nm: str = Field(description="개별/연결명 (ex: 연결재무제표 또는 재무제표 출력)")
    sj_div: str = Field(description="재무제표구분 (BS:재무상태표, IS:손익계산서)")
    sj_nm: str = Field(description="재무제표명 (ex: 재무상태표 또는 손익계산서 출력)")
    thstrm_nm: str = Field(description="당기명 (ex: 제 13 기 3분기말)")
    thstrm_dt: str = Field(description="당기일자 (ex: 2018.09.30 현재)")
    thstrm_amount: str = Field(description="당기금액 (ex: 9,999,999,999)")
    thstrm_add_amount: Optional[str] = Field(description="당기누적금액 (ex: 9,999,999,999)", default=None)
    frmtrm_nm: str = Field(description="전기명 (ex: 제 12 기말)")
    frmtrm_dt: str = Field(description="전기일자 (ex: 2017.01.01 ~ 2017.12.31)")
    frmtrm_amount: str = Field(description="전기금액 (ex: 9,999,999,999)")
    frmtrm_add_amount: Optional[str] = Field(description="전기누적금액 (ex: 9,999,999,999)", default=None)
    bfefrmtrm_nm: str = Field(description="전전기명 (ex: 제 11 기말(※ 사업보고서의 경우에만 출력))")
    bfefrmtrm_dt: str = Field(description="전전기일자 (ex: 2016.12.31 현재(※ 사업보고서의 경우에만 출력))")
    bfefrmtrm_amount: str = Field(description="전전기금액 (ex: 9,999,999,999(※ 사업보고서의 경우에만 출력))")
    ord: int = Field(description="계정과목 정렬순서")
    currency: str = Field(description="통화 단위")


class SingleCompanyMajorAccount(BaseModel, DartHttpBody[SingleCompanyMajorAccountItem]):
    model_config = ConfigDict(title="단일회사 주요계정 응답", populate_by_name=True)


class MultiCompanyMajorAccountItem(BaseModel):
    model_config = ConfigDict(title="다중회사 주요계정 현황", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)", max_length=14)
    bsns_year: str = Field(description="사업 연도 (YYYY)")
    stock_code: str = Field(description="종목 코드 (상장회사의 종목코드 6자리)")
    corp_name: Optional[str] = Field(description="회사명", default=None)
    corp_code: str = Field(description="공시대상회사 고유번호 (8자리)")
    reprt_code: str = Field(
        description="보고서 코드 (1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서:11011)"
    )
    account_nm: str = Field(description="계정명 (ex: 자본총계)")
    fs_div: str = Field(description="개별/연결구분 (OFS:재무제표, CFS:연결재무제표)")
    fs_nm: str = Field(description="개별/연결명 (ex: 연결재무제표 또는 재무제표 출력)")
    sj_div: str = Field(description="재무제표구분 (BS:재무상태표, IS:손익계산서)")
    sj_nm: str = Field(description="재무제표명 (ex: 재무상태표 또는 손익계산서 출력)")
    thstrm_nm: str = Field(description="당기명 (ex: 제 13 기 3분기말)")
    thstrm_dt: str = Field(description="당기일자 (ex: 2018.09.30 현재)")
    thstrm_amount: str = Field(description="당기금액 (ex: 9,999,999,999)")
    thstrm_add_amount: Optional[str] = Field(description="당기누적금액 (ex: 9,999,999,999)", default=None)
    frmtrm_nm: str = Field(description="전기명 (ex: 제 12 기말)")
    frmtrm_dt: str = Field(description="전기일자 (ex: 2017.01.01 ~ 2017.12.31)")
    frmtrm_amount: str = Field(description="전기금액 (ex: 9,999,999,999)")
    frmtrm_add_amount: Optional[str] = Field(description="전기누적금액 (ex: 9,999,999,999)", default=None)
    bfefrmtrm_nm: str = Field(description="전전기명 (ex: 제 11 기말(※ 사업보고서의 경우에만 출력))")
    bfefrmtrm_dt: str = Field(description="전전기일자 (ex: 2016.12.31 현재(※ 사업보고서의 경우에만 출력))")
    bfefrmtrm_amount: str = Field(description="전전기금액 (ex: 9,999,999,999(※ 사업보고서의 경우에만 출력))")
    ord: str = Field(description="계정과목 정렬순서")
    currency: str = Field(description="통화 단위")


class MultiCompanyMajorAccount(BaseModel, DartHttpBody[MultiCompanyMajorAccountItem]):
    model_config = ConfigDict(title="다중회사 주요계정 응답", populate_by_name=True)


class SingleCompanyFullStatementItem(BaseModel):
    model_config = ConfigDict(title="단일회사 전체 재무제표 현황", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)", max_length=14)
    reprt_code: str = Field(
        description="보고서 코드 (1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서:11011)"
    )
    bsns_year: str = Field(description="사업 연도 (YYYY)")
    corp_code: str = Field(description="고유번호 (공시대상회사의 고유번호(8자리))")
    sj_div: str = Field(
        description="재무제표구분 (BS : 재무상태표 IS : 손익계산서 CIS : 포괄손익계산서 CF : 현금흐름표 SCE : 자본변동표)"
    )
    sj_nm: str = Field(description="재무제표명 (ex: 재무상태표 또는 손익계산서 출력)")
    account_id: str = Field(description='계정ID (XBRL 표준계정ID ※ 표준계정ID가 아닐경우 "-표준계정코드 미사용-" 표시)')
    account_nm: str = Field(description="계정명 (계정명칭 ex) 자본총계)")
    account_detail: str = Field(description="계정상세 (※ 자본변동표에만 출력)")
    thstrm_nm: str = Field(description="당기명 (ex: 제 13 기)")
    thstrm_amount: str = Field(
        description="당기금액 (9,999,999,999 ※ 분/반기 보고서이면서 (포괄)손익계산서 일 경우 [3개월] 금액)"
    )
    thstrm_add_amount: Optional[str] = Field(description="당기누적금액 (9,999,999,999)", default=None)
    frmtrm_nm: str = Field(description="전기명 (ex: 제 12 기말)")
    frmtrm_amount: str = Field(description="전기금액 (9,999,999,999)")
    frmtrm_q_nm: Optional[str] = Field(description="전기명(분/반기) (ex: 제 18 기 반기)", default=None)
    frmtrm_q_amount: Optional[str] = Field(
        description="전기금액(분/반기) (9,999,999,999 ※ 분/반기 보고서이면서 (포괄)손익계산서 일 경우 [3개월] 금액)",
        default=None,
    )
    frmtrm_add_amount: Optional[str] = Field(description="전기누적금액 (9,999,999,999)", default=None)
    bfefrmtrm_nm: str = Field(description="전전기명 (ex: 제 11 기말(※ 사업보고서의 경우에만 출력))")
    bfefrmtrm_amount: str = Field(description="전전기금액 (9,999,999,999(※ 사업보고서의 경우에만 출력))")
    ord: str = Field(description="계정과목 정렬순서 (계정과목 정렬순서)")
    currency: str = Field(description="통화 단위 (통화 단위)")


class SingleCompanyFullStatement(BaseModel, DartHttpBody[SingleCompanyFullStatementItem]):
    model_config = ConfigDict(title="단일회사 전체 재무제표 응답", populate_by_name=True)


class SingleCompanyMajorIndicatorItem(BaseModel):
    model_config = ConfigDict(title="단일회사 주요 재무지표 현황", populate_by_name=True)

    reprt_code: str = Field(
        description="보고서 코드 (1분기보고서 : 11013, 반기보고서 : 11012, 3분기보고서 : 11014, 사업보고서 : 11011)"
    )
    bsns_year: str = Field(description="사업 연도 (YYYY)")
    corp_code: str = Field(description="고유번호 (공시대상회사의 고유번호(8자리))")
    stock_code: str = Field(description="종목 코드 (상장회사의 종목코드(6자리))")
    stlm_dt: str = Field(description="결산기준일 (YYYY-MM-DD)")
    idx_cl_code: str = Field(
        description="지표분류코드 (수익성지표 : M210000 안정성지표 : M220000 성장성지표 : M230000 활동성지표 : M240000)"
    )
    idx_cl_nm: str = Field(description="지표분류명 (수익성지표,안정성지표,성장성지표,활동성지표)")
    idx_code: str = Field(description="지표코드 (ex) M211000")
    idx_nm: str = Field(description="지표명 (ex) 영업이익률")
    idx_val: Optional[str] = Field(description="지표값 (ex) 0.256 — 일부 항목은 값이 제공되지 않습니다.", default=None)


class SingleCompanyMajorIndicator(BaseModel, DartHttpBody[SingleCompanyMajorIndicatorItem]):
    model_config = ConfigDict(title="단일회사 주요 재무지표 응답", populate_by_name=True)


class MultiCompanyMajorIndicatorItem(BaseModel):
    model_config = ConfigDict(title="다중회사 주요 재무지표 현황", populate_by_name=True)

    reprt_code: str = Field(
        description="보고서 코드 (1분기보고서 : 11013, 반기보고서 : 11012, 3분기보고서 : 11014, 사업보고서 : 11011)"
    )
    bsns_year: str = Field(description="사업 연도 (YYYY)")
    corp_code: str = Field(description="고유번호 (공시대상회사의 고유번호(8자리))")
    stock_code: str = Field(description="종목 코드 (상장회사의 종목코드(6자리))")
    stlm_dt: str = Field(description="결산기준일 (YYYY-MM-DD)")
    idx_cl_code: str = Field(
        description="지표분류코드 (수익성지표 : M210000 안정성지표 : M220000 성장성지표 : M230000 활동성지표 : M240000)"
    )
    idx_cl_nm: str = Field(description="지표분류명 (수익성지표,안정성지표,성장성지표,활동성지표)")
    idx_code: str = Field(description="지표코드 (ex) M211000")
    idx_nm: str = Field(description="지표명 (ex) 영업이익률")
    idx_val: Optional[str] = Field(description="지표값 (ex) 0.256 — 일부 항목은 값이 제공되지 않습니다.", default=None)


class MultiCompanyMajorIndicator(BaseModel, DartHttpBody[MultiCompanyMajorIndicatorItem]):
    model_config = ConfigDict(title="다중회사 주요 재무지표 응답", populate_by_name=True)


class XbrlTaxonomyItem(BaseModel):
    model_config = ConfigDict(title="XBRL 택사노미 재무제표 양식 현황", populate_by_name=True)

    sj_div: str = Field(
        description="재무제표구분 (BS1:재무상태표, BS2:재무상태표(요약), BS3:재무상태표(비교), BS4:재무상태표(요약,비교), IS1:손익계산서, IS2:손익계산서(요약), IS3:손익계산서(비교), IS4:손익계산서(요약,비교), CIS1:포괄손익계산서, CIS2:포괄손익계산서(요약), CIS3:포괄손익계산서(비교), CIS4:포괄손익계산서(요약,비교), DCIS1:별도손익계산서, DCIS2:별도손익계산서(요약), DCIS3:별도손익계산서(비교), DCIS4:별도손익계산서(요약,비교), DCIS5:별도포괄손익계산서, DCIS6:별도포괄손익계산서(요약), DCIS7:별도포괄손익계산서(비교), DCIS8:별도포괄손익계산서(요약,비교), CF1:현금흐름표, CF2:현금흐름표(요약), CF3:현금흐름표(비교), CF4:현금흐름표(요약,비교), SCE1:자본변동표, SCE2:자본변동표(요약))"
    )
    account_id: str = Field(description='계정ID (XBRL 표준계정ID ※ 표준계정ID가 아닐경우 "-표준계정코드 미사용-" 표시)')
    account_nm: str = Field(description="계정명 (계정명칭 ex) 자본총계)")
    bsns_de: str = Field(description="기준일 (ex: 20221231)")
    label_kor: str = Field(description="한글 출력명 (ex: 자본총계)")
    label_eng: str = Field(description="영문 출력명 (ex: Total Equity)")
    data_tp: Optional[str] = Field(
        default=None,
        description="데이터 유형 (※ 데이타 유형설명 - text block : 제목 - Text : Text - yyyy-mm-dd : Date - X : Monetary Value - (X): Monetary Value(Negative) - X.XX : Decimalized Value - Shares : Number of shares (주식 수) - For each : 공시된 항목이 전후로 반복적으로 공시될 경우 사용 - 공란 : 입력 필요 없음)",
    )
    ifrs_ref: str = Field(description="IFRS Reference (ex: K-IFRS 1001 문단 54 (9),K-IFRS 1007 문단 45)")


class XbrlTaxonomy(BaseModel, DartHttpBody[XbrlTaxonomyItem]):
    model_config = ConfigDict(title="XBRL 택사노미 재무제표 양식 응답", populate_by_name=True)
