"""Provider Scan model repository module."""

from sqlalchemy import update
from sqlalchemy.orm import Session

from url_tribunal.core.enums import ProviderStatus
from url_tribunal.db.models import ProviderScan, Scan
from url_tribunal.dtos import (
    ProviderScanCompleteDTO,
    ProviderScanCreateDTO,
    ProviderScanDTO,
)


class ProviderScanRepository:
    """Provider Scan model repository class."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, data: ProviderScanCreateDTO) -> ProviderScanDTO:
        """Create new ProviderScan record."""

        provider_scan = ProviderScan(
            scan_id=data.scan_id,
            provider_name=data.provider_name,
            external_reference_id=data.external_reference_id,
        )
        self._session.add(provider_scan)
        self._session.flush()

        return ProviderScanDTO.model_validate(provider_scan)

    def set_external_reference_id(
            self,
            provider_scan_id: int,
            external_reference_id: str,
    ) -> None:
        """Set external reference id for the record."""

        stmt = (
            update(ProviderScan)
            .where(ProviderScan.id == provider_scan_id)
            .values(external_reference_id=external_reference_id)
        )
        self._session.execute(stmt)

    def complete_scan(
            self,
            provider_scan_id: int,
            data: ProviderScanCompleteDTO,
    ) -> None:
        """Update record with completed security scan results."""

        stmt = (
            update(ProviderScan)
            .where(ProviderScan.id == provider_scan_id)
            .values(
                status=ProviderStatus.COMPLETED,
                verdict=data.verdict,
                response=data.response,
            )
        )
        self._session.execute(stmt)

    def fail_scan(self, provider_scan_id: int) -> None:
        """Update record with failed security scan results."""

        stmt = (
            update(Scan)
            .where(Scan.id == provider_scan_id)
            .values(status=ProviderStatus.FAILED)
        )
        self._session.execute(stmt)
