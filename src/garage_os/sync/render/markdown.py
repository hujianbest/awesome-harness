"""F010 sync markdown renderer: marker wrapping + extract.

Implements ADR-D10-3 (HTML comment marker, all 3 hosts treat as invisible).
"""

from __future__ import annotations

MARKER_BEGIN = "<!-- garage:context-begin -->"
MARKER_END = "<!-- garage:context-end -->"


def wrap_with_markers(body: str) -> str:
    """Wrap body markdown content with HTML comment markers.

    Returns full marker block (including the marker comment lines themselves).
    """
    return f"{MARKER_BEGIN}\n{body.rstrip()}\n{MARKER_END}\n"


def has_marker_block(content: str) -> bool:
    """True if content contains both begin and end markers."""
    return MARKER_BEGIN in content and MARKER_END in content


def extract_marker_block(content: str) -> str | None:
    """Extract the body between MARKER_BEGIN and MARKER_END (excluding marker lines).

    Returns None if either marker is missing. The returned string is rstripped of
    trailing newlines so SHA-256 hashing is stable across LF/no-LF differences.
    """
    if not has_marker_block(content):
        return None
    begin_idx = content.index(MARKER_BEGIN) + len(MARKER_BEGIN)
    end_idx = content.index(MARKER_END)
    if end_idx <= begin_idx:
        return None
    inner = content[begin_idx:end_idx]
    # Strip leading newline (after MARKER_BEGIN) and trailing newline (before MARKER_END)
    return inner.strip("\n")
