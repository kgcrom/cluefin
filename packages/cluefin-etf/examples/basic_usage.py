import logging

from cluefin_etf import EtfClient, EtfSummary, ProviderName, get_provider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_sample_items(provider: ProviderName, items: list[EtfSummary]) -> None:
    logger.info("%s items=%s", provider.value, len(items))
    for item in items[:3]:
        logger.info(
            "%s %s name=%s category=%s nav=%s aum=%s",
            item.provider.value,
            item.code,
            item.name,
            item.category,
            item.nav,
            item.aum,
        )


def main() -> None:
    for provider_name in (ProviderName.KODEX, ProviderName.KIWOOM, ProviderName.RISE):
        provider = get_provider(provider_name)
        logger.info("provider=%s", provider.info)

        client = EtfClient(provider_name)
        log_sample_items(provider_name, client.fetch_list())


if __name__ == "__main__":
    main()
