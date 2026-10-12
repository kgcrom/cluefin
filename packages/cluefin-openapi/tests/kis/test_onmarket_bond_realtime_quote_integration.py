"""Integration tests for KIS OnmarketBondRealtimeQuote WebSocket module.

These tests require actual API credentials and network access.
They connect to the KIS WebSocket server (prod only) and receive real-time bond market data.

Runs only during KST market hours (Mon-Fri 09:00-15:30). A single bond trades rarely, so data
reception tests skip on timeout instead of failing.

Test bond code: KR103502GA34 (국고01500-5003(20-2), checked with inquire-price 2026-10-11)
Test bond index code: KBPR01 (the H0BICNT0 request example in the KIS portal)
"""

import asyncio

import pytest

from cluefin_openapi.kis._onmarket_bond_realtime_quote import OnmarketBondRealtimeQuote
from cluefin_openapi.kis._onmarket_bond_realtime_quote_types import (
    OnmarketBondIndexRealtimeExecutionItem,
    OnmarketBondRealtimeExecutionItem,
    OnmarketBondRealtimeOrderbookItem,
)
from cluefin_openapi.kis._socket_client import SocketClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.realtime,
    # 시간대 gate 가 먼저 — 장외에는 auth_dev 를 쓰는 _require_prod_env 까지 가지 않는다.
    pytest.mark.usefixtures("kst_market_hours", "_require_prod_env"),
]

BOND_CODE = "KR103502GA34"
BOND_INDEX_CODE = "KBPR01"


@pytest.fixture(scope="module")
def _require_prod_env(auth_dev):
    if auth_dev.env != "prod":
        pytest.skip("OnmarketBondRealtimeQuote requires prod environment (KIS_ENV=prod)")


@pytest.fixture(scope="module")
def approval_key(auth_dev):
    """Fixture to get WebSocket approval key."""
    approval_response = auth_dev.approve()
    return approval_response.approval_key


@pytest.fixture
def socket_client_params(auth_dev, approval_key):
    """Fixture to provide SocketClient initialization parameters."""
    return {
        "approval_key": approval_key,
        "app_key": auth_dev.app_key,
        "secret_key": auth_dev.secret_key,
        "env": "prod",
        "debug": True,
    }


# ===== Execution (H0BJCNT0) Integration Tests =====


@pytest.mark.asyncio
async def test_websocket_connection(socket_client_params):
    """Test WebSocket connection to KIS prod server."""
    async with SocketClient(**socket_client_params) as client:
        assert client.connected is True

    assert client.connected is False


@pytest.mark.asyncio
async def test_subscribe_execution(socket_client_params):
    """Test subscribing to real-time bond execution data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_execution(BOND_CODE)

        assert f"H0BJCNT0:{BOND_CODE}" in client.subscriptions


@pytest.mark.asyncio
async def test_unsubscribe_execution(socket_client_params):
    """Test unsubscribing from real-time bond execution data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_execution(BOND_CODE)
        assert f"H0BJCNT0:{BOND_CODE}" in client.subscriptions

        await realtime.unsubscribe_execution(BOND_CODE)
        assert f"H0BJCNT0:{BOND_CODE}" not in client.subscriptions


@pytest.mark.asyncio
async def test_receive_execution_data(socket_client_params):
    """Test receiving real-time bond execution data.

    Note: This test may timeout outside market hours when no data is being sent.
    """
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_execution(BOND_CODE)

        data_received = False
        timeout = 30

        async def receive_data():
            nonlocal data_received
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "data" and event.tr_id == OnmarketBondRealtimeQuote.TR_ID_EXECUTION:
                    executions = realtime.parse_execution_data(event.data["values"])

                    assert isinstance(executions, list)
                    assert len(executions) >= 1
                    execution = executions[0]

                    assert isinstance(execution, OnmarketBondRealtimeExecutionItem)
                    assert execution.stnd_iscd != ""
                    assert execution.stck_prpr != ""
                    assert execution.bond_cntg_ert != ""

                    data_received = True
                    return

        try:
            await asyncio.wait_for(receive_data(), timeout=timeout)
        except asyncio.TimeoutError:
            pytest.skip(
                f"No bond execution data received within {timeout}s. "
                "This may be expected outside market hours (9:00-15:30 KST)."
            )

        assert data_received is True


@pytest.mark.asyncio
async def test_subscription_events(socket_client_params):
    """Test that execution subscription events are emitted correctly."""
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_execution(BOND_CODE)

        subscribed_event_found = False

        async def check_events():
            nonlocal subscribed_event_found
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "subscribed":
                    assert event.tr_id == "H0BJCNT0"
                    assert event.tr_key == BOND_CODE
                    subscribed_event_found = True
                    return

        try:
            await asyncio.wait_for(check_events(), timeout=5)
        except asyncio.TimeoutError:
            pass

        assert subscribed_event_found is True


# ===== Orderbook (H0BJASP0) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_orderbook(socket_client_params):
    """Test subscribing to real-time bond orderbook data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_orderbook(BOND_CODE)

        assert f"H0BJASP0:{BOND_CODE}" in client.subscriptions


@pytest.mark.asyncio
async def test_unsubscribe_orderbook(socket_client_params):
    """Test unsubscribing from real-time bond orderbook data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_orderbook(BOND_CODE)
        assert f"H0BJASP0:{BOND_CODE}" in client.subscriptions

        await realtime.unsubscribe_orderbook(BOND_CODE)
        assert f"H0BJASP0:{BOND_CODE}" not in client.subscriptions


