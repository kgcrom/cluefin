# cluefin-rpc: Python JSON-RPC 서버 구현 계획

## 1. 개요

### 목적
`cluefin-rpc`는 `cluefin-openapi`(증권사 API)와 `cluefin-ta`(기술 분석)를 JSON-RPC 2.0 프로토콜로 감싸, 외부 프로세스(TypeScript agent-harness 등)가 **stdin/stdout NDJSON** 통신으로 호출할 수 있게 한다.

### 통신 방식
- **전송**: NDJSON — 한 줄 = 한 JSON 메시지, `\n` 구분
- **stdout**: JSON-RPC 응답 전용 (ensure_ascii=False)
- **stderr**: loguru 로그/디버깅
- **요청/응답 매칭**: 숫자 `id`로 추적

### 의존성
```toml
dependencies = [
    "cluefin-openapi",           # 브로커 API 클라이언트 (KIS, Kiwoom, KRX, DART)
    "cluefin-ta",                # 기술 분석 함수
    "pydantic>=2.12.0",          # 데이터 검증
    "pydantic-settings>=2.0.0",  # BaseSettings (.env 로딩)
    "python-dotenv>=1.1.1",      # .env 파일 로딩
    "loguru>=0.7.3",             # 구조화 로깅 (stderr)
    "numpy>=1.24.0",             # 배열 연산 (TA)
]
```

---

## 2. 아키텍처

### 디렉토리 구조

```
apps/cluefin-rpc/
├── pyproject.toml
├── docs/
│   └── implementation-plan.md    ← 이 문서
├── src/cluefin_rpc/
│   ├── __init__.py
│   ├── __main__.py               # 엔트리포인트: from server import main
│   ├── config.py                 # RpcSettings (pydantic-settings)
│   ├── protocol.py               # JSON-RPC 2.0 읽기/쓰기/파싱
│   ├── dispatcher.py             # 메서드 라우팅
│   ├── server.py                 # 메인 이벤트 루프
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── _base.py              # MethodSchema + @rpc_method 데코레이터
│   │   ├── session.py            # 5 meta/session 핸들러
│   │   ├── quote.py              # 12 시세 핸들러
│   │   ├── ta.py                 # 11 기술 분석 핸들러
│   │   ├── account.py            # 7 계좌 핸들러
│   │   └── dart.py               # 4 공시 핸들러
│   └── middleware/
│       ├── __init__.py
│       ├── auth.py               # SessionManager
│       └── errors.py             # 예외 → RPC 에러 매핑
└── tests/
    ├── __init__.py
    ├── test_protocol.py          # 14 tests
    └── test_dispatcher.py        # 8 tests
```

### 데이터 흐름

```
stdin (NDJSON)
  → server.main() — 줄 단위 읽기
    → protocol.parse_request() — JSON-RPC 2.0 검증
      → dispatcher.dispatch(method, params, session_manager)
        → handler(params) 또는 handler(params, session)
          → cluefin-openapi / cluefin-ta 호출
        ← 결과 dict
      ← protocol.write_response() → stdout
    ← protocol.write_error()      → stdout (에러 시)
```

---

## 3. 프로토콜 명세

### JSON-RPC 2.0 요청 형식
```json
{"jsonrpc": "2.0", "id": 1, "method": "rpc.ping", "params": {}}
```

### JSON-RPC 2.0 응답 형식
```json
{"jsonrpc": "2.0", "id": 1, "result": {"status": "ok"}}
```

### 에러 응답 형식
```json
{"jsonrpc": "2.0", "id": 1, "error": {"code": -32601, "message": "Method not found", "data": null}}
```

### 에러 코드

| 코드 | 상수 | 의미 |
|---|---|---|
| `-32700` | `PARSE_ERROR` | 유효하지 않은 JSON |
| `-32600` | `INVALID_REQUEST` | 필수 필드 누락/잘못된 형식 |
| `-32601` | `METHOD_NOT_FOUND` | 등록되지 않은 메서드 |
| `-32602` | `INVALID_PARAMS` | 파라미터 검증 실패 |
| `-32603` | `INTERNAL_ERROR` | 미처리 예외 |
| `-32001` | `AUTH_ERROR` | 인증 실패 (브로커 API) |
| `-32002` | `RATE_LIMIT_ERROR` | Rate limit 초과 |
| `-32003` | `BROKER_API_ERROR` | 브로커 API 오류 |
| `-32004` | `SESSION_ERROR` | 세션 미초기화 |

