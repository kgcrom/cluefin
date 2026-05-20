# Agent-Friendly CLI Discovery PRD

## Summary

`cluefin-cli`를 고수준 wrapper로 유지하거나 확장하는 대신, Agent가 `cluefin-openapi-cli`와 `cluefin-ta-cli`를 직접 탐색하고 조합해서 사용할 수 있도록 두 CLI를 machine-readable catalog로 강화한다.

핵심 목표는 다음과 같다.

- `cluefin-openapi-cli`의 183개 command 전체에 `domain`, `tag`, `use_case`, `examples`, `agent_notes` metadata를 부여한다.
- `cluefin-ta-cli`의 11개 command 전체에 `domain`, `tag`, `use_case`, `examples`, `agent_notes` metadata를 부여한다.
- Agent가 domain/tag 기반으로 필요한 command를 찾을 수 있도록 discovery 명령을 추가한다.
- Agent가 대표 업무 흐름을 이해할 수 있도록 workflow recipe를 JSON으로 제공한다.

## Problem

현재 두 CLI는 이미 JSON 기반 탐색을 일부 지원한다.

```bash
uv run cluefin-openapi-cli list --json
uv run cluefin-openapi-cli describe kis stock current-price --json
uv run cluefin-ta-cli list --json
uv run cluefin-ta-cli describe ta rsi --json
```

하지만 Agent가 실제로 활용하기에는 다음 정보가 부족하다.

- 어떤 command가 `chart`, `statements`, `trading-flow`, `market` 같은 업무 domain에 해당하는지 알기 어렵다.
- provider SDK 구조의 `category`와 Agent 작업 의도의 `domain`이 다르다.
- command별 사용 예시와 입력 힌트가 부족하다.
- 여러 command를 조합하는 대표 workflow가 없다.

## Goals

- Agent가 command catalog를 JSON으로 탐색할 수 있다.
- Agent가 `domain` 또는 `tag`로 command를 필터링할 수 있다.
- `describe --json` 결과에 examples와 agent_notes가 포함된다.
- 모든 command가 최소 1개 이상의 domain과 tag를 가진다.
- 대표 workflow recipe가 JSON으로 제공된다.
- 기존 command 실행 표면과 command 수를 유지한다.

## Non-Goals

- 이번 작업에서 `cluefin-cli`를 삭제하지 않는다.
- 이번 작업에서 workflow recipe를 자동 실행하지 않는다.
- 이번 작업에서 broker API 응답 스키마를 재설계하지 않는다.
- 이번 작업에서 실제 API 통합 테스트를 강제하지 않는다.

## Terminology

- `category`: provider SDK 또는 기존 CLI command 구조의 분류. 예: `kis analysis`, `kiwoom ranking`.
- `domain`: Agent 작업 의도 기준 분류. 예: `chart`, `trading-flow`, `corporate-actions`.
- `tag`: 세부 기능 키워드. 예: `ohlcv`, `foreign`, `dividend`, `momentum`.
- `recipe`: Agent가 여러 command를 조합할 때 참고하는 workflow guide. 실행 기능이 아니라 discovery metadata다.

## Target CLI UX

### cluefin-openapi-cli

```bash
uv run cluefin-openapi-cli domains --json
uv run cluefin-openapi-cli tags --json
uv run cluefin-openapi-cli list --domain chart --json
uv run cluefin-openapi-cli list --tag ohlcv --json
uv run cluefin-openapi-cli list --broker kis --domain market --json
uv run cluefin-openapi-cli describe kis chart period --json
uv run cluefin-openapi-cli recipes --json
uv run cluefin-openapi-cli recipe stock-research --json
```

### cluefin-ta-cli

```bash
uv run cluefin-ta-cli domains --json
uv run cluefin-ta-cli tags --json
uv run cluefin-ta-cli list --domain technical-indicator --json
uv run cluefin-ta-cli list --tag momentum --json
uv run cluefin-ta-cli describe ta rsi --json
```

## Metadata Schema

`CommandSpec`에 다음 필드를 추가한다.

```python
domains: tuple[str, ...] = ()
tags: tuple[str, ...] = ()
use_cases: tuple[str, ...] = ()
examples: tuple[dict[str, Any], ...] = ()
agent_notes: str | None = None
```

`cluefin-openapi-cli`는 다음 필드를 추가로 가진다.

```python
required_credentials: tuple[str, ...] = ()
side_effect: str = "read"
```

`side_effect`는 v1에서 모든 command를 `read`로 둔다.

## Domain Taxonomy

초기 domain 목록은 다음을 기본값으로 한다.

- `statements`
- `chart`
- `news`
- `trading-flow`
- `market`
- `quote`
- `sector`
- `theme`
- `corporate-actions`
- `market-calendar`
- `etf`
- `technical-indicator`
- `risk-metric`
- `portfolio-metric`

