import argparse
import logging

from cluefin_etf import EtfClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch KODEX ETF list.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of items to print. Defaults to all.")
    args = parser.parse_args()

    client = EtfClient("kodex")
    items = client.fetch_list()
    display_items = items[: args.limit] if args.limit is not None else items

    logger.info("fetched %s KODEX ETF items; printing %s", len(items), len(display_items))
    for item in display_items:
        logger.info(
            (
                "code=%s name=%s category=%s listing_date=%s as_of_date=%s "
                "current_price=%s price_change=%s price_change_rate=%s "
                "inav=%s inav_change=%s inav_change_rate=%s aum_100m_krw=%s "
                "return_1w=%s return_1m=%s return_3m=%s return_6m=%s "
                "return_1y=%s return_3y=%s return_ytd=%s return_since_listing=%s "
                "personal_pension=%s retirement_pension=%s detail_url=%s"
            ),
            item.code,
            item.name,
            item.category,
            item.listing_date,
            item.as_of_date,
            item.raw.get("curp"),
            item.raw.get("risep"),
            item.raw.get("risepRt"),
            item.nav,
            item.raw.get("basrp"),
            item.raw.get("basrpRt"),
            item.aum,
            item.raw.get("yieldWeek"),
            item.raw.get("yieldMon1"),
            item.raw.get("yieldMon3"),
            item.raw.get("yieldMon6"),
            item.raw.get("yieldYear1"),
            item.raw.get("yieldYear3"),
            item.raw.get("yieldYear"),
            item.raw.get("yieldList"),
            item.raw.get("dcYn"),
            item.raw.get("irpYn"),
            item.detail_url,
        )


if __name__ == "__main__":
    main()
