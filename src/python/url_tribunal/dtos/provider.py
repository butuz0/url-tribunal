from typing import Any, Optional
from pydantic import BaseModel, ConfigDict

from url_tribunal.core.enums import Verdict


class ProviderScanResultDTO(BaseModel):
    """Provider security scan result Data Transfer Object."""

    model_config = ConfigDict(frozen=True)

    external_reference_id: str
    verdict: Verdict
    response: dict[str, Any]
