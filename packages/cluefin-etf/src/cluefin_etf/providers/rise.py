from cluefin_etf._models import ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider


class RiseProvider(EtfProvider):
    info = ProviderInfo(
        name=ProviderName.RISE,
        display_name="RISE",
        homepage_url="https://www.riseetf.co.kr/",
    )
