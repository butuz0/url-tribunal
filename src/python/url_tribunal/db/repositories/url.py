"""Url model repository module."""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from url_tribunal.db.models import Url
from url_tribunal.dtos.url import UrlDTO


class UrlRepository:
    """Url model repository class."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_hash(self, url_hash: str) -> Optional[UrlDTO]:
        """Fetch a record by its SHA-256 hash."""

        stmt = select(Url).where(Url.url_hash == url_hash)
        url = self._session.scalars(stmt).first()

        if url is None:
            return None

        return UrlDTO.model_validate(url)
