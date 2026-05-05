import argparse
import logging

from cluefin_etf import EtfClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch ACE ETF list.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of items to print. Defaults to all.")
    args = parser.parse_args()

    client = EtfClient("ace")
    items = client.fetch_list()
    display_items = items[: args.limit] if args.limit is not None else items

    logger.info("fetched %s ACE ETF items; printing %s", len(items), len(display_items))
    for item in display_items:
        logger.info(
            "fund_code=%s isin=%s name=%s category=%s pension_flags=%s detail_url=%s",
            item.code,
            item.isin,
            item.name,
            item.category,
            item.raw.get("pensionFlags"),
            item.detail_url,
        )


if __name__ == "__main__":
    main()
