import ipaddress
import re


_PATTERNS = (
    ("EMAIL", re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+(?![\w.-])")),
    ("SSN", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")),
    (
        "PHONE",
        re.compile(
            r"(?<!\d)(?:\+?1[\s.-]?)?(?:\(\d{3}\)|\d{3})"
            r"[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)"
        ),
    ),
    ("URL", re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>]+")),
    (
        "IP",
        re.compile(
            r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"
        ),
    ),
)
_URL_TRAILING_PUNCTUATION = ".,;:!?)]}"


def detect_rule_entities(text: str) -> list[dict]:
    entities = []
    for label, pattern in _PATTERNS:
        for match in pattern.finditer(text):
            start, end = match.span()
            value = match.group()
            if label == "URL":
                value = value.rstrip(_URL_TRAILING_PUNCTUATION)
                end = start + len(value)
                if not value:
                    continue
            elif label == "IP":
                try:
                    ipaddress.IPv4Address(value)
                except ipaddress.AddressValueError:
                    continue

            entities.append(
                {
                    "start": start,
                    "end": end,
                    "text": value,
                    "label": label,
                    "score": 1.0,
                }
            )
    return entities
