"""Database ORM model for third-party security scan records."""

from typing import Any, Optional

from sqlalchemy import JSON
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from url_tribunal.core.enums import ProviderStatus, Verdict
from url_tribunal.db.base import Base


class ProviderScan(Base):
    """Security scan result by a specific provider."""

    __tablename__ = 'provider_scan'

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(ForeignKey('scan.id', ondelete='CASCADE'))

    provider_name: Mapped[str] = mapped_column(String(64))
    external_reference_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    status: Mapped[ProviderStatus] = mapped_column(
        SqlEnum(ProviderStatus, values_callable=lambda e: [m.value for m in e]),
        server_default=ProviderStatus.PENDING.value,
    )
    verdict: Mapped[Verdict] = mapped_column(
        SqlEnum(
            Verdict,
            values_callable=lambda enum: [member.value for member in enum],
        ),
        server_default=Verdict.UNKNOWN.value,
    )
    response: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)

    scan: Mapped['Scan'] = relationship(back_populates='provider_scans')
