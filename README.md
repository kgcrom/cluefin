# Cluefin

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/92b750be06a24d88869fbe83fb4f4cf4)](https://app.codacy.com/gh/kgcrom/cluefin/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![CI Pipeline](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml/badge.svg)](https://github.com/kgcrom/cluefin/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/kgcrom/cluefin)](LICENSE)

한국 주식을 스스로 조사하기 위한 리서치 툴킷입니다.

> 이 프로젝트는 교육 및 연구 목적으로만 제공됩니다. 금융 자문을 구성하지 않으며 어떤 결과도 보장하지 않습니다.

## 왜 만들었나

종목 하나를 제대로 보려면 시세는 증권사 API, 재무와 공시는 DART, 금리와 경기는 한국은행, 미국 고객사·경쟁사는
SEC 에서 따로 받아 맞춰야 합니다. Cluefin 은 이 출처들을 한 클라이언트로 묶고, AI agent 가 그 위에서 데이터를 모아
검증 가능한 판단(기준가·손절가·무효화 조건)을 쓰고, 그 판단을 나중에 실제 가격과 대조할 수 있게 합니다.

## 무엇을 하나

| 구분 | 이름 | 하는 일 |
|------|------|---------|
| 앱 | [cluefin-openapi-cli](apps/cluefin-openapi-cli/) | AI agent 용 JSON CLI. KIS·키움·DART·SEC·ECOS 호출, 전 종목 로컬 캐시(DuckDB) 스크린, 종목 검토 데이터 수집·판단 기록·추적(`review`) |
| 앱 | [cluefin-desk](apps/cluefin-desk/) | 사람이 보는 TUI 대시보드. 시장 개요·순위·테마·ETF·수급·관심종목, 종목 상세(차트·재무·공시), LightGBM + SHAP 다음 날 예측 |
| 라이브러리 | [cluefin-openapi](packages/cluefin-openapi/) | KIS·키움·NH PLUG·DART·SEC EDGAR·ECOS Python 클라이언트 (Pydantic, 속도 제한, 토큰 캐시, 웹소켓) |
| 라이브러리 | [cluefin-openapi-ts](packages/cluefin-openapi-ts/) | KIS·키움·NH PLUG·DART·ECOS TypeScript 클라이언트 (Node 20+, Zod, ESM/CJS, npm 배포) |
| 라이브러리 | [cluefin-ta](packages/cluefin-ta/) | 순수 Python 기술적 분석 (TA-Lib 호환, 42개 함수, 레짐 판정) |
| 라이브러리 | [cluefin-xbrl](packages/cluefin-xbrl/) | DART XBRL 재무제표 파서 |
| 라이브러리 | [cluefin-dart-notes](packages/cluefin-dart-notes/) | DART 공시 원문(dart4 XML) 파서 — 섹션·표·주석 노트 (XBRL 에 없는 서술형 내용) |
| 라이브러리 | [cluefin-sec-notes](packages/cluefin-sec-notes/) | SEC EDGAR 원문 파서 — 10-K/10-Q/8-K Item 본문·주석, Form 3·4·5 내부자 신고, 13F 기관 보유 |
| 라이브러리 | [cluefin-feeds](packages/cluefin-feeds/) | API 밖 공개 피드 — 미 재무부 수익률 곡선, BLS 시계열, Damodaran 국가·업종 데이터 |

분석 agent 는 [`.claude/agents/`](.claude/agents/) 에 있습니다. Claude Code 에서 이 저장소를 열면 바로 쓸 수 있습니다.

| agent | 하는 일 |
|-------|---------|
| `market-scan` | 장세를 수치로 읽고 캐시 스크린으로 후보를 뽑아 깊게 볼 종목을 최대 3개 제안 |
| `company-review` | 종목 하나의 데이터를 모아 buy/hold/sell/watch 와 기준가·손절가·무효화 조건을 담은 리포트 작성 |
| `disclosure-watch` | 관심·보유 종목의 최근 공시·희석 이벤트·뉴스를 훑어 다시 볼 종목만 알림 |
| `agent-audit` | 위 agent 실행에서 수집 누락·놓친 판단·중복 호출을 찾아 agent 문서 개선안 제시 |

## 빠른 시작

**사전 요구사항**: [uv](https://github.com/astral-sh/uv), Python 3.11+. macOS 는 LightGBM 이 쓰는 OpenMP 가 필요합니다.

```bash
brew install libomp                               # macOS 만
git clone https://github.com/kgcrom/cluefin.git && cd cluefin
uv sync --all-packages
cp packages/cluefin-openapi/.env.sample .env      # 키 입력. 앱은 실행 위치의 .env 만 읽는다
```

`.env` 에는 쓰는 출처의 키만 넣으면 됩니다(KIS·키움·DART·ECOS·NH PLUG). SEC 는 키 대신
`SEC_USER_AGENT="이름 이메일"` 을 요구하고, ECOS 키가 없으면 공개 sample 키(한 번에 10행)로 돕니다.
`KIS_ENV=prod` 는 실계좌 키라는 점에 주의하세요.

모든 명령은 저장소 루트에서 실행합니다.

```bash
uv run cluefin-openapi-cli brokers --json                       # 어떤 출처의 키가 잡혔는지 (값은 보이지 않음)
uv run cluefin-openapi-cli search 외국인 순매수 --json            # 자연어로 명령 찾기
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --json

uv run cluefin-openapi-cli cache load --json                    # 장 마감 후 전 종목 캐시 적재 (첫 실행은 2시간 이상)
uv run cluefin-openapi-cli cache trend-setup --json             # 캐시로 스크린

uv run cluefin-openapi-cli review collect --stock-code 005930 --json   # 종목 검토 데이터를 폴더 하나에 수집

uv run cluefin-desk                                             # TUI 대시보드
```

명령 전체와 옵션은 [cluefin-openapi-cli README](apps/cluefin-openapi-cli/README.md) 를 보세요. agent 가 기록한
판단과 HTML 리포트는 `research/` 에 쌓이며 git 에 올리지 않습니다.

## 개발

```bash
uv run lefthook install                            # Git hooks 설정 (최초 1회)
uv run pytest -m "not integration and not slow"    # 단위 테스트 (네트워크 없음)
uv run pytest -m integration                       # 통합 테스트 (실제 API 키 사용)
uv run ruff format . && uv run ruff check . --fix  # 린트
uv run pyright                                     # 타입 검사 (pyproject 의 include 목록만)
```

TypeScript 패키지:

```bash
cd packages/cluefin-openapi-ts
npm install && npm run build
npm run check && npm run test:unit
```

### Git Hooks (Lefthook)

| Hook | 대상 | 실행 내용 |
|------|------|-----------|
| pre-commit | `*.py` | ruff format --check + ruff check (자동 수정 없음) |
| pre-commit | `*.{ts,tsx,js}` | biome check |
| pre-push | `*.py` | pytest (integration·slow 제외) |
| pre-push | `*.py`, `pyproject.toml` | pyright |
| pre-push | `*.{ts,tsx,js}` | vitest (단위 테스트) |

### CI·배포

- CI(`ci.yml`, `ci-openapi-ts.yml`)는 main 에 push 될 때 돕니다. 브랜치에서 돌리려면
  `gh workflow run ci.yml --ref <branch>`.
- PyPI(`cluefin-openapi`): GitHub Actions 의 `publish-openapi` 워크플로를 수동 실행합니다.
- npm(`cluefin-openapi-ts`):

  ```bash
  cd packages/cluefin-openapi-ts
  npm version patch
  npm run publish:preview      # build·check·typecheck·test 후 pack --dry-run
  npm publish --access public
  ```

## 라이선스

[MIT](LICENSE)
