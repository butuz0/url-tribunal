"""Data Transfer Objects for URL entity."""

import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from url_tribunal.core.enums import Verdict


class UrlDTO(BaseModel):
    """Url Data Transfer Object."""

    model_config = ConfigDict(frozen=True, from_attributes=True)

    id: int
    domain_id: int
    url_hash: str = Field(min_length=64, max_length=64)
    full_url: str
    verdict: Verdict
    verdict_confidence: float = Field(ge=0.0, le=1.0)
    last_scanned_at: Optional[dt.datetime] = None
