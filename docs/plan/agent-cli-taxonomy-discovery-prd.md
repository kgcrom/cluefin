# Agent CLI Taxonomy Discovery PRD

## Summary

`cluefin-openapi-cli`와 `cluefin-ta-cli`는 현재 `domains --json`, `tags --json`를 제공하지만 각 항목은 `name`과 `command_count` 중심이다. Agent가 domain/tag 이름만 보고도 어느 정도 추론할 수는 있으나, `ohlcv`, `program-trading`, `corporate-actions`, `portfolio-risk`처럼 약어 또는 시장 용어가 섞이면 오해 가능성이 있다.

이번 개선은 domain/tag catalog 자체를 Agent가 해석 가능한 지식 베이스로 만드는 것이다. `domains --json`, `tags --json`에 설명, 사용 시점, 관련 분류, 대표 command, 예시 필터를 추가한다. 기존 command 실행 표면은 유지한다.

## Problem

현재 discovery 흐름은 다음처럼 동작한다.

```bash
uv run cluefin-openapi-cli domains --json
uv run cluefin-openapi-cli tags --json
uv run cluefin-ta-cli domains --json
uv run cluefin-ta-cli tags --json
```

하지만 응답이 사실상 아래 정보에 머문다.

```json
{
  "name": "chart",
  "command_count": 8
}
```

Agent 입장에서 부족한 점은 다음과 같다.

- `domain`과 `tag`의 의미 차이를 응답만 보고 확정하기 어렵다.
- `tag`는 세부 키워드라 이름만으로 사용 시점을 알기 어렵다.
- `tags --json`에서 어떤 domain과 연결되는지 바로 알 수 없다.
- Agent가 다음 탐색 명령을 만들기 위한 `example_filter`가 없다.
- 잘못된 domain/tag 선택을 줄여 줄 `when_to_use`, `avoid_when` 같은 힌트가 없다.

## Goals

- `domains --json`이 각 domain의 의미와 사용 시점을 설명한다.
- `tags --json`이 각 tag의 의미, 관련 domain, 사용 시점을 설명한다.
- Agent가 응답만 보고 다음 `list --domain` 또는 `list --tag` 명령을 구성할 수 있다.
- 기존 `domains --json`, `tags --json`의 `name`, `command_count` 호환성을 유지한다.
- `cluefin-openapi-cli`와 `cluefin-ta-cli`가 같은 taxonomy schema를 사용한다.
- 모든 실제 domain/tag가 taxonomy 설명 metadata를 가진다는 테스트를 추가한다.

## Non-Goals

- command별 domain/tag 재분류는 이번 범위가 아니다.
- recipe 자동 실행은 이번 범위가 아니다.
- API 응답 데이터 스키마 정규화는 이번 범위가 아니다.
- `apps/cluefin-cli` 삭제는 이번 범위가 아니다.

## Target CLI UX

### Domains

```bash
uv run cluefin-openapi-cli domains --json
uv run cluefin-ta-cli domains --json
```

예상 응답 형태:

```json
{
  "domains": [
    {
      "name": "chart",
      "description": "가격, 거래량, OHLCV 시계열 데이터를 조회하는 command 그룹",
      "when_to_use": "기술적 분석, 가격 추세, 거래량 분석 전 원천 시계열 데이터가 필요할 때 사용",
      "avoid_when": "이미 OHLCV 배열을 확보했고 지표 계산만 필요하면 cluefin-ta-cli의 technical-indicator domain을 사용",
      "related_tags": ["ohlcv", "daily", "minute", "tick"],
      "example_filter": "uv run cluefin-openapi-cli list --domain chart --json",
      "command_count": 8
    }
  ],
  "count": 1
}
```

### Tags

```bash
uv run cluefin-openapi-cli tags --json
uv run cluefin-ta-cli tags --json
```

예상 응답 형태:

```json
{
  "tags": [
    {
      "name": "ohlcv",
      "description": "open, high, low, close, volume 형태의 가격/거래량 데이터",
      "when_to_use": "TA 지표 계산에 필요한 원천 가격 배열을 찾을 때 사용",
      "avoid_when": "이미 지표 값만 필요하고 가격 데이터 조회가 필요 없으면 moving-average, momentum 같은 TA tag 사용",
      "related_domains": ["chart", "technical-indicator"],
      "example_filter": "uv run cluefin-openapi-cli list --tag ohlcv --json",
      "command_count": 6
    }
  ],
  "count": 1
}
```

## Metadata Schema

두 CLI에서 공유할 taxonomy item shape:

```python
name: str
description: str
when_to_use: str
avoid_when: str | None
related_domains: tuple[str, ...]
related_tags: tuple[str, ...]
example_filter: str
command_count: int
```

`domains --json`에서는 `related_tags`가 중요하고, `tags --json`에서는 `related_domains`가 중요하다. 호환성을 위해 두 필드는 모두 포함한다.

## Taxonomy Coverage

초기 구현은 현재 사용 중인 domain/tag 전체를 대상으로 한다.

Domain examples:

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

Tag examples:

- `ohlcv`
- `daily`
- `minute`
- `tick`
- `current-price`
- `order-book`
- `financial-statement`
- `financial-ratio`
- `dividend`
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
- `moving-average`
- `momentum`
- `volatility`
- `volume-indicator`
- `portfolio-risk`

## Implementation Strategy

### Shared Shape, Local Modules