### protocol.py 핵심 함수

```python
def write_response(payload: dict) -> None:
    """JSON-RPC 응답을 stdout에 쓰고 즉시 flush."""

def write_error(request_id: int | str | None, code: int, message: str, data: Any = None) -> None:
    """에러 응답 출력. data는 선택적 디버그 정보."""

def parse_request(line: str) -> dict:
    """JSON-RPC 2.0 요청 파싱/검증. 유효하지 않으면 ValueError 발생."""
```

---

## 4. Phase 0: Foundation

### 목표
서버 코어 인프라 구축 — 프로토콜, 디스패처, 설정, 서버 루프, meta 핸들러 5개.

### 선행 Phase
없음 (최초 Phase)

### 구현 모듈

#### 4.1 `protocol.py` — JSON-RPC 2.0 헬퍼
- `write_response()`, `write_error()`, `parse_request()`
- 에러 코드 상수 정의 (§3 참조)

#### 4.2 `config.py` — 설정
```python
class RpcSettings(BaseSettings):
    # KIS
    kis_app_key: Optional[str] = None
    kis_secret_key: Optional[str] = None
    kis_env: Literal["dev", "prod"] = "dev"
    kis_account_no: Optional[str] = None
    kis_account_product_code: Optional[str] = None

    # Kiwoom
    kiwoom_app_key: Optional[str] = None
    kiwoom_secret_key: Optional[str] = None
    kiwoom_env: Literal["dev", "prod"] = "dev"

    # KRX
    krx_auth_key: Optional[str] = None

    # DART
    dart_auth_key: Optional[str] = None
```
- pydantic-settings `BaseSettings` + python-dotenv로 `.env` 자동 로딩

#### 4.3 `handlers/_base.py` — 메서드 스키마 & 데코레이터

```python
@dataclass
class MethodSchema:
    name: str                         # "rpc.ping"
    description: str                  # 사람이 읽을 수 있는 설명
    parameters: dict[str, Any]        # JSON Schema (params)
    returns: dict[str, Any]           # JSON Schema (return)
    category: str = ""                # "rpc", "quote", "ta", "account", "dart"
    requires_session: bool = True     # False → session 주입 안 함
    broker: str | None = None         # "kis", "kiwoom", "krx", "dart"

def rpc_method(name, description, parameters, returns, category="", requires_session=True, broker=None):
    """데코레이터: fn._rpc_schema에 MethodSchema 부착."""
```

#### 4.4 `dispatcher.py` — 메서드 라우팅

```python
class Dispatcher:
    _registry: dict[str, tuple[Callable, MethodSchema]]

    def register(self, method_name: str, handler: Callable, schema: MethodSchema) -> None
    def dispatch(self, method: str, params: dict | list | None, session_manager: Any) -> Any
    def list_methods(self, category: str | None = None, broker: str | None = None) -> list[dict]

class MethodNotFoundError(Exception):    # code = -32601
class InvalidParamsError(Exception):     # code = -32602
```

- `dispatch()`: params가 None이면 `{}`로 변환, list params는 거부
- `requires_session=True`이면 handler에 session_manager 주입

#### 4.5 `server.py` — 메인 루프

```python
def main() -> int:
    """
    1. RpcSettings 로딩
    2. Dispatcher + SessionManager 생성
    3. 모든 핸들러 등록
    4. stdin 줄 단위 읽기 → parse → dispatch → write
    5. EOF 시 session_manager.close_all()
    6. return 0
    """
```

#### 4.6 `__main__.py` — 엔트리포인트
```python
from cluefin_rpc.server import main
raise SystemExit(main())
```

#### 4.7 `handlers/session.py` — Meta/Session 핸들러 5개

| RPC 메서드 | 설명 | requires_session |
|---|---|---|
| `rpc.ping` | 헬스 체크 (status + UTC timestamp) | No |
| `rpc.list_methods` | 등록된 메서드 목록 (category/broker 필터) | No |
| `session.initialize` | 브로커 세션 초기화 | No |
| `session.status` | 활성 세션 상태 조회 | No |
| `session.close` | 브로커 세션 종료 | No |

