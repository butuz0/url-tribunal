"""API schemas for Scan entity."""

import datetime as dt

from pydantic import BaseModel, ConfigDict

from url_tribunal.api.v1.schemas.provider_scan import ProviderScanSchema
from url_tribunal.core.enums import ScanStatus


class ScanSchema(BaseModel):
    """API response schema for security scan results."""

    model_config = ConfigDict(frozen=True, from_attributes=True)

    id: int
    url_id: int
    status: ScanStatus
    scanned_at: dt.datetime


class ScanDetailSchema(ScanSchema):
    """API response schema for security scan results."""

    provider_scans: list[ProviderScanSchema]
