"""Data Transfer Objects for Domain entity."""

import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

from url_tribunal.core.enums import Verdict


class DomainDTO(BaseModel):
    """Domain Data Transfer Object."""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int
    fqdn: str
    verdict: Verdict
    verdict_confidence: float = Field(ge=0.0, le=1.0)
    created_at: dt.datetime
    updated_at: dt.datetime


class DomainCreateDTO(BaseModel):
    """Domain creation Data Transfer Object."""

    fqdn: str
