from cluefin_etf._errors import ProviderNotFoundError
from cluefin_etf._fetchers import PageFetcher
from cluefin_etf._models import ProviderName
from cluefin_etf._provider import EtfProvider
from cluefin_etf.providers.ace import AceProvider
from cluefin_etf.providers.kiwoom import KiwoomProvider
from cluefin_etf.providers.kodex import KodexProvider
from cluefin_etf.providers.rise import RiseProvider
from cluefin_etf.providers.sol import SolProvider
from cluefin_etf.providers.tiger import TigerProvider

PROVIDER_CLASSES: dict[ProviderName, type[EtfProvider]] = {
    ProviderName.KODEX: KodexProvider,
    ProviderName.TIGER: TigerProvider,
    ProviderName.RISE: RiseProvider,
    ProviderName.ACE: AceProvider,
    ProviderName.SOL: SolProvider,
    ProviderName.KIWOOM: KiwoomProvider,
}


def list_providers() -> tuple[ProviderName, ...]:
    return tuple(PROVIDER_CLASSES)


def get_provider(name: ProviderName | str, fetcher: PageFetcher | None = None) -> EtfProvider:
    try:
        provider_name = ProviderName(name)
        provider_class = PROVIDER_CLASSES[provider_name]
    except (KeyError, ValueError) as exc:
        raise ProviderNotFoundError(f"Unknown ETF provider: {name}") from exc

    return provider_class(fetcher=fetcher)
