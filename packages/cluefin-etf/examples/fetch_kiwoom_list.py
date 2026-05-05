import argparse
import logging

from cluefin_etf import EtfClient, EtfSummary, FetchError, ProviderCapabilityError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_item(item: EtfSummary) -> None:
    logger.info(
        (
            "code=%s name=%s english_name=%s category=%s benchmark=%s listing_date=%s "
            "nav=%s aum=%s return_1m=%s return_3m=%s return_6m=%s return_1y=%s "
            "pension_flags=%s etc_flags=%s detail_url=%s"
        ),
        item.code,
        item.name,
        item.raw.get("goodsEngNm"),
        item.category,
        item.benchmark,
        item.listing_date,
        item.nav,
        item.aum,
        item.raw.get("suik01"),
        item.raw.get("suik03"),
        item.raw.get("suik06"),
        item.raw.get("suik12"),
        item.raw.get("pensionFlags"),
        item.raw.get("etcFlags"),
        item.detail_url,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch Kiwoom ETF list.",
        epilog="Example: uv run python packages/cluefin-etf/examples/fetch_kiwoom_list.py --limit 5",
    )
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of items to print. Defaults to all.")
    args = parser.parse_args()

    client = EtfClient("kiwoom")
    try:
        items = client.fetch_list()
    except ProviderCapabilityError as exc:
        logger.error("Kiwoom list fetch is not available yet: %s", exc)
        return
    except FetchError as exc:
        logger.error("Kiwoom list fetch failed: %s", exc)
        return

    display_items = items[: args.limit] if args.limit is not None else items

    logger.info("fetched %s Kiwoom ETF items; printing %s", len(items), len(display_items))
    for item in display_items:
        log_item(item)


if __name__ == "__main__":
    main()
