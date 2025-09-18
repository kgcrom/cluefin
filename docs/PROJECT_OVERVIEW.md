# Project Overview

## ⚠️ Disclaimer

```
이 프로젝트는 교육 및 연구 목적으로만 제공됩니다.
실제 거래나 투자 사용을 위한 것이 아니며, 금융 자문을 구성하거나 어떤 결과를 보장하지 않습니다.
작성자와 기여자는 이 소프트웨어를 기반으로 한 금융 손실이나 결정에 대해 책임을 지지 않습니다.
투자 결정을 하기 전에 항상 자격을 갖춘 금융 고문과 상담하십시오. 과거 성과는 미래 결과를 나타내지 않습니다.

Cluefin을 사용함으로써 귀하는 자신의 책임 하에 학습이나 실험 목적으로만 사용할 것임을 인정하고 동의합니다.
```

## About Cluefin

> **"Clearly Looking U Entered Financial Information"**  
> 당신의 금융 투자 도우미 - Your Financial Investment Assistant

Cluefin은 한국 금융 투자 툴킷으로 **uv workspace monorepo**로 구성된 프로젝트입니다. 개인 투자자들에게 전문가급 분석 도구를 제공하여 더 스마트한 투자 결정을 돕습니다.

**주요 제공 서비스:**
- 키움증권 API 클라이언트
- 한국거래소(KRX) API 클라이언트  
- 한국 주식시장 분석을 위한 CLI 도구
- ML 기반 주식 예측 및 AI 분석

**현재 개발 상태**: Production Ready - ML 예측, 대화형 조회 시스템, AI 인사이트 모든 기능 구현 완료

## 🚀 Quick Start

```bash
# Setup
uv venv --python 3.10
source .venv/bin/activate  
uv sync --all-packages

# Interactive stock analysis
cluefin-cli inquiry

# Quick analysis with AI insights
cluefin-cli analyze 005930 --ai-analysis

# ML prediction with SHAP explanations
cluefin-cli analyze 035720 --ml-predict --shap-analysis

# Run tests
uv run pytest -m "not integration"  # Unit tests only
uv run pytest -m "integration"      # Integration tests (requires API keys)

# Code quality
uv run ruff check . --fix
```

## ✨ Key Features

### 🔥 Core Capabilities
- **대화형 CLI**: 메뉴 기반 주식 조회 시스템을 갖춘 Rich 터미널 인터페이스
- **Type-Safe API 클라이언트**: 한국 금융 서비스를 위한 완전한 OpenAPI 클라이언트 (rate limiting, 캐싱, 강력한 오류 처리)
- **기술적 분석**: TA-Lib 통합을 통한 150+ 지표 (RSI, MACD, 볼린저 밴드 등)
- **AI 기반 인사이트**: GPT-4를 활용한 시장 분석 및 자연어 설명
- **ML 예측**: LightGBM과 SHAP 설명 기능을 갖춘 주식 움직임 예측 (TimeSeriesSplit을 이용한 시계열 검증)

### 📊 Supported Data Sources
- **키움증권**: 실시간 시세, 계좌 관리, 주문 실행 (OAuth2-style 인증, 내장 rate limiting 및 캐싱)
- **한국거래소(KRX)**: 시장 데이터, 지수, 섹터 정보 (simple auth_key 인증, 선택사항)
- **OpenAI**: AI 기반 시장 인사이트 및 자연어 설명
- **기술적 지표**: 150+ 기술적 지표를 포함한 포괄적인 TA-Lib 통합 (RSI, MACD, 볼린저 밴드, 모멘텀, 변동성 지표 등)

## 🎯 Vision & Goals

### Primary Problems We Solve

1. **정보 파편화**: 여러 플랫폼에 흩어진 금융 데이터 통합
2. **기술적 장벽**: 복잡한 한국 금융 API를 직관적인 CLI 명령어로 단순화
3. **분석 과부하**: AI 기반 인사이트와 객관적인 투자 분석 제공
4. **시간 비효율성**: 분석 시간을 30-60분에서 5분 미만으로 단축

### Target Users

- **개인 투자자**: 포괄적인 시장 분석을 원하는 투자자
- **Python 개발자**: 금융 애플리케이션을 구축하는 개발자
- **연구자**: 한국 금융 시장을 연구하는 학술 연구자
- **알고리즘 트레이더**: 트레이딩 알고리즘 개발자

## 🏗️ Project Philosophy

### Design Principles
1. **Type Safety First**: 한국어 필드 별칭을 가진 광범위한 Pydantic 모델
2. **Developer Experience**: Beautiful Rich UI를 가진 직관적인 CLI
3. **Financial Domain Focus**: 한국 시장 시간대 및 거래 시간 인식
4. **Open Source**: 전문가급 금융 도구에 대한 접근 민주화

### Korean Market Specialization
- **시장 시간대**: 한국 표준시(KST)
- **거래 시간**: ML 모델에서 9:00-15:30 KST 고려
- **한국어 필드 별칭**: `cont_yn: Literal["Y", "N"] = Field(..., alias="cont-yn")`
- **실제 한국 주식 코드 사용**: 삼성전자 "005930" 등 실제 종목코드로 목 데이터 생성

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
uv sync --all-packages

# Install TA-Lib (for technical analysis)
# macOS
brew install ta-lib lightgbm
```

### Environment Setup
```bash
# Copy sample env file to workspace root
cp apps/cluefin-cli/.env.sample .env

# Edit with your API keys
# KIWOOM_APP_KEY=your_app_key
# KIWOOM_SECRET_KEY=your_secret_key  
# KIWOOM_ENV=prod # options: prod | dev(default)
# OPENAI_API_KEY=your_openai_api_key
# KRX_AUTH_KEY=your_krx_auth_key  # Optional for KRX data
```

---

> _"더 스마트하게 투자하세요, 더 어렵게 하지 말고 Cluefin과 함께."_  
> _"Invest smarter, not harder, with Cluefin."_
