# cluefin-ta

NumPy 만으로 구현한 기술적 분석 함수 모음입니다. 두 부분으로 되어 있습니다.

- **TA-Lib 과 같은 값을 내는 지표** — 이동평균·모멘텀·변동성·거래량 지표와 캔들 패턴. C TA-Lib 을 테스트 기준값으로 두고
  NaN 구간 길이까지 맞춥니다.
- **TA-Lib 에 없는 것** — 포트폴리오 성과 지표(`MDD`·`SHARPE`·`PERFORMANCE` 등)와 시장 레짐 판정(`REGIME_*`).

함수 목록은 `src/cluefin_ta/__init__.py`, 인자와 반환값은 각 함수 docstring 에 있습니다.

## 왜 따로 있는가

`cluefin-openapi-cli`(`kis chart technical`, `cache perf`)와 `cluefin-desk`(차트, ML 피처)가 같은 지표 정의를 쓰도록 한 곳에 둔
패키지입니다. 2026-10-11 에 C TA-Lib 으로 바꾸는 안을 검토하고 유지하기로 했습니다. 레짐·성과 지표는 C TA-Lib 에 없어 어차피
남고, 그 코드를 앱으로 옮기면 두 앱에 복제됩니다. C TA-Lib 은 테스트 기준값으로만 쓰는 dev 의존성입니다.

## 설치

PyPI 에 배포하지 않는 uv 워크스페이스 멤버입니다. 저장소 루트에서 `uv sync --all-packages` 로 설치합니다.
`REGIME_HMM` 은 `hmmlearn`(`hmm` extra)이 있어야 하고, 없으면 `ImportError` 가 납니다.

## 예제

```python
import numpy as np
from cluefin_ta import MACD, PERFORMANCE, PERIODIC_RATE, REGIME_MA, RSI, SMA

rng = np.random.default_rng(0)
close = 50_000 * np.exp(np.cumsum(rng.normal(0, 0.02, 300)))  # 오래된 순 float 배열
index = 2_500 * np.exp(np.cumsum(rng.normal(0, 0.01, 300)))  # 같은 날짜의 벤치마크 종가

sma20 = SMA(close, timeperiod=20)  # 앞 19개는 NaN (TA-Lib 과 같은 길이)
rsi = RSI(close, timeperiod=14)
macd, signal, hist = MACD(close)  # 세 출력 모두 앞 33개가 NaN
regime = REGIME_MA(close)  # 0=하락, 1=횡보, 2=상승

stats = PERFORMANCE(close, benchmark=index, risk_free=PERIODIC_RATE(0.035))
print(stats["cagr"], stats["mdd"], stats["sharpe"], stats["beta"])
```

## 걸리는 곳

- **"import 만 바꾸면 된다"는 절반만 맞습니다.** `import cluefin_ta as talib` 로 옮길 수 있는 것은 여기 있는 지표를 기본 옵션으로
  부를 때뿐입니다.
  - `BBANDS`·`STOCH`·`STOCHF` 의 `matype` 계열 인자에 0(SMA)이 아닌 값을 주면 `ValueError` 입니다. 예전에는 받기만 하고
    SMA 로 계산해, 다른 이동평균을 요청해도 경고 없이 SMA 값이 나왔습니다.
  - `BETA` 는 TA-Lib 에도 있는 이름이지만 그 함수의 재구현이 아닙니다. 여기서는 날짜를 맞춘 벤치마크 수익률 대비 베타
    스칼라 하나를 돌려줍니다.
- **`risk_free` 는 기간당 값입니다**(스칼라 또는 `returns` 와 같은 길이의 배열). 연 3.5% 국고채를 그대로 넣으면 매일 3.5% 를
  빼는 셈이니 `PERIODIC_RATE(0.035)` 로 바꿔 넣습니다. ECOS 일별 금리 계열은 퍼센트라 100 으로 나눠 `PERIODIC_RATE` 에 배열째
  넣고, 수익률과 같은 날짜로 맞춥니다.
- **값을 정의할 수 없을 때 돌려주는 값이 함수마다 다릅니다.** `SHARPE`·`SORTINO`·`BETA`·`ALPHA` 는 표본이 2개 미만이거나
  변동성(벤치마크 분산)이 0 이면 NaN 입니다. 0.0 은 "초과수익 없음"으로 읽히기 때문입니다. `MDD`·`CAGR`·`VOLATILITY`·`CALMAR`
  는 빈 입력이나 짧은 입력에 0.0 을 돌려줍니다. 거래정지 종목처럼 가격이 움직이지 않으면 샤프는 NaN 입니다.
- **`SORTINO` 의 하방편차는 전체 기간 수로 나눕니다.** 손실 난 기간 수로만 나누는 구현보다 소르티노 값이 크게 나옵니다.
- **CAGR 기본값은 1년을 252거래일로 봅니다.** KRX 는 1년에 약 245거래일이라 달력과 어긋납니다. 달력 기준으로 보려면
  `PERFORMANCE(..., years=달력일수 / 365.25)` 를 줍니다.
- **벤치마크 배열은 길이가 다르면 `ValueError` 입니다.** 날짜가 안 맞는 배열을 조용히 자르지 않습니다. 거래정지일은 양쪽에서
  빼거나 양쪽에서 채운 뒤 넣습니다.
- **레짐 함수는 모든 봉을 그 봉까지의 데이터만으로 판정합니다.** 변동성 기준선은 그 시점까지의 NATR 퍼센타일이고, HMM 은
  그 시점까지의 수익률로 학습(`refit_every` 마다 재학습)한 모델의 필터링 확률을 씁니다. 백테스트나 ML 피처에 그대로 넣어도
  미래 정보가 섞이지 않는 대신, 같은 봉의 값이 "전체 구간으로 한 번 학습한" 결과와 다릅니다.
- **`CDLENGULFING` 은 ±100 만 내지 않습니다.** 몸통 한쪽 끝이 앞 봉 몸통 끝과 같으면 ±80 입니다(TA-Lib 과 같음). `== 100` 으로
  거르면 이 봉들이 빠집니다.
- **CLI 의 `trend-setup` 수치와는 일부러 다릅니다.** 그쪽은 백테스트 공식을 옮긴 것이라 이 패키지를 쓰지 않습니다(이유는
  `AGENTS.md`).

## 예제 노트북

`examples/ta_quickstart.ipynb` 는 실제 시세로 지표·차트·해석·ML 피처 흐름을 따라갑니다. 저장소 루트에서 실행합니다.

```bash
uv run --with jupyter jupyter lab packages/cluefin-ta/examples/ta_quickstart.ipynb
```

루트 `.env.test` 의 KIS 키를 쓰는데, `.env.test` 의 KIS 는 모의가 아니라 **실서버**입니다. 노트북은 시세 조회만 하지만 토큰은
실계좌 키로 발급됩니다.