핸들러 시그니처 패턴:
```python
# 기본: params만 받음
def handle_ping(params: dict) -> dict:
    return {"status": "ok", "timestamp": datetime.now(UTC).isoformat()}

# 의존성 주입: kwargs로 dispatcher/session_manager 전달
def handle_list_methods(params: dict, *, _dispatcher: Dispatcher | None = None) -> list[dict]:
    return _dispatcher.list_methods(params.get("category"), params.get("broker"))

def handle_session_initialize(params: dict, *, _session_manager: SessionManager | None = None) -> dict:
    return _session_manager.initialize(params["broker"])
```

등록 패턴 (클로저로 의존성 바인딩):
```python
def register_session_handlers(dispatcher: Dispatcher, session_manager: SessionManager) -> None:
    dispatcher.register("rpc.ping", handle_ping, handle_ping._rpc_schema)

    def _list_methods(params: dict) -> list[dict]:
        return handle_list_methods(params, _dispatcher=dispatcher)
    dispatcher.register("rpc.list_methods", _list_methods, handle_list_methods._rpc_schema)

    def _init(params: dict) -> dict:
        return handle_session_initialize(params, _session_manager=session_manager)
    dispatcher.register("session.initialize", _init, handle_session_initialize._rpc_schema)
    # ... session.status, session.close 동일 패턴
```

### 검증

```sh
# 핑
echo '{"jsonrpc":"2.0","id":1,"method":"rpc.ping"}' | uv run -m cluefin_rpc

# 메서드 목록
echo '{"jsonrpc":"2.0","id":2,"method":"rpc.list_methods"}' | uv run -m cluefin_rpc

# 세션 상태
echo '{"jsonrpc":"2.0","id":3,"method":"session.status"}' | uv run -m cluefin_rpc
```

---

## 5. Phase 1: Session + Middleware

### 목표
브로커별 세션 관리(`SessionManager`)와 예외 → RPC 에러 매핑.

### 선행 Phase
Phase 0

### 구현 모듈

#### 5.1 `middleware/auth.py` — SessionManager

```python
class SessionManager:
    def __init__(self, settings: RpcSettings) -> None

    def initialize(self, broker: str) -> dict:
        """broker ∈ {"kis", "kiwoom", "krx", "dart"}"""
        # → {"broker": "...", "status": "initialized", "env": "..."}

    def get_kis(self) -> KisHttpClient           # raises SessionNotInitialized
    def get_kiwoom(self) -> KiwoomClient          # raises SessionNotInitialized
    def get_krx(self) -> KrxClient               # raises SessionNotInitialized
    def get_dart(self) -> DartClient              # raises SessionNotInitialized

    def status(self) -> dict:
        # → {"kis": bool, "kiwoom": bool, "krx": bool, "dart": bool}

    def close(self, broker: str | None = None) -> dict:
        # broker=None → 전체 종료

    def close_all(self) -> dict

class SessionNotInitialized(Exception): ...
```

브로커별 초기화 로직:

| 브로커 | 필수 설정 | 초기화 클래스 |
|---|---|---|
| KIS | `kis_app_key`, `kis_secret_key`, `kis_env` | `cluefin_openapi.kis._auth.Auth` → `KisHttpClient` |
| Kiwoom | `kiwoom_app_key`, `kiwoom_secret_key`, `kiwoom_env` | `cluefin_openapi.kiwoom._auth.Auth` → `Client` |
| KRX | `krx_auth_key` | `cluefin_openapi.krx._client.Client` |
| DART | `dart_auth_key` | `cluefin_openapi.dart._client.Client` |

#### 5.2 `middleware/errors.py` — 예외 매핑

```python
def map_exception_to_rpc_error(exc: Exception) -> tuple[int, str, Any]:
    """
    예외 타입 → (code, message, data) 매핑:

    SessionNotInitialized         → -32004 (SESSION_ERROR)
    KIS/Kiwoom AuthenticationError → -32001 (AUTH_ERROR)
    KIS/Kiwoom RateLimitError     → -32002 (RATE_LIMIT_ERROR), retry_after 포함
    KIS/Kiwoom/KRX/DART APIError  → -32003 (BROKER_API_ERROR), status_code/response_data 포함
    ValueError, TypeError          → -32602 (INVALID_PARAMS)
    기타                           → -32603 (INTERNAL_ERROR)
    """
```

