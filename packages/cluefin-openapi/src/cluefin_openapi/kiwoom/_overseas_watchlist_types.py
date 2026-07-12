from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasWatchlistGroupListItem(BaseModel):
    gcod: str = Field(default="", description="그룹코드")
    name: str = Field(default="", description="그룹명")


class OverseasWatchlistGroupList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 관심종목 그룹 리스트 조회 응답")

    rtcd: str = Field(default="", description="처리결과. S:성공 F:실패")
    nofi: list[OverseasWatchlistGroupListItem] = Field(default_factory=list, description="그룹갯수")


class OverseasWatchlistGroupDetailItem(BaseModel):
    cod2: str = Field(default="", description="종목코드")
    bgb: str = Field(default="", description="북마크 구분")
    bgb_clr: str = Field(default="", description="북마크 컬러")
    stex_tp: str = Field(default="", description="거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX")


class OverseasWatchlistGroupDetail(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 관심종목 그룹 상세 조회 응답")

    rtcd: str = Field(default="", description="처리 결과. S:성공 F:실패")
    nofj: list[OverseasWatchlistGroupDetailItem] = Field(default_factory=list, description="종목 갯수")
