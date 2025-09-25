from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.dart._model import DartHttpBody


class LargeHoldingReportItem(BaseModel):
    model_config = ConfigDict(title="주식등의 대량보유 상황보고 항목", populate_by_name=True)

    rcept_no: str = Field(
        alias="rcept_no",
        description="접수번호(14자리)",
    )
    rcept_dt: str = Field(
        alias="rcept_dt",
        description="공시 접수일자(YYYYMMDD)",
    )
    corp_code: str = Field(
        alias="corp_code",
        description="공시대상회사의 고유번호(8자리)",
    )
    corp_name: Optional[str] = Field(
        default=None,
        alias="corp_name",
        description="공시대상회사의 종목명(상장사) 또는 법인명(기타법인)",
    )
    report_tp: Optional[str] = Field(
        default=None,
        alias="report_tp",
        description="보고구분",
    )
    repror: Optional[str] = Field(
        default=None,
        alias="repror",
        description="대표보고자명",
    )
    stkqy: Optional[str] = Field(
        default=None,
        alias="stkqy",
        description="보유주식등의 수",
    )
    stkqy_irds: Optional[str] = Field(
        default=None,
        alias="stkqy_irds",
        description="보유주식등의 증감",
    )
    stkrt: Optional[str] = Field(
        default=None,
        alias="stkrt",
        description="보유비율",
    )
    stkrt_irds: Optional[str] = Field(
        default=None,
        alias="stkrt_irds",
        description="보유비율 증감",
    )
    ctr_stkqy: Optional[str] = Field(
        default=None,
        alias="ctr_stkqy",
        description="주요체결 주식등의 수",
    )
    ctr_stkrt: Optional[str] = Field(
        default=None,
        alias="ctr_stkrt",
        description="주요체결 보유비율",
    )
    report_resn: Optional[str] = Field(
        default=None,
        alias="report_resn",
        description="보고사유",
    )


class LargeHoldingReport(BaseModel, DartHttpBody[LargeHoldingReportItem]):
    model_config = ConfigDict(title="주식등의 대량보유 상황보고 응답", populate_by_name=True)


class ExecutiveMajorShareholderOwnershipReportItem(BaseModel):
    model_config = ConfigDict(title="임원·주요주주 소유보고 항목", populate_by_name=True)

    rcept_no: str = Field(
        alias="rcept_no",
        description="접수번호(14자리)",
    )
    rcept_dt: str = Field(
        alias="rcept_dt",
        description="공시 접수일자(YYYYMMDD)",
    )
    corp_code: str = Field(
        alias="corp_code",
        description="공시대상회사의 고유번호(8자리)",
    )
    corp_name: Optional[str] = Field(
        default=None,
        alias="corp_name",
        description="회사명",
    )
    repror: Optional[str] = Field(
        default=None,
        alias="repror",
        description="보고자명",
    )
    isu_exctv_rgist_at: Optional[str] = Field(
        default=None,
        alias="isu_exctv_rgist_at",
        description="발행 회사 관계 임원(등기임원, 비등기임원 등)",
    )
    isu_exctv_ofcps: Optional[str] = Field(
        default=None,
        alias="isu_exctv_ofcps",
        description="발행 회사 관계 임원 직위(대표이사, 이사, 전무 등)",
    )
    isu_main_shrhldr: Optional[str] = Field(
        default=None,
        alias="isu_main_shrhldr",
        description="발행 회사 관계 주요 주주(10%이상주주 등)",
    )
    sp_stock_lmp_cnt: Optional[str] = Field(
        default=None,
        alias="sp_stock_lmp_cnt",
        description="특정 증권 등 소유 수",
    )
    sp_stock_lmp_irds_cnt: Optional[str] = Field(
        default=None,
        alias="sp_stock_lmp_irds_cnt",
        description="특정 증권 등 소유 증감 수",
    )
    sp_stock_lmp_rate: Optional[str] = Field(
        default=None,
        alias="sp_stock_lmp_rate",
        description="특정 증권 등 소유 비율",
    )
    sp_stock_lmp_irds_rate: Optional[str] = Field(
        default=None,
        alias="sp_stock_lmp_irds_rate",
        description="특정 증권 등 소유 증감 비율",
    )


class ExecutiveMajorShareholderOwnershipReport(BaseModel, DartHttpBody[ExecutiveMajorShareholderOwnershipReportItem]):
    model_config = ConfigDict(title="임원·주요주주 소유보고 응답", populate_by_name=True)
