"""Integration tests for KIS OnmarketBondRealtimeQuote WebSocket module.

These tests require actual API credentials and network access.
They connect to the KIS WebSocket server (prod only) and receive real-time bond market data.

WARNING: These tests should only be run during market hours (9:00-15:30 KST)
for reliable real-time data. Outside market hours, data may not be available.

Test bond code: KR103502GA34 (국고채권03500-5306)
Test bond index code: 0001
"""

import asyncio
import re
from datetime import datetime, time
from zoneinfo import ZoneInfo

import pytest

from cluefin_openapi.kis._onmarket_bond_realtime_quote import OnmarketBondRealtimeQuote
from cluefin_openapi.kis._onmarket_bond_realtime_quote_types import (
    OnmarketBondIndexRealtimeExecutionItem,
    OnmarketBondRealtimeExecutionItem,
    OnmarketBondRealtimeOrderbookItem,
)
from cluefin_openapi.kis._socket_client import SocketClient

pytestmark = [pytest.mark.integration, pytest.mark.realtime]

BOND_CODE = "KR103502GA34"
BOND_INDEX_CODE = "0001"


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


@pytest.fixture(autouse=True, scope="module")
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
    try:
        async with SocketClient(**socket_client_params) as client:
            assert client.connected is True

        assert client.connected is False

    except Exception as e:
        pytest.fail(f"WebSocket connection failed: {e}")


@pytest.mark.asyncio
async def test_subscribe_execution(socket_client_params):
    """Test subscribing to real-time bond execution data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_execution(BOND_CODE)

            assert f"H0BJCNT0:{BOND_CODE}" in client.subscriptions

    except Exception as e:
        pytest.fail(f"Subscription failed: {e}")


@pytest.mark.asyncio
async def test_unsubscribe_execution(socket_client_params):
    """Test unsubscribing from real-time bond execution data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_execution(BOND_CODE)
            assert f"H0BJCNT0:{BOND_CODE}" in client.subscriptions

            await realtime.unsubscribe_execution(BOND_CODE)
            assert f"H0BJCNT0:{BOND_CODE}" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Unsubscription failed: {e}")


@pytest.mark.asyncio
async def test_receive_execution_data(socket_client_params):
    """Test receiving real-time bond execution data.

    Note: This test may timeout outside market hours when no data is being sent.
    """
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_execution(BOND_CODE)

            data_received = False
            timeout = 30

            async def receive_data():
                nonlocal data_received
                async for event in client.events():
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

    except Exception as e:
        pytest.fail(f"Data reception failed: {e}")


@pytest.mark.asyncio
async def test_subscription_events(socket_client_params):
    """Test that execution subscription events are emitted correctly."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_execution(BOND_CODE)

            subscribed_event_found = False

            async def check_events():
                nonlocal subscribed_event_found
                async for event in client.events():
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

    except Exception as e:
        pytest.fail(f"Subscription event test failed: {e}")


# ===== Orderbook (H0BJASP0) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_orderbook(socket_client_params):
    """Test subscribing to real-time bond orderbook data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_orderbook(BOND_CODE)

            assert f"H0BJASP0:{BOND_CODE}" in client.subscriptions

    except Exception as e:
        pytest.fail(f"Orderbook subscription failed: {e}")


@pytest.mark.asyncio
async def test_unsubscribe_orderbook(socket_client_params):
    """Test unsubscribing from real-time bond orderbook data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_orderbook(BOND_CODE)
            assert f"H0BJASP0:{BOND_CODE}" in client.subscriptions

            await realtime.unsubscribe_orderbook(BOND_CODE)
            assert f"H0BJASP0:{BOND_CODE}" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Orderbook unsubscription failed: {e}")


@pytest.mark.asyncio
async def test_receive_orderbook_data(socket_client_params):
    """Test receiving real-time bond orderbook data.

    Note: This test may timeout outside market hours when no data is being sent.
    """
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_orderbook(BOND_CODE)

            data_received = False
            timeout = 30

            async def receive_data():
                nonlocal data_received
                async for event in client.events():
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

    except Exception as e:
        pytest.fail(f"Orderbook data reception failed: {e}")


@pytest.mark.asyncio
async def test_orderbook_subscription_events(socket_client_params):
    """Test that orderbook subscription events are emitted correctly."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_orderbook(BOND_CODE)

            subscribed_event_found = False

            async def check_events():
                nonlocal subscribed_event_found
                async for event in client.events():
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

    except Exception as e:
        pytest.fail(f"Orderbook subscription event test failed: {e}")


# ===== Bond Index Execution (H0BICNT0) Integration Tests =====


@pytest.mark.asyncio
async def test_subscribe_index_execution(socket_client_params):
    """Test subscribing to real-time bond index execution data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_index_execution(BOND_INDEX_CODE)

            assert f"H0BICNT0:{BOND_INDEX_CODE}" in client.subscriptions

    except Exception as e:
        pytest.fail(f"Index execution subscription failed: {e}")


@pytest.mark.asyncio
async def test_unsubscribe_index_execution(socket_client_params):
    """Test unsubscribing from real-time bond index execution data."""
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_index_execution(BOND_INDEX_CODE)
            assert f"H0BICNT0:{BOND_INDEX_CODE}" in client.subscriptions

            await realtime.unsubscribe_index_execution(BOND_INDEX_CODE)
            assert f"H0BICNT0:{BOND_INDEX_CODE}" not in client.subscriptions

    except Exception as e:
        pytest.fail(f"Index execution unsubscription failed: {e}")


@pytest.mark.asyncio
async def test_receive_index_execution_data(socket_client_params):
    """Test receiving real-time bond index execution data.

    Note: This test may timeout outside market hours when no data is being sent.
    """
    try:
        async with SocketClient(**socket_client_params) as client:
            realtime = OnmarketBondRealtimeQuote(client)

            await realtime.subscribe_index_execution(BOND_INDEX_CODE)

            data_received = False
            timeout = 30

            async def receive_data():
                nonlocal data_received
                async for event in client.events():
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

    except Exception as e:
        pytest.fail(f"Index execution data reception failed: {e}")


# ===== Combined Tests =====


@pytest.mark.asyncio
async def test_combined_execution_and_orderbook(socket_client_params):
    """Test subscribing to both execution and orderbook data simultaneously."""
    try:
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

    except Exception as e:
        pytest.fail(f"Combined subscription test failed: {e}")
