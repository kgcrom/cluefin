from typing import List

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class DomesticThemeGroupItem(BaseModel):
    thema_grp_cd: str = Field(default="", alias="테마그룹코드", max_length=20)
    thema_nm: str = Field(default="", alias="테마명", max_length=20)
    stk_num: str = Field(default="", alias="종목수", max_length=20)
    flu_sig: str = Field(default="", alias="등락기호", max_length=20)
    flu_rt: str = Field(default="", alias="등락율", max_length=20)
    rising_stk_num: str = Field(default="", alias="상승종목수", max_length=20)
    fall_stk_num: str = Field(default="", alias="하락종목수", max_length=20)
    dt_prft_rt: str = Field(default="", alias="기간수익률", max_length=20)
    main_stk: str = Field(default="", alias="주요종목", max_length=20)


class DomesticThemeGroup(BaseModel, KiwoomHttpBody):
    thema_grp: List[DomesticThemeGroupItem] = Field(default_factory=list, alias="테마그룹별")


class DomesticThemeGroupStocksItem(BaseModel):
    stk_cd: str = Field(default="", alias="종목코드", max_length=20)
    stk_nm: str = Field(default="", alias="종목명", max_length=40)
    cur_prc: str = Field(default="", alias="현재가", max_length=20)
    flu_sig: str = Field(default="", alias="등락기호", max_length=20)
    pred_pre: str = Field(default="", alias="전일대비", max_length=20)
    flu_rt: str = Field(default="", alias="등락율", max_length=20)
    acc_trde_qty: str = Field(default="", alias="누적거래량", max_length=20)
    sel_bid: str = Field(default="", alias="매도호가", max_length=20)
    sel_req: str = Field(default="", alias="매도잔량", max_length=20)
    buy_bid: str = Field(default="", alias="매수호가", max_length=20)
    buy_req: str = Field(default="", alias="매수잔량", max_length=20)
    dt_prft_rt_n: str = Field(default="", alias="기간수익률n", max_length=20)


class DomesticThemeGroupStocks(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="테마그룹별요청 응답")

    flu_rt: str = Field(default="", alias="등락률", max_length=20)
    dt_prft_rt: str = Field(default="", alias="기간수익률", max_length=20)
    thema_comp_stk: List[DomesticThemeGroupStocksItem] = Field(default_factory=list, alias="테마구성종목")