두 앱은 별도 패키지이므로 공통 package를 새로 만들지 않는다. 대신 각 앱의 metadata module에 taxonomy catalog를 둔다.

```text
apps/cluefin-openapi-cli/src/cluefin_openapi_cli/metadata.py
apps/cluefin-ta-cli/src/cluefin_ta_cli/metadata.py
```

각 module은 다음 기능을 제공한다.

- domain taxonomy lookup
- tag taxonomy lookup
- command 목록에서 실제 count 계산
- 누락 taxonomy 검증 helper

### Response Construction

`domains --json`, `tags --json`는 기존처럼 registry의 실제 command를 기준으로 count를 계산한다. 여기에 taxonomy catalog 설명을 merge한다.

기존 필드:

- `name`
- `command_count`

추가 필드:

- `description`
- `when_to_use`
- `avoid_when`
- `related_domains`
- `related_tags`
- `example_filter`

## Phases

### Phase 1: Taxonomy Metadata Foundation

Status: `completed`

Tasks:

- OpenAPI CLI taxonomy item dataclass 또는 typed dict를 추가한다.
- TA CLI taxonomy item dataclass 또는 typed dict를 추가한다.
- `domains --json`, `tags --json` 응답 shape를 확장한다.
- 기존 `name`, `command_count`, `count` 필드 호환성을 유지한다.

Acceptance Criteria:

- 두 CLI의 `domains --json`가 `description`, `when_to_use`, `example_filter`를 포함한다.
- 두 CLI의 `tags --json`가 `description`, `when_to_use`, `related_domains`, `example_filter`를 포함한다.
- 기존 테스트가 깨지지 않는다.

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

### Phase 2: OpenAPI Domain/Tag Descriptions

Status: `completed`

Tasks:

- `cluefin-openapi-cli`의 실제 domain 전체에 설명을 추가한다.
- `cluefin-openapi-cli`의 실제 tag 전체에 설명을 추가한다.
- domain별 `related_tags`를 정리한다.
- tag별 `related_domains`를 정리한다.
- 모든 실제 domain/tag가 catalog에 존재하는 coverage 테스트를 추가한다.

Acceptance Criteria:

- OpenAPI CLI의 모든 실제 domain에 설명 metadata가 있다.
- OpenAPI CLI의 모든 실제 tag에 설명 metadata가 있다.
- `ohlcv`, `program-trading`, `corporate-actions`, `market-calendar`, `sector-index`, `theme-group` 설명이 명확하다.
- `example_filter`가 실제 실행 가능한 command 형태다.

Verification:

```bash
uv run pytest apps/cluefin-openapi-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- coverage 테스트와 대표 응답 테스트를 추가한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

### Phase 3: TA Domain/Tag Descriptions

Status: `completed`

Tasks:

- `cluefin-ta-cli`의 실제 domain 전체에 설명을 추가한다.
- `cluefin-ta-cli`의 실제 tag 전체에 설명을 추가한다.
- `technical-indicator`, `risk-metric`, `portfolio-metric`의 차이를 명확히 한다.
- `moving-average`, `momentum`, `volatility`, `volume-indicator`, `portfolio-risk` 설명을 추가한다.
- 모든 실제 domain/tag가 catalog에 존재하는 coverage 테스트를 추가한다.

Acceptance Criteria:

- TA CLI의 모든 실제 domain에 설명 metadata가 있다.
- TA CLI의 모든 실제 tag에 설명 metadata가 있다.
- Agent가 `technical-indicator`와 `portfolio-metric`을 혼동하지 않도록 `when_to_use`와 `avoid_when`이 제공된다.
- `moving-average`, `momentum`, `volatility`는 OHLCV 입력과의 관계가 설명된다.

Verification:

```bash
uv run pytest apps/cluefin-ta-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- coverage 테스트와 대표 응답 테스트를 추가한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

### Phase 4: Agent-Focused Response Tests and Docs

Status: `completed`

Tasks:

- README에 enhanced taxonomy discovery 예시를 추가한다.
- `domains --json`, `tags --json` smoke test를 README 예시와 연결한다.
- Agent workflow 문서에서 `domains`, `tags`, `recipes`의 역할 차이를 명확히 한다.
- 기존 recipe 설명과 taxonomy 설명이 서로 충돌하지 않는지 점검한다.

Acceptance Criteria:

- README 예시가 실제 CLI에서 실행된다.
- 문서에 `domains = 업무 영역`, `tags = 세부 기능`, `recipes = workflow guide`가 명시된다.
- Agent가 domain/tag catalog 응답만 보고 다음 `list` 명령을 만들 수 있다.

Verification:

```bash
uv run pytest apps/cluefin-openapi-cli/tests -v
uv run pytest apps/cluefin-ta-cli/tests -v
uvx ruff format .
uvx ruff check .
```

Completion Rule:

- README smoke test를 추가하거나 기존 테스트를 확장한다.
- 모든 테스트와 format/check가 통과하면 `/commit`을 실행한다.

## Open Questions

- `avoid_when`을 필수 필드로 둘지, 값이 없을 때 `null`을 허용할지 결정해야 한다.
- OpenAPI CLI와 TA CLI의 taxonomy 설명을 완전히 동일한 문구로 맞출지, 앱별 맥락에 맞춰 다르게 둘지 결정해야 한다.
- 향후 `recipes --json`에도 관련 `domains`, `tags`의 상세 설명을 embed할지 검토가 필요하다.
