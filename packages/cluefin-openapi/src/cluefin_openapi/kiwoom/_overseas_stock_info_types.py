from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class OverseasStockInfoExchangeListItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    mkgb: str = Field(default="", description="거래소명")
    upgb: str = Field(default="", description="업종명")
    isEtf: str = Field(default="", description="ETF 여부")


class OverseasStockInfoExchangeList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래소구분 조회 응답", populate_by_name=True)

    result_list: list[OverseasStockInfoExchangeListItem] = Field(
        default_factory=list, description="결과리스트", alias="list"
    )


class OverseasStockInfoStockListItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    mkgb: str = Field(default="", description="거래소명")
    upgb: str = Field(default="", description="업종명")
    isEtf: str = Field(default="", description="ETF 여부")


class OverseasStockInfoStockList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 종목리스트 응답", populate_by_name=True)

    result_list: list[OverseasStockInfoStockListItem] = Field(
        default_factory=list, description="결과리스트", alias="list"
    )


class OverseasStockInfoStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 종목 조회 응답")

    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    mkgb: str = Field(default="", description="거래소명")
    upgb: str = Field(default="", description="업종명")
    isEtf: str = Field(default="", description="ETF 여부")


class OverseasStockInfoSectorListItem(BaseModel):
    inds_cd: str = Field(default="", description="업종코드")
    inds_nm: str = Field(default="", description="업종명")
    inds_enm: str = Field(default="", description="업종영문명")


class OverseasStockInfoSectorList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 업종리스트 응답", populate_by_name=True)

    result_list: list[OverseasStockInfoSectorListItem] = Field(
        default_factory=list, description="결과리스트", alias="list"
    )


class OverseasStockInfoIndexListItem(BaseModel):
    index_cd: str = Field(default="", description="지수코드")
    index_nm: str = Field(default="", description="지수명")
    index_enm: str = Field(default="", description="지수영문명")


class OverseasStockInfoIndexList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국지수 리스트 응답", populate_by_name=True)

    result_list: list[OverseasStockInfoIndexListItem] = Field(
        default_factory=list, description="결과리스트", alias="list"
    )


class OverseasStockInfoEtfEtnListItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분")
    code: str = Field(default="", description="종목코드")
    cate1: str = Field(default="", description="카테고리1")
    cate2: str = Field(default="", description="카테고리2")
    etn: str = Field(default="", description="ETN여부")
    mkgb: str = Field(default="", description="거래소명")
    upnm: str = Field(default="", description="업종명")


class OverseasStockInfoEtfEtnList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국 ETF,ETN 리스트 응답", populate_by_name=True)

    result_list: list[OverseasStockInfoEtfEtnListItem] = Field(
        default_factory=list, description="결과리스트", alias="list"
    )


class OverseasStockInfoEtfCategoryListItem(BaseModel):
    gubun: str = Field(default="", description="구분")
    cate1: str = Field(default="", description="카테고리1차")
    cate1nam: str = Field(default="", description="카테고리1차명")
    cate2: str = Field(default="", description="카테고리2차")
    cate2nam: str = Field(default="", description="카테고리2차명")


