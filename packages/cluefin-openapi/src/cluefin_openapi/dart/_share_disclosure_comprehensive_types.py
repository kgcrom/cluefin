from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.dart._model import DartHttpBody


class LargeHoldingReportItem(BaseModel):
    model_config = ConfigDict(title="주식등의 대량보유 상황보고 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)", max_length=14)
    rcept_dt: str = Field(description="공시 접수일자(YYYYMMDD)")
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)", max_length=8)
    corp_name: str = Field(description="공시대상회사의 종목명(상장사) 또는 법인명(기타법인)")
    report_tp: str = Field(description="보고구분")
    repror: str = Field(description="대표보고자명")
    stkqy: str = Field(description="보유주식등의 수")
    stkqy_irds: str = Field(description="보유주식등의 증감")
    stkrt: str = Field(description="보유비율")
    stkrt_irds: str = Field(description="보유비율 증감")
    ctr_stkqy: str = Field(description="주요체결 주식등의 수")
    ctr_stkrt: str = Field(description="주요체결 보유비율")
    report_resn: str = Field(description="보고사유")


class LargeHoldingReport(BaseModel, DartHttpBody[LargeHoldingReportItem]):
    model_config = ConfigDict(title="주식등의 대량보유 상황보고 응답", populate_by_name=True)


class ExecutiveMajorShareholderOwnershipReportItem(BaseModel):
    model_config = ConfigDict(title="임원·주요주주 소유보고 항목", populate_by_name=True)

    rcept_no: str = Field(description="접수번호(14자리)", max_length=14)
    rcept_dt: str = Field(
        description="공시 접수일자(YYYYMMDD)",
    )
    corp_code: str = Field(description="공시대상회사의 고유번호(8자리)", max_length=8)
    corp_name: str = Field(
        description="회사명",
    )
    repror: str = Field(description="보고자명")
    isu_exctv_rgist_at: str = Field(description="발행 회사 관계 임원(등기임원, 비등기임원 등)")
    isu_exctv_ofcps: str = Field(
        description="발행 회사 관계 임원 직위(대표이사, 이사, 전무 등)",
    )
    isu_main_shrhldr: Optional[str] = Field(description="발행 회사 관계 주요 주주(10%이상주주 등)", default=None)
    sp_stock_lmp_cnt: str = Field(description="특정 증권 등 소유 수")
    sp_stock_lmp_irds_cnt: str = Field(description="특정 증권 등 소유 증감 수")
    sp_stock_lmp_rate: str = Field(
        description="특정 증권 등 소유 비율",
    )
    sp_stock_lmp_irds_rate: str = Field(
        description="특정 증권 등 소유 증감 비율",
    )


class ExecutiveMajorShareholderOwnershipReport(BaseModel, DartHttpBody[ExecutiveMajorShareholderOwnershipReportItem]):
    model_config = ConfigDict(title="임원·주요주주 소유보고 응답", populate_by_name=True)
