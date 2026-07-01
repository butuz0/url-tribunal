"""Domain model repository module."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from url_tribunal.db.models import Domain
from url_tribunal.dtos import DomainCreateDTO, DomainDTO


class DomainRepository:
    """Domain model repository class."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, data: DomainCreateDTO) -> DomainDTO:
        """Create new Domain record."""

        domain = Domain(
            fqdn=data.fqdn,
        )
        self._session.add(domain)
        self._session.flush()

        return DomainDTO.model_validate(domain)

    def get_by_fqdn(self, fqdn: str) -> Optional[DomainDTO]:
        """Fetch a record by its FQDN."""

        stmt = select(Domain).where(Domain.fqdn == fqdn)
        domain = self._session.scalars(stmt).first()

        if domain is None:
            return None

        return DomainDTO.model_validate(domain)
