"""API schemas package."""

from url_tribunal.api.v1.schemas.provider_scan import ProviderScanSchema
from url_tribunal.api.v1.schemas.scan import ScanDetailSchema, ScanSchema
from url_tribunal.api.v1.schemas.url import UrlSchema

__all__ = [
    'ProviderScanSchema',
    'ScanDetailSchema',
    'ScanSchema',
    'UrlSchema',
]
