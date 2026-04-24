"""F011 T2: F010 sync compiler include STYLE entries (FR-1103 + INV-F11-2)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from garage_os.knowledge.knowledge_store import KnowledgeStore
from garage_os.storage.file_storage import FileStorage
from garage_os.sync.compiler import compile_garage_section
from garage_os.types import KnowledgeEntry, KnowledgeType


def _seed_style(workspace_root: Path, n: int = 2) -> None:
    storage = FileStorage(workspace_root / ".garage")
    store = KnowledgeStore(storage)
    for i in range(n):
        store.store(
            KnowledgeEntry(
                id=f"style-{i:03d}",
                type=KnowledgeType.STYLE,
                topic=f"Style preference {i}",
                date=datetime(2026, 4, 24, 10, i),
                tags=["style"],
                content=f"User prefers approach {i}",
            )
        )


class TestStyleSection:
    def test_style_section_appears_in_output(self, tmp_path: Path) -> None:
        _seed_style(tmp_path, n=3)
        compiled = compile_garage_section(tmp_path)
        assert "### Recent Style Preferences" in compiled.body_markdown
        assert "Style preference 0" in compiled.body_markdown or "Style preference 1" in compiled.body_markdown

    def test_style_kind_in_compiled_kinds_list(self, tmp_path: Path) -> None:
        _seed_style(tmp_path, n=1)
        compiled = compile_garage_section(tmp_path)
        assert "style" in compiled.knowledge_kinds

    def test_style_section_omitted_when_empty(self, tmp_path: Path) -> None:
        # Seed only decisions, no style
        storage = FileStorage(tmp_path / ".garage")
        KnowledgeStore(storage).store(
            KnowledgeEntry(
                id="d1",
                type=KnowledgeType.DECISION,
                topic="d",
                date=datetime(2026, 4, 24),
                tags=[],
                content="c",
            )
        )
        compiled = compile_garage_section(tmp_path)
        assert "### Recent Style Preferences" not in compiled.body_markdown
        assert "style" not in compiled.knowledge_kinds

    def test_style_section_after_pattern_section(self, tmp_path: Path) -> None:
        """ADR-D11-2: style 在 pattern 之后 (decision > solution > pattern > style ordering)."""
        storage = FileStorage(tmp_path / ".garage")
        store = KnowledgeStore(storage)
        for kind in [KnowledgeType.PATTERN, KnowledgeType.STYLE]:
            store.store(
                KnowledgeEntry(
                    id=f"{kind.value}-1",
                    type=kind,
                    topic=f"{kind.value} topic",
                    date=datetime(2026, 4, 24),
                    tags=[],
                    content=f"{kind.value} content",
                )
            )
        compiled = compile_garage_section(tmp_path)
        body = compiled.body_markdown
        assert body.index("Recent Patterns") < body.index("Recent Style Preferences")


class TestStylePerKindTop4:
    def test_style_top_4_per_kind(self, tmp_path: Path) -> None:
        _seed_style(tmp_path, n=10)
        compiled = compile_garage_section(tmp_path)
        # PER_KIND_TOP=4
        # All 10 fit budget; only 4 selected per kind ranking
        assert compiled.knowledge_count == 4
