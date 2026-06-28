"""Data Transfer Objects for Scan entity."""

import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

from url_tribunal.core.enums import ScanStatus, Verdict
from url_tribunal.dtos import ProviderScanDTO


class ScanDTO(BaseModel):
    """Scan Data Transfer Object."""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    url_id: int
    status: ScanStatus
    verdict: Verdict
    verdict_confidence: float = Field(ge=0.0, le=1.0)
    scanned_at: dt.datetime


class ScanDetailDTO(ScanDTO):
    """Scan with provider results Data Transfer Object."""

    provider_scans: list[ProviderScanDTO] = Field(default_factory=list)
