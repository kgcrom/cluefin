"""Tests for the method dispatcher."""

import pytest

from cluefin_rpc.dispatcher import Dispatcher, InvalidParamsError, MethodNotFoundError
from cluefin_rpc.handlers._base import MethodSchema


def _make_schema(name: str, category: str = "", broker: str | None = None, requires_session: bool = False):
    return MethodSchema(
        name=name,
        description=f"Test {name}",
        parameters={"type": "object"},
        returns={"type": "object"},
        category=category,
        requires_session=requires_session,
        broker=broker,
    )


class TestDispatcher:
    def test_register_and_dispatch(self):
        d = Dispatcher()
        schema = _make_schema("test.echo")

        def handler(params):
            return {"echo": params.get("msg")}

        d.register("test.echo", handler, schema)
        result = d.dispatch("test.echo", {"msg": "hello"}, None)
        assert result == {"echo": "hello"}

    def test_dispatch_with_session(self):
        d = Dispatcher()
        schema = _make_schema("test.session", requires_session=True)

        def handler(params, session):
            return {"session": session is not None}

        d.register("test.session", handler, schema)
        result = d.dispatch("test.session", {}, "fake_session")
        assert result == {"session": True}

    def test_unknown_method(self):
        d = Dispatcher()
        with pytest.raises(MethodNotFoundError, match="no_such"):
            d.dispatch("no_such", {}, None)

    def test_params_must_be_dict(self):
        d = Dispatcher()
        schema = _make_schema("test.fn")
        d.register("test.fn", lambda p: p, schema)
        with pytest.raises(InvalidParamsError, match="object"):
            d.dispatch("test.fn", [1, 2], None)

    def test_none_params_default_to_empty_dict(self):
        d = Dispatcher()
        schema = _make_schema("test.fn")

        def handler(params):
            return {"empty": len(params) == 0}

        d.register("test.fn", handler, schema)
        result = d.dispatch("test.fn", None, None)
        assert result == {"empty": True}

    def test_list_methods_all(self):
        d = Dispatcher()
        d.register("a.one", lambda p: p, _make_schema("a.one", category="a", broker="kis"))
        d.register("b.two", lambda p: p, _make_schema("b.two", category="b", broker="kiwoom"))
        methods = d.list_methods()
        assert len(methods) == 2
        names = {m["name"] for m in methods}
        assert names == {"a.one", "b.two"}

    def test_list_methods_by_category(self):
        d = Dispatcher()
        d.register("a.one", lambda p: p, _make_schema("a.one", category="quote"))
        d.register("b.two", lambda p: p, _make_schema("b.two", category="ta"))
        methods = d.list_methods(category="quote")
        assert len(methods) == 1
        assert methods[0]["name"] == "a.one"

    def test_list_methods_by_broker(self):
        d = Dispatcher()
        d.register("a.one", lambda p: p, _make_schema("a.one", broker="kis"))
        d.register("b.two", lambda p: p, _make_schema("b.two", broker="kiwoom"))
        methods = d.list_methods(broker="kiwoom")
        assert len(methods) == 1
        assert methods[0]["name"] == "b.two"

    def test_list_methods_combined_filter(self):
        d = Dispatcher()
        d.register("a", lambda p: p, _make_schema("a", category="quote", broker="kis"))
        d.register("b", lambda p: p, _make_schema("b", category="quote", broker="kiwoom"))
        d.register("c", lambda p: p, _make_schema("c", category="ta"))
        methods = d.list_methods(category="quote", broker="kis")
        assert len(methods) == 1
        assert methods[0]["name"] == "a"
