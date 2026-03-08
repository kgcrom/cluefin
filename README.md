# Cluefin

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![CI Pipeline](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml/badge.svg)](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/kgcrom/cluefin)](LICENSE)

**Cluefin: 당신의 금융 투자 도우미.**

> "clue"의 또 다른 의미는 "Clearly Looking for U Entered"입니다.
> 투자자가 금융 의사결정을 분석, 자동화, 최적화할 수 있도록 돕는 파이썬 툴킷입니다.
> _"더 스마트하게 투자하세요, 어렵게 하지 말고 Cluefin과 함께."_

## ⚠️ 면책 조항

```
이 프로젝트는 교육 및 연구 목적으로만 제공됩니다.
실제 거래나 투자 사용을 위한 것이 아니며, 금융 자문을 구성하거나 어떤 결과를 보장하지 않습니다.
작성자와 기여자는 이 소프트웨어를 기반으로 한 금융 손실이나 결정에 대해 책임을 지지 않습니다.
투자 결정을 하기 전에 항상 자격을 갖춘 금융 고문과 상담하십시오. 과거 성과는 미래 결과를 나타내지 않습니다.

Cluefin을 사용함으로써 귀하는 자신의 책임 하에 학습이나 실험 목적으로만 사용할 것임을 인정하고 동의합니다.
```

---

## 🚀 빠른 시작

```bash
# 시스템 의존성 설치 (macOS)
brew install lightgbm

# 클론 및 설정
git clone https://github.com/kgcrom/cluefin.git
cd cluefin
uv venv --python 3.10

# 모든 워크스페이스 의존성 설치
uv sync --all-packages

# 환경 설정
cp apps/cluefin-cli/.env.sample .env
# .env 파일에 API 키 설정 (KIWOOM_APP_KEY, KIWOOM_SECRET_KEY, KIWOOM_ENV, KIS_APP_KEY, KIS_SECRET_KEY, KIS_ENV, DART_AUTH_KEY)

# ML 예측을 포함한 고급 분석
cluefin-cli ta 005930 --chart --ml-predict --shap-analysis

# 테스트 및 코드 품질 검사
uv run pytest -m "not integration"  # 단위 테스트만
uv run ruff check . --fix
```

## ✨ 주요 기능

### 🔥 핵심 기능
- **대화형 CLI**: Rich 기반 터미널 인터페이스로 핵심 분석 기능 제공
- **한국 금융 API**: 키움증권, 한국투자증권(KIS), DART를 위한 타입 안전한 클라이언트
- **ML 기반 예측**: 주식 움직임 예측을 위한 SHAP 설명 기능을 갖춘 LightGBM 모델
- **기술적 분석**: cluefin-ta를 통한 150+ 지표 (RSI, MACD, 볼린저 밴드 등)

### 📊 데이터 소스
- **키움증권**: 실시간 시세, 계좌 관리, 주문 실행
- **한국투자증권(KIS)**: 국내/해외 주식 시세, 계좌 조회, 시장 분석
- **DART**: 기업 공시, 재무제표, 대량보유상황
- **기술적 지표**: 순수 Python 기반 cluefin-ta 라이브러리 (TA-Lib 호환 API)

## 📖 Cluefin을 선택하는 이유?
Cluefin은 모든 사람들에게 금융 투자, 포트폴리오 관리를 단순화하고 도와주는 역할을 합니다.

초보자든 전문가든 시장을 분석하고 거래를 자동화하며 포트폴리오를 효율적으로 관리할 수 있는 도구를 제공합니다.

## 🏁 시작하기

