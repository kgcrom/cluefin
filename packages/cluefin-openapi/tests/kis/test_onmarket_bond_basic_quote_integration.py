"""Integration tests for the KIS onmarket bond basic quote module.

These tests hit the real KIS sandbox API and therefore require valid
credentials to be present in the environment (or in `.env.test`).
"""

import pytest

from cluefin_openapi.kis._http_client import HttpClient


@pytest.mark.integration
def test_get_bond_asking_price(client: HttpClient):
    """Test bond asking price inquiry."""
    try:
        response = client.onmarket_bond_basic_quote.get_bond_asking_price("KR2088012A16")
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")
    except Exception as e:
        pytest.fail(f"get_bond_asking_price failed: {e}")


@pytest.mark.integration
def test_get_bond_price(client: HttpClient):
    """Test bond current price inquiry."""
    try:
        response = client.onmarket_bond_basic_quote.get_bond_price("KR2033022D33")
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")
    except Exception as e:
        pytest.fail(f"get_bond_price failed: {e}")


@pytest.mark.integration
def test_get_bond_execution(client: HttpClient):
    """Test bond execution inquiry."""
    try:
        response = client.onmarket_bond_basic_quote.get_bond_execution("KR2033022D33")
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")
    except Exception as e:
        pytest.fail(f"get_bond_execution failed: {e}")


@pytest.mark.integration
def test_get_bond_daily_price(client: HttpClient):
    """Test bond daily price inquiry."""
    try:
        response = client.onmarket_bond_basic_quote.get_bond_daily_price("KR2033022D33")
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")
    except Exception as e:
        pytest.fail(f"get_bond_daily_price failed: {e}")


@pytest.mark.integration
def test_get_bond_daily_chart_price(client: HttpClient):
    """Test bond daily chart price inquiry."""
    try:
        response = client.onmarket_bond_basic_quote.get_bond_daily_chart_price("KR2033022D33")
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")
    except Exception as e:
        pytest.fail(f"get_bond_daily_chart_price failed: {e}")


@pytest.mark.integration
def test_get_bond_avg_unit_price(client: HttpClient):
    """Test bond average unit price inquiry."""
    try:
        response = client.onmarket_bond_basic_quote.get_bond_avg_unit_price(
            inqr_strt_dt="20260218", inqr_end_dt="20260218"
        )
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")
    except Exception as e:
        pytest.fail(f"get_bond_avg_unit_price failed: {e}")


@pytest.mark.integration
def test_get_bond_info(client: HttpClient):
    """Test bond basic info inquiry."""
    try:
        response = client.onmarket_bond_basic_quote.get_bond_info("KR2033022D33")
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")
    except Exception as e:
        pytest.fail(f"get_bond_info failed: {e}")


@pytest.mark.integration
def test_get_bond_issue_info(client: HttpClient):
    """Test bond issue info inquiry."""
    try:
        response = client.onmarket_bond_basic_quote.get_bond_issue_info("KR6449111CB8")
        assert response is not None
        assert hasattr(response.body, "rt_cd")
        assert hasattr(response.body, "msg_cd")
        assert hasattr(response.body, "msg1")
    except Exception as e:
        pytest.fail(f"get_bond_issue_info failed: {e}")
