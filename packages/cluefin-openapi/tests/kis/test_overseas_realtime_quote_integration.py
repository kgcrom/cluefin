"""Integration tests for KIS OverseasRealtimeQuote WebSocket module.

These tests require actual API credentials and network access.
They connect to the KIS WebSocket server (prod only) and receive real-time overseas stock data.

WARNING: Market hours vary by exchange. Data reception tests use timeout+skip
for graceful handling outside market hours.

Test symbols: AAPL (NAS), MSFT (NAS)
"""

import asyncio
import re

import pytest

from cluefin_openapi.kis._overseas_realtime_quote import OverseasRealtimeQuote
from cluefin_openapi.kis._overseas_realtime_quote_types import (
    OverseasRealtimeDelayedOrderbookItem,
    OverseasRealtimeExecutionItem,
    OverseasRealtimeOrderbookItem,
)
from cluefin_openapi.kis._socket_client import SocketClient

pytestmark = [pytest.mark.integration, pytest.mark.realtime]


def _markexpr_includes(markexpr: str, name: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", markexpr) is not None


@pytest.fixture(autouse=True, scope="module")
def _require_integration_and_realtime(request):
    markexpr = request.config.option.markexpr or ""
    if not (_markexpr_includes(markexpr, "integration") and _markexpr_includes(markexpr, "realtime")):
        pytest.skip('Requires -m "integration and realtime"')


@pytest.fixture(autouse=True, scope="module")
def _require_prod_env(auth_dev):
    if auth_dev.env != "prod":
        pytest.skip("OverseasRealtimeQuote requires prod environment (KIS_ENV=prod)")


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
    }


# ===== WebSocket Connection =====


@pytest.mark.asyncio
async def test_websocket_connection(socket_client_params):
    """Test WebSocket connection to KIS prod server."""
    try:
        async with SocketClient(**socket_client_params) as client:
            assert client.connected is True

        assert client.connected is False

    except Exception as e:
        pytest.fail(f"WebSocket connection failed: {e}")


# ===== Real-time Orderbook (HDFSASP0) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_orderbook(socket_client_params):
    """Test subscribing to real-time overseas orderbook data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe("AAPL", "NAS")

            assert "HDFSASP0:RNASAAPL" in client.subscriptions

    except Exception as e:
        pytest.fail(f"Orderbook subscription failed: {e}")


@pytest.mark.asyncio
async def test_unsubscribe_orderbook(socket_client_params):
    """Test unsubscribing from real-time overseas orderbook data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe("AAPL", "NAS")
            assert "HDFSASP0:RNASAAPL" in client.subscriptions

            await realtime.unsubscribe("AAPL", "NAS")
            assert "HDFSASP0:RNASAAPL" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Orderbook unsubscription failed: {e}")


@pytest.mark.asyncio
async def test_receive_orderbook_data(socket_client_params):
    """Test receiving real-time overseas orderbook data.

    Note: This test may timeout outside US market hours.
    """
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe("AAPL", "NAS")

            data_received = False
            timeout = 30

            async def receive_data():
                nonlocal data_received
                async for event in client.events():
                    if event.event_type == "data" and event.tr_id == OverseasRealtimeQuote.TR_ID:
                        orderbooks = realtime.parse_data(event.data["values"])

                        assert isinstance(orderbooks, list)
                        assert len(orderbooks) >= 1
                        orderbook = orderbooks[0]

                        assert isinstance(orderbook, OverseasRealtimeOrderbookItem)
                        assert orderbook.rsym != ""
                        assert orderbook.pbid1 != ""
                        assert orderbook.pask1 != ""

                        data_received = True
                        return

            try:
                await asyncio.wait_for(receive_data(), timeout=timeout)
            except asyncio.TimeoutError:
                pytest.skip(f"No orderbook data received within {timeout}s. This may be expected outside market hours.")

            assert data_received is True

    except Exception as e:
        pytest.fail(f"Orderbook data reception failed: {e}")


@pytest.mark.asyncio
async def test_orderbook_subscription_events(socket_client_params):
    """Test that orderbook subscription events are emitted correctly."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe("AAPL", "NAS")

            subscribed_event_found = False

            async def check_events():
                nonlocal subscribed_event_found
                async for event in client.events():
                    if event.event_type == "subscribed":
                        assert event.tr_id == "HDFSASP0"
                        assert event.tr_key == "RNASAAPL"
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
async def test_multiple_orderbook_subscriptions(socket_client_params):
    """Test subscribing to multiple stocks' orderbook simultaneously."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe("AAPL", "NAS")
            await asyncio.sleep(0.3)
            await realtime.subscribe("MSFT", "NAS")

            assert "HDFSASP0:RNASAAPL" in client.subscriptions
            assert "HDFSASP0:RNASMSFT" in client.subscriptions

            await realtime.unsubscribe("AAPL", "NAS")
            await realtime.unsubscribe("MSFT", "NAS")
            assert len(client.subscriptions) == 0

    except Exception as e:
        pytest.fail(f"Multiple orderbook subscription test failed: {e}")


