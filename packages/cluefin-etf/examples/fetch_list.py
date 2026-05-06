import argparse
import logging
import textwrap

from cluefin_etf import EtfClient, EtfSummary, FetchError, ProviderCapabilityError, ProviderName, list_providers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_item(item: EtfSummary, *, include_raw: bool) -> None:
    logger.info(
        "provider=%s code=%s isin=%s name=%s category=%s benchmark=%s listing_date=%s "
        "nav=%s aum=%s expense_ratio=%s as_of_date=%s detail_url=%s holdings_url=%s",
        item.provider.value,
        item.code,
        item.isin,
        item.name,
        item.category,
        item.benchmark,
        item.listing_date,
        item.nav,
        item.aum,
        item.expense_ratio,
        item.as_of_date,
        item.detail_url,
        item.holdings_url,
    )
    if include_raw:
        logger.info("raw=%s", item.raw)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch ETF list for one provider.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              uv run python packages/cluefin-etf/examples/fetch_list.py ace --limit 5
              uv run python packages/cluefin-etf/examples/fetch_list.py kiwoom --limit 5
              uv run python packages/cluefin-etf/examples/fetch_list.py kodex --limit 5
              uv run python packages/cluefin-etf/examples/fetch_list.py sol --limit 5
              uv run python packages/cluefin-etf/examples/fetch_list.py tiger --limit 5
            """
        ),
    )
    parser.add_argument(
        "provider",
        choices=[provider.value for provider in list_providers()],
        help="ETF provider to fetch.",
    )
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of items to print. Defaults to 10.")
    parser.add_argument("--raw", action="store_true", help="Print provider-specific raw payload fields.")
    args = parser.parse_args()

    provider = ProviderName(args.provider)
    client = EtfClient(provider)

    try:
        items = client.fetch_list()
    except ProviderCapabilityError as exc:
        logger.error("%s list fetch is not available yet: %s", provider.value, exc)
        return
    except FetchError as exc:
        logger.error("%s list fetch failed: %s", provider.value, exc)
        return

    display_items = items[: args.limit] if args.limit is not None else items
    logger.info("fetched %s %s ETF items; printing %s", len(items), provider.value, len(display_items))

    for item in display_items:
        log_item(item, include_raw=args.raw)


if __name__ == "__main__":
    main()
