"""Database ORM model for security scan sessions."""

import datetime as dt

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Index, desc, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from url_tribunal.core.enums import ScanStatus
from url_tribunal.db.base import Base


class Scan(Base):
    """Audit log for user-initiated security scans."""

    __tablename__ = 'scan'
    __table_args__ = (
        Index(
            'url_id_scanned_at_idx',
            'url_id',
            desc('scanned_at'),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(ForeignKey('url.id', ondelete='CASCADE'))

    status: Mapped[ScanStatus] = mapped_column(
        SqlEnum(
            ScanStatus,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        default=ScanStatus.PENDING.value,
    )
    scanned_at: Mapped[dt.datetime] = mapped_column(server_default=func.now())

    url: Mapped['Url'] = relationship(back_populates='scans')
    provider_scans: Mapped[list['ProviderScan']] = relationship(
        back_populates='scan',
        cascade='all, delete-orphan',
    )
