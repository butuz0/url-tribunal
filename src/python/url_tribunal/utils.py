"""General utility functions."""

import re

SHA256_PATTERN = r'[A-Fa-f0-9]{64}'


def like_sha256(string: str) -> bool:
    """Validate if a string matches SHA256 format."""

    return re.fullmatch(SHA256_PATTERN, string) is not None
