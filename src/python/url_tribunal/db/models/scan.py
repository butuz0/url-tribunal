"""Database ORM model for security scan sessions."""

import datetime as dt

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from url_tribunal.db.base import Base


class Scan(Base):
    """Audit log for user-initiated security scans."""

    __tablename__ = 'scan'

    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(ForeignKey('url.id', ondelete='CASCADE'))

    scanned_at: Mapped[dt.datetime] = mapped_column(server_default=func.now())

    url: Mapped['URL'] = relationship(back_populates='scans')
    provider_scans: Mapped[list['ProviderScan']] = relationship(
        back_populates='scan',
        cascade='all, delete-orphan',
    )
