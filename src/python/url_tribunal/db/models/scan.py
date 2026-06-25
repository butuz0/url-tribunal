"""Database ORM model for security scan sessions."""

import datetime as dt

from sqlalchemy import Enum as SqlEnum, Float, CheckConstraint, text
from sqlalchemy import ForeignKey, Index, desc, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from url_tribunal.core.enums import ScanStatus, Verdict
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
        server_default=ScanStatus.PENDING.value,
    )
    verdict: Mapped[Verdict] = mapped_column(
        SqlEnum(Verdict, values_callable=lambda e: [m.value for m in e]),
        server_default=Verdict.UNKNOWN.value,
    )
    verdict_confidence: Mapped[float] = mapped_column(
        Float(precision=2),
        CheckConstraint(
            'verdict_confidence >= 0.0 AND verdict_confidence <= 1.0',
            name='check_scan_verdict_confidence_range',
        ),
        server_default=text('0.0'),
    )
    scanned_at: Mapped[dt.datetime] = mapped_column(server_default=func.now())

    url: Mapped['Url'] = relationship(back_populates='scans')
    provider_scans: Mapped[list['ProviderScan']] = relationship(
        back_populates='scan',
        cascade='all, delete-orphan',
    )
