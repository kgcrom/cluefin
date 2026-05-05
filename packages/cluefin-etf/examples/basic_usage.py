import logging

from cluefin_etf import EtfClient, ProviderName, get_provider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    provider = get_provider(ProviderName.KODEX)
    logger.info("provider=%s", provider.info)

    client = EtfClient("tiger")
    logger.info("items=%s", client.fetch_list())


if __name__ == "__main__":
    main()
