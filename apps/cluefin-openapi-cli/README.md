# cluefin-openapi-cli

`cluefin-openapi-cli`는 `cluefin-openapi`의 broker API를 **AI agent가 직접 호출하는 용도**로 노출하는 명령줄 인터페이스입니다. 사람이 읽는 화면이 아니라, agent가 JSON을 읽고 다음 명령을 조립하는 것을 전제로 설계했습니다.

- 모든 출력은 JSON입니다. `--json`을 주거나 stdout이 TTY가 아니면 자동으로 JSON입니다.
- 어떤 API를 호출할 수 있는지(`brokers`, `list`), 어떤 parameter를 받는지(`schema`)를 CLI 자체가 JSON으로 알려줍니다. 외부 문서를 미리 읽을 필요가 없습니다.
- 실행 전 `--dry-run`으로 parameter를 로컬 검증하고, 실패는 exit code와 구조화된 `error` JSON으로 돌려줍니다.

## Broker 역할

| broker | role | 용도 |
|---|---|---|
| `kis` | **primary** | 기본 소스. 시세·차트·순위·재무·업종·ETF·일정·휴장일. 모든 작업은 여기서 시작한다. |
| `kiwoom` | **auxiliary** | KIS가 못 보는 빈칸만 채운다. 테마, 업종 구성종목, 틱 차트, 프로그램매매 상세, 거래원(회원사) 수급. |
| `dart` | reference | 공시 원문·기업 고유번호·최대주주. 시세 소스가 아니다. |

Kiwoom command에는 `kis_alternatives` 필드가 있습니다. 비어 있지 않으면 같은 질문을 KIS로 먼저 풀어야 하고, 비어 있으면 그것이 Kiwoom을 쓰는 이유입니다. `brokers --json`의 `kiwoom_only_commands`가 그 목록입니다.

## 빠른 시작

워크스페이스 루트에서 실행합니다.

```bash
uv sync --all-packages
uv run cluefin-openapi-cli --json
```

실제 API 호출 전에는 루트 `.env` 또는 환경변수가 필요합니다. CLI는 현재 작업 디렉터리의 `.env`를 읽고, 같은 키가 환경변수에도 있으면 환경변수가 우선합니다.

```env
KIS_APP_KEY=...
KIS_SECRET_KEY=...
KIWOOM_APP_KEY=...
KIWOOM_SECRET_KEY=...
DART_AUTH_KEY=...
```

어느 broker가 설정돼 있는지는 값을 노출하지 않고 `brokers --json`의 `credentials.configured`로 확인합니다.

## Agent 워크플로

```bash
uv run cluefin-openapi-cli brokers --json                              # 1. 역할·설정 상태·Kiwoom 전용 목록
uv run cluefin-openapi-cli list --broker kis --json                    # 2. 후보 command (brief)
uv run cluefin-openapi-cli schema kis stock current-price --json       # 3. parameter JSON Schema + 호출 예시
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --dry-run --json   # 4. 로컬 검증
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --fields current_price,per --json  # 5. 실행
```

### 1. Discovery

```bash
uv run cluefin-openapi-cli brokers --json
uv run cluefin-openapi-cli list --json
uv run cluefin-openapi-cli list --broker kis --category stock --json
uv run cluefin-openapi-cli list --domain chart --json
uv run cluefin-openapi-cli list --tag ohlcv --json
uv run cluefin-openapi-cli list --query theme --json
uv run cluefin-openapi-cli list --full --json
uv run cluefin-openapi-cli domains --json
uv run cluefin-openapi-cli tags --json
```

`list`는 기본이 **brief**입니다. 한 row에 `qualified_name`, `broker_role`, `description`, `domains`, `tags`, `required`(필수 parameter 이름), `kis_alternatives`만 담아 182개 command 전체가 100KB 이하로 떨어집니다. parameter 전체가 필요하면 `--full`을 주거나, 특정 command만 `schema`로 봅니다. 정렬은 항상 kis → kiwoom → dart 입니다.

