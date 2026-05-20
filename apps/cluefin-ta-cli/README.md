# cluefin-ta-cli

`cluefin-ta-cli`는 `cluefin-ta`의 기술적 분석 함수를 agent-friendly CLI로 노출하는 명령줄 인터페이스입니다.

RPC 서버나 broker session 없이 로컬에서 직접 `cluefin-ta` 함수를 실행합니다. 사용 흐름은 `list`로 탐색하고, `describe`로 입력 schema를 확인한 뒤, `ta <name>`으로 실행하는 방식입니다.

## 빠른 시작

워크스페이스 루트에서 실행합니다.

```bash
uv sync --all-packages
uv run cluefin-ta-cli --help --json
```

## 사용 규칙

### 1. Discovery

전체 command 또는 domain/tag별 command를 탐색합니다.

```bash
uv run cluefin-ta-cli list --json
uv run cluefin-ta-cli list --domain technical-indicator --json
uv run cluefin-ta-cli list --tag momentum --json
uv run cluefin-ta-cli domains --json
uv run cluefin-ta-cli tags --json
```

### 2. Describe

단일 command의 설명, 입력 schema, required 필드, domain/tag, examples, agent_notes, help payload를 확인합니다.

```bash
uv run cluefin-ta-cli describe ta sma --json
uv run cluefin-ta-cli ta sma --help --json
```

Agent는 `describe --json`의 `examples[0].command`를 실행 skeleton으로 사용하고, `agent_notes`에서 입력 배열 조건과 warm-up 구간의 `null` 반환 가능성을 확인할 수 있습니다.

### 3. Command Path

TA command path 규칙은 아래와 같습니다.

- `ta <name>`
- `list`, `describe`, `domains`, `tags`는 meta command

예시:

```bash
uv run cluefin-ta-cli ta sma --params-json '{"close":[100,101,102,103]}' --json
uv run cluefin-ta-cli ta macd --params-json '{"close":[100,101,102,103,104,105]}' --json
uv run cluefin-ta-cli ta sharpe --params-json '{"returns":[0.01,-0.02,0.015,0.005]}' --json
```

## 입력 방식

기본 입력은 schema-derived CLI 옵션입니다.

```bash
uv run cluefin-ta-cli ta sharpe --risk-free-rate 0.02 --periods-per-year 252 --params-json '{"returns":[0.01,-0.02,0.015]}' --json
```

배열 입력은 `--params-json`를 사용합니다.

```bash
uv run cluefin-ta-cli ta sma --params-json '{"close":[100,101,102,103,104]}' --timeperiod 3 --json
```

입력 규칙:

- scalar 필드는 개별 옵션으로 전달 가능
- 배열 입력은 `--params-json` 사용
- 같은 필드를 둘 다 주면 개별 옵션이 `--params-json`보다 우선

## 출력 방식

- `--json`이면 항상 JSON 출력
- stdout이 TTY가 아니면 기본 JSON 출력
- help도 JSON으로 조회 가능

예시:

```bash
uv run cluefin-ta-cli --help --json
uv run cluefin-ta-cli ta --help --json
uv run cluefin-ta-cli ta sma --help --json
uv run cluefin-ta-cli domains --json
uv run cluefin-ta-cli tags --json
```

## Agent Workflow

`cluefin-openapi-cli`에서 OHLCV 데이터를 조회한 뒤, 필요한 배열만 추출해 `cluefin-ta-cli`에 전달합니다.

```bash
uv run cluefin-openapi-cli list --domain chart --json
uv run cluefin-ta-cli list --tag moving-average --json
uv run cluefin-ta-cli describe ta rsi --json
uv run cluefin-ta-cli ta rsi --params-json '{"close":[100,101,102,103,104]}' --json
```

`cluefin-cli` 삭제 또는 정리는 별도 후속 작업입니다. Agent integration은 이 CLI의 JSON discovery를 직접 사용할 수 있습니다.

## 지원 명령

초기 버전은 아래 11개 함수만 노출합니다.

- `sma`
- `ema`
- `rsi`
- `macd`
- `bbands`
- `stoch`
- `adx`
- `atr`
- `obv`
- `mdd`
- `sharpe`
