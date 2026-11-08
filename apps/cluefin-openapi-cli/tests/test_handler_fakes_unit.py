"""The handler fakes bind every call to the real SDK signature, so a wrong keyword fails the handler test."""

from __future__ import annotations

import pytest

from tests._handler_fakes import FakeSession


def test_matching_call_is_recorded() -> None:
    session = FakeSession()
    session.get_kiwoom().theme.get_theme_group_stocks(thema_grp_cd="100", stex_tp="1", cont_yn="Y", next_key="k")
    assert session.calls[0][:2] == ("theme", "get_theme_group_stocks")


def test_misspelled_keyword_is_a_type_error() -> None:
    with pytest.raises(TypeError):
        FakeSession().get_kiwoom().theme.get_theme_group_stocks(thema_grp_cd="100", stex_tp="1", cond_yn="Y")


def test_unknown_method_and_sub_client_are_attribute_errors() -> None:
    api = FakeSession().get_dart().periodic_report_financial_statement
    with pytest.raises(AttributeError, match="no method"):
        getattr(api, "get_everything")  # noqa: B009 - the lookup itself is what raises
    with pytest.raises(AttributeError, match="no sub-client"):
        getattr(FakeSession().get_kis(), "not_a_sub_client")  # noqa: B009