`category`는 provider SDK 구조이고, `domain`은 Agent 업무 의도입니다. 예를 들어 `kis chart period`는 category가 `chart`이고 domain도 `chart`지만, 투자자 수급성 API는 provider별 category가 달라도 `trading-flow` domain으로 함께 찾을 수 있습니다.

Agent용 분류 기준:

- `domains`: 업무 영역입니다. 예: `chart`, `statements`, `trading-flow`.
- `tags`: 세부 기능 또는 데이터 특성입니다. 예: `ohlcv`, `dividend`, `program-trading`.
- `recipes`: 여러 command를 조합하는 workflow guide입니다. Recipe는 command 실행기가 아니라 탐색 순서와 조합 의도를 설명합니다.

`domains --json`, `tags --json`는 `name`, `command_count`뿐 아니라 `description`, `when_to_use`, `avoid_when`, `related_domains`, `related_tags`, `example_filter`를 포함합니다. Agent는 `example_filter`를 그대로 다음 탐색 명령으로 사용할 수 있습니다.

예시 taxonomy 응답:

```json
{
  "name": "chart",
  "description": "Price, volume, and OHLCV time-series lookup commands.",
  "when_to_use": "Use before technical analysis, price trend review, or volume analysis.",
  "avoid_when": "Skip when OHLCV arrays are already in hand; compute indicators from them with the cluefin-ta package.",
  "related_tags": ["ohlcv", "daily", "minute", "tick"],
  "example_filter": "uv run cluefin-openapi-cli list --domain chart --json",
  "command_count": 8
}
```

### 2. Schema

`schema`는 한 command의 **호출 계약 전체**를 JSON으로 냅니다. `describe`는 같은 정보를 discovery metadata 중심으로, `schema`는 실행 중심으로 정리한 것입니다.

```bash
uv run cluefin-openapi-cli schema kis stock current-price --json
uv run cluefin-openapi-cli describe kis stock current-price --json
uv run cluefin-openapi-cli kis stock current-price --help --json
```

`schema` 응답 필드:

- `parameters`: JSON Schema (`additionalProperties: false`). `enum`, `pattern`, `required`가 실행 시 그대로 검증됩니다.
- `options`: parameter마다 `--flag` 이름, 타입, 필수 여부, enum/pattern. 배열·객체 타입은 `pass_via: "--params-json"`.
- `invoke`: 바로 실행 가능한 세 가지 문자열 `flags`, `params_json`, `dry_run`.
- `kis_alternatives`, `broker_role`, `required_credentials`, `agent_notes`.

Agent는 `describe --json`의 `examples[0].command` 또는 `schema --json`의 `invoke.dry_run`을 실행 skeleton으로 사용하고, `agent_notes`를 provider별 주의사항으로 참고할 수 있습니다.

### 3. Workflow Recipes

```bash
uv run cluefin-openapi-cli recipes --json
uv run cluefin-openapi-cli recipe stock-research --json
uv run cluefin-openapi-cli recipe technical-analysis --json
uv run cluefin-openapi-cli recipe market-scan --json
uv run cluefin-openapi-cli recipe corporate-actions --json
uv run cluefin-openapi-cli recipe disclosure-monitoring --json
```

### 4. Command Path

- `kis <category> <name>`
- `kiwoom <category> <name>`
- `dart <name>`
- `brokers`, `list`, `describe`, `schema`, `domains`, `tags`, `recipes`, `recipe`는 meta command

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --json
uv run cluefin-openapi-cli kiwoom chart tick --stock-code KRX:005930 --tic-scope 1 --json
uv run cluefin-openapi-cli dart company-overview --corp-code 00126380 --json
```

## 입력 방식

scalar 필드는 `--flag value` 또는 `--flag=value`로 줍니다. 배열·객체는 `--params-json`에 전체 객체를 넣거나, 해당 flag에 JSON 문자열을 넣습니다.

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --json
uv run cluefin-openapi-cli kis analysis watchlist-multi-quote \
  --params-json '{"stocks":[{"market":"J","stock_code":"005930"},{"market":"J","stock_code":"000660"}]}' \
  --json
```

