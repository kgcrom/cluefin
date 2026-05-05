from cluefin_etf._models import ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider


class TigerProvider(EtfProvider):
    info = ProviderInfo(name=ProviderName.TIGER, display_name="TIGER")
