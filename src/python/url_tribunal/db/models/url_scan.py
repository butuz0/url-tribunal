"""Database ORM model for URL security scan records."""

import datetime as dt

from sqlalchemy import (
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from url_tribunal.db.base import Base


class URLScan(Base):
    """Audit log holding raw JSON outputs from third-party security scans."""

    __tablename__ = 'url_scan'

    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(ForeignKey('url.id', ondelete='CASCADE'))

    scanned_at: Mapped[dt.datetime] = mapped_column(server_default=func.now())
    raw_response: Mapped[dict] = mapped_column(JSON)

    url: Mapped['URL'] = relationship(back_populates='scans')
