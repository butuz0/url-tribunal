"""Database ORM model for Domain security tracking."""

import datetime as dt

from sqlalchemy import CheckConstraint
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from url_tribunal.core.enums import Verdict
from url_tribunal.db.base import Base


class Domain(Base):
    """Represents a unique domain name and its aggregated safety status."""

    __tablename__ = 'domain'

    id: Mapped[int] = mapped_column(primary_key=True)

    fqdn: Mapped[str] = mapped_column(String(255), unique=True)
    verdict: Mapped[Verdict] = mapped_column(
        SqlEnum(
            Verdict,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        server_default=Verdict.UNKNOWN.value,
    )
    verdict_confidence: Mapped[float | int] = mapped_column(
        Float(precision=2),
        CheckConstraint(
            'verdict_confidence >= 0 AND verdict_confidence <= 1',
            name='check_verdict_confidence_range',
        ),
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    urls: Mapped[list['URL']] = relationship(
        back_populates='domain',
        cascade='all, delete-orphan',
    )
