class CluefinEtfError(Exception):
    """Base exception for cluefin-etf."""


class FetchError(CluefinEtfError):
    """Raised when a page cannot be fetched."""


class ProviderNotFoundError(CluefinEtfError):
    """Raised when a provider name is not registered."""


class ProviderCapabilityError(CluefinEtfError):
    """Raised when a provider capability is not implemented yet."""
