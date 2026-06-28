"""Data Transfer Objects package."""

from url_tribunal.dtos.provider import ProviderScanResultDTO
from url_tribunal.dtos.provider_scan import ProviderScanDTO
from url_tribunal.dtos.scan import ScanDetailDTO, ScanDTO
from url_tribunal.dtos.url import UrlDTO

__all__ = [
    'ProviderScanResultDTO',
    'ProviderScanDTO',
    'ScanDetailDTO',
    'ScanDTO',
    'UrlDTO',
]
