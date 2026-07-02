"""Url model repository module."""

from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from url_tribunal.db.models import Url
from url_tribunal.dtos import UrlCreateDTO, UrlDTO, UrlUpdateLastScanDTO


class UrlRepository:
    """Url model repository class."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, data: UrlCreateDTO) -> UrlDTO:
        """Create new Url record."""

        url = Url(
            domain_id=data.domain_id,
            url_hash=data.url_hash,
            full_url=data.full_url,
        )
        self._session.add(url)
        self._session.flush()

        return UrlDTO.model_validate(url)

    def update_last_scan(self, url_id: int, data: UrlUpdateLastScanDTO) -> None:
        """Update url record with last security scan results."""

        stmt = (
            update(Url)
            .where(Url.id == url_id)
            .values(
                last_scan_id=data.last_scan_id,
                verdict=data.verdict,
                verdict_confidence=data.verdict_confidence,
                last_scanned_at=data.last_scanned_at,
            )
        )
        self._session.execute(stmt)

    def get_by_hash(self, url_hash: str) -> Optional[UrlDTO]:
        """Fetch a record by its SHA-256 hash."""

        stmt = select(Url).where(Url.url_hash == url_hash)
        url = self._session.scalars(stmt).first()

        if url is None:
            return None

        return UrlDTO.model_validate(url)
