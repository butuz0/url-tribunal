from enum import StrEnum


class Verdict(StrEnum):
    LEGIT = 'legit'
    SPAM = 'spam'
    MALWARE = 'malware'
    UNKNOWN = 'unknown'
