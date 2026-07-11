from pydantic import BaseModel
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasWatchlistGroupList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 관심종목 그룹 리스트 조회 응답")

    # TODO: 응답 필드 정의


class OverseasWatchlistGroupDetail(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 관심종목 그룹 상세 조회 응답")

    # TODO: 응답 필드 정의
