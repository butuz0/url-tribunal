"""Data Transfer Objects package."""

from url_tribunal.dtos.domain import DomainCreateDTO, DomainDTO
from url_tribunal.dtos.provider import ProviderScanResultDTO
from url_tribunal.dtos.provider_scan import (
    ProviderScanCompleteDTO,
    ProviderScanCreateDTO,
    ProviderScanDTO,
)
from url_tribunal.dtos.scan import (
    ScanCompleteDTO,
    ScanCreateDTO,
    ScanDetailDTO,
    ScanDTO,
    ScanFailDTO,
)
from url_tribunal.dtos.url import (
    UrlCreateDTO,
    UrlDTO,
    UrlUpdateLastScanDTO,
)

__all__ = [
    'DomainCreateDTO',
    'ScanCompleteDTO',
    'DomainDTO',
    'ProviderScanResultDTO',
    'ProviderScanCreateDTO',
    'ProviderScanCompleteDTO',
    'ProviderScanDTO',
    'ScanCreateDTO',
    'ScanDetailDTO',
    'ScanDTO',
    'ScanFailDTO',
    'UrlDTO',
    'UrlCreateDTO',
    'UrlUpdateLastScanDTO',
]
