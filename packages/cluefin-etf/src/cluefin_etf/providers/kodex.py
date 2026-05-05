from cluefin_etf._models import ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider


class KodexProvider(EtfProvider):
    info = ProviderInfo(
        name=ProviderName.KODEX,
        display_name="KODEX",
        homepage_url="https://www.samsungfund.com/etf/main.do",
    )
