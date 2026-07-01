"""Global application enumerations."""

from enum import StrEnum


class ProviderName(StrEnum):
    """Supported security scan providers."""

    URLSCAN = 'urlscan'
    VIRUSTOTAL = 'virustotal'


class Verdict(StrEnum):
    """Security scan results for URLs and domains."""

    LEGIT = 'legit'
    SPAM = 'spam'
    MALWARE = 'malware'
    UNKNOWN = 'unknown'


class ScanStatus(StrEnum):
    """Status of a security scan execution."""

    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'


class ProviderStatus(StrEnum):
    """Status of a provider security scan."""

    PENDING = 'pending'
    POLLING = 'polling'
    COMPLETED = 'completed'
    FAILED = 'failed'
