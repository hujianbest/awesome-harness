"""F010 T2: sync compiler tests.

Covers:
- spec FR-1007 + design ADR-D10-4 (constants) + ADR-D10-5 (markdown structure)
- INV-F10-3: SIZE_BUDGET_BYTES enforced
"""

from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path

import pytest

from garage_os.knowledge.experience_index import ExperienceIndex
from garage_os.knowledge.knowledge_store import KnowledgeStore
from garage_os.storage.file_storage import FileStorage
from garage_os.sync.compiler import (
    EXPERIENCE_TOP_M,
    KNOWLEDGE_TOP_N,
    SIZE_BUDGET_BYTES,
    compile_garage_section,
)
from garage_os.types import ExperienceRecord, KnowledgeEntry, KnowledgeType


def _seed_knowledge(workspace_root: Path, n_per_kind: int = 5) -> None:
    """Seed N entries per kind under .garage/knowledge/."""
    storage = FileStorage(workspace_root / ".garage")
    store = KnowledgeStore(storage)
    for kind in [KnowledgeType.DECISION, KnowledgeType.SOLUTION, KnowledgeType.PATTERN]:
        for i in range(n_per_kind):
            entry = KnowledgeEntry(
                id=f"{kind.value}-test-{i:03d}",
                type=kind,
                topic=f"Test {kind.value} {i}",
                date=datetime(2026, 4, 24, 10, i, 0),
                tags=[kind.value, "f010-test"],
                content=f"Body text for {kind.value} entry {i}. " * 3,
            )
            store.store(entry)


def _seed_experience(workspace_root: Path, n: int = 3) -> None:
    storage = FileStorage(workspace_root / ".garage")
    index = ExperienceIndex(storage)
    for i in range(n):
        record = ExperienceRecord(
            record_id=f"2026-04-24T10-{i:02d}-00",
            task_type=f"Task {i}",
            skill_ids=[f"skill-{i}"],
            tech_stack=["python"],
            domain="testing",
            problem_domain=f"Problem domain {i}",
            outcome="success",
            duration_seconds=120,
            complexity="medium",
            session_id=f"session-{i}",
            lessons_learned=[f"lesson {i}"],
        )
        index.store(record)


class TestTopN:
    def test_default_constants(self) -> None:
        assert KNOWLEDGE_TOP_N == 12
        assert EXPERIENCE_TOP_M == 5
        assert SIZE_BUDGET_BYTES == 16384

    def test_top_4_per_kind(self, tmp_path: Path) -> None:
        """ADR-D10-4: 5 entries per kind seeded → top 4 per kind selected."""
        _seed_knowledge(tmp_path, n_per_kind=5)
        compiled = compile_garage_section(tmp_path)
        # 4 per kind × 3 kinds = 12 knowledge entries
        assert compiled.knowledge_count == 12
        assert set(compiled.knowledge_kinds) == {"decision", "solution", "pattern"}

    def test_top_5_experience(self, tmp_path: Path) -> None:
        _seed_experience(tmp_path, n=10)
        compiled = compile_garage_section(tmp_path)
        assert compiled.experience_count == 5


class TestSizeBudgetEnforced:
    """INV-F10-3: SIZE_BUDGET_BYTES strictly enforced."""

    def test_budget_truncation_emits_warning(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Force tiny budget → truncation emits stderr warning."""
        _seed_knowledge(tmp_path, n_per_kind=4)
        stderr = io.StringIO()
        compiled = compile_garage_section(
            tmp_path, stderr=stderr, size_budget_bytes=512
        )
        # Most entries dropped due to tiny budget
        assert compiled.truncated_count > 0
        assert "Truncated" in stderr.getvalue()
        assert "512 bytes" in stderr.getvalue()

    def test_default_budget_not_exceeded(self, tmp_path: Path) -> None:
        _seed_knowledge(tmp_path, n_per_kind=4)
        _seed_experience(tmp_path, n=5)
        compiled = compile_garage_section(tmp_path)
        # Body must fit in default budget
        assert compiled.size_bytes <= SIZE_BUDGET_BYTES


class TestEmptyKindOmitted:
    """ADR-D10-5: 0 patterns 时 ### Recent Patterns 段不出现."""

    def test_no_patterns_section_when_zero(self, tmp_path: Path) -> None:
        # Seed only decisions, no patterns
        storage = FileStorage(tmp_path / ".garage")
        store = KnowledgeStore(storage)
        store.store(
            KnowledgeEntry(
                id="d-1",
                type=KnowledgeType.DECISION,
                topic="Test",
                date=datetime(2026, 4, 24),
                tags=[],
                content="content",
            )
        )
        compiled = compile_garage_section(tmp_path)
        assert "### Recent Decisions" in compiled.body_markdown
        assert "### Recent Patterns" not in compiled.body_markdown
        assert "### Recent Solutions" not in compiled.body_markdown


class TestMarkdownStructure:
    """ADR-D10-5: header + sections + footer."""

    def test_header_present(self, tmp_path: Path) -> None:
        compiled = compile_garage_section(tmp_path)
        assert "## Garage Knowledge Context" in compiled.body_markdown

    def test_footer_with_synced_at(self, tmp_path: Path) -> None:
        _seed_knowledge(tmp_path, n_per_kind=2)
        compiled = compile_garage_section(tmp_path)
        assert "Synced at" in compiled.body_markdown
        assert "by `garage sync`" in compiled.body_markdown

    def test_empty_garage_emits_no_knowledge_message(self, tmp_path: Path) -> None:
        compiled = compile_garage_section(tmp_path)
        assert compiled.is_empty
        assert "No Garage knowledge or experience yet" in compiled.body_markdown


class TestRanking:
    """ADR-D10-5: decision > solution > pattern ordering in output."""

    def test_section_order(self, tmp_path: Path) -> None:
        _seed_knowledge(tmp_path, n_per_kind=2)
        compiled = compile_garage_section(tmp_path)
        body = compiled.body_markdown
        idx_decision = body.index("Recent Decisions")
        idx_solution = body.index("Recent Solutions")
        idx_pattern = body.index("Recent Patterns")
        assert idx_decision < idx_solution < idx_pattern