### 사전 요구사항
- [uv](https://github.com/astral-sh/uv) 패키지 매니저
- Python 3.10 이상

### 프로젝트 구조
이 프로젝트는 **uv 워크스페이스 모노레포** 구조를 사용합니다:
```
cluefin/
├── packages/
│   ├── cluefin-openapi/        # 한국 금융 API 클라이언트
│   ├── cluefin-openapi-ts/     # 한국 금융 API TypeScript 클라이언트 (KIS, Kiwoom)
│   │   ├── src/
│   │   │   ├── core/           # 공통 HTTP/재시도/레이트리밋/검증 유틸
│   │   │   ├── kis/            # 한국투자증권 API 클라이언트
│   │   │   └── kiwoom/         # 키움증권 API 클라이언트
│   │   └── tests/              # 단위/컨트랙트/스모크 테스트
│   └── cluefin-ta/             # 순수 Python 기술적 분석 라이브러리
│       └── src/cluefin_ta/     # TA-Lib 호환 API, 시스템 의존성 없음
├── apps/cluefin-cli/           # ML 예측 기능이 포함된 대화형 CLI 애플리케이션
└── docs/                       # 아키텍처 및 기술 문서
```

## 🔧 개발

### Git Hooks (Lefthook)
[Lefthook](https://github.com/evilmartians/lefthook)으로 커밋/푸시 시 자동으로 린트와 테스트를 실행합니다.

```bash
# 초기 설정 (clone 후 1회)
uv run lefthook install
```

| Hook | 대상 | 실행 내용 |
|------|------|-----------|
| pre-commit | `*.py` | `ruff format --check` + `ruff check` |
| pre-commit | `*.{ts,tsx,js}` | `biome check` |
| pre-push | `*.py` | `pytest -m "not integration"` |
| pre-push | `*.{ts,tsx,js}` | `vitest` unit test |

### 테스트
```bash
# 모든 테스트 실행
uv run pytest

# 단위 테스트만 실행 (통합 테스트 제외)
uv run pytest -m "not integration"

# 통합 테스트만 실행 (API 키 필요)
uv run pytest -m "integration"

# 특정 패키지 테스트 실행
uv run pytest packages/cluefin-openapi/tests/ -v
uv run pytest apps/cluefin-cli/tests/ -v

# 코드 품질 검사
uv run ruff check . --fix
uv run ruff format .
```

### 컴포넌트 개요

**[cluefin-openapi](packages/cluefin-openapi/)** - 한국 금융 API 클라이언트
- **타입 안전한 Pydantic 모델**: 키움, KIS, DART API를 위한 한국어 필드 별칭 지원
- **구조화된 응답 처리**: `KiwoomHttpResponse[T]` 래퍼 패턴으로 통일된 페이지네이션/상태 처리
- **다양한 인증 방식**: OAuth2 스타일(키움), 토큰 기반(KIS), 단순 auth_key(DART)
- **속도 제한 및 에러 처리**: 한국 시장 API에 최적화
- **테스트 커버리지**: `requests_mock`을 사용한 단위 테스트 및 통합 테스트

**[cluefin-openapi-ts](packages/cluefin-openapi-ts/)** - 한국 금융 API TypeScript 클라이언트
- **KIS/키움 1차 지원**: 인증, 공통 HTTP 클라이언트, REST endpoint 래퍼
- **Node + npm 기반 배포**: `Node >=20` 기준으로 ESM/CJS 동시 제공
- **런타임 검증**: Zod 기반 입력/envelope 검증 + camelCase 응답 변환
- **Biome 기반 품질 관리**: 포맷팅/린팅을 단일 도구로 운영
- **v1 구현 범위**: KIS 47개 + 키움 65개, 총 112개 REST 메서드 메타데이터 기반 제공

**[cluefin-ta](packages/cluefin-ta/)** - 순수 Python 기술적 분석 라이브러리
- **TA-Lib 호환 API**: 드롭인 대체 가능 - `import cluefin_ta as talib`
- **시스템 의존성 없음**: 순수 NumPy 구현 (C 라이브러리 불필요)
- **150+ 지표**: 오버랩, 모멘텀, 변동성, 거래량, 캔들스틱 패턴
- **포트폴리오 지표**: MDD, 샤프, 소르티노, 칼마, CAGR 계산

**[cluefin-cli](apps/cluefin-cli/)** - 대화형 터미널 애플리케이션
- **Rich 기반 UI**: 한국 주식 시장 분석 및 메뉴 네비게이션
- **ML 기반 예측**: 해석 가능성을 위한 SHAP 설명 기능이 포함된 LightGBM 사용
- **기술적 분석**: 150+ cluefin-ta 지표 (RSI, MACD, 볼린저 밴드)
- **한국 시간대 처리**: KST 시간대 및 거래 시간(9:00-15:30) 인식

## 📦 cluefin-openapi-ts npm 배포

### 사전 준비
```bash
cd packages/cluefin-openapi-ts
npm whoami           # 로그인 상태 확인 (필요 시 npm login)
```

### 버전 올리기
```bash
# 패치/마이너/메이저 중 선택
npm version patch
```

### 배포 전 검증
```bash
npm run publish:check
npm pack --dry-run
```

### npmjs 배포
```bash
npm publish --access public
```

### 최근 구현 요약 (cluefin-openapi-ts)
- 패키지명: `cluefin-openapi`
- 런타임: Node (`>=20`)
- 포맷/린트: Biome (`@biomejs/biome`)
- 타입 환경: Node 타입 (`@types/node`)
- 테스트/검증: `npm run test`, `npm run check`, `npm run typecheck`, `npm run build`, `npm run publish:check`

## 📄 라이선스
이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

---

> _"더 스마트하게 투자하세요, 더 어렵게 하지 말고 Cluefin과 함께."_
