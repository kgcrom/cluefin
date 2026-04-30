from __future__ import annotations

import pytest

from cluefin_openapi_cli.handlers.kiwoom import domestic_market_condition as handlers


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
        self.calls: list[tuple[str, tuple, dict]] = []

    def __getattr__(self, method_name: str):
        def call(*args, **kwargs):
            self.calls.append((method_name, args, kwargs))
            return _Response(method_name)

        return call


class _Kiwoom:
    def __init__(self, recorder: _Recorder) -> None:
        self.market_conditions = recorder


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
        "amount_qty_type": "1",
        "date": "20240131",
        "end_date": "20240131",
        "exchange_type": "1",
        "for_prsm_unp_tp": "1",
        "frgn_all": "1",
        "indc_tp": "0",
        "invsr": "6",
        "market_type": "001",
        "min_tic_tp": "0",
        "mmcm_cd": "001",
        "newstk_recvrht_tp": "00",
        "orgn_prsm_unp_tp": "1",
        "qry_dt": "20240131",
        "smtm_netprps_tp": "0",
        "start_date": "20240101",
        "stock_code": "005930",
        "trde_tp": "1",
    }.get(name, f"value_{name}")


def _params_for(handler) -> dict[str, str]:
    schema = handler._rpc_schema.parameters
    return {name: _sample_value(name) for name in schema.get("required", [])}


@pytest.mark.parametrize("handler", handlers._ALL_HANDLERS, ids=lambda handler: handler._rpc_schema.name)
def test_kiwoom_market_condition_handlers_call_underlying_client(handler) -> None:
    recorder = _Recorder()

    result = handler(_params_for(handler), _Session(recorder))

    assert result == {"method": recorder.calls[0][0]}
    assert len(recorder.calls) == 1


def test_stock_quote_by_date_maps_required_arg_and_defaults() -> None:
    recorder = _Recorder()

    handlers.handle_kiwoom_stock_quote_by_date({"stock_code": "005930"}, _Session(recorder))

    method_name, args, kwargs = recorder.calls[0]
    assert method_name == "get_stock_quote_by_date"
    assert args == ("005930",)
    assert kwargs == {"cont_yn": "N", "next_key": ""}


def test_daily_institutional_trading_preserves_positional_order() -> None:
    recorder = _Recorder()
    params = _params_for(handlers.handle_kiwoom_daily_institutional_trading)

    handlers.handle_kiwoom_daily_institutional_trading(params, _Session(recorder))

    method_name, args, kwargs = recorder.calls[0]
    assert method_name == "get_daily_institutional_trading_items"
    assert args == ("20240101", "20240131", "1", "001", "1")
    assert kwargs == {"cont_yn": "N", "next_key": ""}


def test_register_kiwoom_market_condition_handlers_registers_all_handlers() -> None:
    dispatcher = _Dispatcher()

    handlers.register_kiwoom_market_condition_handlers(dispatcher)

    registered_names = [name for name, _, _ in dispatcher.registrations]
    assert registered_names == [handler._rpc_schema.name for handler in handlers._ALL_HANDLERS]
    assert all(schema.broker == "kiwoom" for _, _, schema in dispatcher.registrations)