### 검증

```sh
# 세션 초기화 (.env에 KIS 키 필요)
echo '{"jsonrpc":"2.0","id":1,"method":"session.initialize","params":{"broker":"kis"}}' | uv run -m cluefin_rpc

# 초기화 없이 시세 호출 → SESSION_ERROR (-32004) 예상
echo '{"jsonrpc":"2.0","id":1,"method":"quote.kis.stock_current","params":{"stock_code":"005930"}}' | uv run -m cluefin_rpc
```

---

## 6. Phase 2: TA (기술 분석, 11개)

### 목표
기술 분석 지표 11개 메서드. 모두 `requires_session=False` — **Phase 0 직후 독립 구현 가능**.

### 선행 Phase
Phase 0 (Phase 1 불필요)

### 구현 모듈

`handlers/ta.py` — 모든 메서드는 numpy 배열 입출력.

입력 배열은 `list[float]` → `np.array(x, dtype=np.float64)` 변환.
NaN 값은 None으로 변환하여 JSON 직렬화.

### 메서드 테이블

| RPC 메서드 | cluefin-ta 함수 | 파라미터 | 반환 |
|---|---|---|---|
| `ta.sma` | `SMA(close, timeperiod)` | close (필수), timeperiod=14 | 배열 |
| `ta.ema` | `EMA(close, timeperiod)` | close (필수), timeperiod=14 | 배열 |
| `ta.rsi` | `RSI(close, timeperiod)` | close (필수), timeperiod=14 | 배열 |
| `ta.macd` | `MACD(close, fast, slow, signal)` | close (필수), fastperiod=12, slowperiod=26, signalperiod=9 | {macd, signal, hist} |
| `ta.bbands` | `BBANDS(close, timeperiod, nbdevup, nbdevdn)` | close (필수), timeperiod=20, nbdevup=2.0, nbdevdn=2.0 | {upper, middle, lower} |
| `ta.stoch` | `STOCH(high, low, close, fastk, slowk, slowd)` | high, low, close (필수), fastk_period=14, slowk_period=3, slowd_period=3 | {slowk, slowd} |
| `ta.adx` | `ADX(high, low, close, timeperiod)` | high, low, close (필수), timeperiod=14 | 배열 |
| `ta.atr` | `ATR(high, low, close, timeperiod)` | high, low, close (필수), timeperiod=14 | 배열 |
| `ta.obv` | `OBV(close, volume)` | close, volume (필수) | 배열 |
| `ta.mdd` | `MDD(returns)` | returns (필수) | 스칼라 |
| `ta.sharpe` | `SHARPE(returns, rf, periods)` | returns (필수), risk_free_rate=0.0, periods_per_year=252 | 스칼라 |

### 검증

```sh
# SMA 계산
echo '{"jsonrpc":"2.0","id":1,"method":"ta.sma","params":{"close":[1,2,3,4,5,6,7,8,9,10],"timeperiod":3}}' | uv run -m cluefin_rpc

# RSI 계산
echo '{"jsonrpc":"2.0","id":1,"method":"ta.rsi","params":{"close":[44,44.34,44.09,43.61,44.33,44.83,45.10,45.42,45.84,46.08,45.89,46.03,45.61,46.28,46.28,46.00,46.03,46.41,46.22,46.21],"timeperiod":14}}' | uv run -m cluefin_rpc

# Sharpe Ratio
echo '{"jsonrpc":"2.0","id":1,"method":"ta.sharpe","params":{"returns":[0.01,-0.02,0.03,0.01,-0.01,0.02]}}' | uv run -m cluefin_rpc
```

---

## 7. Phase 3: Quote (시세, 12개)

### 목표
KIS 시세 6 + Kiwoom 차트 4 + KRX 지수 2 = 12개 읽기 전용 시세 조회 메서드.

### 선행 Phase
Phase 0 + Phase 1 (세션 필요)

### 구현 모듈

`handlers/quote.py`

