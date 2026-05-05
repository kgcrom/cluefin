from cluefin_etf._models import ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider


class KiwoomProvider(EtfProvider):
    info = ProviderInfo(name=ProviderName.KIWOOM, display_name="Kiwoom")
