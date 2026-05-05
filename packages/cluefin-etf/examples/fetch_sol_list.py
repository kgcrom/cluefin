import argparse
import logging

from cluefin_etf import EtfClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch SOL ETF list.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of items to print. Defaults to all.")
    args = parser.parse_args()

    client = EtfClient("sol")
    items = client.fetch_list()
    display_items = items[: args.limit] if args.limit is not None else items

    logger.info("fetched %s SOL ETF items; printing %s", len(items), len(display_items))
    for item in display_items:
        logger.info(
            (
                "code=%s name=%s fund_code=%s category=%s nav=%s aum=%s "
                "pension_flags=%s return_1w=%s return_1m=%s return_3m=%s "
                "return_6m=%s return_ytd=%s return_1y=%s return_3y=%s "
                "return_5y=%s return_since_listing=%s detail_url=%s"
            ),
            item.code,
            item.name,
            item.raw.get("fundCode"),
            item.category,
            item.nav,
            item.aum,
            item.raw.get("pensionFlags"),
            item.raw.get("returns", {}).get("week_1"),
            item.raw.get("returns", {}).get("month_1"),
            item.raw.get("returns", {}).get("month_3"),
            item.raw.get("returns", {}).get("month_6"),
            item.raw.get("returns", {}).get("ytd"),
            item.raw.get("returns", {}).get("year_1"),
            item.raw.get("returns", {}).get("year_3"),
            item.raw.get("returns", {}).get("year_5"),
            item.raw.get("returns", {}).get("since_listing"),
            item.detail_url,
        )


if __name__ == "__main__":
    main()
