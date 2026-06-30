# 설계: cluefin-xbrl `extract_notes()` — 재무제표 주석 추출

- 날짜: 2026-06-30
- 대상 패키지: `packages/cluefin-xbrl`
- 상태: 설계 승인 대기 (구현 미착수)

## 배경 / 문제

`cluefin-xbrl`은 DART 재무제표 원본 XBRL을 파싱한다. 현재 동작을 삼성전자 2025
사업보고서(접수번호 `20260310002820`)로 실측한 결과:

- 저수준 파서 `parse_xbrl_file` / `parse_xbrl_directory`는 **5,534개 fact를 전수 추출**하며,
  여기엔 주석(notes)의 정량 데이터와 짧은 서술 fact(665개)가 모두 포함된다.
- `include_taxonomy=True`로 파싱하면 **74개 presentation linkrole**과 1,618개 라벨이 추출된다.
- 그러나 고수준 API `extract_financial_statements`는 74개 중 **5개(BS/IS/CIS/CF/SCE)만 노출**하고,
  나머지 69개(주석 57개 + 별도재무제표 + 문서정보)를 `_identify_statement_type`이
  `None`을 반환하는 경로에서 조용히 폐기한다.

즉 **주석 데이터는 파싱은 되지만 고수준 API로 접근할 수 없다.** 본 설계는 주석 전용
추출 API `extract_notes()`를 추가해 이 간극을 메운다.

### linkrole 분류 (삼성 2025 실측, 74개)

| 분류 | role 코드 | 개수 | 비고 |
|------|-----------|------|------|
| 재무제표 | D2xxxx~D6xxxx | 10 | 5종 × {연결 `*0000`, 별도 `*0005`} |
| **주석** | **D8xxxxx** | **57** | 금융상품·종업원급여·특수관계자·법인세·영업부문 등 |
| 문서/엔티티 정보 | D999xxx, dart-gcd | 7 | 표지·감사인 등 메타데이터 |

### 서술형 주석 본문에 대한 사실 확인

IFRS의 `*Explanatory` **TextBlock**(긴 서술 본문) fact는 이 XBRL에 **0개**다. 주석 전문
문단은 재무제표 원본 XBRL이 아니라 사업보고서 **본문 문서(XBRL 아님)** 에 존재한다. 따라서
본 설계의 범위는 **XBRL에 태깅된 주석(정량 + 짧은 서술 + 차원 구조)** 으로 한정한다. 서술형
본문 파싱은 본 설계의 범위가 아니다.

## 목표 / 비목표

**목표**
- D8 주석 57개 linkrole을 구조화된 객체로 노출하는 `extract_notes()` 추가.
- 주석의 차원(Axis/Member 테이블) 구조를 raw qname으로 보존.
- 연결·별도 주석을 모두 보존하고 `is_consolidated` 플래그로 구분.
- 기존 `extract_financial_statements` 동작과 테스트를 **변경하지 않음**.

**비목표**
- 서술형 주석 본문(TextBlock) 파싱 — XBRL에 데이터 없음.
- 사업보고서 본문 문서 파싱.
- `_def.xml` 기반 정밀 hypercube 차원 필터링 (후속 과제로 명시).
- `extract_financial_statements`의 "연결만 노출" 한계 수정 (별도 주제).

## 확정된 설계 결정

1. **범위**: D8 주석 57개 linkrole만. 재무제표(D2~D6)·문서정보(D999)는 제외.
2. **차원 처리**: 각 line item에 `dimensions: dict[axis_qname, member_qname]`를 raw로 보존.
3. **연결/별도**: 둘 다 별도 항목으로 보존, `is_consolidated` 플래그로 구분, `role_code`로 키잉.
4. **구현 방식 (A안)**: 신규 모듈 `notes.py` + 신규 모델. `statements.py` 불변.

## 아키텍처

### 모듈
- 신규 `packages/cluefin-xbrl/src/cluefin_xbrl/notes.py`.
- `statements.py`는 손대지 않는다 (기존 테스트 무영향).
- 트리 평탄화 로직은 v1에서 `notes.py`에 차원 캡처 버전으로 자체 구현한다.
  `statements.py`와의 중복 제거(공통 tree-walk 헬퍼 추출)는 후속 리팩터로 분리한다.

### 신규 모델 (`_types.py`)

