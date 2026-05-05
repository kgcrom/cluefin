from cluefin_etf._models import ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider


class AceProvider(EtfProvider):
    info = ProviderInfo(
        name=ProviderName.ACE,
        display_name="ACE",
        homepage_url="https://www.aceetf.co.kr/",
    )
