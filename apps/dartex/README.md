# dartex

DART 재무제표 주석 파싱 CLI 도구

## 설치

```bash
cd apps/dartex
uv sync
```

## 사용법

```bash
# DART API 키 설정
export DARTEX_DART_API_KEY="your_api_key"

# 기업 검색
dartex search "카카오"

# 주석 데이터 수집 (5년치)
dartex collect --corp-code 00258801 --years 5

# 특정 섹션 조회
dartex show --corp-code 00258801 --section "주주현황"

# 시계열 데이터 조회
dartex timeseries --corp-code 00258801 --section "주주현황" --format table

# Excel로 내보내기
dartex export --corp-code 00258801 --format excel --output ./kakao_notes.xlsx
```

## 테스트

```bash
# Unit 테스트
uv run pytest apps/dartex/tests -m "not integration" -v

# Integration 테스트 (DART_AUTH_KEY 필요)
uv run pytest apps/dartex/tests -m "integration" -v

# 로그 출력과 함께 실행
uv run pytest apps/dartex/tests -m "integration" -v --log-cli-level=INFO
```

## 기술 스택

- **파싱 엔진**: Docling (MIT, Apple Silicon MPS 지원)
- **DART API**: cluefin-openapi
- **데이터 저장**: SQLite + JSON
- **CLI**: Typer + Rich
