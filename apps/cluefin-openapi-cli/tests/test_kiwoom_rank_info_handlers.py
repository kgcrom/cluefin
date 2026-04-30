from __future__ import annotations

import pytest

from cluefin_openapi_cli.handlers.kiwoom import domestic_rank_info as handlers


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
        self.rank_info = recorder


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
        "base_dt_tp": "0",
        "dt": "1",
        "end_date": "20240131",
        "exchange_type": "1",
        "market_type": "001",
        "member_company_code": "001",
        "orgn_tp": "9000",
        "pot_tp": "0",
        "qry_dt_tp": "1",
        "qry_tp": "1",
        "rank_end": "100",
        "rank_strt": "1",
        "rt_tp": "1",
        "sort_base": "1",
        "sort_cnd": "1",
        "sort_tp": "1",
        "start_date": "20240101",
        "stock_code": "KRX:005930",
        "tm_tp": "1",
        "trde_tp": "1",
    }.get(name, f"value_{name}")


def _params_for(handler) -> dict[str, str]:
    schema = handler._rpc_schema.parameters
    return {name: _sample_value(name) for name in schema.get("required", [])}


@pytest.mark.parametrize("handler", handlers._ALL_HANDLERS, ids=lambda handler: handler._rpc_schema.name)
def test_kiwoom_rank_info_handlers_call_underlying_client(handler) -> None:
    recorder = _Recorder()

    result = handler(_params_for(handler), _Session(recorder))

    assert result == {"method": recorder.calls[0][0]}
    assert len(recorder.calls) == 1


def test_remaining_order_quantity_uses_documented_defaults() -> None:
    recorder = _Recorder()

    handlers.handle_kiwoom_remaining_order_qty({"market_type": "001", "sort_tp": "1"}, _Session(recorder))

    method_name, kwargs = recorder.calls[0]
    assert method_name == "get_top_remaining_order_quantity"
    assert kwargs == {
        "mrkt_tp": "001",
        "sort_tp": "1",
        "trde_qty_tp": "0000",
        "stk_cnd": "0",
        "crd_cnd": "0",
        "stex_tp": "1",
        "cont_yn": "N",
        "next_key": "",
    }


def test_net_buy_trader_maps_required_fields() -> None:
    recorder = _Recorder()
    params = _params_for(handlers.handle_kiwoom_net_buy_trader)

    handlers.handle_kiwoom_net_buy_trader(params, _Session(recorder))

    method_name, kwargs = recorder.calls[0]
    assert method_name == "get_top_net_buy_trader_ranking"
    assert kwargs["stk_cd"] == "KRX:005930"
    assert kwargs["strt_dt"] == "20240101"
    assert kwargs["end_dt"] == "20240131"
    assert kwargs["qry_dt_tp"] == "1"
    assert kwargs["pot_tp"] == "0"
    assert kwargs["dt"] == "1"
    assert kwargs["sort_base"] == "1"
    assert kwargs["cont_yn"] == "N"
    assert kwargs["next_key"] == ""


def test_register_kiwoom_rank_info_handlers_registers_all_handlers() -> None:
    dispatcher = _Dispatcher()

    handlers.register_kiwoom_rank_info_handlers(dispatcher)

    registered_names = [name for name, _, _ in dispatcher.registrations]
    assert registered_names == [handler._rpc_schema.name for handler in handlers._ALL_HANDLERS]
    assert all(schema.broker == "kiwoom" for _, _, schema in dispatcher.registrations)
