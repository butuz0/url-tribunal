"""API schemas for Url entity."""

import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict

from url_tribunal.core.enums import Verdict


class UrlSchema(BaseModel):
    """API response schema for URL security status."""

    model_config = ConfigDict(frozen=True, from_attributes=True)

    id: int
    domain_id: int
    last_scan_id: Optional[int] = None
    url_hash: str
    full_url: str
    verdict: Verdict
    verdict_confidence: float | int
    last_scanned_at: Optional[dt.datetime] = None
