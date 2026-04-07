# cluefin-openapi-cli

`cluefin-openapi-cli`는 `cluefin-openapi`의 broker API를 agent-friendly CLI로 노출하는 명령줄 인터페이스입니다.

CLI 내부에 독립 command registry를 가지며, 사용 흐름은 `list`로 탐색하고, `describe`로 입력 schema를 확인한 뒤, broker-first command path로 실행하는 방식입니다.

## 빠른 시작

워크스페이스 루트에서 실행합니다.

```bash
uv sync --all-packages
uv run cluefin-openapi-cli --help --json
```

실제 API 호출 전에는 루트 `.env` 또는 환경변수가 필요합니다.

```env
KIS_APP_KEY=...
KIS_SECRET_KEY=...
KIWOOM_APP_KEY=...
KIWOOM_SECRET_KEY=...
DART_AUTH_KEY=...
```

CLI는 현재 작업 디렉터리의 `.env`를 자동으로 읽습니다. 같은 키가 환경변수에도 있으면 환경변수가 우선합니다.

## 사용 규칙

### 1. Discovery

전체 command 또는 broker/category별 command를 탐색합니다.

```bash
uv run cluefin-openapi-cli list --json
uv run cluefin-openapi-cli list --broker kis --category stock --json
```

### 2. Describe

단일 command의 설명, 입력 schema, required 필드, help payload를 확인합니다.

```bash
uv run cluefin-openapi-cli describe kis stock current-price --json
uv run cluefin-openapi-cli kis stock current-price --help --json
```

### 3. Command Path

broker-first path 규칙은 아래와 같습니다.

- `kis <category> <name>`
- `kiwoom <category> <name>`
- `dart <name>`
- `list`, `describe`는 meta command

예시:

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --json
uv run cluefin-openapi-cli kiwoom chart tick --stock-code KRX:005930 --tic-scope 1 --json
uv run cluefin-openapi-cli dart company-overview --corp-code 00126380 --json
```

## 입력 방식

기본 입력은 schema-derived CLI 옵션입니다.

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --json
```

배열이나 객체 같은 복합 입력은 `--params-json`를 사용합니다.

```bash
uv run cluefin-openapi-cli kis analysis watchlist-multi-quote \
  --params-json '{"stocks":[{"market":"J","stock_code":"005930"},{"market":"J","stock_code":"000660"}]}' \
  --json
```

입력 규칙:

- scalar 필드는 개별 옵션으로 전달 가능
- 복합 입력은 `--params-json` 사용 권장
- 같은 필드를 둘 다 주면 개별 옵션이 `--params-json`보다 우선

## 출력 방식

- `--json`이면 항상 JSON 출력
- stdout이 TTY가 아니면 기본 JSON 출력
- help도 JSON으로 조회 가능

예시:

```bash
uv run cluefin-openapi-cli --help --json
uv run cluefin-openapi-cli kis --help --json
uv run cluefin-openapi-cli kis stock --help --json
uv run cluefin-openapi-cli kis stock current-price --help --json
```

## 예시

KIS:

```bash
uv run cluefin-openapi-cli list --broker kis --category stock --json
uv run cluefin-openapi-cli describe kis stock current-price --json
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --json
```

Kiwoom:

```bash
uv run cluefin-openapi-cli kiwoom chart tick --stock-code KRX:005930 --tic-scope 1 --json
```

DART:

```bash
uv run cluefin-openapi-cli dart company-overview --corp-code 00126380 --json
```

## 동작 원칙

- CLI 내부 registry가 command metadata와 executor set을 직접 관리
- 실제 broker client 생성은 `cluefin_openapi.client_factory`를 사용
- KIS, Kiwoom은 토큰 캐시를 사용하고, DART는 stateless client로 동작

## 주의사항

- 실 API 호출에는 broker credential이 필요합니다
- `.env`가 없거나 값이 비어 있으면 해당 broker command는 실행되지 않습니다
- 일부 command는 복합 입력 때문에 사실상 `--params-json`가 필요합니다
