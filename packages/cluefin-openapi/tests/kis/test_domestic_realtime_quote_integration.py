"""Integration tests for KIS DomesticRealtimeQuote WebSocket module.

These tests require actual API credentials and network access.
They connect to the KIS WebSocket server and receive real-time market data.

Runs only during KRX continuous trading (Mon-Fri 09:00-15:20 KST) and on prod: the execution TR
H0UNCNT0 (통합) is not offered on the mock server. Samsung Electronics trades every few seconds then,
so a data timeout is a failure, not a skip.
"""

import asyncio

import pytest

from cluefin_openapi.kis._domestic_realtime_quote import DomesticRealtimeQuote
from cluefin_openapi.kis._domestic_realtime_quote_types import (
    DomesticRealtimeExecutionItem,
    DomesticRealtimeOrderbookItem,
)
from cluefin_openapi.kis._socket_client import SocketClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.realtime,
    # 시간대 gate 가 먼저 — 장외에는 auth_dev 를 쓰는 _require_prod_env 까지 가지 않는다.
    pytest.mark.usefixtures("krx_continuous_hours", "_require_prod_env"),
]


@pytest.fixture(scope="module")
def _require_prod_env(auth_dev):
    # H0UNCNT0 (실시간 체결가 통합) 은 모의투자 미지원 — 포털 명세의 virtualTrId 가 "모의투자 미지원" 이다.
    if auth_dev.env != "prod":
        pytest.skip("DomesticRealtimeQuote execution (H0UNCNT0) requires prod environment (KIS_ENV=prod)")


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
        "env": auth_dev.env,
        "debug": True,
    }


@pytest.mark.asyncio
async def test_websocket_connection(socket_client_params):
    """Test WebSocket connection to KIS server."""
    async with SocketClient(**socket_client_params) as client:
        assert client.connected is True

    # After context exit, should be disconnected
    assert client.connected is False


@pytest.mark.asyncio
async def test_subscribe_execution(socket_client_params):
    """Test subscribing to real-time execution data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe to Samsung Electronics
        await realtime.subscribe_execution("005930")

        # Verify subscription is registered
        assert "H0UNCNT0:005930" in client.subscriptions


@pytest.mark.asyncio
async def test_unsubscribe_execution(socket_client_params):
    """Test unsubscribing from real-time execution data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe first
        await realtime.subscribe_execution("005930")
        assert "H0UNCNT0:005930" in client.subscriptions

        # Then unsubscribe
        await realtime.unsubscribe_execution("005930")
        assert "H0UNCNT0:005930" not in client.subscriptions


@pytest.mark.asyncio
async def test_receive_execution_data(socket_client_params):
    """Test receiving real-time execution data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe to Samsung Electronics (high-volume stock)
        await realtime.subscribe_execution("005930")

        # Wait for data events (with timeout)
        data_received = False
        timeout = 30  # seconds

        async def receive_data():
            nonlocal data_received
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "data" and event.tr_id == DomesticRealtimeQuote.TR_ID_EXECUTION:
                    # Parse the data (returns list of items)
                    executions = realtime.parse_execution_data(event.data["values"])

                    # Verify it's a valid list
                    assert isinstance(executions, list)
                    assert len(executions) >= 1
                    execution = executions[0]

                    # Verify the first item is a valid model
                    assert isinstance(execution, DomesticRealtimeExecutionItem)
                    assert execution.mksc_shrn_iscd == "005930"
                    assert execution.stck_prpr != ""  # Should have a price
                    # Verify sign codes are valid (1~5)
                    assert execution.prdy_vrss_sign in ["1", "2", "3", "4", "5"]
                    assert execution.oprc_vrss_prpr_sign in ["1", "2", "3", "4", "5"]

                    data_received = True
                    return

        try:
            await asyncio.wait_for(receive_data(), timeout=timeout)
        except asyncio.TimeoutError:
            pytest.fail(f"No execution data for 005930 within {timeout}s during continuous trading hours.")

        assert data_received is True


@pytest.mark.asyncio
async def test_multiple_subscriptions(socket_client_params):
    """Test subscribing to multiple stocks simultaneously."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe to multiple stocks
        stock_codes = ["005930", "000660", "035720"]  # Samsung, SK Hynix, Kakao

        for code in stock_codes:
            await realtime.subscribe_execution(code)
            # Small delay between subscriptions for rate limiting
            await asyncio.sleep(0.3)

        # Verify all subscriptions
        for code in stock_codes:
            assert f"H0UNCNT0:{code}" in client.subscriptions

        # Unsubscribe from all
        for code in stock_codes:
            await realtime.unsubscribe_execution(code)

        assert len(client.subscriptions) == 0


@pytest.mark.asyncio
async def test_subscription_events(socket_client_params):
    """Test that subscription events are emitted correctly."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe and check for subscribed event
        await realtime.subscribe_execution("005930")

        # Check for the subscribed event in the queue
        subscribed_event_found = False

        async def check_events():
            nonlocal subscribed_event_found
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "subscribed":
                    assert event.tr_id == "H0UNCNT0"
                    assert event.tr_key == "005930"
                    subscribed_event_found = True
                    return

        try:
            await asyncio.wait_for(check_events(), timeout=5)
        except asyncio.TimeoutError:
            pass

        assert subscribed_event_found is True


# ===== Orderbook (H0STASP0) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_orderbook(socket_client_params):
    """Test subscribing to real-time orderbook data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe to Samsung Electronics orderbook
        await realtime.subscribe_orderbook("005930")

        # Verify subscription is registered
        assert "H0STASP0:005930" in client.subscriptions


