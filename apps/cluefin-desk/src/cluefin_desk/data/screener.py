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
