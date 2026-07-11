from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasSectorIndustryPeriodProfitRateItem(BaseModel):
    inds_cd: str = Field(default="", description="업종코드")
    inds_nm: str = Field(default="", description="업종명")
    perf_1d: str = Field(default="", description="1일 수익률. 소수점 둘째 자리까지 포맷된 숫자")
    perf_5d: str = Field(default="", description="5일 수익률. 소수점 둘째 자리까지 포맷된 숫자")
    perf_1m: str = Field(default="", description="1개월 수익률. 소수점 둘째 자리까지 포맷된 숫자")
    perf_3m: str = Field(default="", description="3개월 수익률. 소수점 둘째 자리까지 포맷된 숫자")
    perf_6m: str = Field(default="", description="6개월 수익률. 소수점 둘째 자리까지 포맷된 숫자")
    perf_ytd: str = Field(default="", description="연중 수익률. 소수점 둘째 자리까지 포맷된 숫자")
    perf_1y: str = Field(default="", description="1년 수익률. 소수점 둘째 자리까지 포맷된 숫자")


class OverseasSectorIndustryPeriodProfitRate(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 업종별 기간별 수익률 조회 응답")

    result_list: list[OverseasSectorIndustryPeriodProfitRateItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasSectorIndustryFluctuationRankItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="한글종목명")
    stk_enm: str = Field(default="", description="영문종목명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량")
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    cntr_tm: str = Field(default="", description="시간. HH:mm")


class OverseasSectorIndustryFluctuationRank(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 업종별 등락률 상위/하위 조회 응답")

    result_list: list[OverseasSectorIndustryFluctuationRankItem] = Field(default_factory=list, description="결과리스트")
