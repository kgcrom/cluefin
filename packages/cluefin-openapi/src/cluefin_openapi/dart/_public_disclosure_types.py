from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from cluefin_openapi.dart._model import DartHttpBody, DartStatusCode


class PublicDisclosureSearchItem(BaseModel):
    model_config = ConfigDict(title="공시검색 결과 항목", populate_by_name=True)

    corp_cls: str = Field(
        alias="법인구분",
        description="법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)",
    )
    corp_name: str = Field(
        alias="종목명(법인명)",
        description="공시대상회사의 종목명(상장사) 또는 법인명(기타법인)",
    )
    corp_code: str = Field(
        alias="고유번호",
        description="공시대상회사의 고유번호(8자리)",
    )
    stock_code: str = Field(
        alias="종목코드",
        description="상장회사의 종목코드(6자리)",
    )
    report_nm: str = Field(
        alias="보고서명",
        description="공시 보고서명. 기재정정, 첨부정정 등 수정 사유가 포함될 수 있습니다.",
    )
    rcept_no: str = Field(
        alias="접수번호",
        description="접수번호(14자리). 전자공시시스템 공시뷰어 연결에 사용됩니다.",
    )
    flr_nm: str = Field(
        alias="공시 제출인명",
        description="공시를 제출한 개인 또는 기관명",
    )
    rcept_dt: str = Field(
        alias="접수일자",
        description="공시 접수일자(YYYYMMDD)",
    )
    rm: str = Field(
        alias="비고",
        description=(
            "공시 사유 코드: 유(한국채권자유증권시장부 소관), 코(코스닥시장본부 소관), "
            "채(채권시장본부 소관), 넥(코넥스시장본부 소관), 공(공시보고서참고사유 존재), "
            "연(정정서류 관련 공시), 정(정정서류 참조사항), 철(정정서류 관련철회사유)"
        ),
    )


class PublicDisclosureSearch(BaseModel, DartHttpBody):
    model_config = ConfigDict(title="공시검색 요청 응답")

    list: List[PublicDisclosureSearchItem] = Field(default_factory=list, alias="공시검색")


class CompanyOverview(BaseModel):
    model_config = ConfigDict(title="기업개황 응답", populate_by_name=True)

    status: DartStatusCode = Field(
        alias="에러 및 정보 코드",
        description="에러 및 정보 코드(※메시지 설명 참조)",
    )
    message: str = Field(
        alias="에러 및 정보 메시지",
        description="에러 및 정보 메시지(※메시지 설명 참조)",
    )
    corp_name: str = Field(alias="정식명칭")
    corp_name_eng: str = Field(
        alias="영문명칭",
        description="영문정식회사명칭",
    )
    stock_name: str = Field(alias="종목명(상장사) 또는 약식명칭(기타법인)")
    stock_code: str = Field(
        alias="상장회사인 경우 주식의 종목코드",
        description="상장회사의 종목코드(6자리)",
    )
    ceo_nm: str = Field(alias="대표자명")
    corp_cls: str = Field(
        alias="법인구분",
        description="법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)",
    )
    jurir_no: str = Field(alias="법인등록번호")
    bizr_no: str = Field(alias="사업자등록번호")
    adres: str = Field(alias="주소")
    hm_url: str = Field(alias="홈페이지")
    ir_url: str = Field(alias="IR홈페이지")
    phn_no: str = Field(alias="전화번호")
    fax_no: str = Field(alias="팩스번호")
    induty_code: str = Field(alias="업종코드")
    est_dt: str = Field(alias="설립일(YYYYMMDD)")
    acc_mt: str = Field(alias="결산월(MM)")


class UniqueNumberItem(BaseModel):
    model_config = ConfigDict(title="공시대상회사 고유번호 항목", populate_by_name=True)

    corp_code: str = Field(
        alias="corp_code",
        description="공시대상회사의 고유번호(8자리)",
    )
    corp_name: str = Field(
        alias="corp_name",
        description="공시대상회사 정식명칭",
    )
    corp_eng_name: Optional[str] = Field(
        default=None,
        alias="corp_eng_name",
        description="공시대상회사 영문 정식명칭",
    )
    corp_cls: Optional[str] = Field(
        default=None,
        alias="corp_cls",
        description="법인구분: Y(유가), K(코스닥), N(코넥스), E(기타)",
    )
    stock_code: Optional[str] = Field(
        default=None,
        alias="stock_code",
        description="상장회사의 경우 주식 종목코드(6자리)",
    )
    modify_date: str = Field(
        alias="modify_date",
        description="기업개황정보 최종변경일자(YYYYMMDD)",
    )


class UniqueNumber(BaseModel, DartHttpBody):
    model_config = ConfigDict(title="공시대상회사 고유번호 목록", populate_by_name=True)

    list: List[UniqueNumberItem] = Field(
        default_factory=list,
        alias="list",
        description="공시대상회사 고유번호 목록",
    )
