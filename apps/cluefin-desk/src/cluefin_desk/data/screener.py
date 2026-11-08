import logging
from dataclasses import dataclass

from cluefin_desk.data.fetcher import DomesticDataFetcher

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ScreeningItem:
    rank: int
    stock_code: str
    stock_name: str
    current_price: str
    change_rate: str
    volume: str
    change_sign: str = ""
    extra: str = ""


def _signed_int(value: str) -> str:
    """키움 수량은 `+112362604`·`--5516442` 처럼 부호가 겹쳐 오기도 한다 — 천 단위 쉼표로 다시 쓴다."""
    text = (value or "").strip()
    negative = text.startswith("-")
    try:
        number = int(text.lstrip("+-"))
    except ValueError:
        return value
    return f"{'-' if negative else ''}{number:,}"


def _million_won_to_eok(value: str) -> str:
    """ka10030 거래금액(백만원) → 억원."""
    try:
        return f"{abs(int(value)) / 100:,.0f}억"
    except (ValueError, TypeError):
        return value


class StockScreener:
    def __init__(self, fetcher: DomesticDataFetcher):
        self.fetcher = fetcher

    def get_top_gainers(self) -> list[ScreeningItem]:
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

    def get_top_losers(self) -> list[ScreeningItem]:
        try:
            response = self.fetcher.get_top_percentage_change(sort_tp="3")
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

    def get_top_volume(self) -> list[ScreeningItem]:
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

    def get_top_value(self) -> list[ScreeningItem]:
        try:
            response = self.fetcher.get_top_trading_volume(sort_tp="3")
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
                    extra=_million_won_to_eok(item.trde_amt),
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch top value: {e}")
            return []

    def get_top_foreigner_net_buy(self) -> list[ScreeningItem]:
        try:
            response = self.fetcher.get_top_foreigner_period_trading(trde_tp="2")
            items = response.body.for_dt_trde_upper
            return [
                ScreeningItem(
                    rank=idx + 1,
                    stock_code=item.stk_cd,
                    stock_name=item.stk_nm,
                    current_price=item.cur_prc,
                    change_rate="",
                    volume=item.trde_qty,
                    extra=_signed_int(item.netprps_qty),
                )
                for idx, item in enumerate(items)
            ]
        except Exception as e:
            logger.error(f"Failed to fetch foreigner net buy: {e}")
            return []

    def get_new_high_price(self) -> list[ScreeningItem]:
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

    def get_price_volatility(self) -> list[ScreeningItem]:
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

    def get_price_plunge(self) -> list[ScreeningItem]:
        try:
            response = self.fetcher.get_price_volatility(flu_tp="2")
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
            logger.error(f"Failed to fetch price plunge: {e}")
            return []

    def get_top_margin_ratio(self) -> list[ScreeningItem]:
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

    def get_short_selling_top(self) -> list[ScreeningItem]:
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

    def get_disparity_index_top(self) -> list[ScreeningItem]:
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
