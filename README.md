# Cluefin

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![CI Pipeline](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml/badge.svg)](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/kgcrom/cluefin)](LICENSE)

> **Cluefin: 당신의 금융 투자 도우미.**

## ⚠️ Disclaimer

```
이 프로젝트는 교육 및 연구 목적으로만 제공됩니다.
실제 거래나 투자 사용을 위한 것이 아니며, 금융 자문을 구성하거나 어떤 결과를 보장하지 않습니다.
작성자와 기여자는 이 소프트웨어를 기반으로 한 금융 손실이나 결정에 대해 책임을 지지 않습니다.
투자 결정을 하기 전에 항상 자격을 갖춘 금융 고문과 상담하십시오. 과거 성과는 미래 결과를 나타내지 않습니다.

Cluefin을 사용함으로써 귀하는 자신의 책임 하에 학습이나 실험 목적으로만 사용할 것임을 인정하고 동의합니다.
```

> "clue"의 또 다른 의미는 "Clearly Looking for U Entered"입니다.
> 투자자가 금융 의사결정을 분석, 자동화, 최적화할 수 있도록 돕는 파이썬 툴킷입니다.
> _"더 스마트하게 투자하세요, 어렵게 하지 말고 Cluefin과 함께."_

---

## 🚀 Quick Start

```bash
# Setup
uv sync --dev

# Interactive stock analysis
cluefin-cli inquiry

# Run tests
uv run pytest

# Code quanlity
uv run ruff check . --fix
```

## ✨ 주요 기능

### 🔥 핵심 기능
- **대화형 CLI**: 메뉴 기반 주식 조회 시스템을 갖춘 리치 터미널 인터페이스
- **한국 금융 API**: 키움증권 & 한국거래소(KRX)를 위한 타입 안전한 클라이언트
- **ML 기반 예측**: 주식 움직임 예측을 위한 SHAP 설명 기능을 갖춘 LightGBM 모델
- **기술적 분석**: TA-Lib 통합을 통한 20+ 지표 (RSI, MACD, 볼린저 밴드 등)
- **AI 인사이트**: 시장 분석 및 자연어 설명을 위한 GPT-4 통합

### 📊 데이터 소스
- **키움증권**: 실시간 시세, 계좌 관리, 주문 실행
- **한국거래소(KRX)**: 시장 데이터, 지수, 섹터 정보
- **기술적 지표**: 포괄적인 TA-Lib 통합
- **AI 분석**: OpenAI 기반 시장 인사이트 및 설명

## 📖 Cluefin을 선택하는 이유?
Cluefin은 모든 사람들에게 금융 투자, 포트폴리오 관리를 단순화하고 도와주는 역할을합니다.

초보자든 전문가든 시장을 분석하고 거래를 자동화하며 포트폴리오를 효율적으로 관리할 수 있는 도구를 제공합니다.

## 🏁 Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation
```bash
# Clone repository
git clone https://github.com/kgcrom/cluefin.git
cd cluefin

# Install dependencies
uv sync --dev

# Install TA-Lib (for technical analysis)
# macOS
brew install ta-lib

# Ubuntu/Debian
sudo apt-get install libta-lib0-dev
```

### 환경 설정
```bash
# Copy sample env files
cp packages/cluefin-openapi/.env.sample packages/cluefin-openapi/.env
cp apps/cluefin-cli/.env.sample apps/cluefin-cli/.env

# Edit with you API keys
# KIWOOM_APP_KEY=your_app_key
# KIWOOM_SECRET_KEY=your_secret_key  
# OPENAI_API_KEY=your_openai_api_key
```

### Quick Usage
```bash
# Interactive stock inquiry
cluefin-cli inquiry

# Quick analysis with AI insights
cluefin-cli analyze 005930 --ai-analysis

# ML predict and print shap
cluefin-cli analyze 035720 --ml-predict --shap-analysis 
```

## 🔧 Development

### Local Development Setup
```bash
# Install all dependencies (packages + CLI app)
uv sync --dev

# Run all tests (unit + integration)
uv run pytest

# Run unit tests only
uv run pytest packages/cluefin-openapi/tests/unit/ -v

# Run integration tests (requires API keys)
uv run pytest packages/cluefin-openapi/tests/integration/ -v

# Code quality checks
uv run ruff check . --fix
uv run ruff format .
```

### Project layout
This project uses a **uv workspace monorepo**:
```
cluefin/
├── packages/cluefin-openapi/    # financial Open API clients
├── apps/cluefin-cli/           # Interactive CLI application
└── docs/                       # Comprehensive documentation
```

### CI/CD Pipeline
- **CI Pipeline**: Runs linting, testing, building, and security scans
- **Release Pipeline**: Handles package publishing and deployment
- **Dependency Update**: Automated dependency updates via GitHub Actions

환경 변수 설정은 [docs/ENVIRONMENT_VARIABLES.md](docs/ENVIRONMENT_VARIABLES.md)를 참조하세요.

## 📄 라이선스
이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

---

> _"더 스마트하게 투자하세요, 더 어렵게 하지 말고 Cluefin과 함께."_
