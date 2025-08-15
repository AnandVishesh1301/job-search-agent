import re
from typing import Iterable

# Very light, targeted boilerplate removal. Expand as you see patterns in your data.
EEO_PATTERNS: Iterable[re.Pattern] = [
    re.compile(r"equal opportunity employer.*?(?:\n|\.)", re.I),
    re.compile(r"EEO is the law.*", re.I),
    re.compile(r"background check.*?(?:required|may be required).*", re.I),
    re.compile(r"E-?verify.*", re.I),
    re.compile(r"reasonable accommodation.*", re.I),
    re.compile(r"benefits(?:\s+include|\s*:).*", re.I),
]
LEGAL_PATTERNS: Iterable[re.Pattern] = [
    re.compile(r"privacy policy.*", re.I),
    re.compile(r"terms of use.*", re.I),
]
GENERIC_PATTERNS: Iterable[re.Pattern] = [
    re.compile(r"about the company.*", re.I),
    re.compile(r"who we are.*", re.I),
]

def strip_boilerplate(text: str, max_len: int = 8000) -> str:
    """Remove common disclaimer/boilerplate lines and trim."""
    cleaned = text
    for patt_group in (EEO_PATTERNS, LEGAL_PATTERNS):
        for patt in patt_group:
            cleaned = re.sub(patt, "", cleaned)

    # Optional: collapse excessive whitespace
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = cleaned.strip()

    # Clip long tails to keep token usage sane
    return cleaned[:max_len]
