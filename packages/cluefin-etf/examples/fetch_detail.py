import argparse
import logging
import textwrap

from cluefin_etf import EtfClient, EtfDetail, FetchError, ProviderCapabilityError, ProviderName, list_providers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        description="Fetch detailed ETF information for one provider.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            Examples:
              uv run python packages/cluefin-etf/examples/fetch_detail.py ace KR5101877748
              uv run python packages/cluefin-etf/examples/fetch_detail.py kiwoom 253250
              uv run python packages/cluefin-etf/examples/fetch_detail.py kodex 2ETFN7
              uv run python packages/cluefin-etf/examples/fetch_detail.py sol 210980
              uv run python packages/cluefin-etf/examples/fetch_detail.py tiger 102110
            """
        ),
    )
    parser.add_argument(
        "provider",
        choices=[provider.value for provider in list_providers()],
        help="ETF provider to fetch.",
    )
    parser.add_argument(
        "code",
        help=(
            "Provider-specific ETF identifier. Most providers accept a six-digit ticker; "
            "some also accept their own fund code or ISIN."
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

    provider = ProviderName(args.provider)
    client = EtfClient(provider)

    try:
        detail = client.fetch_detail(args.code)
    except ProviderCapabilityError as exc:
        logger.error("%s detail fetch is not available yet: %s", provider.value, exc)
        return
    except FetchError as exc:
        logger.error("%s detail fetch failed for %s: %s", provider.value, args.code, exc)
        return

    log_detail(detail, include_raw=args.raw, holdings_limit=args.holdings_limit)


if __name__ == "__main__":
    main()
