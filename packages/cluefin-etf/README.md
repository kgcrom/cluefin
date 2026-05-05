# cluefin-etf

Research-oriented package for Korean ETF page scraping.

The package defines shared fetchers, a provider registry, and provider
interfaces for KODEX, TIGER, RISE, ACE, SOL, and Kiwoom ETF pages.

## Current Support

| Provider | `fetch_list` | `fetch_detail` |
| --- | --- | --- |
| KODEX | Implemented | Not implemented |
| TIGER | Not implemented | Not implemented |
| RISE | Not implemented | Not implemented |
| ACE | Implemented | Not implemented |
| SOL | Implemented | Not implemented |
| Kiwoom | Implemented | Not implemented |

## Usage

```python
from cluefin_etf import EtfClient

kodex_items = EtfClient("kodex").fetch_list()
kiwoom_items = EtfClient("kiwoom").fetch_list()
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
