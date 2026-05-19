import json
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from cluefin_cli.domains.models import DisclosureHeadline, FinancialMetric, NewsHeadline, StatementSnapshot
from cluefin_cli.main import cli


@patch("cluefin_cli.commands.statements.StatementsService")
def test_statements_command_json_uses_service(mock_service_cls: MagicMock) -> None:
    service = MagicMock()
    service.fetch.return_value = [
        StatementSnapshot(
            stock_code="005930",
            source="dart",
            company_name="Samsung Electronics",
            accounts=[FinancialMetric(name="Revenue", value="1000")],
        )
    ]
    mock_service_cls.return_value = service

    result = CliRunner().invoke(cli, ["statements", "005930", "--year", "2024", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["ok"] is True
    assert payload["command"] == "statements"
    assert payload["data"]["items"][0]["accounts"][0]["name"] == "Revenue"
    service.fetch.assert_called_once()


@patch("cluefin_cli.commands.statements.StatementsService")
def test_statements_command_json_error_envelope(mock_service_cls: MagicMock) -> None:
    service = MagicMock()
    service.fetch.side_effect = ValueError("missing credentials")
    mock_service_cls.return_value = service

    result = CliRunner().invoke(cli, ["statements", "005930", "--json"])

    assert result.exit_code == 1
    payload = json.loads(result.output)
    assert payload["ok"] is False
    assert payload["error"]["type"] == "ValueError"
    assert payload["error"]["message"] == "missing credentials"


@patch("cluefin_cli.commands.news.NewsService")
def test_news_command_json_uses_service(mock_service_cls: MagicMock) -> None:
    service = MagicMock()
    service.fetch.return_value = {
        "news": [NewsHeadline(source="kis", title="실적 발표", published_at="20260519090000")],
        "disclosures": [DisclosureHeadline(source="dart", report_name="사업보고서", rcept_no="20260519000123")],
    }
    mock_service_cls.return_value = service

    result = CliRunner().invoke(cli, ["news", "005930", "--source", "all", "--query", "실적", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["ok"] is True
    assert payload["command"] == "news"
    assert payload["data"]["news"][0]["title"] == "실적 발표"
    assert payload["data"]["disclosures"][0]["report_name"] == "사업보고서"
    service.fetch.assert_called_once()
