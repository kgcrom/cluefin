from cluefin_etf._models import ProviderInfo, ProviderName
from cluefin_etf._provider import EtfProvider


class SolProvider(EtfProvider):
    info = ProviderInfo(name=ProviderName.SOL, display_name="SOL")
