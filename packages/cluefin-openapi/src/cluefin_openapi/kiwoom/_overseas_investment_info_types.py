from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasInvestmentInfoResearch(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 리서치(미국주식/ETF) 응답")

    # TODO: 응답 필드 정의
