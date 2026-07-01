"""urlscan.io v1 API security scan."""

from typing import Any

from requests import HTTPError

from url_tribunal.core.enums import ProviderName, Verdict
from url_tribunal.dtos import ProviderScanResultDTO
from url_tribunal.providers.base import BaseHTTPProvider
from url_tribunal.providers.exceptions import (
    ProviderInfrastructureError,
    ProviderResultNotReadyError,
)


class UrlScanProvider(BaseHTTPProvider):
    """Security scan client for urlscan.io V1 API."""

    provider_name = ProviderName.URLSCAN
    weight = 1
    base_url = 'https://urlscan.io/api/v1'
    _malicious_score_threshold = 65

    def submit_url(self, url: str) -> str:
        """Submit the target URL to urlscan.io URL analysis."""

        result = self._make_request(
            method='POST',
            endpoint='scan',
            data={'url': url},
        )
        return self._parse_external_ref_id(result.json())

    def fetch_results(self, external_reference_id: str) -> ProviderScanResultDTO:
        """Fetch urlscan.io URL analysis results."""

        try:
            result = self._make_request(
                method='GET',
                endpoint=f'result/{external_reference_id}/',
            )
        except HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                raise ProviderResultNotReadyError(
                    f'{self.provider_name} report {external_reference_id} is still processing.'
                ) from exc
            raise ProviderInfrastructureError(
                f'{self.provider_name} infrastructure failure: {exc}'
            ) from exc

        payload = result.json()

        return ProviderScanResultDTO(
            external_reference_id=external_reference_id,
            verdict=self._parse_verdict(payload),
            response=self._parse_response(payload),
        )

    def _get_default_headers(self) -> dict[str, str]:
        """Default headers for HTTP requests."""

        return {'api-key': self._api_key}

    @staticmethod
    def _parse_external_ref_id(data: dict[str, Any]) -> str:
        """Extract analysis id from submission response."""

        return data['uuid']

    @staticmethod
    def _parse_response(data: dict[str, Any]) -> dict[str, Any]:
        """Extract and sanitize raw urlscan.io analysis response."""

        verdicts = data.get('verdicts', {})
        task = data.get('task', {})
        page = data.get('page', {})
        stats = data.get('stats', {})

        return {
            'verdicts': verdicts,
            'task': {
                'time': task.get('time'),
                'report_url': task.get('reportURL'),
                'screenshot_url': task.get('screenshotURL'),
            },
            'page': {
                'url': page.get('url'),
                'domain': page.get('domain'),
                'apex_domain': page.get('apexDomain'),
                'title': page.get('title'),
                'server': page.get('server'),
                'ip': page.get('ip'),
                'country': page.get('country'),
            },
            'stats': {
                'malicious_count': stats.get('malicious', 0),
                'secure_percentage': stats.get('securePercentage', 100),
            },
        }

    def _parse_verdict(self, data: dict[str, Any]) -> Verdict:
        """Calculate verdict based on urlscan.io analysis stats."""

        overall = data.get('verdicts', {}).get('overall', {})
        is_malicious = overall.get('malicious', False)
        score = overall.get('score', 0)

        if is_malicious or score > self._malicious_score_threshold:
            return Verdict.MALWARE

        return Verdict.LEGIT
