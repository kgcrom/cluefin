# TODO

## cluefin-etf provider list implementation

- Implement ETF list fetching provider by provider.
- Keep provider-specific list response entities separate while each provider is being implemented.
- After all provider list implementations are complete, review the provider entities and parsers together.
- Commonize only the parts that are demonstrably shared across providers.
- Keep provider-specific behavior separated when response shape, pagination, transport, or field semantics differ.

## Provider notes

- KODEX list fields are mapped from the product table semantics:
  - `basp` is iNAV in KRW, mapped to `EtfSummary.nav`.
  - `nav` is net assets in KRW 100M units, mapped to `EtfSummary.aum`.
  - `curp`, `risep`, `risepRt`, `basrp`, `basrpRt`, period yields, and pension flags stay in provider `raw`.
- ACE allfund is a Next.js static chunk-backed list:
  - `/modal/allfund` is used to discover the current `allfund-*.js` chunk.
  - The list exposes fundCode/ISIN-like identifiers, not 6-digit exchange tickers.
  - Until ACE detail is implemented, `EtfSummary.code` and `EtfSummary.isin` both use the allfund fundCode.
  - 6-digit stock code, NAV, AUM, and other detail fields should be filled from ACE detail data later.
- SOL list is a server-rendered HTML table:
  - `/ko/fund` is the primary list source and should be fetched with request first.
  - The row detail URL exposes SOL `FUND_CD`; the visible product name contains the exchange code in parentheses.
  - `EtfSummary.code` uses the visible exchange code, while SOL `FUND_CD`, badges, pension flags, and return columns stay in provider `raw`.
  - The displayed net asset value is in KRW 100M units and is mapped as shown to `EtfSummary.aum`.