핸들러 시그니처 — 세션 의존:
```python
@rpc_method(name="quote.kis.stock_current", ..., category="quote", broker="kis", requires_session=True)
def handle_kis_stock_current(params: dict, session) -> dict:
    kis = session.get_kis()
    response = kis.domestic_basic_quote.get_stock_current_price("J", params["stock_code"])
    return response
```

### 메서드 테이블

#### KIS (6개)

| RPC 메서드 | cluefin-openapi 호출 | 파라미터 |
|---|---|---|
| `quote.kis.stock_current` | `kis.domestic_basic_quote.get_stock_current_price("J", stock_code)` | stock_code (필수), market |
| `quote.kis.stock_daily` | `kis.domestic_basic_quote.get_stock_current_price_daily(...)` | stock_code (필수), market, period, adj_price |
| `quote.kis.stock_period` | `kis.domestic_basic_quote.get_stock_period_quote(...)` | stock_code, start_date, end_date (필수), market, period, adj_price |
| `quote.kis.stock_investor` | `kis.domestic_basic_quote.get_stock_current_price_investor(...)` | stock_code (필수), market |
| `quote.kis.etf_current` | `kis.domestic_basic_quote.get_etfetn_current_price(fid_input_iscd)` | stock_code (필수) |
| `quote.kis.sector_index` | `kis.domestic_issue_other.get_sector_current_index(...)` | market, sector_code (필수) |

#### Kiwoom (4개)

| RPC 메서드 | cluefin-openapi 호출 | 파라미터 |
|---|---|---|
| `quote.kiwoom.stock_daily` | `kiwoom.chart.get_stock_daily(stk_cd, base_dt, upd_stkpc_tp)` | stock_code, base_date (필수), adj_price |
| `quote.kiwoom.stock_minute` | `kiwoom.chart.get_stock_minute(stk_cd, tic_scope)` | stock_code, tic_scope (필수), adj_price |
| `quote.kiwoom.stock_weekly` | `kiwoom.chart.get_stock_weekly(...)` | stock_code, base_date (필수), adj_price |
| `quote.kiwoom.stock_monthly` | `kiwoom.chart.get_stock_monthly(...)` | stock_code, base_date (필수), adj_price |

#### KRX (2개)

| RPC 메서드 | cluefin-openapi 호출 | 파라미터 |
|---|---|---|
| `quote.krx.kospi` | `krx.stock.get_kospi(base_date)` | base_date (필수) |
| `quote.krx.kosdaq` | `krx.stock.get_kosdaq(base_date)` | base_date (필수) |

### 검증

```sh
# KIS 현재가 (세션 초기화 먼저 필요 → 두 줄 파이프)
printf '{"jsonrpc":"2.0","id":1,"method":"session.initialize","params":{"broker":"kis"}}\n{"jsonrpc":"2.0","id":2,"method":"quote.kis.stock_current","params":{"stock_code":"005930"}}\n' | uv run -m cluefin_rpc

# Kiwoom 일봉
printf '{"jsonrpc":"2.0","id":1,"method":"session.initialize","params":{"broker":"kiwoom"}}\n{"jsonrpc":"2.0","id":2,"method":"quote.kiwoom.stock_daily","params":{"stock_code":"005930","base_date":"20250101"}}\n' | uv run -m cluefin_rpc

# KRX 코스피
printf '{"jsonrpc":"2.0","id":1,"method":"session.initialize","params":{"broker":"krx"}}\n{"jsonrpc":"2.0","id":2,"method":"quote.krx.kospi","params":{"base_date":"20250224"}}\n' | uv run -m cluefin_rpc
```

---

## 8. Phase 4: Account + DART (11개)

### 목표
계좌 조회 7개 + 공시 조회 4개. 모두 **세션 필요, 읽기 전용** — 주문 실행은 노출하지 않는다.

### 선행 Phase
Phase 0 + Phase 1 (세션 필요)

### 구현 모듈

`handlers/account.py`, `handlers/dart.py`

### 메서드 테이블 — Account (7개)

#### KIS (3개)

| RPC 메서드 | cluefin-openapi 호출 | 파라미터 |
|---|---|---|
| `account.kis.balance` | `kis.domestic_account.get_stock_balance(...)` | inqr_dvsn (01: 요약, 02: 상세, 기본 02) |
| `account.kis.tradable_buy` | `kis.domestic_account.get_buy_tradable_inquiry(...)` | inqr_dvsn (기본 01) |
| `account.kis.tradable_sell` | `kis.domestic_account.get_sell_tradable_inquiry(...)` | stock_code (필수) |

