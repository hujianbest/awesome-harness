"""Tests for memory extraction orchestration."""

from datetime import datetime

import pytest

from garage_os.memory.candidate_store import CandidateStore
from garage_os.storage.file_storage import FileStorage


@pytest.fixture
def temp_storage(tmp_path):
    """Create a temporary FileStorage instance."""
    return FileStorage(tmp_path)


@pytest.fixture
def candidate_store(temp_storage):
    """Create a CandidateStore instance with temporary storage."""
    return CandidateStore(temp_storage)


@pytest.fixture
def archived_session_payload():
    """Create a minimal archived session payload."""
    now = datetime.now().isoformat()
    return {
        "session_id": "session-001",
        "pack_id": "hf-design",
        "topic": "F003 design",
        "state": "completed",
        "current_node_id": None,
        "created_at": now,
        "updated_at": now,
        "context": {
            "pack_id": "hf-design",
            "topic": "F003 design",
            "graph_variant_id": None,
            "user_goals": [],
            "constraints": [],
            "metadata": {"problem_domain": "memory-pipeline", "tags": ["workspace-first"]},
        },
        "artifacts": [
            {
                "path": "docs/designs/2026-04-18-garage-memory-auto-extraction-design.md",
                "status": "approved",
            }
        ],
        "host": "claude-code",
        "host_version": "unknown",
        "garage_version": "0.1.0",
    }


