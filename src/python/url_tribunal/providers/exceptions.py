"""Exceptions for external provider integrations."""


class ProviderError(Exception):
    """Base exception for external security scan provider issues."""


class ProviderResultNotReadyError(ProviderError):
    """Scan is still processing on the provider side."""


class ProviderInfrastructureError(ProviderError):
    """Network issues, rate limits, or provider downtime."""


class UnknownProviderError(ProviderError):
    """Provider not supported."""