#### Kiwoom (4개)

| RPC 메서드 | cluefin-openapi 호출 | 파라미터 |
|---|---|---|
| `account.kiwoom.balance` | `kiwoom.account.get_execution_balance(dmst_stex_tp)` | exchange (KRX/NXT, 기본 KRX) |
| `account.kiwoom.executed` | `kiwoom.account.get_executed(qry_tp, sell_tp, stex_tp)` | qry_tp, sell_tp, stex_tp (기본 0) |
| `account.kiwoom.unexecuted` | `kiwoom.account.get_unexecuted(all_stk_tp, trde_tp, stex_tp)` | all_stk_tp, trde_tp, stex_tp (기본 0) |
| `account.kiwoom.profit_loss` | `kiwoom.account.get_daily_realized_profit_loss(strt_dt, end_dt)` | start_date, end_date (필수, YYYYMMDD) |

### 메서드 테이블 — DART (4개)

| RPC 메서드 | cluefin-openapi 호출 | 파라미터 |
|---|---|---|
| `dart.disclosure_search` | `dart.public_disclosure.public_disclosure_search(...)` | corp_code, bgn_de, end_de, last_reprt_at, pblntf_ty, corp_cls, page_no, page_count |
| `dart.company_overview` | `dart.public_disclosure.company_overview(corp_code)` | corp_code (필수) |
| `dart.corp_code_lookup` | `dart.public_disclosure.corp_code()` → XML 파싱 | (없음) |
| `dart.major_shareholder` | `dart.periodic_report_key_information.get_major_shareholder_status(...)` | corp_code, bsns_year, reprt_code (필수: 11013/11012/11014/11011) |

### 검증

```sh
# KIS 잔고
printf '{"jsonrpc":"2.0","id":1,"method":"session.initialize","params":{"broker":"kis"}}\n{"jsonrpc":"2.0","id":2,"method":"account.kis.balance","params":{}}\n' | uv run -m cluefin_rpc

# DART 기업 개황
printf '{"jsonrpc":"2.0","id":1,"method":"session.initialize","params":{"broker":"dart"}}\n{"jsonrpc":"2.0","id":2,"method":"dart.company_overview","params":{"corp_code":"00126380"}}\n' | uv run -m cluefin_rpc
```

---

## 9. Phase 의존 관계

```
Phase 0 (Foundation)
 │  protocol, dispatcher, config, server, session handlers (5 meta)
 │
 ├──→ Phase 1 (Session + Middleware)
 │      SessionManager, 에러 매핑
 │      │
 │      ├──→ Phase 3 (Quote, 12개)
 │      │      KIS 6 + Kiwoom 4 + KRX 2
 │      │
 │      └──→ Phase 4 (Account + DART, 11개)
 │             Account 7 + DART 4
 │
 └──→ Phase 2 (TA, 11개)  ← 독립, Phase 0 직후 가능
        requires_session=False, numpy 기반
```

**핵심 포인트:**
- Phase 2(TA)는 `requires_session=False`이므로 Phase 1 없이 Phase 0 직후 구현 가능
- Phase 3과 Phase 4는 모두 세션이 필요하므로 Phase 1이 선행되어야 함
- Phase 3과 Phase 4는 서로 독립적이므로 병렬 구현 가능

---

## 10. 전체 메서드 레지스트리 (39개)

### Meta (5개, requires_session=False)

| # | RPC 메서드 | 핸들러 모듈 | broker |
|---|---|---|---|
| 1 | `rpc.ping` | session.py | — |
| 2 | `rpc.list_methods` | session.py | — |
| 3 | `session.initialize` | session.py | — |
| 4 | `session.status` | session.py | — |
| 5 | `session.close` | session.py | — |

### Quote (12개, requires_session=True)

