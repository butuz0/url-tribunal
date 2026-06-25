"""DB repositories package."""

from url_tribunal.db.repositories.scan import ScanRepository
from url_tribunal.db.repositories.url import UrlRepository

__all__ = [
    'ScanRepository',
    'UrlRepository',
]
