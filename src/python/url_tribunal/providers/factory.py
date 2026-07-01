"""Security scan providers factory module."""

from url_tribunal.core.config import Settings
from url_tribunal.core.enums import ProviderName
from url_tribunal.providers.base import BaseHTTPProvider
from url_tribunal.providers.exceptions import UnknownProviderError
from url_tribunal.providers.urlscan import UrlScanProvider
from url_tribunal.providers.virustotal import VirusTotalProvider


class HTTPProviderFactory:
    """HTTP security scan providers factory."""

    _providers = {
        ProviderName.URLSCAN: (UrlScanProvider, lambda s: s.providers.urlscan_api_key),
        ProviderName.VIRUSTOTAL: (VirusTotalProvider, lambda s: s.providers.virustotal_api_key),
    }

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get_provider(self, provider_name: ProviderName) -> BaseHTTPProvider:
        """Initialize and return the requested provider instance."""

        if provider_name not in self._providers:
            raise UnknownProviderError(f'Provider {provider_name} is not supported.')

        provider_class, key_getter = self._providers[provider_name]
        api_key = key_getter(self._settings)

        if not api_key:
            raise ValueError(f'{provider_name} API key is missing in settings.')

        return provider_class(api_key=api_key)
