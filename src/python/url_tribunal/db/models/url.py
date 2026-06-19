"""Database ORM model for URL security tracking."""

import datetime as dt
from typing import Optional

from sqlalchemy import (
    String,
    Text,
    Enum as SqlEnum,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from url_tribunal.core.enums import Verdict
from url_tribunal.db.base import Base


class URL(Base):
    """Represents a URL string, identified by its SHA-256 hash."""

    __tablename__ = 'url'

    id: Mapped[int] = mapped_column(primary_key=True)
    domain_id: Mapped[int] = mapped_column(ForeignKey('domain.id', ondelete='CASCADE'))

    url_hash: Mapped[str] = mapped_column(String(64), unique=True)
    full_url: Mapped[str] = mapped_column(Text)
    verdict: Mapped[Verdict] = mapped_column(
        SqlEnum(
            Verdict,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        server_default=Verdict.UNKNOWN.value,
    )
    last_scanned_at: Mapped[Optional[dt.datetime]] = mapped_column(default=None)

    domain: Mapped['Domain'] = relationship(back_populates='urls')
    scans: Mapped[list['URLScan']] = relationship(
        back_populates='url',
        cascade='all, delete-orphan',
    )