입력 규칙:

- 같은 필드를 둘 다 주면 개별 flag가 `--params-json`보다 우선
- 모든 parameter는 네트워크 호출 전에 로컬 검증: `required`, 알려지지 않은 필드, 타입, `enum`, `pattern`, 숫자·길이 범위
- 문자열에 제어문자, `..` 경로 이동, `%`(사전 URL 인코딩), `?`, `#`가 들어 있으면 거부. 중첩 JSON 내부도 검사
- 검증 실패는 exit 2, `error.data.issues[]`에 필드별 `problem`, `value`, `allowed`, `hint`

### `--dry-run`

parameter 병합·검증만 수행하고 broker를 호출하지 않습니다. 토큰 발급도 일어나지 않습니다.

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --dry-run --json
```

응답에는 최종 `params`, `credentials.configured`(값 노출 없이 설정 여부), `kis_alternatives`, 그대로 실행할 `execute` 문자열이 들어 있습니다.

## 출력 방식

- `--json`: 항상 JSON. stdout이 TTY가 아니면 기본값
- `--compact`: 한 줄 JSON. agent 컨텍스트에 가장 저렴
- `--fields a,b.c`: 결과 field mask. 최상위 키 또는 점 경로. 리스트 값이면 각 요소에 적용. 없는 키는 조용히 생략되므로 반환 키를 확인할 것
- client 라이브러리의 DEBUG/INFO 로그는 stderr에서 숨김. `CLUEFIN_OPENAPI_DEBUG=1`이면 표시

```bash
uv run cluefin-openapi-cli kis stock current-price --stock-code 005930 --fields stock_code,current_price,per --compact
uv run cluefin-openapi-cli kiwoom theme group --query-type 0 --date-type 10 --theme-name "" \
  --fluctuation-type 1 --exchange-type 1 --fields thema_grp.thema_grp_cd,thema_grp.thema_nm --json
```

## 오류와 exit code

실패하면 stdout에 아래 envelope 하나만 나옵니다(JSON 모드). agent는 `exit_code`와 `retryable`로 분기합니다.

```json
{
  "error": {
    "type": "ValidationError",
    "message": "Parameter validation failed.",
    "exit_code": 2,
    "retryable": false,
    "hint": "Run `schema kis stock current-price --json` and fix the listed fields.",
    "data": {"command": "kis.stock.current-price", "missing": [], "issues": [{"field": "market", "problem": "not one of the allowed values", "value": "X", "allowed": ["J", "NX", "UN"]}]}
  }
}
```

| exit | 의미 | agent 행동 |
|---|---|---|
| 0 | 성공 | |
| 1 | CLI/client 내부의 예상치 못한 실패 | 그대로 재시도하지 말 것 |
| 2 | usage·검증 오류 | 인자를 고친다. `schema`를 다시 본다 |
| 3 | 자격증명 누락·거부 | `.env`/환경변수 확인. 재시도 무의미 |
| 4 | broker API·네트워크·타임아웃·응답 파싱 실패 | `retryable`이 true일 때만 한 번 재시도 |
| 5 | broker rate limit | `data.retry_after`초(없으면 1초 이상) 대기 후 재시도 |

`error.type` 예: `ValidationError`, `CredentialsMissing`, `AuthenticationError`, `RateLimitError`, `BrokerUnavailable`, `BrokerApiError`, `BrokerRejectedRequest`, `ResponseParseError`(존재하지 않는 종목코드처럼 broker가 빈 응답을 준 경우), `ExecutionError`.

## 뼈대: 모듈과 요청 흐름

```
src/cluefin_openapi_cli/
├── main.py         진입점. argv 파싱 → meta command 또는 broker command 분기, 출력·오류 envelope
├── registry.py     CommandSpec(경로·schema·role·kis_alternatives·executor) 조립과 조회
├── metadata.py     BROKER_ROLES, KIWOOM_KIS_ALTERNATIVES, domain/tag taxonomy, 예시·agent_notes 생성
├── validation.py   네트워크 호출 전 로컬 검증(required/enum/pattern/범위)과 문자열 하드닝
├── errors.py       exit code 계약(EXIT_CODES)과 broker 예외 → CliError 분류(classify_exception)
├── output.py       JSON 직렬화, --compact, --fields 마스킹
├── recipes.py      여러 command를 엮는 workflow guide
└── handlers/
    ├── _base.py    @rpc_method 데코레이터, KIS/Kiwoom 응답 추출 헬퍼
    ├── kis/        category별 handler 모듈 (stock, chart, ranking, financial, …)
    ├── kiwoom/     category별 handler 모듈 (theme, sector, etf, program, …)
    └── dart.py
