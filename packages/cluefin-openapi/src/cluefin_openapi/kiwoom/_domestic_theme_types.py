from typing import List

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class DomesticThemeGroupItem(BaseModel):
    """테마그룹별요청 항목.

    문서에 적힌 길이 제약(대부분 20자)은 **응답** 모델에 걸지 않는다 — 2026-09-02 실측에서
    테마명이 20자를 넘는 그룹이 있어 `string_too_long` 으로 응답 전체가 거부되고 desk 의
    테마 탭이 빈 화면이 되었다. 응답 검증은 정상 데이터를 거부하는 쪽으로만 작동한다.
    """

    thema_grp_cd: str = Field(default="", description="테마그룹코드")
    thema_nm: str = Field(default="", description="테마명")
    stk_num: str = Field(default="", description="종목수")
    flu_sig: str = Field(default="", description="등락기호")
    flu_rt: str = Field(default="", description="등락율")
    rising_stk_num: str = Field(default="", description="상승종목수")
    fall_stk_num: str = Field(default="", description="하락종목수")
    dt_prft_rt: str = Field(default="", description="기간수익률")
    main_stk: str = Field(default="", description="주요종목")


class DomesticThemeGroup(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="테마그룹별요청 응답")

    thema_grp: List[DomesticThemeGroupItem] = Field(default_factory=list, description="테마그룹별")


class DomesticThemeGroupStocksItem(BaseModel):
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    cur_prc: str = Field(default="", description="현재가")
    flu_sig: str = Field(default="", description="등락기호")
    pred_pre: str = Field(default="", description="전일대비")
    flu_rt: str = Field(default="", description="등락율")
    acc_trde_qty: str = Field(default="", description="누적거래량")
    sel_bid: str = Field(default="", description="매도호가")
    sel_req: str = Field(default="", description="매도잔량")
    buy_bid: str = Field(default="", description="매수호가")
    buy_req: str = Field(default="", description="매수잔량")
    dt_prft_rt_n: str = Field(default="", description="기간수익률n")


class DomesticThemeGroupStocks(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="테마구성종목요청 응답")

    flu_rt: str = Field(default="", description="등락률")
    dt_prft_rt: str = Field(default="", description="기간수익률")
    thema_comp_stk: List[DomesticThemeGroupStocksItem] = Field(default_factory=list, description="테마구성종목")
