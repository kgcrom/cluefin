from __future__ import annotations

import pytest

from cluefin_openapi_cli.handlers.kiwoom import domestic_foreign as handlers


class _Body:
    def __init__(self, method_name: str) -> None:
        self.method_name = method_name

    def model_dump(self) -> dict[str, str]:
        return {"method": self.method_name}


class _Response:
    def __init__(self, method_name: str) -> None:
        self.body = _Body(method_name)


class _Recorder:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def __getattr__(self, method_name: str):
        def call(**kwargs):
            self.calls.append((method_name, kwargs))
            return _Response(method_name)

        return call


class _Kiwoom:
    def __init__(self, recorder: _Recorder) -> None:
        self.foreign = recorder


class _Session:
    def __init__(self, recorder: _Recorder) -> None:
        self._kiwoom = _Kiwoom(recorder)

    def get_kiwoom(self) -> _Kiwoom:
        return self._kiwoom


class _Dispatcher:
    def __init__(self) -> None:
        self.registrations: list[tuple[str, object, object]] = []

    def register(self, name, handler, schema) -> None:
        self.registrations.append((name, handler, schema))


def _sample_value(name: str) -> str:
    return {
        "amount_qty_type": "0",
        "exchange_type": "1",
        "market_type": "001",
        "period": "1",
        "stock_code": "KRX:005930",
        "stock_industry_type": "0",
    }.get(name, f"value_{name}")


def _params_for(handler) -> dict[str, str]:
    schema = handler._rpc_schema.parameters
    return {name: _sample_value(name) for name in schema.get("required", [])}


@pytest.mark.parametrize("handler", handlers._ALL_HANDLERS, ids=lambda handler: handler._rpc_schema.name)
def test_kiwoom_foreign_handlers_call_underlying_client(handler) -> None:
    recorder = _Recorder()

    result = handler(_params_for(handler), _Session(recorder))

    assert result == {"method": recorder.calls[0][0]}
    assert len(recorder.calls) == 1


def test_foreign_investor_trading_trend_uses_documented_defaults() -> None:
    recorder = _Recorder()

    handlers.handle_kiwoom_foreign_investor_trading_trend({"stock_code": "KRX:005930"}, _Session(recorder))

    method_name, kwargs = recorder.calls[0]
    assert method_name == "get_foreign_investor_trading_trend_by_stock"
    assert kwargs == {"stk_cd": "KRX:005930", "cont_yn": "N", "next_key": ""}


def test_consecutive_net_buy_sell_maps_optional_defaults() -> None:
    recorder = _Recorder()
    params = _params_for(handlers.handle_kiwoom_consecutive_net_buy_sell)

    handlers.handle_kiwoom_consecutive_net_buy_sell(params, _Session(recorder))

    method_name, kwargs = recorder.calls[0]
    assert method_name == "get_consecutive_net_buy_sell_status_by_institution_foreigner"
    assert kwargs == {
        "dt": "1",
        "mrkt_tp": "001",
        "stk_inds_tp": "0",
        "amt_qty_tp": "0",
        "stex_tp": "1",
        "netslmt_tp": "2",
        "strt_dt": "",
        "end_dt": "",
    }


def test_register_kiwoom_foreign_handlers_registers_all_handlers() -> None:
    dispatcher = _Dispatcher()

    handlers.register_kiwoom_foreign_handlers(dispatcher)

    registered_names = [name for name, _, _ in dispatcher.registrations]
    assert registered_names == [handler._rpc_schema.name for handler in handlers._ALL_HANDLERS]
    assert all(schema.broker == "kiwoom" for _, _, schema in dispatcher.registrations)
