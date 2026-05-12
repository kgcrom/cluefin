import argparse
import logging
import textwrap

from cluefin_etf import EtfClient, EtfDetail, FetchError, ProviderCapabilityError, ProviderName, list_providers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROVIDER_SEPARATOR = "=" * 40

DEFAULT_DETAIL_CODES = {
    ProviderName.KODEX: "2ETFN7",
    ProviderName.TIGER: "102110",
    ProviderName.RISE: "252400",
    ProviderName.ACE: "KR5101877748",
    ProviderName.SOL: "210980",
    ProviderName.KIWOOM: "253250",
}


def log_detail(detail: EtfDetail, *, include_raw: bool, holdings_limit: int) -> None:
    logger.info(
        "provider=%s code=%s isin=%s name=%s category=%s benchmark=%s listing_date=%s "
        "nav=%s aum=%s expense_ratio=%s as_of_date=%s detail_url=%s holdings_url=%s holdings=%s",
        detail.provider.value,
        detail.code,
        detail.isin,
        detail.name,
        detail.category,
        detail.benchmark,
        detail.listing_date,
        detail.nav,
        detail.aum,
        detail.expense_ratio,
        detail.as_of_date,
        detail.detail_url,
        detail.holdings_url,
        len(detail.holdings),
    )
    if include_raw:
        logger.info("raw=%s", detail.raw)

    if not detail.holdings:
        logger.info("holdings: no items")
        return

    display_holdings = detail.holdings if holdings_limit < 0 else detail.holdings[:holdings_limit]
    logger.info(
        "holdings items (showing %s of %s): rank code name quantity valuation_amount weight as_of_date",
        len(display_holdings),
        len(detail.holdings),
    )
    for holding in display_holdings:
        logger.info(
            "holding rank=%s code=%s name=%s quantity=%s valuation_amount=%s weight=%s as_of_date=%s",
            holding.rank,
            holding.code,
            holding.name,
            holding.quantity,
            holding.valuation_amount,
            holding.weight,
            holding.as_of_date,
        )
        if include_raw:
            logger.info("holding_raw rank=%s raw=%s", holding.rank, holding.raw)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch detailed ETF information for all supported providers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              uv run python packages/cluefin-etf/examples/fetch_detail.py --holdings-limit 5
            """
        ),
    )
    parser.add_argument("--raw", action="store_true", help="Print provider-specific raw payload fields.")
    parser.add_argument(
        "--holdings-limit",
        type=int,
        default=30,
        help="Maximum number of holdings to print. Use -1 to print all holdings. Defaults to 30.",
    )
    args = parser.parse_args()

    for provider in list_providers():
        fetch_and_log_provider_detail(provider, include_raw=args.raw, holdings_limit=args.holdings_limit)


def fetch_and_log_provider_detail(provider: ProviderName, *, include_raw: bool, holdings_limit: int) -> None:
    code = DEFAULT_DETAIL_CODES[provider]
    logger.info("%s START %s %s", PROVIDER_SEPARATOR, provider.value, PROVIDER_SEPARATOR)

    client = EtfClient(provider)

    try:
        detail = client.fetch_detail(code)
    except ProviderCapabilityError as exc:
        logger.error("%s detail fetch is not available yet: %s", provider.value, exc)
        return
    except FetchError as exc:
        logger.error("%s detail fetch failed for %s: %s", provider.value, code, exc)
        return

    log_detail(detail, include_raw=include_raw, holdings_limit=holdings_limit)


if __name__ == "__main__":
    main()
