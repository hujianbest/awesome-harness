"""F010 T2: render/mdc.py tests (cursor `.mdc` front matter).

Covers ADR-D10-3 r2 文件物理布局 + FR-1004 cursor `.mdc` front matter.
"""

from __future__ import annotations

from garage_os.sync.render.markdown import wrap_with_markers
from garage_os.sync.render.mdc import MDC_FRONT_MATTER, render_mdc_with_front_matter


class TestFrontMatterAlwaysApply:
    def test_front_matter_contains_always_apply(self) -> None:
        assert "alwaysApply: true" in MDC_FRONT_MATTER

    def test_front_matter_yaml_format(self) -> None:
        # Starts and ends with `---` lines
        assert MDC_FRONT_MATTER.startswith("---\n")
        assert MDC_FRONT_MATTER.rstrip().endswith("---")

    def test_front_matter_description_mentions_garage_sync(self) -> None:
        assert "garage sync" in MDC_FRONT_MATTER


class TestRenderMdcLayout:
    """ADR-D10-3 r2: front matter at top, then user prose blank, then markers."""

    def test_front_matter_above_marker_block(self) -> None:
        marker_block = wrap_with_markers("body")
        out = render_mdc_with_front_matter(marker_block)
        # Front matter starts at offset 0
        assert out.startswith("---\n")
        # Marker comes after front matter
        fm_end = out.index("---\n", 4) + len("---\n")
        marker_idx = out.index("<!-- garage:context-begin -->")
        assert marker_idx > fm_end

    def test_full_output_parseable(self) -> None:
        marker_block = wrap_with_markers("knowledge content")
        out = render_mdc_with_front_matter(marker_block)
        # Front matter + marker block + body all present
        assert "alwaysApply: true" in out
        assert "<!-- garage:context-begin -->" in out
        assert "knowledge content" in out
        assert "<!-- garage:context-end -->" in out


class TestMarkdownNoFrontMatter:
    """ADR-D10-3 r2: claude/opencode 不需要 front matter (sentinel — markdown.py 不输出 YAML)."""

    def test_wrap_with_markers_no_front_matter(self) -> None:
        out = wrap_with_markers("body")
        # 纯 markdown body, 不含 alwaysApply 等 YAML key
        assert "alwaysApply" not in out
        assert "---" not in out  # no YAML separator
