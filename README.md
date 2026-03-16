# Cluefin

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![CI Pipeline](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml/badge.svg)](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/kgcrom/cluefin)](LICENSE)

한국 금융 투자 분석 툴킷. 키움/KIS/DART API 클라이언트, 기술적 분석, ML 예측을 제공합니다.

> 이 프로젝트는 교육 및 연구 목적으로만 제공됩니다. 금융 자문을 구성하지 않으며 어떤 결과도 보장하지 않습니다.

## 빠른 시작

```bash
brew install lightgbm          # macOS 시스템 의존성
git clone https://github.com/kgcrom/cluefin.git && cd cluefin
uv sync --all-packages
cp apps/cluefin-cli/.env.sample .env  # API 키 설정
```

**사전 요구사항**: [uv](https://github.com/astral-sh/uv), Python 3.10+

## 프로젝트 구조

uv 워크스페이스 모노레포:

| 패키지 | 설명 |
|--------|------|
| [cluefin-openapi](packages/cluefin-openapi/) | 키움/KIS/DART Python API 클라이언트 (Pydantic, 속도 제한, 인증) |
| [cluefin-openapi-ts](packages/cluefin-openapi-ts/) | KIS/키움 TypeScript API 클라이언트 (Node 20+, Zod, ESM/CJS) |
| [cluefin-ta](packages/cluefin-ta/) | 순수 Python 기술적 분석 (TA-Lib 호환, 150+ 지표) |
| [cluefin-xbrl](packages/cluefin-xbrl/) | DART XBRL 재무제표 파서 |
| [cluefin-cli](apps/cluefin-cli/) | Rich 기반 CLI (기술적 분석, LightGBM + SHAP 예측) |
| [cluefin-desk](apps/cluefin-desk/) | TUI 대시보드 |
| [cluefin-rpc](apps/cluefin-rpc/) | RPC 서버 |

## 개발

```bash
uv run lefthook install                        # Git hooks 설정 (최초 1회)
uv run pytest -m "not integration"             # 단위 테스트
uv run pytest -m integration                   # 통합 테스트 (API 키 필요)
uv run ruff format . && uv run ruff check . --fix  # 린트
```

### TypeScript (cluefin-openapi-ts)

```bash
cd packages/cluefin-openapi-ts
npm install && npm run build
npm run check && npm run test:unit
```

### Git Hooks (Lefthook)

| Hook | 대상 | 실행 내용 |
|------|------|-----------|
| pre-commit | `*.py` | ruff format + check |
| pre-commit | `*.{ts,tsx,js}` | biome check |
| pre-push | `*.py` | pytest (단위 테스트) |
| pre-push | `*.{ts,tsx,js}` | vitest (단위 테스트) |

### npm 배포 (cluefin-openapi-ts)

```bash
cd packages/cluefin-openapi-ts
npm version patch
npm run publish:check && npm pack --dry-run
npm publish --access public
```

## 라이선스

[MIT](LICENSE)
