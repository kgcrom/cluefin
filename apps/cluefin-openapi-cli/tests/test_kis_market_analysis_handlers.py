from __future__ import annotations

import pytest

from cluefin_openapi_cli.handlers.kis import domestic_market_analysis as handlers


class _Dumpable:
    def __init__(self, value: str) -> None:
        self.value = value

    def model_dump(self) -> dict[str, str]:
        return {"value": self.value}


class _Response:
    def __init__(self, method_name: str) -> None:
        self.body = type("Body", (), {"output": _Dumpable(method_name)})()


class _Recorder:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def __getattr__(self, method_name: str):
        def call(**kwargs):
            self.calls.append((method_name, kwargs))
            return _Response(method_name)

        return call


class _Kis:
    def __init__(self, recorder: _Recorder) -> None:
        self.domestic_market_analysis = recorder


class _Session:
    def __init__(self, recorder: _Recorder) -> None:
        self._kis = _Kis(recorder)

    def get_kis(self) -> _Kis:
        return self._kis


class _Dispatcher:
    def __init__(self) -> None:
        self.registrations: list[tuple[str, object, object]] = []

    def register(self, name, handler, schema) -> None:
        self.registrations.append((name, handler, schema))


def _sample_value(name: str):
    if name == "stocks":
        return [
            {"market": "J", "stock_code": "005930"},
            {"market": "NX", "stock_code": "000660"},
        ]
    return {
        "date": "20240131",
        "end_date": "20240131",
        "exchange_code": "J",
        "market": "J",
        "market_code": "KSP",
        "market_div_code": "1",
        "price_cls_code": "0",
        "sector_code": "0001",
        "sort_by": "0",
        "sort_by_2": "1",
        "start_date": "20240101",
        "stock_code": "005930",
        "sub_sector_code": "0001",
        "user_id": "test_user",
    }.get(name, f"value_{name}")


def _params_for(handler) -> dict:
    schema = handler._rpc_schema.parameters
    return {name: _sample_value(name) for name in schema.get("required", [])}


@pytest.mark.parametrize("handler", handlers._ALL_HANDLERS, ids=lambda handler: handler._rpc_schema.name)
def test_kis_market_analysis_handlers_call_underlying_client(handler) -> None:
    recorder = _Recorder()
    result = handler(_params_for(handler), _Session(recorder))

    assert result == {"data": {"value": recorder.calls[0][0]}}
    assert len(recorder.calls) == 1


def test_watchlist_multi_quote_expands_to_thirty_slots() -> None:
    recorder = _Recorder()
    params = _params_for(handlers.handle_kis_watchlist_multi_quote)

    handlers.handle_kis_watchlist_multi_quote(params, _Session(recorder))

    method_name, kwargs = recorder.calls[0]
    assert method_name == "get_watchlist_multi_quote"
    assert kwargs["fid_cond_mrkt_div_code_1"] == "J"
    assert kwargs["fid_input_iscd_1"] == "005930"
    assert kwargs["fid_cond_mrkt_div_code_2"] == "NX"
    assert kwargs["fid_input_iscd_2"] == "000660"
    assert kwargs["fid_cond_mrkt_div_code_3"] == ""
    assert kwargs["fid_input_iscd_30"] == ""
    assert len(kwargs) == 60


def test_member_trend_tick_uses_documented_defaults() -> None:
    recorder = _Recorder()

    handlers.handle_kis_member_trend_tick({}, _Session(recorder))

    method_name, kwargs = recorder.calls[0]
    assert method_name == "get_member_trading_trend_tick"
    assert kwargs == {
        "fid_cond_scr_div_code": "20432",
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": "",
        "fid_input_iscd_2": "99999",
        "fid_mrkt_cls_code": "",
        "fid_vol_cnt": "",
    }


def test_register_kis_market_analysis_handlers_registers_all_handlers() -> None:
    dispatcher = _Dispatcher()

    handlers.register_kis_market_analysis_handlers(dispatcher)

    registered_names = [name for name, _, _ in dispatcher.registrations]
    assert registered_names == [handler._rpc_schema.name for handler in handlers._ALL_HANDLERS]
    assert all(schema.broker == "kis" for _, _, schema in dispatcher.registrations)
