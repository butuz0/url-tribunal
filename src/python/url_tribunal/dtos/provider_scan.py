"""Data Transfer Objects for ProviderScan entity."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from url_tribunal.core.enums import ProviderStatus, Verdict


class ProviderScanDTO(BaseModel):
    """Provider scan Data Transfer Object."""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    provider_name: str
    external_reference_id: Optional[str] = None
    status: ProviderStatus
    verdict: Verdict
    response: Optional[dict[str, Any]] = None


class ProviderScanCreateDTO(BaseModel):
    """Provider scan creation Data Transfer Object."""

    scan_id: int
    provider_name: str
    external_reference_id: Optional[str] = None
    response: Optional[dict[str, Any]] = None


class ProviderScanCompleteDTO(BaseModel):
    """Data Transfer Object for successful provider scan execution."""

    verdict: Verdict
    response: Optional[dict[str, Any]] = None
