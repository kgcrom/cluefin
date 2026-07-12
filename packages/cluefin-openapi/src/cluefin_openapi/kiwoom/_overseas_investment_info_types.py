from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasInvestmentInfoResearchItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="누적거래량")


class OverseasInvestmentInfoResearch(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 리서치(미국주식/ETF) 응답")

    result_list: list[OverseasInvestmentInfoResearchItem] = Field(default_factory=list, description="결과리스트")
