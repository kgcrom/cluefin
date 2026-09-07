from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from cluefin_openapi.kiwoom._model import KiwoomHttpBody


class DomesticForeignInvestorTradingTrendByStockItem(BaseModel):
    dt: str = Field(default="", description="일자")
    close_pric: str = Field(default="", description="종가")
    pred_pre: str = Field(default="", description="전일대비")
    trde_qty: str = Field(default="", description="거래량")
    chg_qty: str = Field(default="", description="변동수량")
    poss_stkcnt: str = Field(default="", description="보유주식수")
    wght: str = Field(default="", description="비중")
    gain_pos_stkcnt: str = Field(default="", description="취득가능주식수")
    frgnr_limit: str = Field(default="", description="외국인한도")
    frgnr_limit_irds: str = Field(default="", description="외국인한도증감")
    limit_exh_rt: str = Field(default="", description="한도소진률")


class DomesticForeignInvestorTradingTrendByStock(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식외국인종목별매매동향 응답")

    stk_frgnr: list[DomesticForeignInvestorTradingTrendByStockItem] = Field(
        default_factory=list, description="주식외국인"
    )


class DomesticForeignStockInstitution(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="주식기관 응답")

    date: str = Field(default="", description="날짜")
    close_pric: str = Field(default="", description="종가")
    pre: str = Field(default="", description="대비")
    orgn_dt_acc: str = Field(default="", description="기관기간누적")
    orgn_daly_nettrde: str = Field(default="", description="기관일별순매매")
    frgnr_daly_nettrde: str = Field(default="", description="외국인일별순매매")
    frgnr_qota_rt: str = Field(default="", description="외국인지분율")


class DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeignerItem(BaseModel):
    rank: str = Field(default="", description="순위")
    stk_cd: str = Field(default="", description="종목코드")
    stk_nm: str = Field(default="", description="종목명")
    prid_stkpc_flu_rt: str = Field(default="", description="기간중주가등락률")
    orgn_nettrde_amt: str = Field(default="", description="기관순매매금액")
    orgn_nettrde_qty: str = Field(default="", description="기관순매매량")
    orgn_cont_netprps_dys: str = Field(default="", description="기관계연속순매수일수")
    orgn_cont_netprps_qty: str = Field(default="", description="기관계연속순매수량")
    orgn_cont_netprps_amt: str = Field(default="", description="기관계연속순매수금액")
    frgnr_nettrde_qty: str = Field(default="", description="외국인순매매량")
    frgnr_nettrde_amt: str = Field(default="", description="외국인순매매액")
    frgnr_cont_netprps_dys: str = Field(default="", description="외국인연속순매수일수")
    frgnr_cont_netprps_qty: str = Field(default="", description="외국인연속순매수량")
    frgnr_cont_netprps_amt: str = Field(default="", description="외국인연속순매수금액")
    nettrde_qty: str = Field(default="", description="순매매량")
    nettrde_amt: str = Field(default="", description="순매매액")
    tot_cont_netprps_dys: str = Field(default="", description="합계연속순매수일수")
    tot_cont_nettrde_qty: str = Field(default="", description="합계연속순매매수량")
    tot_cont_netprps_amt: str = Field(default="", description="합계연속순매수금액")


class DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeigner(BaseModel, KiwoomHttpBody):
    model_config = ConfigDict(title="기관외국인연속순매수매도상태 응답")

    orgn_frgnr_cont_trde_prst: list[DomesticForeignConsecutiveNetBuySellStatusByInstitutionForeignerItem] = Field(
        default_factory=list, description="기관외국인연속매매현황"
    )