@pytest.mark.asyncio
async def test_unsubscribe_orderbook(socket_client_params):
    """Test unsubscribing from real-time orderbook data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe first
        await realtime.subscribe_orderbook("005930")
        assert "H0STASP0:005930" in client.subscriptions

        # Then unsubscribe
        await realtime.unsubscribe_orderbook("005930")
        assert "H0STASP0:005930" not in client.subscriptions


@pytest.mark.asyncio
async def test_receive_orderbook_data(socket_client_params):
    """Test receiving real-time orderbook data."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe to Samsung Electronics orderbook (high-volume stock)
        await realtime.subscribe_orderbook("005930")

        # Wait for data events (with timeout)
        data_received = False
        timeout = 30  # seconds

        async def receive_data():
            nonlocal data_received
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "data" and event.tr_id == DomesticRealtimeQuote.TR_ID_ORDERBOOK:
                    # Parse the data (returns list of items)
                    orderbooks = realtime.parse_orderbook_data(event.data["values"])

                    # Verify it's a valid list
                    assert isinstance(orderbooks, list)
                    assert len(orderbooks) >= 1
                    orderbook = orderbooks[0]

                    # Verify the first item is a valid model
                    assert isinstance(orderbook, DomesticRealtimeOrderbookItem)
                    assert orderbook.mksc_shrn_iscd == "005930"
                    assert orderbook.askp1 != ""  # Should have ask price
                    assert orderbook.bidp1 != ""  # Should have bid price
                    # Verify hour_cls_code is valid (0: 장중, A: 장후예상, B: 장전예상, C: VI발동, D: 시간외단일가)
                    assert orderbook.hour_cls_code in ["0", "A", "B", "C", "D"]

                    data_received = True
                    return

        try:
            await asyncio.wait_for(receive_data(), timeout=timeout)
        except asyncio.TimeoutError:
            pytest.fail(f"No orderbook data for 005930 within {timeout}s during continuous trading hours.")

        assert data_received is True


@pytest.mark.asyncio
async def test_multiple_orderbook_subscriptions(socket_client_params):
    """Test subscribing to multiple stocks' orderbook simultaneously."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe to multiple stocks
        stock_codes = ["005930", "000660", "035720"]  # Samsung, SK Hynix, Kakao

        for code in stock_codes:
            await realtime.subscribe_orderbook(code)
            # Small delay between subscriptions for rate limiting
            await asyncio.sleep(0.3)

        # Verify all subscriptions
        for code in stock_codes:
            assert f"H0STASP0:{code}" in client.subscriptions

        # Unsubscribe from all
        for code in stock_codes:
            await realtime.unsubscribe_orderbook(code)

        assert len(client.subscriptions) == 0


@pytest.mark.asyncio
async def test_orderbook_subscription_events(socket_client_params):
    """Test that orderbook subscription events are emitted correctly."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe and check for subscribed event
        await realtime.subscribe_orderbook("005930")

        # Check for the subscribed event in the queue
        subscribed_event_found = False

        async def check_events():
            nonlocal subscribed_event_found
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "subscribed":
                    assert event.tr_id == "H0STASP0"
                    assert event.tr_key == "005930"
                    subscribed_event_found = True
                    return

        try:
            await asyncio.wait_for(check_events(), timeout=5)
        except asyncio.TimeoutError:
            pass

        assert subscribed_event_found is True


@pytest.mark.asyncio
async def test_combined_execution_and_orderbook(socket_client_params):
    """Test subscribing to both execution and orderbook data simultaneously."""
    async with SocketClient(**socket_client_params) as client:
        realtime = DomesticRealtimeQuote(client)

        # Subscribe to both execution and orderbook for Samsung
        await realtime.subscribe_execution("005930")
        await asyncio.sleep(0.3)
        await realtime.subscribe_orderbook("005930")

        # Verify both subscriptions are registered
        assert "H0UNCNT0:005930" in client.subscriptions
        assert "H0STASP0:005930" in client.subscriptions

        # Try to receive data from either stream
        data_received = {"execution": False, "orderbook": False}
        timeout = 30  # seconds

        async def receive_data():
            async for event in client.events():
                if event.event_type == "error":
                    pytest.fail(f"KIS WebSocket error: {event.error}")
                if event.event_type == "data":
                    if event.tr_id == DomesticRealtimeQuote.TR_ID_EXECUTION:
                        executions = realtime.parse_execution_data(event.data["values"])
                        assert isinstance(executions, list)
                        assert len(executions) >= 1
                        assert isinstance(executions[0], DomesticRealtimeExecutionItem)
                        data_received["execution"] = True
                    elif event.tr_id == DomesticRealtimeQuote.TR_ID_ORDERBOOK:
                        orderbooks = realtime.parse_orderbook_data(event.data["values"])
                        assert isinstance(orderbooks, list)
                        assert len(orderbooks) >= 1
                        assert isinstance(orderbooks[0], DomesticRealtimeOrderbookItem)
                        data_received["orderbook"] = True

                    # Exit if we received at least one type of data
                    if data_received["execution"] or data_received["orderbook"]:
                        return

        try:
            await asyncio.wait_for(receive_data(), timeout=timeout)
        except asyncio.TimeoutError:
            pytest.fail(f"No execution or orderbook data for 005930 within {timeout}s during continuous trading hours.")

        # At least one type should be received
        assert data_received["execution"] or data_received["orderbook"]

        # Unsubscribe from both
        await realtime.unsubscribe_execution("005930")
        await realtime.unsubscribe_orderbook("005930")
        assert len(client.subscriptions) == 0
