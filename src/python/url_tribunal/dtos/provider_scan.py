"""Data Transfer Objects for ProviderScan entity."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from url_tribunal.core.enums import Verdict


class ProviderScanDTO(BaseModel):
    """Provider scan Data Transfer Object."""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    provider_name: str
    verdict: Verdict
    response: Optional[dict[str, Any]] = None