# ===== Delayed Execution (HDFSCNT0) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_execution(socket_client_params):
    """Test subscribing to real-time delayed execution data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe_execution("DNASAAPL")

            assert "HDFSCNT0:DNASAAPL" in client.subscriptions

    except Exception as e:
        pytest.fail(f"Execution subscription failed: {e}")


@pytest.mark.asyncio
async def test_unsubscribe_execution(socket_client_params):
    """Test unsubscribing from real-time delayed execution data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe_execution("DNASAAPL")
            assert "HDFSCNT0:DNASAAPL" in client.subscriptions

            await realtime.unsubscribe_execution("DNASAAPL")
            assert "HDFSCNT0:DNASAAPL" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Execution unsubscription failed: {e}")


@pytest.mark.asyncio
async def test_receive_execution_data(socket_client_params):
    """Test receiving real-time delayed execution data.

    Note: This test may timeout outside US market hours.
    """
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe_execution("DNASAAPL")

            data_received = False
            timeout = 30

            async def receive_data():
                nonlocal data_received
                async for event in client.events():
                    if event.event_type == "data" and event.tr_id == OverseasRealtimeQuote.TR_ID_EXECUTION:
                        executions = realtime.parse_execution_data(event.data["values"])

                        assert isinstance(executions, list)
                        assert len(executions) >= 1
                        execution = executions[0]

                        assert isinstance(execution, OverseasRealtimeExecutionItem)
                        assert execution.rsym != ""
                        assert execution.last != ""
                        assert execution.sign != ""

                        data_received = True
                        return

            try:
                await asyncio.wait_for(receive_data(), timeout=timeout)
            except asyncio.TimeoutError:
                pytest.skip(f"No execution data received within {timeout}s. This may be expected outside market hours.")

            assert data_received is True

    except Exception as e:
        pytest.fail(f"Execution data reception failed: {e}")


@pytest.mark.asyncio
async def test_execution_subscription_events(socket_client_params):
    """Test that execution subscription events are emitted correctly."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe_execution("DNASAAPL")

            subscribed_event_found = False

            async def check_events():
                nonlocal subscribed_event_found
                async for event in client.events():
                    if event.event_type == "subscribed":
                        assert event.tr_id == "HDFSCNT0"
                        assert event.tr_key == "DNASAAPL"
                        subscribed_event_found = True
                        return

            try:
                await asyncio.wait_for(check_events(), timeout=5)
            except asyncio.TimeoutError:
                pass

            assert subscribed_event_found is True

    except Exception as e:
        pytest.fail(f"Execution subscription event test failed: {e}")


# ===== Delayed Orderbook Asia (HDFSASP1) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_delayed_orderbook(socket_client_params):
    """Test subscribing to delayed orderbook data (Asia)."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe_delayed_orderbook("DHKS00700")

            assert "HDFSASP1:DHKS00700" in client.subscriptions

    except Exception as e:
        pytest.fail(f"Delayed orderbook subscription failed: {e}")


