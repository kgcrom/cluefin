# cluefin-etf

Research-oriented package for Korean ETF page scraping.

The package defines shared fetchers, a provider registry, and provider
interfaces for KODEX, TIGER, RISE, ACE, SOL, and Kiwoom ETF pages.

## Provider Support

| Provider | `fetch_list` | `fetch_detail` | Homepage |
| --- | --- | --- | --- |
| KODEX | Implemented | Implemented | https://www.samsungfund.com/etf/main.do |
| TIGER | Implemented | Implemented | https://investments.miraeasset.com/magi/index.do |
| RISE | Implemented | Implemented | https://www.riseetf.co.kr/ |
| ACE | Implemented | Implemented | https://www.aceetf.co.kr/ |
| SOL | Implemented | Implemented | https://www.soletf.com/ko/main |
| Kiwoom | Implemented | Implemented | https://www.kiwoometf.com/ |

## Usage

```python
from cluefin_etf import EtfClient

items = EtfClient("kodex").fetch_list()
detail = EtfClient("kodex").fetch_detail("2ETFN7")
```

## Examples

Run examples from the repository root. Both scripts execute all supported providers.

```bash
uv run python packages/cluefin-etf/examples/fetch_list.py --limit 5
uv run python packages/cluefin-etf/examples/fetch_detail.py --holdings-limit 5
```

Use `--raw` to include provider-specific raw fields. Use `--holdings-limit -1` to print all holdings.

## Tests

Fast unit tests use local fixtures and mocked fetchers:

```bash
uv run pytest packages/cluefin-etf/tests -m "not integration"
```

Integration tests call public provider sites and may fail when a provider site is unavailable or changes its markup/API:

```bash
uv run pytest packages/cluefin-etf/tests -m integration
```
