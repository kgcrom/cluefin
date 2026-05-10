# cluefin-etf

Research-oriented package for Korean ETF page scraping.

The package defines shared fetchers, a provider registry, and provider
interfaces for KODEX, TIGER, RISE, ACE, SOL, and Kiwoom ETF pages.

## Current Support

| Provider | `fetch_list` | `fetch_detail` |
| --- | --- | --- |
| KODEX | Implemented | Implemented |
| TIGER | Implemented | Implemented |
| RISE | Implemented | Implemented |
| ACE | Implemented | Implemented |
| SOL | Implemented | Implemented |
| Kiwoom | Implemented | Implemented |

## Usage

```python
from cluefin_etf import EtfClient

kodex_items = EtfClient("kodex").fetch_list()
kiwoom_items = EtfClient("kiwoom").fetch_list()
```

## List Lookup Examples

```bash
uv run python packages/cluefin-etf/examples/fetch_list.py kodex --limit 5
uv run python packages/cluefin-etf/examples/fetch_list.py rise --limit 5
uv run python packages/cluefin-etf/examples/fetch_list.py tiger --limit 5
uv run python packages/cluefin-etf/examples/fetch_list.py ace --raw
```

## Detail Lookup Examples

```bash
uv run python packages/cluefin-etf/examples/fetch_detail.py ace KR5101877748
uv run python packages/cluefin-etf/examples/fetch_detail.py kiwoom 253250
uv run python packages/cluefin-etf/examples/fetch_detail.py kodex 2ETFN7
uv run python packages/cluefin-etf/examples/fetch_detail.py rise 252400
uv run python packages/cluefin-etf/examples/fetch_detail.py sol 210980
uv run python packages/cluefin-etf/examples/fetch_detail.py tiger 102110
```

## Tests

Fast unit tests use local fixtures and mocked fetchers:

```bash
uv run pytest packages/cluefin-etf/tests -m "not integration"
```

Integration tests call public provider sites and may fail when a provider site is unavailable or changes its markup/API:

```bash
uv run pytest packages/cluefin-etf/tests -m integration
```

## Provider Homepages

| Provider | Homepage |
| --- | --- |
| KODEX | https://www.samsungfund.com/etf/main.do |
| TIGER | https://investments.miraeasset.com/magi/index.do |
| RISE | https://www.riseetf.co.kr/ |
| ACE | https://www.aceetf.co.kr/ |
| SOL | https://www.soletf.com/ko/main |
| Kiwoom | https://www.kiwoometf.com/ |