@pytest.mark.asyncio
async def test_unsubscribe_delayed_orderbook(socket_client_params):
    """Test unsubscribing from delayed orderbook data (Asia)."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe_delayed_orderbook("DHKS00700")
            assert "HDFSASP1:DHKS00700" in client.subscriptions

            await realtime.unsubscribe_delayed_orderbook("DHKS00700")
            assert "HDFSASP1:DHKS00700" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Delayed orderbook unsubscription failed: {e}")


@pytest.mark.asyncio
async def test_receive_delayed_orderbook_data(socket_client_params):
    """Test receiving delayed orderbook data (Asia).

    Note: This test may timeout outside HK market hours.
    """
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe_delayed_orderbook("DHKS00700")

            data_received = False
            timeout = 30

            async def receive_data():
                nonlocal data_received
                async for event in client.events():
                    if event.event_type == "data" and event.tr_id == OverseasRealtimeQuote.TR_ID_DELAYED_ORDERBOOK:
                        orderbooks = realtime.parse_delayed_orderbook_data(event.data["values"])

                        assert isinstance(orderbooks, list)
                        assert len(orderbooks) >= 1
                        orderbook = orderbooks[0]

                        assert isinstance(orderbook, OverseasRealtimeDelayedOrderbookItem)
                        assert orderbook.rsym != ""
                        assert orderbook.pbid1 != ""
                        assert orderbook.pask1 != ""

                        data_received = True
                        return

            try:
                await asyncio.wait_for(receive_data(), timeout=timeout)
            except asyncio.TimeoutError:
                pytest.skip(
                    f"No delayed orderbook data received within {timeout}s. This may be expected outside market hours."
                )

            assert data_received is True

    except Exception as e:
        pytest.fail(f"Delayed orderbook data reception failed: {e}")


# ===== Execution Notification (H0GSCNI0) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_execution_notification(socket_client_params):
    """Test subscribing to execution notification.

    Note: Only tests subscribe. Data reception requires actual orders.
    """
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe_execution_notification("testuser")

            assert "H0GSCNI0:testuser" in client.subscriptions

    except Exception as e:
        pytest.fail(f"Execution notification subscription failed: {e}")


@pytest.mark.asyncio
async def test_unsubscribe_execution_notification(socket_client_params):
    """Test unsubscribing from execution notification."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe_execution_notification("testuser")
            assert "H0GSCNI0:testuser" in client.subscriptions

            await realtime.unsubscribe_execution_notification("testuser")
            assert "H0GSCNI0:testuser" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Execution notification unsubscription failed: {e}")


# ===== Combined Tests =====


@pytest.mark.asyncio
async def test_combined_orderbook_and_execution(socket_client_params):
    """Test subscribing to both orderbook and execution data simultaneously."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe("AAPL", "NAS")
            await asyncio.sleep(0.3)
            await realtime.subscribe_execution("DNASAAPL")

            assert "HDFSASP0:RNASAAPL" in client.subscriptions
            assert "HDFSCNT0:DNASAAPL" in client.subscriptions

            data_received = {"orderbook": False, "execution": False}
            timeout = 30

            async def receive_data():
                async for event in client.events():
                    if event.event_type == "data":
                        if event.tr_id == OverseasRealtimeQuote.TR_ID:
                            orderbooks = realtime.parse_data(event.data["values"])
                            assert isinstance(orderbooks, list)
                            assert len(orderbooks) >= 1
                            assert isinstance(orderbooks[0], OverseasRealtimeOrderbookItem)
                            data_received["orderbook"] = True
                        elif event.tr_id == OverseasRealtimeQuote.TR_ID_EXECUTION:
                            executions = realtime.parse_execution_data(event.data["values"])
                            assert isinstance(executions, list)
                            assert len(executions) >= 1
                            assert isinstance(executions[0], OverseasRealtimeExecutionItem)
                            data_received["execution"] = True

                        if data_received["orderbook"] or data_received["execution"]:
                            return

            try:
                await asyncio.wait_for(receive_data(), timeout=timeout)
            except asyncio.TimeoutError:
                pytest.skip(f"No data received within {timeout}s. This may be expected outside market hours.")

            assert data_received["orderbook"] or data_received["execution"]

            await realtime.unsubscribe("AAPL", "NAS")
            await realtime.unsubscribe_execution("DNASAAPL")
            assert len(client.subscriptions) == 0

    except Exception as e:
        pytest.fail(f"Combined subscription test failed: {e}")


@pytest.mark.asyncio
async def test_multiple_market_subscriptions(socket_client_params):
    """Test subscribing to multiple stocks from the same market."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe("AAPL", "NAS")
            await asyncio.sleep(0.3)
            await realtime.subscribe("MSFT", "NAS")

            assert "HDFSASP0:RNASAAPL" in client.subscriptions
            assert "HDFSASP0:RNASMSFT" in client.subscriptions

            await realtime.unsubscribe("AAPL", "NAS")
            await realtime.unsubscribe("MSFT", "NAS")
            assert len(client.subscriptions) == 0

    except Exception as e:
        pytest.fail(f"Multiple market subscription test failed: {e}")


@pytest.mark.asyncio
async def test_subscribe_with_night_service_type(socket_client_params):
    """Test subscribing with night service type (service_type='D')."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OverseasRealtimeQuote(client)

            await realtime.subscribe("AAPL", "NAS", service_type="D")

            assert "HDFSASP0:DNASAAPL" in client.subscriptions

            await realtime.unsubscribe("AAPL", "NAS", service_type="D")
            assert "HDFSASP0:DNASAAPL" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Night service type subscription failed: {e}")
