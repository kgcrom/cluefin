# Cluefin CLI

기술적 지표, 터미널 차트 및 **머신러닝 기반 가격 예측**을 제공하는 한국 주식 시장 분석용 강력한 명령줄 인터페이스입니다.

![CLI Demo](https://img.shields.io/badge/CLI-Korean%20Stock%20Analysis-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![ML](https://img.shields.io/badge/ML-LightGBM%20%2B%20SHAP-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 주요 기능

### **포괄적 주식 분석**
- 실시간 한국 주식 데이터 분석 (KOSPI, KOSDAQ)
- 외국인 거래량 분석 (매수/매도 흐름)
- 시장 지수 모니터링 (KOSPI, KOSDAQ)
- 다중 기간 분석 (1개월, 3개월, 6개월, 1년)
- DART 공시 기반 펀더멘털 데이터 (배당, 재무지표, 주요 주주)

### **기술적 지표**
- **RSI (상대강도지수)** - 과매수/과매도 상황을 위한 모멘텀 오실레이터
- **MACD (이동평균수렴확산)** - 추세 추종 모멘텀 지표
- **이동평균선** - SMA(5, 20, 50) 및 EMA(12, 26)
- **볼린저 밴드** - 변동성 및 추세 분석
- **스토캐스틱 오실레이터** - 종가와 가격대를 비교하는 모멘텀 지표
- **지지/저항 레벨** - 주요 가격대 식별

### **터미널 시각화**
- 터미널에서 직접 렌더링되는 아름다운 ASCII 차트
- 이동평균선 오버레이가 포함된 가격 차트
- 거래량 분석 차트
- 과매수/과매도 구간이 포함된 RSI 오실레이터 시각화
- MACD 히스토그램 및 시그널 라인 차트
- 색상으로 구분된 데이터가 포함된 풍부한 형식의 테이블


### **🤖 머신러닝 예측**
- **LightGBM 기반 분류** - 익일 가격 움직임에 대한 이진 예측
- **150개 이상의 기술적 지표** - TA-Lib을 사용한 향상된 피처 엔지니어링
- **SHAP 모델 해석가능성** - 예측을 주도하는 피처 이해
- **피처 중요도 분석** - 가격 움직임에 영향을 미치는 주요 요소 식별
- **시계열 교차검증** - 시계열 데이터를 위한 적절한 검증
- **성능 메트릭** - 정확도, 정밀도, 재현율, F1-score, AUC

## Quick Start

### Prerequisites
- Python 3.10 or higher
- uv package manager
- **TA-Lib system dependency** (for ML features)

### Installation

1. **Clone and setup workspace:**
```bash
git clone https://github.com/kgcrom/cluefin
cd cluefin
uv venv --python 3.10
```

2. **Install system dependencies:**
```bash
# macOS
brew install ta-lib lightgbm
```

3. **Install all workspace dependencies:**
```bash
uv sync --all-packages
```

4. **Configure environment (optional):**
```bash
cp apps/cluefin-cli/.env.sample .env
# Edit .env with your API keys (KIWOOM_APP_KEY, KIWOOM_SECRET_KEY, KIWOOM_ENV, KRX_AUTH_KEY, DART_AUTH_KEY)
```

### Basic Usage

```bash
# Basic stock analysis
cluefin-cli ta 005930

# With terminal charts
cluefin-cli ta 005930 --chart

# 🤖 With ML prediction
cluefin-cli ta 005930 --ml-predict

# 📊 With basic feature importance
cluefin-cli ta 005930 --ml-predict --feature-importance

# 🔍 With detailed SHAP analysis
cluefin-cli ta 005930 --ml-predict --shap-analysis

# 🚀 Full analysis (all features)
cluefin-cli ta 005930 --chart --ml-predict --shap-analysis

# 📘 Fundamental analysis (DART)
cluefin-cli fa 005930

# 📘 Fundamental analysis for 2023 business report with top 3 shareholders
cluefin-cli fa 005930 --year 2023 --report annual --max-shareholders 3
```

## 명령어 참조

### `ta` 명령어

포괄적인 기술적 지표 및 시장 데이터로 한국 주식을 분석합니다.

```bash
cluefin-cli ta [OPTIONS] STOCK_CODE
```

#### 인수
- `STOCK_CODE` - 한국 주식 코드 (예: 삼성전자는 `005930`)

#### 옵션
- `-c, --chart` - 터미널에서 대화형 차트 표시
- `-m, --ml-predict` - ML 기반 가격 예측 포함 🤖
- `-f, --feature-importance` - 기본 피처 중요도 표시 (--ml-predict 필요) 📊
- `-s, --shap-analysis` - 설명이 포함된 상세 SHAP 분석 표시 (--ml-predict 필요) 🔍
- `--help` - 명령어 도움말 표시

#### 예제

```bash
# 삼성전자 기본 분석
cluefin-cli ta 005930

# SK하이닉스 차트 포함
cluefin-cli ta 000660 --chart

# 삼성전자 ML 예측 포함
cluefin-cli ta 005930 --ml-predict

# LG화학 ML + 기본 피처 중요도
cluefin-cli ta 051910 --ml-predict --feature-importance

# 삼성바이오로직스 ML + 상세 SHAP 분석
cluefin-cli ta 207940 --ml-predict --shap-analysis

# LG에너지솔루션 - 전체 분석
cluefin-cli ta 373220 --chart --ml-predict --shap-analysis
```

### `fa` 명령어

DART 공시 데이터를 기반으로 기업의 펀더멘털 정보를 조회합니다.

```bash
cluefin-cli fa [OPTIONS] STOCK_CODE
```

#### 인수
- `STOCK_CODE` - 한국 주식 코드 (예: 삼성전자는 `005930`)

#### 옵션
- `--year` - 조회할 사업연도 (기본값: 전년도)
- `--report` - 공시 보고서 구분 (`annual`, `q1`, `half`, `q3`)
- `--max-shareholders` - 출력할 주요 주주 수 (기본값: 5)
- `--help` - 명령어 도움말 표시

#### 예제

```bash
# 2023 사업보고서를 기준으로 삼성전자 기본적 분석
cluefin-cli fa 005930 --year 2023 --report annual

# 상위 3명의 주요 주주만 확인
cluefin-cli fa 005930 --max-shareholders 3
```

## 📈 Supported Stocks

CLI는 KOSPI와 KOSDAQ에서 거래되는 모든 한국 주식을 지원합니다. 다음은 인기 종목 예시입니다:

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

Create a `.env` file in the **workspace root** directory:

```env
# Kiwoom Securities API (for real-time Korean stock data)
KIWOOM_APP_KEY=your_app_key_here
KIWOOM_SECRET_KEY=your_secret_key_here
KIWOOM_ENV=prod # options: prod | dev(default)

# Korea Exchange (KRX) API
KRX_AUTH_KEY=your_auth_key_here

# Financial Supervisory Service DART API
DART_AUTH_KEY=your_dart_auth_key_here

# Optional ML model configuration
ML_MODEL_PATH=models/
ML_CACHE_DIR=.ml_cache/
```

### API Integration

The CLI integrates with Korean financial APIs through the `cluefin-openapi` package:

1. **Kiwoom Securities API**: OAuth2-style authentication for real-time stock data, orders, and account information
1. **Korea Exchange (KRX)**: Simple auth_key authentication for market data, indices, and sector information  
1. **Financial Supervisory Service (DART)**: Fundamental disclosures, periodic reports, dividends, and shareholder data

**Note**: The CLI can work with limited functionality without API keys, using mock data for demonstration purposes.

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
├── src/cluefin_cli/              # Main application code
│   ├── commands/                 # CLI command implementations
│   │   ├── analysis/             # Technical analysis module
│   │   │   └── indicators.py     # Technical indicators computation
│   │   ├── technical_analysis.py # Main TA command (Click-based)
│   │   ├── fundamental_analysis.py # Fundamental analysis command
│   │   └── import_cmd.py         # Data import command
│   ├── config/                   # Application configuration
│   │   └── settings.py           # Pydantic settings management
│   ├── data/                     # Data layer abstraction
│   │   ├── duckdb_manager.py     # DuckDB database management
│   │   ├── fetcher.py            # Data retrieval from cluefin-openapi
│   │   ├── importer.py           # Stock chart data importer
│   │   ├── industry_importer.py  # Industry code importer
│   │   └── industry_chart_importer.py # Industry chart data importer
│   ├── display/                  # Terminal visualization
│   │   └── charts.py             # ASCII chart rendering (plotext)
│   ├── ml/                       # 🤖 Machine Learning pipeline
│   │   ├── diagnostics.py        # Model performance evaluation
│   │   ├── explainer.py          # SHAP-based model explainability
│   │   ├── feature_engineering.py  # TA-Lib feature generation (150+ indicators)
│   │   ├── models.py             # LightGBM classifier implementation
│   │   └── predictor.py          # Complete ML prediction pipeline
│   ├── utils/                    # Shared utilities
│   │   └── formatters.py         # Korean currency and text formatting
│   └── main.py                   # CLI entry point and Click app
├── tests/unit/                   # Unit test suite
│   ├── commands/                 # Command tests
│   └── ml/                       # ML pipeline and model tests
├── pyproject.toml               # Package dependencies and configuration
└── README.md                    # This documentation
```

### Adding New Features

1. **New Technical Indicators**: Add to `src/cluefin_cli/commands/analysis/indicators.py` or `src/cluefin_cli/ml/feature_engineering.py`
2. **Chart Types**: Extend `src/cluefin_cli/display/charts.py`
3. **Data Sources**: Modify `src/cluefin_cli/data/fetcher.py`
4. **CLI Commands**: Add new commands to `src/cluefin_cli/commands/`
5. **ML Models**: Extend `src/cluefin_cli/ml/models.py` or add new model classes
6. **SHAP Visualizations**: Enhance `src/cluefin_cli/ml/explainer.py`
7. **Utility Functions**: Add to `src/cluefin_cli/utils/formatters.py`

### Running Tests

```bash
# From workspace root directory
cd cluefin

# Run all CLI tests 
uv run pytest apps/cluefin-cli/tests/ -v

# Run unit tests only (excludes integration tests)
uv run pytest -m "not integration"

# Run specific test module
uv run pytest apps/cluefin-cli/tests/unit/ml/test_ml_pipeline.py -v

# Code quality checks
uv run ruff check . --fix
uv run ruff format .

# Test ML pipeline with real example
cluefin-cli ta 005930 --ml-predict --shap-analysis
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
