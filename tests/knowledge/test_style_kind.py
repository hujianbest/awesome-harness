"""F011 T1: KnowledgeType.STYLE + TYPE_DIRECTORIES tests (INV-F11-1)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from garage_os.knowledge.knowledge_store import KnowledgeStore
from garage_os.storage.file_storage import FileStorage
from garage_os.types import KnowledgeEntry, KnowledgeType


class TestStyleEnum:
    def test_style_enum_value(self) -> None:
        assert KnowledgeType.STYLE.value == "style"

    def test_style_in_type_directories(self) -> None:
        assert KnowledgeType.STYLE in KnowledgeStore.TYPE_DIRECTORIES
        assert KnowledgeStore.TYPE_DIRECTORIES[KnowledgeType.STYLE] == "knowledge/style"


class TestStyleStorage:
    def test_create_and_list_style_entry(self, tmp_path: Path) -> None:
        storage = FileStorage(tmp_path / ".garage")
        store = KnowledgeStore(storage)
        entry = KnowledgeEntry(
            id="style-001",
            type=KnowledgeType.STYLE,
            topic="Functional Python preference",
            date=datetime(2026, 4, 24),
            tags=["python", "functional"],
            content="Prefer dataclass + pure functions over classes with state.",
        )
        store.store(entry)

        entries = store.list_entries(knowledge_type=KnowledgeType.STYLE)
        assert len(entries) == 1
        assert entries[0].topic == "Functional Python preference"
        assert entries[0].type == KnowledgeType.STYLE

    def test_style_directory_created(self, tmp_path: Path) -> None:
        storage = FileStorage(tmp_path / ".garage")
        store = KnowledgeStore(storage)
        store.store(
            KnowledgeEntry(
                id="s1",
                type=KnowledgeType.STYLE,
                topic="t",
                date=datetime(2026, 4, 24),
                tags=[],
                content="c",
            )
        )
        # File should be under .garage/knowledge/style/
        style_dir = tmp_path / ".garage" / "knowledge" / "style"
        assert style_dir.is_dir()
        files = list(style_dir.glob("*.md"))
        assert len(files) == 1