```text
NoteLineItem                       # StatementLineItem + dimensions
  concept_local_name: str
  concept_qname: str
  label_ko: str | None
  label_en: str | None
  value: Decimal | None
  unit: str | None
  period: XbrlPeriod | None
  depth: int = 0
  order: float = 0.0
  is_abstract: bool = False
  dimensions: dict[str, str] = {}   # axis_qname -> member_qname (raw)

NoteSection
  role_code: str                    # 예: "D834480"
  role_uri: str                     # 전체 linkrole URI
  title: str | None                 # 루트 노드의 label_ko ("종업원급여에 대한 공시")
  is_consolidated: bool             # 끝자리 0 -> True, 5 -> False (관례 휴리스틱)
  line_items: list[NoteLineItem] = []
  periods: list[XbrlPeriod] = []

ParsedNotes
  source_file: str
  entity_id: str | None
  notes: dict[str, NoteSection] = {}   # key = role_code
```

### 핵심 로직 (`notes.py`)

- `extract_notes(doc: XbrlDocument) -> ParsedNotes`
  - `doc.taxonomy`가 없으면 기존과 동일하게 `ValueError`.
  - `doc.taxonomy.presentation_trees`를 순회하며 D8 role만 선별, 각각을 `NoteSection`으로 구성.
  - `extract_financial_statements`의 "first match only"를 **적용하지 않음** — 57개 role을
    `role_code` 키로 전부 유지(연결·별도 모두).
- `_identify_note_role(linkrole: str) -> tuple[str, bool] | None`
  - 정규식 `role-(D8\d+)` 매칭. 매칭되면 `(role_code, is_consolidated)` 반환, 아니면 `None`.
  - `is_consolidated = not role_code.endswith("5")`.
- `_collect_note_line_items(node, facts_by_concept, labels, items)`
  - 기존 `_collect_line_items`와 동형이되 각 fact의 `dimensions`를 `NoteLineItem`에 복사.
  - 차원만 다른 동일 concept은 각각 별도 line item으로 보존(요청대로 raw 유지).

### 공개 API (`__init__.py`)
`extract_notes`, `ParsedNotes`, `NoteSection`, `NoteLineItem`를 import 및 `__all__`에 추가.

## 데이터 흐름

```
parse_xbrl_directory(dir, include_taxonomy=True)
  -> XbrlDocument(facts, taxonomy{labels, presentation_trees})
       |
       v
extract_notes(doc)
  presentation_trees 순회
    -> _identify_note_role(linkrole)  # D8만 통과
    -> _collect_note_line_items(...)  # 차원 보존 평탄화
  -> ParsedNotes(notes={role_code: NoteSection})
```

## 오류 처리
- `doc.taxonomy is None` → `ValueError` (기존 `extract_financial_statements`와 동일 메시지 규약).
- D8 role이 하나도 없으면 빈 `ParsedNotes`(notes={}) 반환 — 예외 아님.
- 라벨 없는 concept → `label_ko`/`label_en`은 `None` (기존 동작과 동일).

## 알려진 한계 (v1 허용, 후속 과제)
1. **concept명 전역 매칭**: fact를 `concept_local_name`으로만 매칭하므로, 여러 주석 role이
   공유하는 concept은 중복 귀속될 수 있다. 정밀한 hypercube(`_def.xml` 차원 관계) 기반
   필터링은 후속 과제. → v1 허용.
2. **is_consolidated 휴리스틱**: 끝자리 0/5 규칙. 삼성 2025 실측 57개는 전부 정확(28/29 쌍
   일치 + 단독 코드 `D861305` 이익잉여금처분계산서도 의미상 별도로 일치)하나, 미래 공시의
   예외 가능성이 있다. raw `role_code`를 항상 노출해 소비자가 덮어쓸 수 있게 한다.
3. **서술형 주석 본문**: XBRL에 미태깅(0개)이라 파싱 대상 아님.

## 테스트 전략
- **단위 테스트**: 신규 픽스처 필요. 현 `sample.xbrl`엔 D8 role이 없다(StatementOfFinancialPosition
  하나뿐). 차원이 있는 축약 주석 role(예: D834480 종업원급여 일부) 픽스처를 만들어
  `_identify_note_role` 분류, 차원 보존, `is_consolidated` 플래그, 빈 taxonomy `ValueError`를 검증.
- **통합 테스트**(`@pytest.mark.integration`): 삼성전자 실데이터로 `extract_notes` 실행 →
  57개 section, 차원 보존, 주요 주석(종업원급여·금융상품·특수관계자) 존재를 검증. 본 설계
  과정에서 작성한 검증 스크립트를 재활용한다.

## 영향 범위
- 신규: `notes.py`, `_types.py`에 모델 3종, `__init__.py` export 4종, 테스트.
- 변경 없음: `parser.py`, `taxonomy.py`, `statements.py` 및 기존 테스트.
- 의존성 변경 없음 (arelle-release, pydantic 그대로).

## 미해결 질문
- (해결) v1에서 concept 전역 매칭 한계를 허용하고 hypercube 필터링은 후속으로 둔다.
