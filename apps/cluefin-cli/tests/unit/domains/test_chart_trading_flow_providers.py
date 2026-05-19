from types import SimpleNamespace

from cluefin_cli.domains.providers.kis import KisProvider
from cluefin_cli.domains.providers.kiwoom import KiwoomProvider


class Response:
    def __init__(self, body: object):
        self.body = body


def test_kiwoom_provider_normalizes_daily_ohlcv() -> None:
    provider = KiwoomProvider(client_factory=lambda broker: object())
    provider._client = SimpleNamespace(
        chart=SimpleNamespace(
            get_stock_daily=lambda **_: Response(
                SimpleNamespace(
                    stk_dt_pole_chart_qry=[
                        SimpleNamespace(
                            dt="20250102",
                            open_pric="-70000",
                            high_pric="71000",
                            low_pric="69000",
                            cur_prc="-70500",
                            trde_qty="1,000",
                        )
                    ]
                )
            )
        )
    )

    series = provider.fetch_ohlcv(stock_code="005930", interval="daily", days=10)

    assert series.source == "kiwoom"
    assert series.points[0].timestamp == "20250102"
    assert series.points[0].open == 70000
    assert series.points[0].close == 70500
    assert series.points[0].volume == 1000


def test_kis_provider_normalizes_daily_ohlcv() -> None:
    provider = KisProvider(client_factory=lambda broker: object())
    provider._client = SimpleNamespace(
        domestic_basic_quote=SimpleNamespace(
            get_stock_period_quote=lambda *_: Response(
                SimpleNamespace(
                    output2=[
                        SimpleNamespace(
                            stck_bsop_date="20250102",
                            stck_oprc="70000",
                            stck_hgpr="71000",
                            stck_lwpr="69000",
                            stck_clpr="70500",
                            acml_vol="1000",
                        )
                    ]
                )
            )
        )
    )

    series = provider.fetch_ohlcv(stock_code="005930", interval="daily", days=10)

    assert series.source == "kis"
    assert series.points[0].timestamp == "20250102"
    assert series.points[0].close == 70500


def test_kiwoom_provider_normalizes_trading_flow_empty_case() -> None:
    provider = KiwoomProvider(client_factory=lambda broker: object())
    provider._client = SimpleNamespace(
        chart=SimpleNamespace(
            get_individual_stock_institutional_chart=lambda **_: Response(SimpleNamespace(stk_invsr_orgn_chart=[]))
        )
    )

    snapshot = provider.fetch_trading_flow(stock_code="005930", start_date="20240101", end_date="20241231")

    assert snapshot.rows == []
    assert snapshot.totals == {}


def test_kis_provider_normalizes_trading_flow() -> None:
    provider = KisProvider(client_factory=lambda broker: object())
    provider._client = SimpleNamespace(
        domestic_market_analysis=SimpleNamespace(
            get_investor_trading_trend_by_stock_daily=lambda *_: Response(
                SimpleNamespace(
                    output2=[
                        SimpleNamespace(
                            stck_bsop_date="20241231",
                            prsn_ntby_qty="10",
                            frgn_ntby_qty="-3",
                            orgn_ntby_qty="2",
                            scrt_ntby_qty="",
                            ivtr_ntby_qty="",
                            pe_fund_ntby_vol="",
                            bank_ntby_qty="",
                            insu_ntby_qty="",
                            fund_ntby_qty="",
                            etc_ntby_qty="",
                        )
                    ]
                )
            )
        )
    )

    snapshot = provider.fetch_trading_flow(stock_code="005930", start_date="20240101", end_date="20241231")

    assert snapshot.rows[0]["foreign"] == -3
    assert snapshot.totals["individual"] == 10
    assert snapshot.totals["institution"] == 2
