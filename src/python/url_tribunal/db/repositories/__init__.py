"""DB repositories package."""

from url_tribunal.db.repositories.domain import DomainRepository
from url_tribunal.db.repositories.provider_scan import ProviderScanRepository
from url_tribunal.db.repositories.scan import ScanRepository
from url_tribunal.db.repositories.url import UrlRepository

__all__ = [
    'DomainRepository',
    'ProviderScanRepository',
    'ScanRepository',
    'UrlRepository',
]
