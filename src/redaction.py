"""Log-safe redaction helpers (no bootstrap imports)."""

from __future__ import annotations

import re
from typing import Mapping


def redact_text(text: str, known_values: Mapping[str, str] | None = None) -> str:
    """Best-effort redaction for diagnostics."""

    if not text:
        return text
    redacted = text
    if known_values:
        for value in sorted(known_values.values(), key=len, reverse=True):
            if len(value) >= 8 and value in redacted:
                redacted = redacted.replace(value, "[REDACTED]")
    redacted = re.sub(
        r"(?i)\b(api[_-]?key|token|secret|password|bearer)\s*[:=]\s*\S+",
        r"\1=[REDACTED]",
        redacted,
    )
    return redacted
