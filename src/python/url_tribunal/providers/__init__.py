"""Security scan providers package."""

from url_tribunal.providers.base import BaseHTTPProvider, BaseProvider
from url_tribunal.providers.exceptions import (
    ProviderError,
    ProviderInfrastructureError,
    ProviderResultNotReadyError,
    UnknownProviderError,
)
from url_tribunal.providers.factory import HTTPProviderFactory
from url_tribunal.providers.urlscan import UrlScanProvider
from url_tribunal.providers.virustotal import VirusTotalProvider

__all__ = [
    'BaseProvider',
    'BaseHTTPProvider',
    'UrlScanProvider',
    'VirusTotalProvider',
    'HTTPProviderFactory',
    'ProviderError',
    'ProviderResultNotReadyError',
    'ProviderInfrastructureError',
    'UnknownProviderError',
]
