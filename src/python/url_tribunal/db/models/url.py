"""Database ORM model for URL security tracking."""

import datetime as dt
from typing import Optional

from sqlalchemy import CheckConstraint
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from url_tribunal.core.enums import Verdict
from url_tribunal.db.base import Base


class Url(Base):
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
    verdict_confidence: Mapped[float] = mapped_column(
        Float(precision=2),
        CheckConstraint(
            'verdict_confidence >= 0 AND verdict_confidence <= 1',
            name='check_verdict_confidence_range',
        ),
        server_default=text('0.0'),
    )
    last_scanned_at: Mapped[Optional[dt.datetime]] = mapped_column(default=None)

    domain: Mapped['Domain'] = relationship(back_populates='urls')
    scans: Mapped[list['Scan']] = relationship(
        back_populates='url',
        cascade='all, delete-orphan',
    )
