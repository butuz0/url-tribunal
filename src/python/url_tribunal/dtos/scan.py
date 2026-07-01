"""Data Transfer Objects for Scan entity."""

import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from url_tribunal.core.enums import ScanStatus, Verdict
from url_tribunal.dtos.provider_scan import ProviderScanDTO


class ScanDTO(BaseModel):
    """Scan Data Transfer Object."""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    url_id: int
    status: ScanStatus
    verdict: Verdict
    verdict_confidence: float = Field(ge=0.0, le=1.0)
    scanned_at: Optional[dt.datetime]


class ScanDetailDTO(ScanDTO):
    """Scan with provider results Data Transfer Object."""

    provider_scans: list[ProviderScanDTO] = Field(default_factory=list)

    @classmethod
    def from_components(
            cls,
            scan_dto: ScanDTO,
            provider_scans: list[ProviderScanDTO],
    ) -> 'ScanDetailDTO':
        """Combine base scan DTO and provider scans into a detail DTO."""

        return cls(
            provider_scans=provider_scans,
            **scan_dto.model_dump(),
        )


class ScanCreateDTO(BaseModel):
    """Data Transfer Object for Scan creation."""

    url_id: int


class ScanCompleteDTO(BaseModel):
    """Data Transfer Object for successful security scan execution."""

    verdict: Verdict
    verdict_confidence: float = Field(ge=0.0, le=1.0)
    scanned_at: dt.datetime


class ScanFailDTO(BaseModel):
    """Data Transfer Object for unsuccessful security scan execution."""

    failed_at: dt.datetime
