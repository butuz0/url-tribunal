"""Scan model repository module."""

from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload

from url_tribunal.core.enums import ScanStatus
from url_tribunal.db.models import Scan, Url
from url_tribunal.dtos import (
    ScanCompleteDTO,
    ScanCreateDTO,
    ScanDetailDTO,
    ScanDTO,
    ScanFailDTO,
)


class ScanRepository:
    """Scan model repository class."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, data: ScanCreateDTO) -> ScanDTO:
        """Create new scan record."""

        scan = Scan(
            url_id=data.url_id,
        )
        self._session.add(scan)
        self._session.flush()

        return ScanDTO.model_validate(scan)

    def complete_scan(self, scan_id: int, data: ScanCompleteDTO) -> None:
        """Update record with completed security scan results."""

        stmt = (
            update(Scan)
            .where(Scan.id == scan_id)
            .values(
                status=ScanStatus.COMPLETED,
                verdict=data.verdict,
                verdict_confidence=data.verdict_confidence,
                scanned_at=data.scanned_at,
            )
        )
        self._session.execute(stmt)

    def fail_scan(self, scan_id: int, data: ScanFailDTO) -> None:
        """Update record with failed security scan results."""

        stmt = (
            update(Scan)
            .where(Scan.id == scan_id)
            .values(
                status=ScanStatus.FAILED,
                scanned_at=data.failed_at,
            )
        )
        self._session.execute(stmt)

    def get_with_providers(self, scan_id: int) -> Optional[ScanDetailDTO]:
        """Fetch scan with all provider results."""

        stmt = (
            select(Scan)
            .options(joinedload(Scan.provider_scans))
            .where(Scan.id == scan_id)
        )
        scan = self._session.scalars(stmt).unique().first()

        return ScanDetailDTO.model_validate(scan) if scan else None

    def list_by_url_hash(self, url_hash: str) -> list[ScanDTO]:
        """Fetch all scans for a specific URL."""

        stmt = (
            select(Scan)
            .join(Url, Url.id == Scan.url_id)
            .where(Url.url_hash == url_hash)
            .order_by(Scan.scanned_at.desc())
        )
        scans = self._session.scalars(stmt).all()

        return [ScanDTO.model_validate(scan) for scan in scans]
