"""Global application enumerations."""

from enum import StrEnum


class Verdict(StrEnum):
    """Security scan results for URLs and domains."""

    LEGIT = 'legit'
    SPAM = 'spam'
    MALWARE = 'malware'
    UNKNOWN = 'unknown'
