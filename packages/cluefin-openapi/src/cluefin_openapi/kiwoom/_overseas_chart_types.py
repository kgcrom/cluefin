from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasChartTickItem(BaseModel):
    cur_prc: str = Field(default="", description="현재가(종가)")
    trde_qty: str = Field(default="", description="거래량")
    open_pric: str = Field(default="", description="시가")
    high_pric: str = Field(default="", description="고가")
    low_pric: str = Field(default="", description="저가")
    cntr_tm: str = Field(default="", description="체결시간")
    bus_dt: str = Field(default="", description="영업일자")
    upd_stkpc_tp: str = Field(default="", description="수정주가구분")
    upd_rt: str = Field(default="", description="수정비율")


class OverseasChartTick(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 틱 차트 응답")

    result_list: list[OverseasChartTickItem] = Field(default_factory=list, description="결과리스트")


class OverseasChartMinuteItem(BaseModel):
    cur_prc: str = Field(default="", description="현재가(종가). 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    trde_qty: str = Field(default="", description="거래량")
    open_pric: str = Field(default="", description="시가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cntr_tm: str = Field(default="", description="체결시간. YYYYMMDDHHmmss")
    bus_dt: str = Field(default="", description="영업일자. YYYYMMDD")
    upd_stkpc_tp: str = Field(default="", description="수정주가구분")
    upd_rt: str = Field(default="", description="수정비율")


class OverseasChartMinute(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 분 차트 응답")

    result_list: list[OverseasChartMinuteItem] = Field(default_factory=list, description="결과리스트")


class OverseasChartDailyItem(BaseModel):
    cur_prc: str = Field(default="", description="현재가(종가). 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    acc_trde_prica: str = Field(default="", description="누적거래대금")
    open_pric: str = Field(default="", description="시가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    dt: str = Field(default="", description="일자. YYYYMMDD")
    upd_stkpc_tp: str = Field(default="", description="수정주가구분")
    upd_rt: str = Field(default="", description="수정비율")


class OverseasChartDaily(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 일 차트 응답")

    result_list: list[OverseasChartDailyItem] = Field(default_factory=list, description="결과리스트")


class OverseasChartWeeklyItem(BaseModel):
    cur_prc: str = Field(default="", description="현재가(종가). 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    acc_trde_prica: str = Field(default="", description="누적거래대금")
    open_pric: str = Field(default="", description="시가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    dt: str = Field(default="", description="일자. YYYYMMDD")
    upd_stkpc_tp: str = Field(default="", description="수정주가구분")
    upd_rt: str = Field(default="", description="수정비율")


class OverseasChartWeekly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 주 차트 응답")

    result_list: list[OverseasChartWeeklyItem] = Field(default_factory=list, description="결과리스트")


class OverseasChartMonthlyItem(BaseModel):
    cur_prc: str = Field(default="", description="현재가(종가). 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    acc_trde_prica: str = Field(default="", description="누적거래대금")
    open_pric: str = Field(default="", description="시가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    dt: str = Field(default="", description="일자. YYYYMMDD")
    upd_stkpc_tp: str = Field(default="", description="수정주가구분")
    upd_rt: str = Field(default="", description="수정비율")


class OverseasChartMonthly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 월 차트 응답")

    result_list: list[OverseasChartMonthlyItem] = Field(default_factory=list, description="결과리스트")


class OverseasChartYearlyItem(BaseModel):
    cur_prc: str = Field(default="", description="현재가(종가). 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    acc_trde_prica: str = Field(default="", description="누적거래대금")
    open_pric: str = Field(default="", description="시가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    dt: str = Field(default="", description="일자. YYYYMMDD")
    upd_stkpc_tp: str = Field(default="", description="수정주가구분")
    upd_rt: str = Field(default="", description="수정비율")


class OverseasChartYearly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 년 차트 응답")

    result_list: list[OverseasChartYearlyItem] = Field(default_factory=list, description="결과리스트")


class OverseasChartQuarterlyItem(BaseModel):
    cur_prc: str = Field(default="", description="현재가(종가). 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    acc_trde_prica: str = Field(default="", description="누적거래대금")
    open_pric: str = Field(default="", description="시가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    dt: str = Field(default="", description="일자. YYYYMMDD")
    upd_stkpc_tp: str = Field(default="", description="수정주가구분")
    upd_rt: str = Field(default="", description="수정비율")


class OverseasChartQuarterly(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 분기 차트 응답")

    result_list: list[OverseasChartQuarterlyItem] = Field(default_factory=list, description="결과리스트")