@pytest.mark.asyncio
async def test_receive_orderbook_data(socket_client_params):
    """Test receiving real-time bond orderbook data.

    Note: This test may timeout outside market hours when no data is being sent.
    """
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_orderbook(BOND_CODE)

        data_received = False
        timeout = 30

        async def receive_data():
            nonlocal data_received
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "data" and event.tr_id == OnmarketBondRealtimeQuote.TR_ID_ORDERBOOK:
                    orderbooks = realtime.parse_orderbook_data(event.data["values"])

                    assert isinstance(orderbooks, list)
                    assert len(orderbooks) >= 1
                    orderbook = orderbooks[0]

                    assert isinstance(orderbook, OnmarketBondRealtimeOrderbookItem)
                    assert orderbook.stnd_iscd != ""
                    assert orderbook.askp1 != ""
                    assert orderbook.bidp1 != ""

                    data_received = True
                    return

        try:
            await asyncio.wait_for(receive_data(), timeout=timeout)
        except asyncio.TimeoutError:
            pytest.skip(
                f"No bond orderbook data received within {timeout}s. "
                "This may be expected outside market hours (9:00-15:30 KST)."
            )

        assert data_received is True


@pytest.mark.asyncio
async def test_orderbook_subscription_events(socket_client_params):
    """Test that orderbook subscription events are emitted correctly."""
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_orderbook(BOND_CODE)

        subscribed_event_found = False

        async def check_events():
            nonlocal subscribed_event_found
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "subscribed":
                    assert event.tr_id == "H0BJASP0"
                    assert event.tr_key == BOND_CODE
                    subscribed_event_found = True
                    return

        try:
            await asyncio.wait_for(check_events(), timeout=5)
        except asyncio.TimeoutError:
            pass

        assert subscribed_event_found is True


# ===== Bond Index Execution (H0BICNT0) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_index_execution(socket_client_params):
    """Test subscribing to real-time bond index execution data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_index_execution(BOND_INDEX_CODE)

        assert f"H0BICNT0:{BOND_INDEX_CODE}" in client.subscriptions


@pytest.mark.asyncio
async def test_unsubscribe_index_execution(socket_client_params):
    """Test unsubscribing from real-time bond index execution data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_index_execution(BOND_INDEX_CODE)
        assert f"H0BICNT0:{BOND_INDEX_CODE}" in client.subscriptions

        await realtime.unsubscribe_index_execution(BOND_INDEX_CODE)
        assert f"H0BICNT0:{BOND_INDEX_CODE}" not in client.subscriptions


@pytest.mark.asyncio
async def test_receive_index_execution_data(socket_client_params):
    """Test receiving real-time bond index execution data.

    Note: This test may timeout outside market hours when no data is being sent.
    """
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_index_execution(BOND_INDEX_CODE)

        data_received = False
        timeout = 30

        async def receive_data():
            nonlocal data_received
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "data" and event.tr_id == OnmarketBondRealtimeQuote.TR_ID_INDEX_EXECUTION:
                    index_data = realtime.parse_index_execution_data(event.data["values"])

                    assert isinstance(index_data, list)
                    assert len(index_data) >= 1
                    item = index_data[0]

                    assert isinstance(item, OnmarketBondIndexRealtimeExecutionItem)
                    assert item.nmix_id != ""
                    assert item.totl_ernn_nmix != ""

                    data_received = True
                    return

        try:
            await asyncio.wait_for(receive_data(), timeout=timeout)
        except asyncio.TimeoutError:
            pytest.skip(
                f"No bond index execution data received within {timeout}s. "
                "This may be expected outside market hours (9:00-15:30 KST)."
            )

        assert data_received is True


# ===== Combined Tests =====


@pytest.mark.asyncio
async def test_combined_execution_and_orderbook(socket_client_params):
    """Test subscribing to both execution and orderbook data simultaneously."""
    async with SocketClient(**socket_client_params) as client:
        realtime = OnmarketBondRealtimeQuote(client)

        await realtime.subscribe_execution(BOND_CODE)
        await asyncio.sleep(0.3)
        await realtime.subscribe_orderbook(BOND_CODE)

        assert f"H0BJCNT0:{BOND_CODE}" in client.subscriptions
        assert f"H0BJASP0:{BOND_CODE}" in client.subscriptions

        data_received = {"execution": False, "orderbook": False}
        timeout = 30

        async def receive_data():
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "data":
                    if event.tr_id == OnmarketBondRealtimeQuote.TR_ID_EXECUTION:
                        executions = realtime.parse_execution_data(event.data["values"])
                        assert isinstance(executions, list)
                        assert len(executions) >= 1
                        assert isinstance(executions[0], OnmarketBondRealtimeExecutionItem)
                        data_received["execution"] = True
                    elif event.tr_id == OnmarketBondRealtimeQuote.TR_ID_ORDERBOOK:
                        orderbooks = realtime.parse_orderbook_data(event.data["values"])
                        assert isinstance(orderbooks, list)
                        assert len(orderbooks) >= 1
                        assert isinstance(orderbooks[0], OnmarketBondRealtimeOrderbookItem)
                        data_received["orderbook"] = True

                    if data_received["execution"] or data_received["orderbook"]:
                        return

        try:
            await asyncio.wait_for(receive_data(), timeout=timeout)
        except asyncio.TimeoutError:
            pytest.skip(
                f"No data received within {timeout}s. This may be expected outside market hours (9:00-15:30 KST)."
            )

        assert data_received["execution"] or data_received["orderbook"]

        await realtime.unsubscribe_execution(BOND_CODE)
        await realtime.unsubscribe_orderbook(BOND_CODE)
        assert len(client.subscriptions) == 0
