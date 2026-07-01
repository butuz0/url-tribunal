"""VirusTotal v3 API security scan."""

from typing import Any

from requests import HTTPError

from url_tribunal.core.enums import ProviderName, Verdict
from url_tribunal.dtos import ProviderScanResultDTO
from url_tribunal.providers.base import BaseHTTPProvider
from url_tribunal.providers.exceptions import (
    ProviderInfrastructureError,
    ProviderResultNotReadyError,
)


class VirusTotalProvider(BaseHTTPProvider):
    """Security scan client for VirusTotal V3 API."""

    provider_name = ProviderName.VIRUSTOTAL
    weight = 1
    base_url = 'https://www.virustotal.com/api/v3'
    _scan_ready_status = 'completed'
    _malicious_count_threshold = 0

    def submit_url(self, url: str) -> str:
        """Submit the target URL to VirusTotal URL analysis."""

        result = self._make_request(
            method='POST',
            endpoint='urls',
            data={'url': url},
        )
        return self._parse_external_ref_id(result.json())

    def fetch_results(self, external_reference_id: str) -> ProviderScanResultDTO:
        """Fetch VirusTotal URL analysis results."""

        try:
            result = self._make_request(
                method='GET',
                endpoint=f'analyses/{external_reference_id}',
            )
        except HTTPError as exc:
            raise ProviderInfrastructureError(f'VirusTotal network error: {exc}') from exc

        payload = result.json()

        if not self._is_scan_ready(payload):
            raise ProviderResultNotReadyError(
                f'VirusTotal scan {external_reference_id} is still processing.'
            )

        return ProviderScanResultDTO(
            external_reference_id=external_reference_id,
            verdict=self._parse_verdict(payload),
            response=self._parse_response(payload),
        )

    def _get_default_headers(self) -> dict[str, str]:
        """Default headers for HTTP requests."""

        return {'x-apikey': self._api_key}

    @staticmethod
    def _parse_external_ref_id(data: dict[str, Any]) -> str:
        """Extract analysis id from submission response."""

        return data['data']['id']

    def _is_scan_ready(self, data: dict[str, Any]) -> bool:
        """Check if the response is a completed scan result."""

        status = data.get('data', {}).get('attributes', {}).get('status')
        return status == self._scan_ready_status

    @staticmethod
    def _parse_response(data: dict[str, Any]) -> dict[str, Any]:
        """Extract and sanitize raw VirusTotal analysis response."""

        attributes = data.get('data', {}).get('attributes', {})

        return {
            'stats': attributes.get('stats', {}),
            'status': attributes.get('status', 'unknown'),
            'sha256': data.get('meta', {}).get('file_info', {}).get('sha256'),
        }

    def _parse_verdict(self, data: dict[str, Any]) -> Verdict:
        """Calculate verdict based on VirusTotal analysis stats."""

        stats = data.get('data', {}).get('attributes', {}).get('stats', {})
        malicious = stats.get('malicious', 0)

        if malicious > self._malicious_count_threshold:
            return Verdict.MALWARE

        return Verdict.LEGIT