class TestExtractionOrchestrator:
    """Test T2/T3 extraction orchestration."""

    def test_extract_generates_candidate_batch(
        self,
        temp_storage,
        candidate_store,
        archived_session_payload,
    ) -> None:
        """Valid evidence should produce a batch with at least one candidate."""
        from garage_os.memory.extraction_orchestrator import (
            ExtractionConfig,
            MemoryExtractionOrchestrator,
        )

        orchestrator = MemoryExtractionOrchestrator(temp_storage, candidate_store, ExtractionConfig())

        summary = orchestrator.extract_for_archived_session(archived_session_payload)

        assert summary["evaluation_summary"] == "evaluated_with_candidates"
        assert summary["batch_id"].startswith("batch-")
        stored_batch = candidate_store.retrieve_batch(summary["batch_id"])
        assert stored_batch is not None
        assert len(stored_batch["candidate_ids"]) >= 1

    def test_extract_records_no_evidence(self, temp_storage, candidate_store) -> None:
        """Missing evidence should produce a no_evidence batch."""
        from garage_os.memory.extraction_orchestrator import (
            ExtractionConfig,
            MemoryExtractionOrchestrator,
        )

        orchestrator = MemoryExtractionOrchestrator(temp_storage, candidate_store, ExtractionConfig())

        summary = orchestrator.extract_for_archived_session(
            {
                "session_id": "session-002",
                "pack_id": "hf-design",
                "topic": "Empty session",
                "context": {"metadata": {}},
                "artifacts": [],
            }
        )

        assert summary["evaluation_summary"] == "no_evidence"
        stored_batch = candidate_store.retrieve_batch(summary["batch_id"])
        assert stored_batch is not None
        assert stored_batch["candidate_ids"] == []

    def test_extract_truncates_to_max_pending_and_records_truncated_count(
        self,
        temp_storage,
        candidate_store,
        archived_session_payload,
    ) -> None:
        """Sessions with more than 5 candidate signals must be truncated to 5 with truncated_count > 0 (FR-303a)."""
        from garage_os.memory.extraction_orchestrator import (
            ExtractionConfig,
            MemoryExtractionOrchestrator,
        )

        oversized = dict(archived_session_payload)
        oversized["session_id"] = "session-oversized"
        oversized["artifacts"] = [
            {"path": f"docs/example/file-{idx}.md", "status": "approved"}
            for idx in range(8)
        ]

        orchestrator = MemoryExtractionOrchestrator(
            temp_storage,
            candidate_store,
            ExtractionConfig(),
        )

        summary = orchestrator.extract_for_archived_session(oversized)

        assert summary["evaluation_summary"] == "evaluated_with_candidates"
        assert len(summary["candidate_ids"]) == 5
        assert summary["truncated_count"] >= 1
        stored_batch = candidate_store.retrieve_batch(summary["batch_id"])
        assert stored_batch is not None
        assert stored_batch["truncated_count"] == summary["truncated_count"]

    def test_extract_attaches_source_evidence_anchors(
        self,
        temp_storage,
        candidate_store,
        archived_session_payload,
    ) -> None:
        """Auto-extracted candidates must carry source_evidence_anchors (design §11.6 / FR-302b)."""
        from garage_os.memory.extraction_orchestrator import (
            ExtractionConfig,
            MemoryExtractionOrchestrator,
        )

        orchestrator = MemoryExtractionOrchestrator(
            temp_storage,
            candidate_store,
            ExtractionConfig(),
        )
        orchestrator.extract_for_archived_session(archived_session_payload)

        items_dir = temp_storage._get_full_path("memory/candidates/items")
        files = list(items_dir.glob("*.md"))
        assert files, "expected candidate items to be persisted"
        for path in files:
            text = path.read_text(encoding="utf-8")
            assert "source_evidence_anchors" in text, (
                f"candidate {path.name} is missing source_evidence_anchors"
            )

    def test_extract_emits_complete_experience_summary_candidate(
        self,
        temp_storage,
        candidate_store,
        archived_session_payload,
    ) -> None:
        """experience_summary candidates must include the fields publisher needs."""
        from garage_os.memory.extraction_orchestrator import (
            ExtractionConfig,
            MemoryExtractionOrchestrator,
        )

        orchestrator = MemoryExtractionOrchestrator(
            temp_storage,
            candidate_store,
            ExtractionConfig(),
        )
        orchestrator.extract_for_archived_session(archived_session_payload)

        candidates = candidate_store.list_candidates_by_status("pending_review")
        experience_candidates = [
            c for c in candidates if c["candidate_type"] == "experience_summary"
        ]
        assert experience_candidates, (
            "expected at least one experience_summary candidate from problem_domain signal"
        )
        for candidate in experience_candidates:
            for required in (
                "task_type",
                "domain",
                "problem_domain",
                "outcome",
                "duration_seconds",
            ):
                assert required in candidate, (
                    f"experience_summary candidate missing field '{required}'"
                )

    def test_extraction_failure_writes_error_batch(
        self,
        temp_storage,
        candidate_store,
        archived_session_payload,
        monkeypatch,
    ) -> None:
        """When extraction explodes after archive, orchestrator must persist an error batch (FR-307)."""
        from garage_os.memory.extraction_orchestrator import (
            ExtractionConfig,
            MemoryExtractionOrchestrator,
        )

        orchestrator = MemoryExtractionOrchestrator(
            temp_storage,
            candidate_store,
            ExtractionConfig(),
        )

        def _boom(self, archived_session, signals):
            raise RuntimeError("synthetic extraction failure")

        monkeypatch.setattr(
            MemoryExtractionOrchestrator,
            "_generate_candidates",
            _boom,
        )

        summary = orchestrator.extract_for_archived_session(archived_session_payload)

        assert summary["evaluation_summary"] == "extraction_failed"
        assert "synthetic extraction failure" in summary["metadata"].get("error", "")
        stored = candidate_store.retrieve_batch(summary["batch_id"])
        assert stored is not None
        assert stored["evaluation_summary"] == "extraction_failed"

    def test_extract_records_evaluated_no_candidate(
        self,
        temp_storage,
        candidate_store,
        archived_session_payload,
    ) -> None:
        """Explicitly filtered candidates should produce evaluated_no_candidate."""
        from garage_os.memory.extraction_orchestrator import (
            ExtractionConfig,
            MemoryExtractionOrchestrator,
        )

        config = ExtractionConfig(min_priority_score=0.99)
        orchestrator = MemoryExtractionOrchestrator(temp_storage, candidate_store, config)

        summary = orchestrator.extract_for_archived_session(archived_session_payload)

        assert summary["evaluation_summary"] == "evaluated_no_candidate"
        stored_batch = candidate_store.retrieve_batch(summary["batch_id"])
        assert stored_batch is not None
        assert stored_batch["candidate_ids"] == []
