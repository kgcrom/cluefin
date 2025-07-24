from pydantic import BaseModel, Field

from cluefin_openapi.krx._model import KrxHttpBody


class EsgSociallyResponsibleInvestmentBondItem(BaseModel):
    base_date: str = Field(description="기준일자 (YYYYMMDD)", alias="BAS_DD")
    issuer_name: str = Field(description="발행기관", alias="ISUR_NM")
    issued_code: str = Field(description="표준코드", alias="ISU_CD")
    bond_type: str = Field(description="채권종류", alias="SRI_BND_TP_NM")
    issued_name: str = Field(description="종목명", alias="ISU_NM")
    listing_date: str = Field(description="상장일", alias="LIST_DD")
    issue_date: str = Field(description="발행일", alias="ISU_DD")
    redemption_date: str = Field(description="상환일", alias="REDMPT_DD")
    issue_rate: str = Field(description="표면이자율", alias="ISU_RT")
    issue_amount: str = Field(description="발행금액", alias="ISU_AMT")
    listing_amount: str = Field(description="상장금액", alias="LIST_AMT")
    bond_type_name: str = Field(description="채권유형", alias="BND_TP_NM")


class EsgSociallyResponsibleInvestmentBond(BaseModel, KrxHttpBody):
    data: list[EsgSociallyResponsibleInvestmentBondItem] = Field(
        default_factory=list, description="사회책임투자채권 정보", alias="OutBlock_1"
    )
