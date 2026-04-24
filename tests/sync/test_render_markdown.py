"""F010 T2: render/markdown.py tests (marker wrapping + extract)."""

from __future__ import annotations

from garage_os.sync.render.markdown import (
    MARKER_BEGIN,
    MARKER_END,
    extract_marker_block,
    has_marker_block,
    wrap_with_markers,
)


class TestMarkerConstants:
    def test_html_comment_format(self) -> None:
        assert MARKER_BEGIN == "<!-- garage:context-begin -->"
        assert MARKER_END == "<!-- garage:context-end -->"


class TestWrapWithMarkers:
    def test_basic_wrap(self) -> None:
        out = wrap_with_markers("hello body")
        assert MARKER_BEGIN in out
        assert MARKER_END in out
        assert "hello body" in out

    def test_marker_at_start_and_end(self) -> None:
        out = wrap_with_markers("body")
        lines = out.strip().split("\n")
        assert lines[0] == MARKER_BEGIN
        assert lines[-1] == MARKER_END


class TestExtractMarkerBlock:
    def test_extract_returns_inner_body(self) -> None:
        full = wrap_with_markers("inner content")
        extracted = extract_marker_block(full)
        assert extracted == "inner content"

    def test_extract_returns_none_when_no_markers(self) -> None:
        assert extract_marker_block("plain text no markers") is None

    def test_extract_returns_none_when_only_begin(self) -> None:
        assert extract_marker_block(f"{MARKER_BEGIN}\nbody\n") is None

    def test_extract_with_user_content_outside(self) -> None:
        """User content above + below markers preserved separately."""
        full = (
            "# My project notes\n\n"
            f"{MARKER_BEGIN}\n"
            "garage knowledge body\n"
            f"{MARKER_END}\n\n"
            "More user content below\n"
        )
        extracted = extract_marker_block(full)
        assert extracted == "garage knowledge body"
        # User content outside markers preserved when extracted only
        assert "# My project notes" not in (extracted or "")


class TestHasMarkerBlock:
    def test_has_both_markers(self) -> None:
        assert has_marker_block(wrap_with_markers("body"))

    def test_missing_end_marker(self) -> None:
        assert not has_marker_block(f"{MARKER_BEGIN}\nbody\n")

    def test_no_markers(self) -> None:
        assert not has_marker_block("plain text")
