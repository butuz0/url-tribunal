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
