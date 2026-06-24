"""API schemas for Url entity."""

import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict

from url_tribunal.core.enums import Verdict


class UrlSchema(BaseModel):
    """API response schema for URL security status."""

    model_config = ConfigDict(frozen=True)

    id: int
    hash: str
    full_url: str
    verdict: Verdict
    confidence: float | int
    last_scanned_at: Optional[dt.datetime] = None
