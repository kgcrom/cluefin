from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasRankInfoRealtimeSymbolQueryRankItem(BaseModel):
    rank: str = Field(default="", description="종목순위")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    sign: str = Field(default="", description="등락부호. +: 상승, -:하락, '': 보합")
    chg_val: str = Field(default="", description="직전대비 순위변화값")
    curr_pric: str = Field(default="", description="현재가. 소수점 넷째 자리까지 포맷된 숫자")
    sign_for_gjga: str = Field(default="", description="기준가대비 부호. +: 상승, -:하락, '': 보합")
    diff_rate_for_gjga: str = Field(
        default="", description="기준가대비 등락률. 단위: %, 소수점 넷째 자리까지 포맷된 백분율"
    )
    sign_for_prev: str = Field(default="", description="직전기준대비 부호. +: 상승, -:하락, '': 보합")
    diff_rate_for_prev: str = Field(
        default="", description="직전기준대비 등락률. 단위: %, 소수점 넷째 자리까지 포맷된 백분율"
    )
    stex_tp: str = Field(default="", description="거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX")


class OverseasRankInfoRealtimeSymbolQueryRank(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 실시간 종목 조회 순위 응답")

    base_date: str = Field(default="", description="기준날짜. YYYYMMDD")
    base_time: str = Field(default="", description="기준시간. HHmmss")
    result_list: list[OverseasRankInfoRealtimeSymbolQueryRankItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoWatchlistRegistrationTopItem(BaseModel):
    rank: str = Field(default="", description="순위")
    rank_flu_sig: str = Field(default="", description="순위등락부호. +:상승, -:하락, 0:순위변동없음, N:신규진입")
    rank_flu: str = Field(default="", description="순위등락폭. 부호가 포함된 숫자")
    stex_tp: str = Field(default="", description="거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일거래량대비. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")


class OverseasRankInfoWatchlistRegistrationTop(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 관심종목 등록 상위 응답")

    result_list: list[OverseasRankInfoWatchlistRegistrationTopItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoPeriodFluctuationRankStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    stdt_base_pric: str = Field(
        default="", description="시작일기준가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    endt_base_pric: str = Field(
        default="", description="종료일기준가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    stdt_trde_qty: str = Field(default="", description="시작일거래량. 단위: 1주")
    endt_trde_qty: str = Field(default="", description="종료일거래량. 단위: 1주")


class OverseasRankInfoPeriodFluctuationRankStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 등락률상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoPeriodFluctuationRankStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoPeriodFluctuationRankEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    stdt_base_pric: str = Field(
        default="", description="시작일기준가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    endt_base_pric: str = Field(
        default="", description="종료일기준가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    stdt_trde_qty: str = Field(default="", description="시작일거래량. 단위: 1주")
    endt_trde_qty: str = Field(default="", description="종료일거래량. 단위: 1주")


class OverseasRankInfoPeriodFluctuationRankEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 등락률상위(ETF) 응답")

    result_list: list[OverseasRankInfoPeriodFluctuationRankEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoPeriodFluctuationRankWatchlistItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    stdt_base_pric: str = Field(
        default="", description="시작일기준가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    endt_base_pric: str = Field(
        default="", description="종료일기준가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    stdt_trde_qty: str = Field(default="", description="시작일거래량. 단위: 1주")
    endt_trde_qty: str = Field(default="", description="종료일거래량. 단위: 1주")


class OverseasRankInfoPeriodFluctuationRankWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 기간별 등락률상위(관심종목) 응답")

    result_list: list[OverseasRankInfoPeriodFluctuationRankWatchlistItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoTodayTradingVolumeTopStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    pred_rt: str = Field(default="", description="전일비. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    trde_prica: str = Field(default="", description="거래대금. 단위: 천USD")


class OverseasRankInfoTodayTradingVolumeTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 거래량 상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoTodayTradingVolumeTopStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoTodayTradingVolumeTopEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    pred_rt: str = Field(default="", description="전일비. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    trde_prica: str = Field(default="", description="거래대금. 단위: 천USD")


class OverseasRankInfoTodayTradingVolumeTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 거래량 상위(ETF) 응답")

    result_list: list[OverseasRankInfoTodayTradingVolumeTopEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoTodayTradingValueTopStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소 구분. ND:NASDAQ,NY:NYSE,NA:AMEX")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    pred_trde_qty: str = Field(default="", description="전일거래량. 단위: 1주")
    trde_prica: str = Field(default="", description="거래대금. 단위: 천USD")


class OverseasRankInfoTodayTradingValueTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 거래대금 상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoTodayTradingValueTopStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoTodayTradingValueTopEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소 구분")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    pred_trde_qty: str = Field(default="", description="전일거래량. 단위: 1주")
    trde_prica: str = Field(default="", description="거래대금. 단위: 천USD")


class OverseasRankInfoTodayTradingValueTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 당일 거래대금 상위(ETF) 응답")

    result_list: list[OverseasRankInfoTodayTradingValueTopEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoMarketCapTopStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    mac: str = Field(default="", description="시가총액. 단위: 천USD")
    trde_pre_rt: str = Field(default="", description="거래대비율. 소수점 둘째 자리까지 포맷된 숫자")
    mac_wght: str = Field(default="", description="시가총액비. 소수점 둘째 자리까지 포맷된 숫자")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")


class OverseasRankInfoMarketCapTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가총액상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoMarketCapTopStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasRankInfoMarketCapTopEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. ND:NASDAQ,NY:NYSE,NA:AMEX")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    mac: str = Field(default="", description="시가총액. 단위: 천USD")
    trde_pre_rt: str = Field(default="", description="거래대비율. 소수점 둘째 자리까지 포맷된 숫자")
    mac_wght: str = Field(default="", description="시가총액비. 소수점 둘째 자리까지 포맷된 숫자")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")


class OverseasRankInfoMarketCapTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가총액상위(ETF) 응답")

    result_list: list[OverseasRankInfoMarketCapTopEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasRankInfoKiwoomTradingTopStockItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    kw_high_rank: str = Field(default="", description="키움상위순위")
    kw_high_rank_sig: str = Field(default="", description="키움상위순위등락부호. 0:신규,1:상승,2:하락,3:동일")
    kw_high_rank_hl: str = Field(default="", description="키움상위 순위등락폭")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")


class OverseasRankInfoKiwoomTradingTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="키움 거래 상위 종목(미국주식) 응답")

    result_list: list[OverseasRankInfoKiwoomTradingTopStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasRankInfoKiwoomTradingTopEtfItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    kw_high_rank: str = Field(default="", description="키움상위순위")
    kw_high_rank_sig: str = Field(default="", description="키움상위순위등락부호. 0:신규,1:상승,2:하락,3:동일")
    kw_high_rank_hl: str = Field(default="", description="키움상위 순위등락폭")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")


class OverseasRankInfoKiwoomTradingTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="키움 거래 상위 종목(미국 ETF) 응답")

    result_list: list[OverseasRankInfoKiwoomTradingTopEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasRankInfoPreviousDayFluctuationRankStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    sel_req: str = Field(default="", description="매도잔량. 단위: 1주")
    buy_req: str = Field(default="", description="매수잔량. 단위: 1주")
    trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    cnt: str = Field(default="", description="횟수")


class OverseasRankInfoPreviousDayFluctuationRankStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 전일대비 등락률상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoPreviousDayFluctuationRankStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoPreviousDayFluctuationRankEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    sel_req: str = Field(default="", description="매도잔량. 단위: 1주")
    buy_req: str = Field(default="", description="매수잔량. 단위: 1주")
    trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    cnt: str = Field(default="", description="횟수")


class OverseasRankInfoPreviousDayFluctuationRankEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 전일대비 등락률상위(ETF) 응답")

    result_list: list[OverseasRankInfoPreviousDayFluctuationRankEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoOpenPriceFluctuationRankStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    open_pric_pre: str = Field(default="", description="시가대비 등락률. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    cntr_tm: str = Field(default="", description="체결시간. HH:mm")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasRankInfoOpenPriceFluctuationRankStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가대비 등락률상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoOpenPriceFluctuationRankStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoOpenPriceFluctuationRankEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    open_pric_pre: str = Field(default="", description="시가대비 등락률. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    cntr_tm: str = Field(default="", description="체결시간. HH:mm")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasRankInfoOpenPriceFluctuationRankEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가대비 등락률상위(ETF) 응답")

    result_list: list[OverseasRankInfoOpenPriceFluctuationRankEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoOpenPriceFluctuationRankWatchlistItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    open_pric_pre: str = Field(default="", description="시가대비. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    cntr_tm: str = Field(default="", description="시간. HH:mm")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasRankInfoOpenPriceFluctuationRankWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 시가대비 등락률상위(관심종목) 응답")

    result_list: list[OverseasRankInfoOpenPriceFluctuationRankWatchlistItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoCumulativeFluctuationTopStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    hgst_pric: str = Field(default="", description="최고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    stk_high_dt: str = Field(default="", description="종목최고일자. YYYYMMDD")
    lwst_pric: str = Field(default="", description="최저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    stk_low_dt: str = Field(default="", description="종목최저일자. YYYYMMDD")
    acc_flu_rt: str = Field(default="", description="누적등락률. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    acc_flu_amt: str = Field(default="", description="누적등락폭. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")


class OverseasRankInfoCumulativeFluctuationTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 누적 등락률 상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoCumulativeFluctuationTopStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoCumulativeFluctuationTopEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    hgst_pric: str = Field(default="", description="최고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    stk_high_dt: str = Field(default="", description="종목최고일자. YYYYMMDD")
    lwst_pric: str = Field(default="", description="최저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    stk_low_dt: str = Field(default="", description="종목최저일자. YYYYMMDD")
    acc_flu_rt: str = Field(default="", description="누적등락률. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    acc_flu_amt: str = Field(default="", description="누적등락폭. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")


class OverseasRankInfoCumulativeFluctuationTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 누적 등락률 상위(ETF) 응답")

    result_list: list[OverseasRankInfoCumulativeFluctuationTopEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoPreviousDayTradingTopStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_rt: str = Field(default="", description="전일비. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="당일거래량. 단위: 1주")


class OverseasRankInfoPreviousDayTradingTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 전일 거래상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoPreviousDayTradingTopStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoPreviousDayTradingTopEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_rt: str = Field(default="", description="전일비. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="당일거래량. 단위: 1주")


class OverseasRankInfoPreviousDayTradingTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 전일 거래상위(ETF) 응답")

    result_list: list[OverseasRankInfoPreviousDayTradingTopEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoHighLowPriceRiseFallStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    oyr_hgst: str = Field(default="", description="연중최고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    oyr_lwst: str = Field(default="", description="연중최저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    week52_hgst_pric: str = Field(
        default="",
        description="52주 최고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자",
        alias="52wk_hgst_pric",
    )
    week52_lwst_pric: str = Field(
        default="",
        description="52주 최저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자",
        alias="52wk_lwst_pric",
    )
    hl_pre_sig: str = Field(
        default="", description="최저가/최고가 대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )
    hl_pre: str = Field(default="", description="최저가/최고가대비")
    pre_flu_rt: str = Field(default="", description="대비등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    base_dt: str = Field(default="", description="최고/최저일시. YYYYMMDD")
    acc_trde_qty: str = Field(default="", description="누적거래량")


class OverseasRankInfoHighLowPriceRiseFallStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 최고최저가대비 상승하락(주식/업종) 응답")

    result_list: list[OverseasRankInfoHighLowPriceRiseFallStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoHighLowPriceRiseFallEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    oyr_hgst: str = Field(default="", description="연중최고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    oyr_lwst: str = Field(default="", description="연중최저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    week52_hgst_pric: str = Field(
        default="",
        description="52주 최고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자",
        alias="52wk_hgst_pric",
    )
    week52_lwst_pric: str = Field(
        default="",
        description="52주 최저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자",
        alias="52wk_lwst_pric",
    )
    hl_pre_sig: str = Field(
        default="", description="최저가/최고가 대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락"
    )
    hl_pre: str = Field(default="", description="최저가/최고가대비")
    pre_flu_rt: str = Field(default="", description="대비등락율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    base_dt: str = Field(default="", description="최고/최저일시. YYYYMMDD")
    acc_trde_qty: str = Field(default="", description="누적거래량")


class OverseasRankInfoHighLowPriceRiseFallEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 최고최저가대비 상승하락(ETF) 응답")

    result_list: list[OverseasRankInfoHighLowPriceRiseFallEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoSpecificDateRiseFallStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    base_dt: str = Field(default="", description="기준일자. YYYYMMDD")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    trde_prica: str = Field(default="", description="누적거래대금")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 소수점 다섯째 자리까지 포맷된 백분율")


class OverseasRankInfoSpecificDateRiseFallStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 특정일자 상승/하락(주식/업종) 응답")

    result_list: list[OverseasRankInfoSpecificDateRiseFallStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoSpecificDateRiseFallEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    base_dt: str = Field(default="", description="기준일자. YYYYMMDD")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    trde_prica: str = Field(default="", description="누적거래대금")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 소수점 다섯째 자리까지 포맷된 백분율")


class OverseasRankInfoSpecificDateRiseFallEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 특정일자 상승/하락(ETF) 응답")

    result_list: list[OverseasRankInfoSpecificDateRiseFallEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoTurnoverRateTopStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    trde_tern_rt: str = Field(
        default="", description="거래회전율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    avg_tern_rt_2d: str = Field(
        default="", description="2일 평균 회전율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율", alias="2d_avg_tern_rt"
    )
    avg_tern_rt_10d: str = Field(
        default="", description="10일 평균 회전율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율", alias="10d_avg_tern_rt"
    )
    avg_tern_rt_20d: str = Field(
        default="", description="20일 평균 회전율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율", alias="20d_avg_tern_rt"
    )


class OverseasRankInfoTurnoverRateTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 회전율 상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoTurnoverRateTopStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasRankInfoTurnoverRateTopEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    trde_tern_rt: str = Field(
        default="", description="거래회전율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    avg_tern_rt_2d: str = Field(
        default="", description="2일 평균 회전율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율", alias="2d_avg_tern_rt"
    )
    avg_tern_rt_10d: str = Field(
        default="", description="10일 평균 회전율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율", alias="10d_avg_tern_rt"
    )
    avg_tern_rt_20d: str = Field(
        default="", description="20일 평균 회전율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율", alias="20d_avg_tern_rt"
    )


class OverseasRankInfoTurnoverRateTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 회전율 상위(ETF) 응답")

    result_list: list[OverseasRankInfoTurnoverRateTopEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasRankInfoConsecutiveRiseFallRankStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    base_close_pric: str = Field(default="", description="기준일종가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    base_pre_rt: str = Field(default="", description="기준일대비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    conti_dt: str = Field(default="", description="연속일수")


class OverseasRankInfoConsecutiveRiseFallRankStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연속상승/하락 순위(주식/업종) 응답")

    result_list: list[OverseasRankInfoConsecutiveRiseFallRankStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoConsecutiveRiseFallRankEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    base_close_pric: str = Field(default="", description="기준일종가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    base_pre_rt: str = Field(default="", description="기준일대비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    conti_dt: str = Field(default="", description="연속일수")


class OverseasRankInfoConsecutiveRiseFallRankEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연속상승/하락 순위(ETF) 응답")

    result_list: list[OverseasRankInfoConsecutiveRiseFallRankEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoConsecutiveRiseFallRankWatchlistItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    base_close_pric: str = Field(default="", description="기준일종가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    base_pre_rt: str = Field(default="", description="기준일대비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    conti_dt: str = Field(default="", description="연속일수")


class OverseasRankInfoConsecutiveRiseFallRankWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연속상승/하락 순위(관심종목) 응답")

    result_list: list[OverseasRankInfoConsecutiveRiseFallRankWatchlistItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoQuoteRemainingVolumeTopStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    tot_sel_req: str = Field(default="", description="매도호가총잔량. 단위: 1주")
    tot_buy_req: str = Field(default="", description="매수호가총잔량. 단위: 1주")
    buy_req: str = Field(default="", description="순매수잔량. 순매수잔량/매수비율 검색일 경우")
    buy_rt: str = Field(
        default="", description="매수비율. 소수점 제거 된 100배 값으로 제공 예) '2658'는 26.58를 의미합니다."
    )
    sel_req: str = Field(default="", description="순매도잔량. 순매도잔량/매도비율 검색일 경우")
    sel_rt: str = Field(
        default="", description="매도비율. 소수점 제거 된 100배 값으로 제공 예) '2658'는 26.58를 의미합니다."
    )
    cntr_tm: str = Field(default="", description="시간. HH:mm")


class OverseasRankInfoQuoteRemainingVolumeTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 호가잔량상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoQuoteRemainingVolumeTopStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoQuoteRemainingVolumeTopEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    tot_sel_req: str = Field(default="", description="매도호가총잔량. 단위: 1주")
    tot_buy_req: str = Field(default="", description="매수호가총잔량. 단위: 1주")
    buy_req: str = Field(default="", description="순매수잔량. 순매수잔량/매수비율 검색일 경우")
    buy_rt: str = Field(
        default="", description="매수비율. 소수점 제거 된 100배 값으로 제공 예) '2658'는 26.58를 의미합니다."
    )
    sel_req: str = Field(default="", description="순매도잔량. 순매도잔량/매도비율 검색일 경우")
    sel_rt: str = Field(
        default="", description="매도비율. 소수점 제거 된 100배 값으로 제공 예) '2658'는 26.58를 의미합니다."
    )
    cntr_tm: str = Field(default="", description="시간. HH:mm")


class OverseasRankInfoQuoteRemainingVolumeTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 호가잔량상위(ETF) 응답")

    result_list: list[OverseasRankInfoQuoteRemainingVolumeTopEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoDaytimeTradingDisparityTopStockItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    reg_close_pric: str = Field(
        default="", description="정규장종가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    reg_pre_sig: str = Field(default="", description="정규장대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    reg_pre: str = Field(default="", description="정규장대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    dispty_rt: str = Field(default="", description="괴리율")
    cntr_tm: str = Field(default="", description="체결시간")
    cntr_str: str = Field(default="", description="체결강도")
    cnt: str = Field(default="", description="횟수")


class OverseasRankInfoDaytimeTradingDisparityTopStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 주간거래 괴리율 상위(주식/업종) 응답")

    result_list: list[OverseasRankInfoDaytimeTradingDisparityTopStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasRankInfoDaytimeTradingDisparityTopEtfItem(BaseModel):
    rank: str = Field(default="", description="순위")
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    reg_close_pric: str = Field(
        default="", description="정규장종가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자"
    )
    reg_pre_sig: str = Field(default="", description="정규장대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    reg_pre: str = Field(default="", description="정규장대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    dispty_rt: str = Field(default="", description="괴리율")
    cntr_tm: str = Field(default="", description="체결시간")
    cntr_str: str = Field(default="", description="체결강도")
    cnt: str = Field(default="", description="횟수")
    sel_req: str = Field(default="", description="매도잔량. 단위: 1주")
    buy_req: str = Field(default="", description="매수잔량. 단위: 1주")


class OverseasRankInfoDaytimeTradingDisparityTopEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 주간거래 괴리율 상위(ETF) 응답")

    result_list: list[OverseasRankInfoDaytimeTradingDisparityTopEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )
