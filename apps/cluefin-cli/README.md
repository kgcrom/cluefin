# Cluefin CLI

A powerful command-line interface for Korean stock market analysis with technical indicators, terminal charts, AI-powered insights, and **machine learning-based price prediction**.

![CLI Demo](https://img.shields.io/badge/CLI-Korean%20Stock%20Analysis-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![ML](https://img.shields.io/badge/ML-LightGBM%20%2B%20SHAP-orange)
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

### **🤖 Machine Learning Prediction**
- **LightGBM-based Classification** - Binary prediction for next-day price movement
- **150+ Technical Indicators** - Enhanced feature engineering using TA-Lib
- **SHAP Model Explainability** - Understand which features drive predictions
- **Feature Importance Analysis** - Identify key factors affecting price movements
- **Time Series Cross-Validation** - Proper validation for temporal data
- **Performance Metrics** - Accuracy, precision, recall, F1-score, and AUC

## Quick Start

### Prerequisites
- Python 3.10 or higher
- uv package manager
- **TA-Lib system dependency** (for ML features)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd apps/cluefin-cli
   ```

2. **Install TA-Lib system dependency:**
   ```bash
   # macOS
   brew install ta-lib
   
   # Ubuntu/Debian
   sudo apt-get install libta-lib0-dev
   
   # Windows
   # Download from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
   ```

3. **Install Python dependencies:**
   ```bash
   uv sync --dev
   ```

4. **Configure environment (optional):**
   ```bash
   cp .env.sample .env
   # Edit .env with your API keys
   ```

### Basic Usage

```bash
# Basic stock analysis
cluefin-cli analyze 005930

# With terminal charts
cluefin-cli analyze 005930 --chart

# With AI-powered analysis
cluefin-cli analyze 005930 --ai-analysis

# 🤖 With ML prediction
cluefin-cli analyze 005930 --ml-predict

# 📊 With basic feature importance
cluefin-cli analyze 005930 --ml-predict --feature-importance

# 🔍 With detailed SHAP analysis
cluefin-cli analyze 005930 --ml-predict --shap-analysis

# 🚀 Full analysis (all features)
cluefin-cli analyze 005930 --chart --ai-analysis --ml-predict --shap-analysis
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
- `-c, --chart` - Display interactive charts in terminal
- `-a, --ai-analysis` - Include AI-powered market analysis (requires OpenAI API key)
- `-m, --ml-predict` - Include ML-based price prediction 🤖
- `-f, --feature-importance` - Display basic feature importance (requires --ml-predict) 📊
- `-s, --shap-analysis` - Display detailed SHAP analysis with explanations (requires --ml-predict) 🔍
- `--help` - Show command help

#### Examples

```bash
# Samsung Electronics basic analysis
cluefin-cli analyze 005930

# SK Hynix with charts
cluefin-cli analyze 000660 --chart

# NAVER with AI insights
cluefin-cli analyze 035420 --chart --ai-analysis

# Samsung with ML prediction
cluefin-cli analyze 005930 --ml-predict

# LG Chem with ML + basic feature importance
cluefin-cli analyze 051910 --ml-predict --feature-importance

# Samsung Biologics with ML + detailed SHAP analysis
cluefin-cli analyze 207940 --ml-predict --shap-analysis

# LG Energy Solution - full analysis
cluefin-cli analyze 373220 --chart --ai-analysis --ml-predict --shap-analysis
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

# ML Features (no additional configuration required)
# - LightGBM: Works out of the box
# - SHAP: Auto-configured with TreeExplainer
# - TA-Lib: Requires system dependency (see Installation)
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

### 🤖 ML Prediction Output

```
==================================================
🎯 ML Prediction Results
┌─────────────────────────────────────────────────┐
│ Signal: 📈 BUY (67.3%)                         │
│ Confidence: 67.3%                              │
│ Up Probability: 67.3%                          │
│ Down Probability: 32.7%                        │
└─────────────────────────────────────────────────┘

📊 Model Performance
┌─────────────────────────────────────────────────┐
│ Validation Accuracy: 64.2%                     │
│ Validation F1-Score: 0.638                     │
│ Validation AUC: 0.721                          │
└─────────────────────────────────────────────────┘
```

### 🔍 SHAP Analysis Output

```
🔍 Top 15 Feature Importance (SHAP)
┌──────┬─────────────────────┬────────────┬────────────┬────────────┐
│ Rank │ Feature             │ Importance │ Mean SHAP  │ Impact     │
├──────┼─────────────────────┼────────────┼────────────┼────────────┤
│  1   │ rsi_14             │   0.0234   │  +0.0156   │ 📈 UP     │
│  2   │ macd_signal        │   0.0198   │  -0.0087   │ 📉 DOWN   │
│  3   │ bb_position        │   0.0167   │  +0.0123   │ 📈 UP     │
│  4   │ volume_ratio       │   0.0142   │  +0.0089   │ 📈 UP     │
│  5   │ sma_20             │   0.0134   │  -0.0067   │ 📉 DOWN   │
└──────┴─────────────────────┴────────────┴────────────┴────────────┘
```

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
|       |-- ml/                # 🤖 ML prediction module
|           |-- feature_engineering.py  # TA-Lib + custom features
|           |-- models.py              # LightGBM predictor
|           |-- explainer.py           # SHAP analysis
|           |-- predictor.py           # ML pipeline
|-- main.py                    # CLI entry point
|-- pyproject.toml            # Dependencies (includes ML libs)
|-- README.md                 # This file
```

### Adding New Features

1. **New Technical Indicators**: Add to `src/cluefin_cli/analysis/indicators.py` or `src/cluefin_cli/ml/feature_engineering.py`
2. **Chart Types**: Extend `src/cluefin_cli/display/charts.py`
3. **Data Sources**: Modify `src/cluefin_cli/data/fetcher.py`
4. **CLI Commands**: Add to `src/cluefin_cli/commands/`
5. **ML Models**: Extend `src/cluefin_cli/ml/models.py` or add new model classes
6. **SHAP Visualizations**: Enhance `src/cluefin_cli/ml/explainer.py`

### Running Tests
```bash
# Run linting
uv run ruff check . --fix

# Format code
uv run ruff format .

# Test ML pipeline (requires sample data)
cluefin-cli analyze 005930 --ml-predict --shap-analysis
```

### 🤖 ML Model Architecture

The ML prediction system uses a sophisticated pipeline:

1. **Feature Engineering** (150+ features)
   - TA-Lib technical indicators (RSI, MACD, Bollinger Bands, etc.)
   - Custom price-based features (ratios, volatility, momentum)
   - Lag features for temporal patterns
   - Volume-based indicators

2. **Model Training**
   - **LightGBM Classifier** for binary up/down prediction
   - **Time Series Split** to prevent data leakage
   - **Early Stopping** to prevent overfitting
   - **Cross-Validation** with proper temporal ordering

3. **Model Interpretation**
   - **SHAP TreeExplainer** for feature importance
   - **Individual Prediction Explanations** 
   - **Global Feature Rankings**
   - **Directional Impact Analysis** (positive/negative contributions)

### ML Performance Guidelines

- **Accuracy > 60%**: Good predictive performance
- **AUC > 0.7**: Excellent discrimination between up/down movements  
- **F1-Score > 0.6**: Balanced precision and recall
- **Minimum 30 days**: Required historical data for training
- **Recommended 100+ days**: For reliable model performance

**⚠️ Important**: Stock prediction is inherently uncertain. Use ML predictions as one factor among many in investment decisions.

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