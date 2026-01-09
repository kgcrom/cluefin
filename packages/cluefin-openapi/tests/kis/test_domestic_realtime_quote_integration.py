"""Integration tests for KIS DomesticRealtimeQuote WebSocket module.

These tests require actual API credentials and network access.
They connect to the KIS WebSocket server and receive real-time market data.

WARNING: These tests should only be run during market hours (9:00-15:30 KST)
for reliable real-time data. Outside market hours, data may not be available.
"""

import asyncio
import os
import re
from datetime import datetime, time
from zoneinfo import ZoneInfo

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._domestic_realtime_quote import DomesticRealtimeQuote
from cluefin_openapi.kis._domestic_realtime_quote_types import (
    DomesticRealtimeExecutionItem,
    DomesticRealtimeOrderbookItem,
)
from cluefin_openapi.kis._socket_client import SocketClient

pytestmark = [pytest.mark.integration, pytest.mark.realtime]


def _markexpr_includes(markexpr: str, name: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", markexpr) is not None


def _is_kst_market_hours() -> bool:
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    if now.weekday() >= 5:
        return False
    return time(9, 0) <= now.time() <= time(15, 30)


@pytest.fixture(autouse=True, scope="module")
def _require_integration_and_realtime(request):
    markexpr = request.config.option.markexpr or ""
    if not (_markexpr_includes(markexpr, "integration") and _markexpr_includes(markexpr, "realtime")):
        pytest.skip('Requires -m "integration and realtime"')


@pytest.fixture(autouse=True, scope="module")
def _require_kst_market_hours():
    if not _is_kst_market_hours():
        pytest.skip("Requires KST market hours (Mon-Fri 09:00-15:30)")


@pytest.fixture(scope="module")
def auth_dev():
    """Fixture to create Auth instance for dev environment."""
    dotenv.load_dotenv(dotenv_path=".env.test")
    app_key = os.getenv("KIS_APP_KEY")
    secret_key = os.getenv("KIS_SECRET_KEY")

    if not app_key or not secret_key:
        pytest.skip("KIS API credentials not available in environment variables")

    return Auth(app_key=app_key, secret_key=SecretStr(secret_key), env="dev")


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
        "env": "dev",
        "debug": True,
    }


@pytest.mark.asyncio
async def test_websocket_connection(socket_client_params):
    """Test WebSocket connection to KIS server."""
    try:
        async with SocketClient(**socket_client_params) as client:
            assert client.connected is True

        # After context exit, should be disconnected
        assert client.connected is False

    except Exception as e:
        pytest.fail(f"WebSocket connection failed: {e}")


@pytest.mark.asyncio
async def test_subscribe_execution(socket_client_params):
    """Test subscribing to real-time execution data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = DomesticRealtimeQuote(client)

            # Subscribe to Samsung Electronics
            await realtime.subscribe_execution("005930")

            # Verify subscription is registered
            assert "H0UNCNT0:005930" in client.subscriptions

    except Exception as e:
        pytest.fail(f"Subscription failed: {e}")


@pytest.mark.asyncio
async def test_unsubscribe_execution(socket_client_params):
    """Test unsubscribing from real-time execution data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = DomesticRealtimeQuote(client)

            # Subscribe first
            await realtime.subscribe_execution("005930")
            assert "H0UNCNT0:005930" in client.subscriptions

            # Then unsubscribe
            await realtime.unsubscribe_execution("005930")
            assert "H0UNCNT0:005930" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Unsubscription failed: {e}")


@pytest.mark.asyncio
async def test_receive_execution_data(socket_client_params):
    """Test receiving real-time execution data.

    Note: This test may timeout outside market hours when no data is being sent.
    """
    try:
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
                # Outside market hours, no data may be available
                pytest.skip(
                    f"No execution data received within {timeout}s. "
                    "This may be expected outside market hours (9:00-15:30 KST)."
                )

            assert data_received is True

    except Exception as e:
        pytest.fail(f"Data reception failed: {e}")


@pytest.mark.asyncio
async def test_multiple_subscriptions(socket_client_params):
    """Test subscribing to multiple stocks simultaneously."""
    try:
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

    except Exception as e:
        pytest.fail(f"Multiple subscription test failed: {e}")


@pytest.mark.asyncio
async def test_subscription_events(socket_client_params):
    """Test that subscription events are emitted correctly."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = DomesticRealtimeQuote(client)

            # Subscribe and check for subscribed event
            await realtime.subscribe_execution("005930")

            # Check for the subscribed event in the queue
            subscribed_event_found = False

            async def check_events():
                nonlocal subscribed_event_found
                async for event in client.events():
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

    except Exception as e:
        pytest.fail(f"Subscription event test failed: {e}")


# ===== Orderbook (H0STASP0) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_orderbook(socket_client_params):
    """Test subscribing to real-time orderbook data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = DomesticRealtimeQuote(client)

            # Subscribe to Samsung Electronics orderbook
            await realtime.subscribe_orderbook("005930")

            # Verify subscription is registered
            assert "H0STASP0:005930" in client.subscriptions

    except Exception as e:
        pytest.fail(f"Orderbook subscription failed: {e}")


@pytest.mark.asyncio
async def test_unsubscribe_orderbook(socket_client_params):
    """Test unsubscribing from real-time orderbook data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = DomesticRealtimeQuote(client)

            # Subscribe first
            await realtime.subscribe_orderbook("005930")
            assert "H0STASP0:005930" in client.subscriptions

            # Then unsubscribe
            await realtime.unsubscribe_orderbook("005930")
            assert "H0STASP0:005930" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Orderbook unsubscription failed: {e}")


@pytest.mark.asyncio
async def test_receive_orderbook_data(socket_client_params):
    """Test receiving real-time orderbook data.

    Note: This test may timeout outside market hours when no data is being sent.
    Orderbook data updates more frequently than execution data.
    """
    try:
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
                # Outside market hours, no data may be available
                pytest.skip(
                    f"No orderbook data received within {timeout}s. "
                    "This may be expected outside market hours (9:00-15:30 KST)."
                )

            assert data_received is True

    except Exception as e:
        pytest.fail(f"Orderbook data reception failed: {e}")


@pytest.mark.asyncio
async def test_multiple_orderbook_subscriptions(socket_client_params):
    """Test subscribing to multiple stocks' orderbook simultaneously."""
    try:
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

    except Exception as e:
        pytest.fail(f"Multiple orderbook subscription test failed: {e}")


@pytest.mark.asyncio
async def test_orderbook_subscription_events(socket_client_params):
    """Test that orderbook subscription events are emitted correctly."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = DomesticRealtimeQuote(client)

            # Subscribe and check for subscribed event
            await realtime.subscribe_orderbook("005930")

            # Check for the subscribed event in the queue
            subscribed_event_found = False

            async def check_events():
                nonlocal subscribed_event_found
                async for event in client.events():
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

    except Exception as e:
        pytest.fail(f"Orderbook subscription event test failed: {e}")


@pytest.mark.asyncio
async def test_combined_execution_and_orderbook(socket_client_params):
    """Test subscribing to both execution and orderbook data simultaneously."""
    try:
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
                pytest.skip(
                    f"No data received within {timeout}s. This may be expected outside market hours (9:00-15:30 KST)."
                )

            # At least one type should be received
            assert data_received["execution"] or data_received["orderbook"]

            # Unsubscribe from both
            await realtime.unsubscribe_execution("005930")
            await realtime.unsubscribe_orderbook("005930")
            assert len(client.subscriptions) == 0

    except Exception as e:
        pytest.fail(f"Combined subscription test failed: {e}")
