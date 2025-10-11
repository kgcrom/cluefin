# Cluefin

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![CI Pipeline](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml/badge.svg)](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/kgcrom/cluefin)](LICENSE)

**Cluefin: 당신의 금융 투자 도우미.**

> "clue"의 또 다른 의미는 "Clearly Looking for U Entered"입니다.
> 투자자가 금융 의사결정을 분석, 자동화, 최적화할 수 있도록 돕는 파이썬 툴킷입니다.
> _"더 스마트하게 투자하세요, 어렵게 하지 말고 Cluefin과 함께."_

## ⚠️ Disclaimer

```
이 프로젝트는 교육 및 연구 목적으로만 제공됩니다.
실제 거래나 투자 사용을 위한 것이 아니며, 금융 자문을 구성하거나 어떤 결과를 보장하지 않습니다.
작성자와 기여자는 이 소프트웨어를 기반으로 한 금융 손실이나 결정에 대해 책임을 지지 않습니다.
투자 결정을 하기 전에 항상 자격을 갖춘 금융 고문과 상담하십시오. 과거 성과는 미래 결과를 나타내지 않습니다.

Cluefin을 사용함으로써 귀하는 자신의 책임 하에 학습이나 실험 목적으로만 사용할 것임을 인정하고 동의합니다.
```

---

## 🚀 Quick Start

```bash
# Install system dependencies (macOS)
brew install ta-lib lightgbm

# Clone and setup
git clone https://github.com/kgcrom/cluefin.git
cd cluefin
uv venv --python 3.10
source .venv/bin/activate

# Install all workspace dependencies
uv sync --all-packages

# Configure environment
cp apps/cluefin-cli/.env.sample .env
# Edit .env with your API keys (KIWOOM_APP_KEY, KIWOOM_SECRET_KEY, KIWOOM_ENV, KIS_APP_KEY, KIS_SECRET_KEY, KIS_ENV, KRX_AUTH_KEY, DART_AUTH_KEY, OPENAI_API_KEY)

# Advanced analysis with ML prediction
cluefin-cli ta 005930 --chart --ai-analysis --ml-predict --shap-analysis

# Run tests and code quality checks
uv run pytest -m "not integration"  # Unit tests only
uv run ruff check . --fix
```

## ✨ 주요 기능

### 🔥 핵심 기능
- **대화형 CLI**: Rich 기반 터미널 인터페이스로 핵심 분석 기능 제공
- **한국 금융 API**: 키움증권, 한국투자증권(KIS), 한국거래소(KRX), DART를 위한 타입 안전한 클라이언트
- **ML 기반 예측**: 주식 움직임 예측을 위한 SHAP 설명 기능을 갖춘 LightGBM 모델
- **기술적 분석**: TA-Lib 통합을 통한 20+ 지표 (RSI, MACD, 볼린저 밴드 등)
- **AI 인사이트**: 시장 분석 및 자연어 설명을 위한 GPT-4 통합

### 📊 데이터 소스
- **키움증권**: 실시간 시세, 계좌 관리, 주문 실행
- **한국투자증권(KIS)**: 국내/해외 주식 시세, 계좌 조회, 시장 분석
- **한국거래소(KRX)**: 시장 데이터, 지수, 섹터 정보
- **DART**: 기업 공시, 재무제표, 대량보유상황
- **기술적 지표**: 포괄적인 TA-Lib 통합
- **AI 분석**: OpenAI 기반 시장 인사이트 및 설명

## 📖 Cluefin을 선택하는 이유?
Cluefin은 모든 사람들에게 금융 투자, 포트폴리오 관리를 단순화하고 도와주는 역할을합니다.

초보자든 전문가든 시장을 분석하고 거래를 자동화하며 포트폴리오를 효율적으로 관리할 수 있는 도구를 제공합니다.

## 🏁 Getting Started

### Prerequisites
- [uv](https://github.com/astral-sh/uv) package manager

### Project Layout
This project uses a **uv workspace monorepo** structure:
```
cluefin/
├── packages/cluefin-openapi/    # Korean financial API clients
│   ├── src/cluefin_openapi/
│   │   ├── kiwoom/             # Kiwoom Securities API client
│   │   ├── kis/                # Korea Investment & Securities API client
│   │   ├── krx/                # Korea Exchange API client
│   │   └── dart/               # DART corporate disclosure API client
│   └── tests/                  # Unit and integration tests
├── apps/cluefin-cli/           # Interactive CLI application with ML predictions
└── docs/                       # Architecture and technical documentation
```

## 🔧 Development

### Testing
```bash
# Run all tests
uv run pytest

# Run unit tests only (excludes integration tests)
uv run pytest -m "not integration"

# Run integration tests only (requires API keys)
uv run pytest -m "integration"

# Run specific package tests
uv run pytest packages/cluefin-openapi/tests/ -v
uv run pytest apps/cluefin-cli/tests/ -v

# Code quality
uv run ruff check . --fix
uv run ruff format .
```

### Component Overview

**[cluefin-openapi](packages/cluefin-openapi/)** - Korean Financial API Clients
- **Type-safe Pydantic models** for Kiwoom, KIS, KRX, and DART APIs with Korean field aliases
- **Structured response handling** with `KiwoomHttpResponse[T]` wrapper pattern
- **Multiple authentication methods**: OAuth2-style (Kiwoom), token-based (KIS), simple auth_key (KRX, DART)
- **Rate limiting and error handling** optimized for Korean market APIs
- **Test coverage** with unit tests using `requests_mock` and integration tests

**[cluefin-cli](apps/cluefin-cli/)** - Interactive Terminal Application  
- **Rich-based UI** with Korean stock market analysis and menu navigation
- **ML-powered predictions** using LightGBM with SHAP explanations for interpretability
- **Technical analysis** with 150+ TA-Lib indicators (RSI, MACD, Bollinger Bands)
- **AI-powered insights** via OpenAI integration for market analysis
- **Korean timezone handling** (KST) and trading hours (9:00-15:30) awareness

## 📄 라이선스
이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

---

> _"더 스마트하게 투자하세요, 더 어렵게 하지 말고 Cluefin과 함께."_
