from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasSectorIndustryPeriodProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 업종별 기간별 수익률 조회 응답")

    # TODO: 응답 필드 정의


class OverseasSectorIndustryFluctuationRank(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 업종별 등락률 상위/하위 조회 응답")

    # TODO: 응답 필드 정의
