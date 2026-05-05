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
