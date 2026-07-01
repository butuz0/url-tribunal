"""Base infrastructure for external security scan providers."""

from abc import ABC, abstractmethod
from typing import Any, ClassVar, Optional

import requests
from requests import Response

from url_tribunal.core.enums import ProviderName
from url_tribunal.dtos import ProviderScanResultDTO


class BaseProvider(ABC):
    """Abstract base class for all external security scan APIs."""

    provider_name: ClassVar[ProviderName]
    weight: ClassVar[float]

    @abstractmethod
    def submit_url(self, url: str) -> str:
        """Submit a target URL to the provider for scanning."""

    @abstractmethod
    def fetch_results(self, external_reference_id: str) -> ProviderScanResultDTO:
        """Retrieve scanning results from the provider."""


class BaseHTTPProvider(BaseProvider, ABC):
    """Base class for HTTP-based external security scan APIs."""

    base_url: ClassVar[str]

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def _get_default_headers(self) -> dict[str, str]:
        """Default headers for HTTP requests."""

        return {}

    def _make_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[dict[str, Any]] = None,
            headers: Optional[dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Response:
        """Execute an HTTP request."""

        base = self.base_url.rstrip('/')
        path = endpoint.lstrip('/')
        url = f'{base}/{path}'

        request_headers = self._get_default_headers()
        if headers:
            request_headers.update(headers)

        response = requests.request(
            method=method,
            url=url,
            data=data if method.upper() == 'POST' else None,
            headers=request_headers,
            **kwargs,
        )
        response.raise_for_status()

        return response
