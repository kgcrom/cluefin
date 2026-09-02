from dataclasses import dataclass
from typing import List

from loguru import logger

from cluefin_desk.data.fetcher import DomesticDataFetcher


@dataclass
class ScreeningItem:
    rank: int
    stock_code: str
    stock_name: str
    current_price: str
    change_rate: str
    volume: str
    change_sign: str = ""
    extra: str = ""


class StockScreener:
    def __init__(self, fetcher: DomesticDataFetcher):
        self.fetcher = fetcher

    def get_top_gainers(self) -> List[ScreeningItem]:
        try:
            response = self.fetcher.get_top_percentage_change(sort_tp="1")
            items = response.body.pred_pre_flu_rt_upper
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.stk_cd,
                    stock_name=item.stk_nm,
                    current_price=item.cur_prc,
                    change_rate=item.flu_rt,
                    volume=item.now_trde_qty,
                    change_sign=item.pred_pre_sig,
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch top gainers: {e}")
            return []

    def get_top_losers(self) -> List[ScreeningItem]:
        try:
            response = self.fetcher.get_top_percentage_change(sort_tp="2")
            items = response.body.pred_pre_flu_rt_upper
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.stk_cd,
                    stock_name=item.stk_nm,
                    current_price=item.cur_prc,
                    change_rate=item.flu_rt,
                    volume=item.now_trde_qty,
                    change_sign=item.pred_pre_sig,
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch top losers: {e}")
            return []

    def get_top_volume(self) -> List[ScreeningItem]:
        try:
            response = self.fetcher.get_top_trading_volume()
            items = response.body.tdy_trde_qty_upper
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.stk_cd,
                    stock_name=item.stk_nm,
                    current_price=item.cur_prc,
                    change_rate=item.flu_rt,
                    volume=item.trde_qty,
                    change_sign=item.pred_pre_sig,
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch top volume: {e}")
            return []

    def get_top_value(self) -> List[ScreeningItem]:
        try:
            response = self.fetcher.get_top_transaction_value()
            items = response.body.trde_prica_upper
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.stk_cd,
                    stock_name=item.stk_nm,
                    current_price=item.cur_prc,
                    change_rate=item.flu_rt,
                    volume=item.now_trde_qty,
                    change_sign=item.pred_pre_sig,
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch top value: {e}")
            return []

    def get_top_foreigner_net_buy(self) -> List[ScreeningItem]:
        try:
            response = self.fetcher.get_top_foreigner_period_trading(trde_tp="1")
            items = response.body.for_dt_trde_upper
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.stk_cd,
                    stock_name=item.stk_nm,
                    current_price=item.cur_prc,
                    change_rate="",
                    volume=item.trde_qty,
                    extra=item.netprps_qty,
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch foreigner net buy: {e}")
            return []

    def get_new_high_price(self) -> List[ScreeningItem]:
        try:
            response = self.fetcher.get_new_high_low_price(ntl_tp="1")
            items = response.body.ntl_pric
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.stk_cd,
                    stock_name=item.stk_nm,
                    current_price=item.cur_prc,
                    change_rate=item.flu_rt,
                    volume=item.trde_qty,
                    change_sign=item.pred_pre_sig,
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch new high price: {e}")
            return []

    def get_price_volatility(self) -> List[ScreeningItem]:
        try:
            response = self.fetcher.get_price_volatility(flu_tp="1")
            items = response.body.pric_jmpflu
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.stk_cd,
                    stock_name=item.stk_nm,
                    current_price=item.cur_prc,
                    change_rate=item.flu_rt,
                    volume=item.trde_qty,
                    change_sign=item.pred_pre_sig,
                    extra=item.jmp_rt,
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch price volatility: {e}")
            return []

    def get_top_margin_ratio(self) -> List[ScreeningItem]:
        try:
            response = self.fetcher.get_top_margin_ratio()
            items = response.body.crd_rt_upper
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.stk_cd,
                    stock_name=item.stk_nm,
                    current_price=item.cur_prc,
                    change_rate=item.flu_rt,
                    volume=item.now_trde_qty,
                    change_sign=item.pred_pre_sig,
                    extra=item.crd_rt,
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch margin ratio: {e}")
            return []

    # ──────────────────────────────────────
    # KIS-backed rankings (empty without KIS keys)
    # ──────────────────────────────────────

    def get_dividend_yield_top(self) -> List[ScreeningItem]:
        """배당수익률 상위 (KIS). 시세 없이 배당 정보만 내려오는 랭킹이라
        current_price/volume 은 비운다. extra = 배당수익률(%)."""
        if not self.fetcher.has_kis:
            return []
        try:
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.sht_cd,
                    stock_name=item.isin_name,
                    current_price="-",
                    change_rate="",
                    volume="-",
                    extra=item.divi_rate,
                )
                for idx, item in enumerate(self.fetcher.get_dividend_yield_top())
            ]
        except Exception as e:
            logger.error(f"Failed to fetch dividend yield top: {e}")
            return []

    def get_short_selling_top(self) -> List[ScreeningItem]:
        """공매도 상위 (KIS, 당일). extra = 공매도 거래량 비중(%)."""
        if not self.fetcher.has_kis:
            return []
        try:
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.mksc_shrn_iscd,
                    stock_name=item.hts_kor_isnm,
                    current_price=item.stck_prpr,
                    change_rate=item.prdy_ctrt,
                    volume=item.acml_vol,
                    extra=item.ssts_vol_rlim,
                )
                for idx, item in enumerate(self.fetcher.get_short_selling_top())
            ]
        except Exception as e:
            logger.error(f"Failed to fetch short selling top: {e}")
            return []

    def get_credit_balance_top(self) -> List[ScreeningItem]:
        """신용잔고 상위 (KIS, 잔고비율순). extra = 융자잔고비율(%)."""
        if not self.fetcher.has_kis:
            return []
        try:
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.mksc_shrn_iscd,
                    stock_name=item.hts_kor_isnm,
                    current_price=item.stck_prpr,
                    change_rate=item.prdy_ctrt,
                    volume=item.acml_vol,
                    extra=item.whol_loan_rmnd_rate,
                )
                for idx, item in enumerate(self.fetcher.get_credit_balance_top())
            ]
        except Exception as e:
            logger.error(f"Failed to fetch credit balance top: {e}")
            return []

    def get_disparity_index_top(self) -> List[ScreeningItem]:
        """이격도(20일) 상위 (KIS). extra = 20일 이격도."""
        if not self.fetcher.has_kis:
            return []
        try:
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.mksc_shrn_iscd,
                    stock_name=item.hts_kor_isnm,
                    current_price=item.stck_prpr,
                    change_rate=item.prdy_ctrt,
                    volume=item.acml_vol,
                    extra=item.d20_dsrt,
                )
                for idx, item in enumerate(self.fetcher.get_disparity_index_rank())
            ]
        except Exception as e:
            logger.error(f"Failed to fetch disparity index top: {e}")
            return []
