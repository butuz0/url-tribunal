"""Database ORM model for Domain security tracking."""

import datetime as dt

from sqlalchemy import (
    String,
    Enum as SqlEnum,
    func,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

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
