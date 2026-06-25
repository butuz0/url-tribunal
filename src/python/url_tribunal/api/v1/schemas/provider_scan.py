"""API schemas for ProviderScan entity."""

from typing import Optional, Any

from pydantic import BaseModel, ConfigDict

from url_tribunal.core.enums import Verdict


class ProviderScanSchema(BaseModel):
    """API response schema for provider security scan results."""

    model_config = ConfigDict(frozen=True, from_attributes=True)

    id: int
    provider_name: str
    verdict: Verdict
    response: Optional[dict[str, Any]]