class OverseasStockInfoEtfCategoryList(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국 ETF 카테고리 리스트 응답", populate_by_name=True)

    result_list: list[OverseasStockInfoEtfCategoryListItem] = Field(
        default_factory=list, description="결과리스트", alias="list"
    )


class OverseasStockInfoVolumeSurgeStockItem(BaseModel):
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
    sdnin_rt: str = Field(default="", description="급증률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasStockInfoVolumeSurgeStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량급등락(주식/업종) 응답")

    result_list: list[OverseasStockInfoVolumeSurgeStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoVolumeSurgeEtfItem(BaseModel):
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
    sdnin_rt: str = Field(default="", description="급증률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasStockInfoVolumeSurgeEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량급등락(ETF) 응답")

    result_list: list[OverseasStockInfoVolumeSurgeEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoPriceByRangeStockItem(BaseModel):
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
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasStockInfoPriceByRangeStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격대별주가(주식/업종) 응답")

    stk_num: str = Field(default="", description="종목수")
    rising_stk_num: str = Field(default="", description="상승")
    flat_stk_num: str = Field(default="", description="보합")
    fall_stk_num: str = Field(default="", description="하락")
    result_list: list[OverseasStockInfoPriceByRangeStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoPriceByRangeEtfItem(BaseModel):
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
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasStockInfoPriceByRangeEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격대별주가(ETF) 응답")

    stk_num: str = Field(default="", description="종목수")
    rising_stk_num: str = Field(default="", description="상승")
    flat_stk_num: str = Field(default="", description="보합")
    fall_stk_num: str = Field(default="", description="하락")
    result_list: list[OverseasStockInfoPriceByRangeEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoPriceSurgeStockItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명한글")
    stk_enm: str = Field(default="", description="영문종목명")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    base_pric: str = Field(default="", description="기준가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    base_pre: str = Field(default="", description="기준대비. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="거래량. 단위: 1주")
    sdnin_rt: str = Field(default="", description="급증률")


class OverseasStockInfoPriceSurgeStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격급등락(주식/업종) 응답")

    result_list: list[OverseasStockInfoPriceSurgeStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoPriceSurgeEtfItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명한글")
    stk_enm: str = Field(default="", description="영문종목명")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    base_pric: str = Field(default="", description="기준가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    base_pre: str = Field(default="", description="기준대비. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="거래량")
    sdnin_rt: str = Field(default="", description="급증률")


class OverseasStockInfoPriceSurgeEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격급등락(ETF) 응답")

    result_list: list[OverseasStockInfoPriceSurgeEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoPriceSurgeWatchlistItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    base_pric: str = Field(default="", description="기준가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    base_pre: str = Field(default="", description="기준가 대비. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    sdnin_rt: str = Field(default="", description="급등락율")


class OverseasStockInfoPriceSurgeWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 가격급등락(관심종목) 응답")

    result_list: list[OverseasStockInfoPriceSurgeWatchlistItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoHighLowApproachStockItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량")
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="당일고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="당일저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasStockInfoHighLowApproachStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 고가/저가 접근(주식/업종) 응답")

    result_list: list[OverseasStockInfoHighLowApproachStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoHighLowApproachEtfItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량")
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="당일고가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="당일저가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasStockInfoHighLowApproachEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 고가/저가 접근(ETF) 응답")

    result_list: list[OverseasStockInfoHighLowApproachEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoHighLowApproachWatchlistItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    tp: str = Field(default="", description="신종목구분자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    sel_bid: str = Field(
        default="", description="(최우선)매도호가. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    buy_bid: str = Field(
        default="", description="(최우선)매수호가. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    high_pric: str = Field(default="", description="고가. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    low_pric: str = Field(default="", description="저가. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")


class OverseasStockInfoHighLowApproachWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 고가/저가 접근(관심종목) 응답")

    result_list: list[OverseasStockInfoHighLowApproachWatchlistItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoVolumeRenewalStockItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    prev_trde_qty: str = Field(default="", description="이전거래량")
    acc_trde_qty: str = Field(default="", description="거래량")
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasStockInfoVolumeRenewalStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량갱신(주식/업종) 응답")

    result_list: list[OverseasStockInfoVolumeRenewalStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoVolumeRenewalEtfItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    prev_trde_qty: str = Field(default="", description="이전거래량")
    acc_trde_qty: str = Field(default="", description="거래량")
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasStockInfoVolumeRenewalEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량갱신(ETF) 응답")

    result_list: list[OverseasStockInfoVolumeRenewalEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoVolumeRenewalWatchlistItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    prev_trde_qty: str = Field(default="", description="이전거래량")
    acc_trde_qty: str = Field(default="", description="거래량")
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")


class OverseasStockInfoVolumeRenewalWatchlist(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 거래량갱신(관심종목) 응답")

    result_list: list[OverseasStockInfoVolumeRenewalWatchlistItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoNewHighLowStockItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량")
    pre_trde_rt: str = Field(
        default="", description="전일거래대비. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="250일고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="250일저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    pred_trde_qty: str = Field(default="", description="전일거래량")


class OverseasStockInfoNewHighLowStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 신고가/신저가(주식/업종) 응답")

    result_list: list[OverseasStockInfoNewHighLowStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoNewHighLowEtfItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량")
    pre_trde_rt: str = Field(
        default="", description="전일거래대비. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율"
    )
    sel_bid: str = Field(default="", description="매도호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    buy_bid: str = Field(default="", description="매수호가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    high_pric: str = Field(default="", description="250일고가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    low_pric: str = Field(default="", description="250일저가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    pred_trde_qty: str = Field(default="", description="전일거래량")


class OverseasStockInfoNewHighLowEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 신고가/신저가(ETF) 응답")

    result_list: list[OverseasStockInfoNewHighLowEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoGapUpDownStockItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    base_close_pric: str = Field(default="", description="전일종가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    gap_rt: str = Field(default="", description="갭비율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    pre_high_pric: str = Field(default="", description="전일고가")
    pred_trde_qty: str = Field(default="", description="전일거래량")


class OverseasStockInfoGapUpDownStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 갭상승/갭하락(주식/업종) 응답")

    result_list: list[OverseasStockInfoGapUpDownStockItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoGapUpDownEtfItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량")
    open_pric: str = Field(default="", description="시가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    base_close_pric: str = Field(default="", description="전일종가. 단위: USD, 소수점 넷째 자리까지 포맷된 숫자")
    gap_rt: str = Field(default="", description="갭비율. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    pre_high_pric: str = Field(default="", description="전일고가")
    pred_trde_qty: str = Field(default="", description="전일거래량")


class OverseasStockInfoGapUpDownEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 갭상승/갭하락(ETF) 응답")

    result_list: list[OverseasStockInfoGapUpDownEtfItem] = Field(default_factory=list, description="결과리스트")


class OverseasStockInfoRemainingRatioSurgeStockItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    base_rt: str = Field(default="", description="기준비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율", alias="int")
    now_rt: str = Field(default="", description="현재비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    sdnin_rt: str = Field(default="", description="급증률. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    tot_sel_req: str = Field(default="", description="총매도잔량")
    tot_buy_req: str = Field(default="", description="총매수잔량")


class OverseasStockInfoRemainingRatioSurgeStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 잔량률급증(주식/업종) 응답")

    result_list: list[OverseasStockInfoRemainingRatioSurgeStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoRemainingRatioSurgeEtfItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    base_rt: str = Field(default="", description="기준비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율", alias="int")
    now_rt: str = Field(default="", description="현재비율. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    sdnin_rt: str = Field(default="", description="급증률. 단위: %, 소수점 둘째 자리까지 포맷된 백분율")
    tot_sel_req: str = Field(default="", description="총매도잔량")
    tot_buy_req: str = Field(default="", description="총매수잔량")


class OverseasStockInfoRemainingRatioSurgeEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 잔량률급증(ETF) 응답")

    result_list: list[OverseasStockInfoRemainingRatioSurgeEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoVolumeConcentrationStockItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량")
    pric_cnd_st: str = Field(default="", description="가격대시작")
    pric_cnd_ed: str = Field(default="", description="가격대끝")
    prps_qty: str = Field(default="", description="매물량")
    prps_rt: str = Field(default="", description="매물비")


class OverseasStockInfoVolumeConcentrationStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 매물대집중(주식/업종) 응답")

    result_list: list[OverseasStockInfoVolumeConcentrationStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoVolumeConcentrationEtfItem(BaseModel):
    mgn_type: str = Field(default="", description="증거금률")
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    cur_prc: str = Field(default="", description="현재가. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    pred_pre_sig: str = Field(default="", description="전일대비기호. 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락")
    pred_pre: str = Field(default="", description="전일대비. 단위: USD, 부호 포함 소수점 넷째 자리까지 포맷된 숫자")
    flu_rt: str = Field(default="", description="등락률. 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율")
    acc_trde_qty: str = Field(default="", description="거래량")
    pric_cnd_st: str = Field(default="", description="가격대시작")
    pric_cnd_ed: str = Field(default="", description="가격대끝")
    prps_qty: str = Field(default="", description="매물량")
    prps_rt: str = Field(default="", description="매물비")


class OverseasStockInfoVolumeConcentrationEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 매물대집중(ETF) 응답")

    result_list: list[OverseasStockInfoVolumeConcentrationEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoYearlyFluctuationRateStockItem(BaseModel):
    dt: str = Field(default="", description="연도. 0:평균, YYYY:년도")
    m01_prft_rt: str = Field(default="", description="1월 수익률")
    m02_prft_rt: str = Field(default="", description="2월 수익률")
    m03_prft_rt: str = Field(default="", description="3월 수익률")
    m04_prft_rt: str = Field(default="", description="4월 수익률")
    m05_prft_rt: str = Field(default="", description="5월 수익률")
    m06_prft_rt: str = Field(default="", description="6월 수익률")
    m07_prft_rt: str = Field(default="", description="7월 수익률")
    m08_prft_rt: str = Field(default="", description="8월 수익률")
    m09_prft_rt: str = Field(default="", description="9월 수익률")
    m10_prft_rt: str = Field(default="", description="10월 수익률")
    m11_prft_rt: str = Field(default="", description="11월 수익률")
    m12_prft_rt: str = Field(default="", description="12월 수익률")


class OverseasStockInfoYearlyFluctuationRateStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 등락률(종목) 응답")

    result_list: list[OverseasStockInfoYearlyFluctuationRateStockItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoYearlyFluctuationRateBySectorItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    m01_prft_rt: str = Field(default="", description="1월 수익률")
    m02_prft_rt: str = Field(default="", description="2월 수익률")
    m03_prft_rt: str = Field(default="", description="3월 수익률")
    m04_prft_rt: str = Field(default="", description="4월 수익률")
    m05_prft_rt: str = Field(default="", description="5월 수익률")
    m06_prft_rt: str = Field(default="", description="6월 수익률")
    m07_prft_rt: str = Field(default="", description="7월 수익률")
    m08_prft_rt: str = Field(default="", description="8월 수익률")
    m09_prft_rt: str = Field(default="", description="9월 수익률")
    m10_prft_rt: str = Field(default="", description="10월 수익률")
    m11_prft_rt: str = Field(default="", description="11월 수익률")
    m12_prft_rt: str = Field(default="", description="12월 수익률")


class OverseasStockInfoYearlyFluctuationRateBySector(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 업종별 종목등락률 응답")

    result_list: list[OverseasStockInfoYearlyFluctuationRateBySectorItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoYearlyFluctuationRateByEtfCategoryItem(BaseModel):
    stex_tp: str = Field(default="", description="거래소구분. NA: AMEX, ND: NASDAQ, NY: NYSE")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    stk_enm: str = Field(default="", description="종목영문명")
    m01_prft_rt: str = Field(default="", description="1월 수익률")
    m02_prft_rt: str = Field(default="", description="2월 수익률")
    m03_prft_rt: str = Field(default="", description="3월 수익률")
    m04_prft_rt: str = Field(default="", description="4월 수익률")
    m05_prft_rt: str = Field(default="", description="5월 수익률")
    m06_prft_rt: str = Field(default="", description="6월 수익률")
    m07_prft_rt: str = Field(default="", description="7월 수익률")
    m08_prft_rt: str = Field(default="", description="8월 수익률")
    m09_prft_rt: str = Field(default="", description="9월 수익률")
    m10_prft_rt: str = Field(default="", description="10월 수익률")
    m11_prft_rt: str = Field(default="", description="11월 수익률")
    m12_prft_rt: str = Field(default="", description="12월 수익률")


class OverseasStockInfoYearlyFluctuationRateByEtfCategory(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 ETF 카테고리별 종목등락률 응답")

    result_list: list[OverseasStockInfoYearlyFluctuationRateByEtfCategoryItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoYearlyFluctuationRateSectorItem(BaseModel):
    dt: str = Field(default="", description="연도. 0:평균, YYYY:년도")
    m01_prft_rt: str = Field(default="", description="1월 수익률")
    m02_prft_rt: str = Field(default="", description="2월 수익률")
    m03_prft_rt: str = Field(default="", description="3월 수익률")
    m04_prft_rt: str = Field(default="", description="4월 수익률")
    m05_prft_rt: str = Field(default="", description="5월 수익률")
    m06_prft_rt: str = Field(default="", description="6월 수익률")
    m07_prft_rt: str = Field(default="", description="7월 수익률")
    m08_prft_rt: str = Field(default="", description="8월 수익률")
    m09_prft_rt: str = Field(default="", description="9월 수익률")
    m10_prft_rt: str = Field(default="", description="10월 수익률")
    m11_prft_rt: str = Field(default="", description="11월 수익률")
    m12_prft_rt: str = Field(default="", description="12월 수익률")


class OverseasStockInfoYearlyFluctuationRateSector(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 등락률(업종) 응답")

    result_list: list[OverseasStockInfoYearlyFluctuationRateSectorItem] = Field(
        default_factory=list, description="결과리스트"
    )


class OverseasStockInfoYearlyFluctuationRateEtfItem(BaseModel):
    dt: str = Field(default="", description="연도. 0:평균, YYYY:년도")
    m01_prft_rt: str = Field(default="", description="1월 수익률")
    m02_prft_rt: str = Field(default="", description="2월 수익률")
    m03_prft_rt: str = Field(default="", description="3월 수익률")
    m04_prft_rt: str = Field(default="", description="4월 수익률")
    m05_prft_rt: str = Field(default="", description="5월 수익률")
    m06_prft_rt: str = Field(default="", description="6월 수익률")
    m07_prft_rt: str = Field(default="", description="7월 수익률")
    m08_prft_rt: str = Field(default="", description="8월 수익률")
    m09_prft_rt: str = Field(default="", description="9월 수익률")
    m10_prft_rt: str = Field(default="", description="10월 수익률")
    m11_prft_rt: str = Field(default="", description="11월 수익률")
    m12_prft_rt: str = Field(default="", description="12월 수익률")


class OverseasStockInfoYearlyFluctuationRateEtf(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="미국주식 연도별 등락률(ETF) 응답")

    result_list: list[OverseasStockInfoYearlyFluctuationRateEtfItem] = Field(
        default_factory=list, description="결과리스트"
    )