```

한 번의 broker command 실행은 다음 순서로 흐릅니다.

```
argv ─▶ _parse_named_options ─▶ registry.resolve_command(path)
     ─▶ _merge_params (--params-json ⊕ flags → 타입 변환)
     ─▶ validation.validate_params (실패: exit 2, issues[])
     ─▶ --dry-run 이면 여기서 종료 (토큰 발급 없음)
     ─▶ registry.invoke_command → BrokerClientFactory → handler(params, session)
     ─▶ 예외: errors.classify_exception → exit 3/4/5 + error envelope
     ─▶ output.select_fields(--fields) → render_output(--compact)
```

command 하나는 handler 함수에 붙은 `@rpc_method(name="stock.current_price", parameters={JSON Schema}, broker="kis")` 하나로 정의됩니다. `name`의 점이 CLI 경로(`kis stock current-price`)가 되고, `parameters`가 그대로 `schema` 출력과 flag 목록과 로컬 검증 규칙이 됩니다. 새 command를 추가하려면 handler 모듈에 함수를 쓰고 그 모듈의 `_ALL_HANDLERS`에 넣으면 끝입니다. Kiwoom command가 KIS와 겹치면 `metadata.KIWOOM_KIS_ALTERNATIVES`에 한 줄을 추가합니다.

검증 테스트(`tests/`):

- `test_agent_surface.py`: role·alternatives·schema·dry-run·검증·field mask·exit code 분류
- `test_cli_contract.py`: 182개 command 전부 `schema`가 유효하고 `invoke.dry_run` 예시가 실제로 exit 0으로 통과하는지, README 코드 블록의 명령이 실행되는지
- `test_handler_client_contract.py`: handler가 호출하는 client 메서드·응답 필드가 실제 `cluefin-openapi`에 존재하는지
- `test_rpc_registry.py`: command 수(182)·metadata 완결성·taxonomy 커버리지

## 동작 원칙

- CLI 내부 registry가 command metadata와 executor set을 직접 관리
- 실제 broker client 생성은 `cluefin_openapi.client_factory`를 사용
- KIS, Kiwoom은 토큰 캐시를 사용하고, DART는 stateless client로 동작
- 모든 command는 `side_effect: "read"`. 주문·계좌 변경 command는 없다
- Agent integration은 이 CLI의 JSON discovery를 직접 사용합니다. agent용 사용 규칙은 `SKILL.md`에 있습니다

## 주의사항

- 실 API 호출에는 broker credential이 필요합니다. `brokers --json`으로 먼저 확인합니다
- `.env`가 없거나 값이 비어 있으면 해당 broker command는 exit 3으로 실패합니다
- 일부 command는 복합 입력 때문에 사실상 `--params-json`이 필요합니다. `schema`의 `options[].pass_via`를 봅니다
