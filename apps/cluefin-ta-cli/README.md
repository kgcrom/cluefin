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

전체 command를 탐색합니다.

```bash
uv run cluefin-ta-cli list --json
```

### 2. Describe

단일 command의 설명, 입력 schema, required 필드, help payload를 확인합니다.

```bash
uv run cluefin-ta-cli describe ta sma --json
uv run cluefin-ta-cli ta sma --help --json
```

### 3. Command Path

TA command path 규칙은 아래와 같습니다.

- `ta <name>`
- `list`, `describe`는 meta command

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
```

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
