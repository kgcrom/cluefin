# Cluefin CLI

A powerful command-line interface for Korean stock market analysis with technical indicators, terminal charts, and AI-powered insights.

![CLI Demo](https://img.shields.io/badge/CLI-Korean%20Stock%20Analysis-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ( Features

### **Comprehensive Stock Analysis**
- Real-time Korean stock data analysis (KOSPI, KOSDAQ)
- Foreign trading volume analysis (buy/sell flows)
- Market index monitoring (KOSPI, KOSDAQ)
- Multiple time period analysis (1M, 3M, 6M, 1Y)

### **Technical Indicators**
- **RSI (Relative Strength Index)** - Momentum oscillator for overbought/oversold conditions
- **MACD (Moving Average Convergence Divergence)** - Trend-following momentum indicator
- **Moving Averages** - SMA(5, 20, 50) and EMA(12, 26)
- **Bollinger Bands** - Volatility and trend analysis
- **Stochastic Oscillator** - Momentum indicator comparing closing price to price range
- **Support & Resistance Levels** - Key price levels identification

### **Terminal Visualization**
- Beautiful ASCII charts rendered directly in your terminal
- Price charts with moving average overlays
- Volume analysis charts
- RSI oscillator visualization with overbought/oversold zones
- MACD histogram and signal line charts
- Rich formatted tables with color-coded data

### **AI-Powered Analysis**
- Natural language market analysis using OpenAI GPT-4
- Contextual insights based on technical indicators
- Korean market-specific analysis and terminology
- Risk assessment and trading recommendations

## Quick Start

### Prerequisites
- Python 3.10 or higher
- uv package manager

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd apps/cluefin-cli
   ```

2. **Install dependencies:**
   ```bash
   uv sync --dev
   ```

3. **Configure environment (optional):**
   ```bash
   cp .env.sample .env
   # Edit .env with your API keys
   ```

### Basic Usage

```bash
# Basic stock analysis
uv run python main.py analyze 005930

# With terminal charts
uv run python main.py analyze 005930 --chart

# With AI-powered analysis
uv run python main.py analyze 005930 --ai-analysis

# Different time periods
uv run python main.py analyze 005930 --period 1Y --chart
```

## Command Reference

### `analyze` Command

Analyze Korean stocks with comprehensive technical indicators and market data.

```bash
cluefin-cli analyze [OPTIONS] STOCK_CODE
```

#### Arguments
- `STOCK_CODE` - Korean stock code (e.g., `005930` for Samsung Electronics)

#### Options
- `-p, --period TEXT` - Data period: `1M`, `3M`, `6M`, `1Y` (default: `3M`)
- `-c, --chart` - Display interactive charts in terminal
- `-a, --ai-analysis` - Include AI-powered market analysis (requires OpenAI API key)
- `--help` - Show command help

#### Examples

```bash
# Samsung Electronics basic analysis
cluefin-cli analyze 005930

# SK Hynix with 6-month data and charts
cluefin-cli analyze 000660 --period 6M --chart

# NAVER with full analysis including AI insights
cluefin-cli analyze 035420 --chart --ai-analysis
```

## <� Supported Stocks

The CLI supports all Korean stocks traded on KOSPI and KOSDAQ. Here are some popular examples:

| Stock Code | Company | Market |
|------------|---------|---------|
| `005930` | Samsung Electronics | KOSPI |
| `000660` | SK Hynix | KOSPI |
| `035420` | NAVER | KOSPI |
| `051910` | LG Chemical | KOSPI |
| `207940` | Samsung Biologics | KOSPI |
| `373220` | LG Energy Solution | KOSPI |

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Kiwoom Securities API (for real data)
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_SECRET_KEY=your_secret_key_here

# OpenAI API (for AI analysis)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Environment setting
KIWOOM_ENVIRONMENT=dev
```

### API Integration

Currently, the CLI uses mock data for demonstration. To enable real data:

1. **Kiwoom Securities API**: Sign up for API access and add credentials to `.env`
2. **OpenAI API**: Get an API key from OpenAI for AI-powered analysis

## Output Examples

### Basic Analysis Output

Stock Information - 005930

| Metric        | Value            |
|---------------|------------------|
| Current Price | 64,775          |
| Change        | -1,300 (-1.97%) |
| Volume        | 7,544,353        |
|---------------|------------------|

Technical Indicators

| Indicator | Value    | Signal     |
|-----------|----------|------------|
| RSI (14)  | 57.60    | Neutral    |
| MACD      | 429.71   | Bullish    |
| SMA (20)  | 63,110  | Above MA20 |
|-----------|----------|------------|


### Chart Visualization
The `--chart` option displays beautiful ASCII charts directly in your terminal:
- Price charts with moving averages
- Volume analysis
- RSI oscillator with key levels
- MACD with signal lines and histogram


## Development

### Project Structure
```
apps/cluefin-cli/
|-- src/
|   |-- cluefin_cli/
|       |-- commands/           # CLI commands
|       |-- data/              # Data fetching
|       |-- analysis/          # Technical indicators & AI
|       |-- display/           # Chart rendering
|       |-- config/            # Configuration
|-- main.py                    # CLI entry point
|-- pyproject.toml            # Dependencies
|-- README.md                 # This file
```

### Adding New Features

1. **New Technical Indicators**: Add to `src/cluefin_cli/analysis/indicators.py`
2. **Chart Types**: Extend `src/cluefin_cli/display/charts.py`
3. **Data Sources**: Modify `src/cluefin_cli/data/fetcher.py`
4. **CLI Commands**: Add to `src/cluefin_cli/commands/`

### Running Tests
```bash
# Run linting
uv run ruff check . --fix

# Format code
uv run ruff format .
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## Support

- **Documentation**: Check the main [Cluefin documentation](../../README.md)
- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/your-org/cluefin/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/your-org/cluefin/discussions)

## Related Projects

- **[cluefin-openapi](../../packages/cluefin-openapi/)** - Korean financial API clients

---

** Built with love for Korean financial markets ** 

*"Clearly Looking U Entered Financial Information"*