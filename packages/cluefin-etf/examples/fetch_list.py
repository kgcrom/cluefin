import argparse
import logging

from cluefin_etf import EtfClient, ProviderCapabilityError, ProviderName, list_providers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch ETF list for one provider.")
    parser.add_argument(
        "provider",
        choices=[provider.value for provider in list_providers()],
        help="ETF provider to fetch.",
    )
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of items to print. Defaults to 10.")
    args = parser.parse_args()

    provider = ProviderName(args.provider)
    client = EtfClient(provider)

    try:
        items = client.fetch_list()
    except ProviderCapabilityError as exc:
        logger.error("%s list fetch is not available yet: %s", provider.value, exc)
        return

    display_items = items[: args.limit] if args.limit is not None else items
    logger.info("fetched %s %s ETF items; printing %s", len(items), provider.value, len(display_items))

    for item in display_items:
        logger.info(
            "provider=%s code=%s isin=%s name=%s category=%s benchmark=%s listing_date=%s "
            "nav=%s aum=%s as_of_date=%s detail_url=%s",
            item.provider.value,
            item.code,
            item.isin,
            item.name,
            item.category,
            item.benchmark,
            item.listing_date,
            item.nav,
            item.aum,
            item.as_of_date,
            item.detail_url,
        )


if __name__ == "__main__":
    main()