| # | RPC 메서드 | 핸들러 모듈 | broker |
|---|---|---|---|
| 6 | `quote.kis.stock_current` | quote.py | kis |
| 7 | `quote.kis.stock_daily` | quote.py | kis |
| 8 | `quote.kis.stock_period` | quote.py | kis |
| 9 | `quote.kis.stock_investor` | quote.py | kis |
| 10 | `quote.kis.etf_current` | quote.py | kis |
| 11 | `quote.kis.sector_index` | quote.py | kis |
| 12 | `quote.kiwoom.stock_daily` | quote.py | kiwoom |
| 13 | `quote.kiwoom.stock_minute` | quote.py | kiwoom |
| 14 | `quote.kiwoom.stock_weekly` | quote.py | kiwoom |
| 15 | `quote.kiwoom.stock_monthly` | quote.py | kiwoom |
| 16 | `quote.krx.kospi` | quote.py | krx |
| 17 | `quote.krx.kosdaq` | quote.py | krx |

### TA (11개, requires_session=False)

| # | RPC 메서드 | 핸들러 모듈 | broker |
|---|---|---|---|
| 18 | `ta.sma` | ta.py | — |
| 19 | `ta.ema` | ta.py | — |
| 20 | `ta.rsi` | ta.py | — |
| 21 | `ta.macd` | ta.py | — |
| 22 | `ta.bbands` | ta.py | — |
| 23 | `ta.stoch` | ta.py | — |
| 24 | `ta.adx` | ta.py | — |
| 25 | `ta.atr` | ta.py | — |
| 26 | `ta.obv` | ta.py | — |
| 27 | `ta.mdd` | ta.py | — |
| 28 | `ta.sharpe` | ta.py | — |

### Account (7개, requires_session=True)

| # | RPC 메서드 | 핸들러 모듈 | broker |
|---|---|---|---|
| 29 | `account.kis.balance` | account.py | kis |
| 30 | `account.kis.tradable_buy` | account.py | kis |
| 31 | `account.kis.tradable_sell` | account.py | kis |
| 32 | `account.kiwoom.balance` | account.py | kiwoom |
| 33 | `account.kiwoom.executed` | account.py | kiwoom |
| 34 | `account.kiwoom.unexecuted` | account.py | kiwoom |
| 35 | `account.kiwoom.profit_loss` | account.py | kiwoom |

### DART (4개, requires_session=True)

| # | RPC 메서드 | 핸들러 모듈 | broker |
|---|---|---|---|
| 36 | `dart.disclosure_search` | dart.py | dart |
| 37 | `dart.company_overview` | dart.py | dart |
| 38 | `dart.corp_code_lookup` | dart.py | dart |
| 39 | `dart.major_shareholder` | dart.py | dart |

---

## 11. 실행 및 테스트 방법

### 서버 실행
```sh
cd cluefin
echo '{"jsonrpc":"2.0","id":1,"method":"rpc.ping"}' | uv run -m cluefin_rpc
```

### 테스트 실행
```sh
cd cluefin

# 전체 테스트
uv run pytest apps/cluefin-rpc/tests/

# 개별 모듈
uv run pytest apps/cluefin-rpc/tests/test_protocol.py     # protocol (14 tests)
uv run pytest apps/cluefin-rpc/tests/test_dispatcher.py    # dispatcher (8 tests)
```

### 핸들러 패턴 요약

**패턴 1 — Stateless (session 불필요)**
```python
@rpc_method(name="rpc.ping", ..., requires_session=False)
def handle_ping(params: dict) -> dict:
    return {"status": "ok", "timestamp": ...}
```

**패턴 2 — Session 의존**
```python
@rpc_method(name="quote.kis.stock_current", ..., broker="kis", requires_session=True)
def handle_kis_stock_current(params: dict, session) -> dict:
    kis = session.get_kis()
    return kis.domestic_basic_quote.get_stock_current_price(...)
```

**패턴 3 — Kwargs 의존성 주입**
```python
@rpc_method(name="rpc.list_methods", ..., requires_session=False)
def handle_list_methods(params: dict, *, _dispatcher: Dispatcher | None = None) -> list[dict]:
    return _dispatcher.list_methods(...)
```

### RPC 메서드 명명 규칙
```
{category}.{broker?}.{action}
```
- `rpc.ping` — category=rpc, action=ping
- `quote.kis.stock_current` — category=quote, broker=kis, action=stock_current
- `ta.sma` — category=ta, action=sma (broker 없음)
- `dart.company_overview` — category=dart, action=company_overview (broker=dart)
