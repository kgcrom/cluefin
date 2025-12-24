"""Integration tests for KIS DomesticRealtimeQuote WebSocket module.

These tests require actual API credentials and network access.
They connect to the KIS WebSocket server and receive real-time market data.

WARNING: These tests should only be run during market hours (9:00-15:30 KST)
for reliable real-time data. Outside market hours, data may not be available.
"""

import asyncio
import os

import dotenv
import pytest
from pydantic import SecretStr

from cluefin_openapi.kis._auth import Auth
from cluefin_openapi.kis._domestic_realtime_quote import DomesticRealtimeQuote
from cluefin_openapi.kis._domestic_realtime_quote_types import DomesticRealtimeExecutionItem
from cluefin_openapi.kis._socket_client import SocketClient


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


@pytest.mark.integration
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


@pytest.mark.integration
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


@pytest.mark.integration
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


@pytest.mark.integration
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
                        # Parse the data
                        execution = realtime.parse_execution_data(event.data["values"])

                        # Verify it's a valid model
                        assert isinstance(execution, DomesticRealtimeExecutionItem)
                        assert execution.mksc_shrn_iscd == "005930"
                        assert execution.stck_prpr != ""  # Should have a price

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


@pytest.mark.integration
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


@pytest.mark.integration
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
