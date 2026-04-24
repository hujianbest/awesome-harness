"""F010 sync .mdc renderer: cursor `.cursor/rules/<name>.mdc` front matter.

Implements ADR-D10-3 r2 文件物理布局 + FR-1004 cursor `.mdc` front matter.

For cursor: `.mdc` files MUST have YAML front matter at the top with
`alwaysApply: true` so cursor auto-loads the file. Garage marker block goes
below the front matter (with optional user prose between front matter and marker
that is byte-level preserved).
"""

from __future__ import annotations

MDC_FRONT_MATTER = (
    "---\n"
    "alwaysApply: true\n"
    "description: Garage 自动同步的项目知识与近期经验. 由 `garage sync` 写入. "
    "不要手动编辑 garage:context-begin/end 之间内容.\n"
    "---\n"
)


def render_mdc_with_front_matter(marker_block: str) -> str:
    """Build a complete .mdc file content with front matter + marker block.

    Used when writing to a fresh file (no existing user content); pipeline takes
    care of preserving user content outside markers when file already exists.
    """
    return f"{MDC_FRONT_MATTER}\n{marker_block}"
