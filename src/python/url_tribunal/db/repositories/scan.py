"""Scan model repository module."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from url_tribunal.db.models import Scan, Url
from url_tribunal.dtos import ScanDetailDTO, ScanDTO


class ScanRepository:
    """Scan model repository class."""

    def __init__(self, session: Session) -> None:
        self._session = session

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
            .join(Url)
            .where(Url.url_hash == url_hash)
            .order_by(Scan.scanned_at.desc())
        )
        scans = self._session.scalars(stmt).all()

        return [ScanDTO.model_validate(scan) for scan in scans]
