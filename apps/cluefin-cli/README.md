# Cluefin CLI

`cluefin-cli`는 한국 금융시장 데이터를 도메인 단위로 조회하는 사용자용 CLI입니다. AI Agent와 자동화에서 안정적으로 소비할 수 있도록 모든 신규 도메인 명령은 `--json` 출력을 지원합니다.

## 설치

```bash
uv sync --all-packages
```

API 조회에는 `.env`에 Kiwoom, KIS, DART 인증 정보를 설정해야 합니다.

```bash
cp apps/cluefin-cli/.env.sample .env
```

## JSON 출력

JSON 모드는 stdout에 banner, progress, Rich table이 섞이지 않는 envelope를 출력합니다.

성공 envelope:

```json
{
  "ok": true,
  "command": "chart",
  "source": "kiwoom",
  "params": {},
  "data": {},
  "warnings": [],
  "meta": {}
}
```

실패 envelope:

```json
{
  "ok": false,
  "command": "chart",
  "error": {
    "type": "ValueError",
    "message": "missing credentials"
  },
  "warnings": [],
  "meta": {}
}
```

## 도메인 명령

### `statements`

재무제표, 재무지표, 배당, 주요주주, XBRL 데이터를 조회합니다.

```bash
cluefin-cli statements 005930 --json
cluefin-cli statements 005930 --source all --year 2024 --report annual --include-xbrl --statement-type BS --json
```

주요 옵션:

- `--source auto|dart|kis|all`
- `--year YYYY`
- `--report annual|q1|half|q3`
- `--include-xbrl`
- `--statement-type BS|IS|CIS|CF|SCE`

### `chart`

Kiwoom 또는 KIS OHLCV를 공통 DTO로 정규화하고, 필요하면 `cluefin-ta` 기반 지표를 포함합니다.

```bash
cluefin-cli chart 005930 --indicators --json
cluefin-cli chart 005930 --source kis --interval daily --days 120 --json
```

주요 옵션:

- `--source auto|kiwoom|kis`
- `--interval daily|minute`
- `--days INTEGER`
- `--volume`
- `--indicators`
- `--render`

### `news`

KIS 시장 공시/뉴스 제목과 DART 공시 검색 결과를 조회합니다.

```bash
cluefin-cli news 005930 --source all --json
cluefin-cli news --query 실적 --days 14 --json
```

주요 옵션:

- `--source auto|kis|dart|all`
- `--days INTEGER`
- `--query TEXT`

### `trading-flow`

Kiwoom/KIS 투자자별 수급 데이터를 공통 DTO로 정규화합니다.

```bash
cluefin-cli trading-flow 005930 --json
cluefin-cli trading-flow 005930 --source all --start-date 20240101 --end-date 20241231 --json
```

주요 옵션:

- `--source auto|kiwoom|kis|all`
- `--start-date YYYYMMDD`
- `--end-date YYYYMMDD`

날짜를 지정하지 않으면 최근 1년을 기본 범위로 사용합니다.

### `market`

시장/업종/랭킹/테마성 데이터를 대표 시나리오 중심으로 조회합니다.

```bash
cluefin-cli market volume --json
cluefin-cli market ranking --json
cluefin-cli market theme --json
cluefin-cli market sector --json
```

공통 옵션:

- `--source auto|kis|kiwoom|all`
- `--limit INTEGER`

기본 source:

- `volume`: KIS
- `ranking`: KIS
- `theme`: Kiwoom
- `sector`: KIS

## Deprecated Commands

기존 명령은 호환성을 위해 아직 등록되어 있지만 deprecation 예정입니다. 신규 자동화와 Agent 연동은 위 도메인 명령을 사용하세요.

```bash
cluefin-cli ta 005930
cluefin-cli fa 005930
cluefin-cli xbrl 005930
```

## 개발 검증

```bash
uv run pytest apps/cluefin-cli/tests -v
uv run ruff format . --check
uv run ruff check .
```