## Tag Taxonomy

초기 tag 목록은 다음을 기본값으로 한다.

- `ohlcv`
- `daily`
- `minute`
- `tick`
- `current-price`
- `order-book`
- `conclusion`
- `overtime`
- `financial-statement`
- `financial-ratio`
- `dividend`
- `shareholder`
- `disclosure`
- `announcement`
- `foreign`
- `institution`
- `program-trading`
- `ranking`
- `volume-rank`
- `market-cap`
- `short-selling`
- `credit`
- `sector-index`
- `theme-group`
- `ipo`
- `capital-increase`
- `capital-reduction`
- `merger-split`
- `shareholder-meeting`
- `moving-average`
- `momentum`
- `volatility`
- `volume-indicator`
- `portfolio-risk`

## Implementation Strategy

### Metadata Location

Handler decorator 183개를 직접 수정하지 않는다. 대신 별도 metadata module을 둔다.

```text
apps/cluefin-openapi-cli/src/cluefin_openapi_cli/metadata.py
apps/cluefin-ta-cli/src/cluefin_ta_cli/metadata.py
```

`cluefin-openapi-cli`는 command 수가 많기 때문에 rule + override 방식으로 구성한다.

- broker/category 기반 default rule
- command path 기반 override
- 모든 command coverage 테스트

`cluefin-ta-cli`는 11개 command만 있으므로 수동 metadata map을 둔다.

## Phases

### Phase 1: CommandSpec Metadata Foundation

Status: `completed`

Tasks:

- `cluefin-openapi-cli` `CommandSpec`에 metadata 필드를 추가한다.
- `cluefin-ta-cli` `CommandSpec`에 metadata 필드를 추가한다.
- `_command_summary()`가 metadata 필드를 JSON에 포함하도록 수정한다.
- 기존 `list --json`, `describe --json` 동작과 command count를 유지한다.

Acceptance Criteria:

- 기존 openapi CLI command count `183` 유지.
- 기존 ta CLI command count `11` 유지.
- `describe --json`에 `domains`, `tags`, `use_cases`, `examples`, `agent_notes` 필드가 포함된다.

Verification:

```bash
uv run pytest apps/cluefin-openapi-cli/tests -v
uv run pytest apps/cluefin-ta-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- 수정 코드 검증 테스트를 추가한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

### Phase 2: cluefin-openapi-cli Domain/Tag Metadata

Status: `completed`

Tasks:

- `cluefin_openapi_cli/metadata.py`를 추가한다.
- 183개 command 전체에 최소 1개 domain과 tag가 부여되도록 rule과 override를 작성한다.
- KIS, Kiwoom, DART command별 domain/tag 분류를 정리한다.
- required credentials와 side effect metadata를 추가한다.

Acceptance Criteria:

- 모든 openapi command가 `domains`와 `tags`를 가진다.
- category와 domain이 분리되어 표현된다.
- 주요 command가 기대 domain에 매핑된다.
  - `kis.chart.period` -> `chart`
  - `kis.market.announcement` -> `news`, `market`
  - `kis.schedule.dividend` -> `corporate-actions`
  - `kiwoom.theme.group` -> `theme`, `market`
  - `dart.disclosure-search` -> `news`, `statements`

Verification:

```bash
uv run pytest apps/cluefin-openapi-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- 모든 command metadata coverage 테스트를 추가한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

### Phase 3: cluefin-ta-cli Domain/Tag Metadata

Status: `completed`

Tasks:

- `cluefin_ta_cli/metadata.py`를 추가한다.
- 11개 command 전체에 domain/tag/use_case/examples/agent_notes를 부여한다.
- TA command별 입력 요구사항을 agent_notes에 명확히 기록한다.

Acceptance Criteria:

- 모든 TA command가 `domains`와 `tags`를 가진다.
- `sma`, `ema`는 `moving-average`, `trend` 태그를 가진다.
- `rsi`, `macd`, `stoch`, `adx`는 `momentum` 또는 `trend` 태그를 가진다.
- `bbands`, `atr`은 `volatility` 태그를 가진다.
- `obv`는 `volume-indicator` 태그를 가진다.
- `mdd`, `sharpe`는 `portfolio-risk` 또는 `portfolio-metric` domain을 가진다.

Verification:

