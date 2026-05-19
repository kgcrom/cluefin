"""Static command metadata for AI-friendly CLI discovery."""

from __future__ import annotations

from typing import Any

DOMAIN_COMMANDS: list[dict[str, Any]] = [
    {
        "name": "statements",
        "summary": "Fetch financial statements, metrics, dividends, shareholders, and optional DART XBRL data.",
        "usage": "cluefin-cli statements STOCK_CODE [OPTIONS]",
        "arguments": [
            {
                "name": "stock_code",
                "required": True,
                "description": "Korean stock code, for example 005930.",
            }
        ],
        "options": [
            {
                "name": "--source",
                "type": "choice",
                "choices": ["auto", "dart", "kis", "all"],
                "default": "auto",
                "description": "Data provider selection. auto prefers DART and uses KIS only when explicitly requested.",
            },
            {"name": "--year", "type": "string", "default": "previous_year", "description": "Business year YYYY."},
            {
                "name": "--report",
                "type": "choice",
                "choices": ["annual", "q1", "half", "q3"],
                "default": "annual",
                "description": "DART report period.",
            },
            {
                "name": "--include-xbrl",
                "type": "boolean",
                "default": False,
                "description": "Include DART XBRL statement extraction when available.",
            },
            {
                "name": "--statement-type",
                "type": "choice",
                "choices": ["BS", "IS", "CIS", "CF", "SCE"],
                "default": None,
                "description": "Filter XBRL statement type.",
            },
            {"name": "--json", "type": "boolean", "default": False, "description": "Emit JSON data envelope."},
        ],
        "examples": [
            "cluefin-cli statements 005930 --json",
            "cluefin-cli statements 005930 --source all --year 2024 --report annual --include-xbrl --json",
        ],
        "returns": ["StatementSnapshot"],
    },
    {
        "name": "chart",
        "summary": "Fetch normalized OHLCV chart data and optional cluefin-ta indicators.",
        "usage": "cluefin-cli chart STOCK_CODE [OPTIONS]",
        "arguments": [
            {
                "name": "stock_code",
                "required": True,
                "description": "Korean stock code, for example 005930.",
            }
        ],
        "options": [
            {
                "name": "--source",
                "type": "choice",
                "choices": ["auto", "kiwoom", "kis"],
                "default": "auto",
                "description": "Data provider selection. auto tries Kiwoom and falls back to KIS.",
            },
            {
                "name": "--interval",
                "type": "choice",
                "choices": ["daily", "minute"],
                "default": "daily",
                "description": "Chart interval.",
            },
            {"name": "--days", "type": "integer", "default": 300, "description": "Maximum number of OHLCV points."},
            {
                "name": "--volume",
                "type": "boolean",
                "default": False,
                "description": "Include volume column in table output.",
            },
            {
                "name": "--indicators",
                "type": "boolean",
                "default": False,
                "description": "Calculate SMA, RSI, and MACD indicators.",
            },
            {
                "name": "--render",
                "type": "boolean",
                "default": False,
                "description": "Render terminal chart in non-JSON mode.",
            },
            {"name": "--json", "type": "boolean", "default": False, "description": "Emit JSON data envelope."},
        ],
        "examples": [
            "cluefin-cli chart 005930 --indicators --json",
            "cluefin-cli chart 005930 --source kis --interval daily --days 120 --json",
        ],
        "returns": ["OhlcvSeries"],
    },
    {
        "name": "news",
        "summary": "Fetch KIS market announcement headlines and DART disclosure search results.",
        "usage": "cluefin-cli news [STOCK_CODE] [OPTIONS]",
        "arguments": [
            {
                "name": "stock_code",
                "required": False,
                "description": "Optional Korean stock code, for example 005930.",
            }
        ],
        "options": [
            {
                "name": "--source",
                "type": "choice",
                "choices": ["auto", "kis", "dart", "all"],
                "default": "auto",
                "description": "Data provider selection. auto uses KIS headline data.",
            },
            {"name": "--days", "type": "integer", "default": 7, "description": "Lookback window in days."},
            {"name": "--query", "type": "string", "default": None, "description": "Search text for provider query."},
            {"name": "--json", "type": "boolean", "default": False, "description": "Emit JSON data envelope."},
        ],
        "examples": [
            "cluefin-cli news 005930 --source all --json",
            "cluefin-cli news --query 실적 --days 14 --json",
        ],
        "returns": ["NewsHeadline", "DisclosureHeadline"],
    },
    {
        "name": "trading-flow",
        "summary": "Fetch normalized investor trading flow by stock.",
        "usage": "cluefin-cli trading-flow STOCK_CODE [OPTIONS]",
        "arguments": [
            {
                "name": "stock_code",
                "required": True,
                "description": "Korean stock code, for example 005930.",
            }
        ],
        "options": [
            {
                "name": "--source",
                "type": "choice",
                "choices": ["auto", "kiwoom", "kis", "all"],
                "default": "auto",
                "description": "Data provider selection. auto tries Kiwoom and falls back to KIS.",
            },
            {
                "name": "--start-date",
                "type": "string",
                "default": "one_year_before_end_date",
                "description": "Start date YYYYMMDD.",
            },
            {"name": "--end-date", "type": "string", "default": "today", "description": "End date YYYYMMDD."},
            {"name": "--json", "type": "boolean", "default": False, "description": "Emit JSON data envelope."},
        ],
        "examples": [
            "cluefin-cli trading-flow 005930 --json",
            "cluefin-cli trading-flow 005930 --source all --start-date 20240101 --end-date 20241231 --json",
        ],
        "returns": ["TradingFlowSnapshot"],
    },
    {
        "name": "market",
        "summary": "Fetch market scanner data grouped by representative scenarios.",
        "usage": "cluefin-cli market SUBCOMMAND [OPTIONS]",
        "subcommands": [
            {"name": "volume", "summary": "Trading volume rank.", "default_source": "kis"},
            {"name": "ranking", "summary": "Price fluctuation rank.", "default_source": "kis"},
            {"name": "theme", "summary": "Theme group rank.", "default_source": "kiwoom"},
            {"name": "sector", "summary": "Sector quote/rank data.", "default_source": "kis"},
        ],
        "options": [
            {
                "name": "--source",
                "type": "choice",
                "choices": ["auto", "kis", "kiwoom", "all"],
                "default": "auto",
                "description": "Data provider selection.",
            },
            {"name": "--limit", "type": "integer", "default": 20, "description": "Maximum number of items."},
            {"name": "--json", "type": "boolean", "default": False, "description": "Emit JSON data envelope."},
        ],
        "examples": [
            "cluefin-cli market volume --json",
            "cluefin-cli market ranking --json",
            "cluefin-cli market theme --json",
            "cluefin-cli market sector --json",
        ],
        "returns": ["MarketRankItem"],
    },
]


def describe_commands(command_name: str | None = None) -> list[dict[str, Any]]:
    """Return metadata for all domain commands or one selected command."""
    if command_name is None:
        return DOMAIN_COMMANDS
    return [item for item in DOMAIN_COMMANDS if item["name"] == command_name]
