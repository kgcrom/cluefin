import json
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from cluefin_cli.domains.models import IndicatorSnapshot, OhlcvPoint, OhlcvSeries, TradingFlowSnapshot
from cluefin_cli.main import cli


@patch("cluefin_cli.commands.chart.ChartService")
def test_chart_command_json_uses_service(mock_service_cls: MagicMock) -> None:
    service = MagicMock()
    service.fetch.return_value = OhlcvSeries(
        stock_code="005930",
        source="kiwoom",
        interval="daily",
        points=[OhlcvPoint(timestamp="20250102", open=1, high=2, low=1, close=2, volume=100)],
        indicators=[IndicatorSnapshot(name="sma_20", values=[None], latest=None)],
    )
    mock_service_cls.return_value = service

    result = CliRunner().invoke(cli, ["chart", "005930", "--indicators", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["ok"] is True
    assert payload["command"] == "chart"
    assert payload["source"] == "kiwoom"
    assert payload["data"]["points"][0]["timestamp"] == "20250102"
    assert payload["data"]["indicators"][0]["name"] == "sma_20"
    service.fetch.assert_called_once_with(
        stock_code="005930", source="auto", interval="daily", days=300, indicators=True
    )


@patch("cluefin_cli.commands.trading_flow.TradingFlowService")
def test_trading_flow_command_json_uses_service(mock_service_cls: MagicMock) -> None:
    service = MagicMock()
    service.fetch.return_value = [
        TradingFlowSnapshot(
            stock_code="005930",
            source="kis",
            start_date="20240101",
            end_date="20241231",
            rows=[{"date": "20241231", "foreign": 10.0}],
            totals={"foreign": 10.0},
        )
    ]
    mock_service_cls.return_value = service

    result = CliRunner().invoke(
        cli,
        ["trading-flow", "005930", "--source", "kis", "--start-date", "20240101", "--end-date", "20241231", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["ok"] is True
    assert payload["command"] == "trading-flow"
    assert payload["data"]["items"][0]["rows"][0]["foreign"] == 10.0
    service.fetch.assert_called_once_with(
        stock_code="005930",
        source="kis",
        start_date="20240101",
        end_date="20241231",
    )


@patch("cluefin_cli.commands.trading_flow.TradingFlowService")
def test_trading_flow_command_json_error_envelope(mock_service_cls: MagicMock) -> None:
    service = MagicMock()
    service.fetch.side_effect = RuntimeError("provider failed")
    mock_service_cls.return_value = service

    result = CliRunner().invoke(cli, ["trading-flow", "005930", "--json"])

    assert result.exit_code == 1
    payload = json.loads(result.output)
    assert payload["ok"] is False
    assert payload["error"]["type"] == "RuntimeError"
    assert payload["error"]["message"] == "provider failed"