```bash
uv run pytest apps/cluefin-ta-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- 모든 TA command metadata coverage 테스트를 추가한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

### Phase 4: Domain/Tag Discovery Commands

Status: `completed`

Tasks:

- `cluefin-openapi-cli list --domain`, `list --tag` 필터를 추가한다.
- `cluefin-ta-cli list --domain`, `list --tag` 필터를 추가한다.
- 두 CLI에 `domains --json`, `tags --json` 명령을 추가한다.
- 필터 조합은 AND 조건으로 처리한다.

Acceptance Criteria:

- 아래 명령이 JSON으로 동작한다.

```bash
uv run cluefin-openapi-cli list --domain chart --json
uv run cluefin-openapi-cli list --tag ohlcv --json
uv run cluefin-openapi-cli domains --json
uv run cluefin-openapi-cli tags --json
uv run cluefin-ta-cli list --domain technical-indicator --json
uv run cluefin-ta-cli list --tag momentum --json
uv run cluefin-ta-cli domains --json
uv run cluefin-ta-cli tags --json
```

Verification:

```bash
uv run pytest apps/cluefin-openapi-cli/tests -v
uv run pytest apps/cluefin-ta-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- CLI JSON output 테스트를 추가한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

### Phase 5: Examples and Agent Notes

Status: `completed`

Tasks:

- `describe --json` 결과에 examples와 agent_notes를 포함한다.
- openapi command는 provider별 params-json 예시를 포함한다.
- ta command는 배열 입력이 `--params-json`으로 들어가야 함을 예시에 포함한다.
- root/help JSON에 discovery 명령 사용법을 갱신한다.

Acceptance Criteria:

- `describe kis chart period --json`에 실행 가능한 example skeleton이 포함된다.
- `describe ta rsi --json`에 close 배열 입력 예시가 포함된다.
- `agent_notes`는 Agent가 API 선택 시 주의해야 할 조건을 설명한다.

Verification:

```bash
uv run pytest apps/cluefin-openapi-cli/tests -v
uv run pytest apps/cluefin-ta-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- describe metadata 테스트를 추가한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

### Phase 6: Workflow Recipes

Status: `completed`

Tasks:

- `cluefin-openapi-cli`에 recipe metadata를 추가한다.
- `recipes --json` 명령을 추가한다.
- `recipe <name> --json` 명령을 추가한다.
- recipe가 참조하는 command가 실제 registry에 존재하는지 테스트한다.

Initial Recipes:

- `stock-research`
- `technical-analysis`
- `market-scan`
- `corporate-actions`
- `disclosure-monitoring`

Acceptance Criteria:

- 아래 명령이 JSON으로 동작한다.

```bash
uv run cluefin-openapi-cli recipes --json
uv run cluefin-openapi-cli recipe stock-research --json
```

- 각 recipe는 steps, command references, purpose, expected inputs를 포함한다.
- recipe는 실행하지 않고 Agent guide 역할만 한다.

Verification:

```bash
uv run pytest apps/cluefin-openapi-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- recipe command와 reference 검증 테스트를 추가한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

### Phase 7: Documentation and Migration Guidance

Status: `pending`

Tasks:

- `cluefin-openapi-cli` README에 domain/tag discovery 사용법을 추가한다.
- `cluefin-ta-cli` README에 domain/tag discovery 사용법을 추가한다.
- Agent가 두 CLI를 조합하는 예시 workflow를 문서화한다.
- `cluefin-cli` 삭제 또는 deprecation은 후속 PR로 분리한다.

Acceptance Criteria:

- README에 `list --domain`, `list --tag`, `domains`, `tags`, `recipes`, `recipe` 예시가 포함된다.
- `cluefin-cli` 삭제는 이번 PR 범위가 아님을 명시한다.

Verification:

```bash
uv run pytest apps/cluefin-openapi-cli/tests -v
uv run pytest apps/cluefin-ta-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- 문서 예시와 CLI 명령이 어긋나지 않도록 smoke test를 추가한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

## Test Requirements

각 phase는 수정 범위에 맞는 테스트를 반드시 추가한다.

Minimum Tests:

- command count 유지 테스트
- 모든 command metadata coverage 테스트
- `list --domain` 필터 테스트
- `list --tag` 필터 테스트
- `domains --json` 테스트
- `tags --json` 테스트
- `describe --json` metadata 테스트
- recipe 목록/상세 테스트
- recipe command reference 유효성 테스트

## Phase Completion Policy

각 phase가 끝날 때 반드시 아래 순서를 따른다.

1. 수정된 코드를 검증할 수 있는 테스트 코드 추가
2. 관련 테스트 실행
3. 전체 포맷 및 린트 실행

```bash
uvx ruff format .
uvx ruff check .
```

4. 모든 검증 통과 확인
5. `/commit` 실행

검증 실패 시 `/commit`을 실행하지 않는다.

## Tracking

진행 상태는 [feature_list.json](./feature_list.json)에서 관리한다.

상태 값:

- `pending`: 아직 시작하지 않음
- `in_progress`: 진행 중
- `blocked`: 외부 결정 또는 선행 작업이 필요함
- `completed`: 구현, 테스트, format/check, commit 완료
