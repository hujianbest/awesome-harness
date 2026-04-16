"""Tests for Artifact-Board synchronization protocol."""

import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from garage_os.types import (
    ArtifactReference,
    ArtifactRole,
    ArtifactStatus,
)
from garage_os.runtime.artifact_board_sync import (
    ArtifactBoardSync,
    SyncResult,
    SyncAction,
    SyncLogEntry,
)


class TestArtifactBoardSync:
    """Test suite for ArtifactBoardSync."""

    def test_consistent_state_no_sync_needed(self, tmp_path):
        """Test that consistent artifacts require no synchronization."""
        # Arrange: Create a markdown file with front matter
        artifact_file = tmp_path / "docs" / "design.md"
        artifact_file.parent.mkdir(parents=True, exist_ok=True)

        front_matter = {
            "id": "design-001",
            "status": "draft",
            "date": "2026-04-15T12:00:00Z",
        }
        body = "# Design Document\n\nSome content."
        content = f"---\n{self._dict_to_yaml(front_matter)}---\n{body}"
        artifact_file.write_text(content)

        # Create artifact reference matching the file
        artifact = ArtifactReference(
            artifact_role=ArtifactRole.DESIGN,
            path=Path("docs/design.md"),
            status=ArtifactStatus.DRAFT,
            created_at=datetime.fromisoformat("2026-04-15T12:00:00"),
            updated_at=datetime.fromisoformat("2026-04-15T12:00:00"),
        )

        session_dir = tmp_path / "sessions" / "session-001"
        session_dir.mkdir(parents=True, exist_ok=True)

        sync = ArtifactBoardSync(root_dir=tmp_path)

        # Act
        result = sync.sync(
            artifacts=[artifact],
            trigger="session_resume",
            session_dir=session_dir,
        )

        # Assert
        assert len(result.consistent) == 1
        assert len(result.updated) == 0
        assert len(result.orphaned) == 0
        assert len(result.untracked) == 0

    def test_file_updated_board_syncs(self, tmp_path):
        """Test that board syncs when file is updated."""
        # Arrange: Create a file with updated status
        artifact_file = tmp_path / "docs" / "design.md"
        artifact_file.parent.mkdir(parents=True, exist_ok=True)

        front_matter = {
            "id": "design-001",
            "status": "review",  # File has 'review' status
            "date": "2026-04-15T14:00:00Z",  # File has newer date
        }
        body = "# Design Document\n\nUpdated content."
        content = f"---\n{self._dict_to_yaml(front_matter)}---\n{body}"
        artifact_file.write_text(content)

        # Board has 'draft' status (outdated)
        artifact = ArtifactReference(
            artifact_role=ArtifactRole.DESIGN,
            path=Path("docs/design.md"),
            status=ArtifactStatus.DRAFT,  # Board has 'draft'
            created_at=datetime.fromisoformat("2026-04-15T12:00:00"),
            updated_at=datetime.fromisoformat("2026-04-15T12:00:00"),
        )

        session_dir = tmp_path / "sessions" / "session-001"
        session_dir.mkdir(parents=True, exist_ok=True)

        sync = ArtifactBoardSync(root_dir=tmp_path)

        # Act
        result = sync.sync(
            artifacts=[artifact],
            trigger="session_resume",
            session_dir=session_dir,
        )

        # Assert
        assert len(result.consistent) == 0
        assert len(result.updated) == 1
        assert len(result.orphaned) == 0
        assert len(result.untracked) == 0

        # Verify the artifact was updated
        updated_artifact = result.updated[0]
        assert updated_artifact.status == ArtifactStatus.REVIEW
        assert updated_artifact.path == Path("docs/design.md")

    def test_file_deleted_marked_orphan(self, tmp_path):
        """Test that deleted files are marked as orphaned."""
        # Arrange: Board references a file that doesn't exist
        artifact = ArtifactReference(
            artifact_role=ArtifactRole.DESIGN,
            path=Path("docs/design.md"),
            status=ArtifactStatus.DRAFT,
            created_at=datetime.fromisoformat("2026-04-15T12:00:00"),
            updated_at=datetime.fromisoformat("2026-04-15T12:00:00"),
        )

        session_dir = tmp_path / "sessions" / "session-001"
        session_dir.mkdir(parents=True, exist_ok=True)

        sync = ArtifactBoardSync(root_dir=tmp_path)

        # Act
        result = sync.sync(
            artifacts=[artifact],
            trigger="session_resume",
            session_dir=session_dir,
        )

        # Assert
        assert len(result.consistent) == 0
        assert len(result.updated) == 0
        assert len(result.orphaned) == 1
        assert len(result.untracked) == 0

        # Verify orphan info
        orphan_info = result.orphaned[0]
        assert orphan_info.artifact_role == ArtifactRole.DESIGN
        assert orphan_info.path == Path("docs/design.md")

    def test_untracked_file_logged(self, tmp_path):
        """Test that untracked files are logged."""
        # Arrange: Create a file not referenced in board
        artifact_file = tmp_path / "docs" / "untracked.md"
        artifact_file.parent.mkdir(parents=True, exist_ok=True)

        front_matter = {
            "id": "untracked-001",
            "status": "draft",
            "date": "2026-04-15T12:00:00Z",
        }
        body = "# Untracked Document"
        content = f"---\n{self._dict_to_yaml(front_matter)}---\n{body}"
        artifact_file.write_text(content)

        # Board is empty (no artifacts)
        session_dir = tmp_path / "sessions" / "session-001"
        session_dir.mkdir(parents=True, exist_ok=True)

        sync = ArtifactBoardSync(root_dir=tmp_path)

        # Act
        result = sync.sync(
            artifacts=[],
            trigger="session_resume",
            session_dir=session_dir,
        )

        # Assert
        assert len(result.consistent) == 0
        assert len(result.updated) == 0
        assert len(result.orphaned) == 0
        assert len(result.untracked) == 1

        # Verify untracked info
        untracked_info = result.untracked[0]
        assert untracked_info == Path("docs/untracked.md")

    def test_sync_log_json_format(self, tmp_path):
        """Test that sync log is written in correct JSON format."""
        # Arrange: Create a file that needs syncing
        artifact_file = tmp_path / "docs" / "design.md"
        artifact_file.parent.mkdir(parents=True, exist_ok=True)

        front_matter = {
            "id": "design-001",
            "status": "review",
            "date": "2026-04-15T14:00:00Z",
        }
        body = "# Design"
        content = f"---\n{self._dict_to_yaml(front_matter)}---\n{body}"
        artifact_file.write_text(content)

        artifact = ArtifactReference(
            artifact_role=ArtifactRole.DESIGN,
            path=Path("docs/design.md"),
            status=ArtifactStatus.DRAFT,
            created_at=datetime.fromisoformat("2026-04-15T12:00:00"),
            updated_at=datetime.fromisoformat("2026-04-15T12:00:00"),
        )

        session_dir = tmp_path / "sessions" / "session-001"
        session_dir.mkdir(parents=True, exist_ok=True)

        sync = ArtifactBoardSync(root_dir=tmp_path)

        # Act
        with patch("garage_os.runtime.artifact_board_sync.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.fromisoformat("2026-04-15T15:00:00")
            result = sync.sync(
                artifacts=[artifact],
                trigger="session_resume",
                session_dir=session_dir,
            )

        # Assert: Check sync-log.json
        log_file = session_dir / "sync-log.json"
        assert log_file.exists()

        log_content = json.loads(log_file.read_text())
        assert log_content["trigger"] == "session_resume"
        assert "timestamp" in log_content
        assert log_content["artifact_path"] == "docs/design.md"
        assert log_content["board_status"] == "draft"
        assert log_content["file_status"] == "review"
        assert log_content["action"] == "board_updated"
        assert log_content["resolved_by"] == "artifact_first_rule"

    def test_trigger_session_resume(self, tmp_path):
        """Test sync triggered on session resume."""
        artifact_file = tmp_path / "docs" / "design.md"
        artifact_file.parent.mkdir(parents=True, exist_ok=True)

        front_matter = {"status": "draft", "date": "2026-04-15T12:00:00Z"}
        content = f"---\n{self._dict_to_yaml(front_matter)}---\n# Design"
        artifact_file.write_text(content)

        artifact = ArtifactReference(
            artifact_role=ArtifactRole.DESIGN,
            path=Path("docs/design.md"),
            status=ArtifactStatus.DRAFT,
            created_at=datetime.fromisoformat("2026-04-15T12:00:00"),
            updated_at=datetime.fromisoformat("2026-04-15T12:00:00"),
        )

        session_dir = tmp_path / "sessions" / "session-001"
        session_dir.mkdir(parents=True, exist_ok=True)

        sync = ArtifactBoardSync(root_dir=tmp_path)

        # Act
        result = sync.sync(
            artifacts=[artifact],
            trigger="session_resume",
            session_dir=session_dir,
        )

        # Assert
        assert len(result.consistent) == 1

        # Verify log contains correct trigger
        log_file = session_dir / "sync-log.json"
        log_content = json.loads(log_file.read_text())
        assert log_content["trigger"] == "session_resume"

    def test_trigger_skill_pre_execute(self, tmp_path):
        """Test sync triggered before skill execution."""
        artifact_file = tmp_path / "docs" / "design.md"
        artifact_file.parent.mkdir(parents=True, exist_ok=True)

        front_matter = {"status": "review", "date": "2026-04-15T14:00:00Z"}
        content = f"---\n{self._dict_to_yaml(front_matter)}---\n# Design"
        artifact_file.write_text(content)

        artifact = ArtifactReference(
            artifact_role=ArtifactRole.DESIGN,
            path=Path("docs/design.md"),
            status=ArtifactStatus.DRAFT,
            created_at=datetime.fromisoformat("2026-04-15T12:00:00"),
            updated_at=datetime.fromisoformat("2026-04-15T12:00:00"),
        )

        session_dir = tmp_path / "sessions" / "session-001"
        session_dir.mkdir(parents=True, exist_ok=True)

        sync = ArtifactBoardSync(root_dir=tmp_path)

        # Act
        result = sync.sync(
            artifacts=[artifact],
            trigger="skill_pre_execute",
            session_dir=session_dir,
        )

        # Assert
        assert len(result.updated) == 1

        # Verify log contains correct trigger
        log_file = session_dir / "sync-log.json"
        log_content = json.loads(log_file.read_text())
        assert log_content["trigger"] == "skill_pre_execute"

    def test_trigger_skill_post_execute(self, tmp_path):
        """Test sync triggered after skill execution."""
        artifact_file = tmp_path / "docs" / "design.md"
        artifact_file.parent.mkdir(parents=True, exist_ok=True)

        front_matter = {"status": "approved", "date": "2026-04-15T16:00:00Z"}
        content = f"---\n{self._dict_to_yaml(front_matter)}---\n# Design"
        artifact_file.write_text(content)

        artifact = ArtifactReference(
            artifact_role=ArtifactRole.DESIGN,
            path=Path("docs/design.md"),
            status=ArtifactStatus.REVIEW,
            created_at=datetime.fromisoformat("2026-04-15T12:00:00"),
            updated_at=datetime.fromisoformat("2026-04-15T14:00:00"),
        )

        session_dir = tmp_path / "sessions" / "session-001"
        session_dir.mkdir(parents=True, exist_ok=True)

        sync = ArtifactBoardSync(root_dir=tmp_path)

        # Act
        result = sync.sync(
            artifacts=[artifact],
            trigger="skill_post_execute",
            session_dir=session_dir,
        )

        # Assert
        assert len(result.updated) == 1

        # Verify log contains correct trigger
        log_file = session_dir / "sync-log.json"
        log_content = json.loads(log_file.read_text())
        assert log_content["trigger"] == "skill_post_execute"

    def _dict_to_yaml(self, data: dict) -> str:
        """Convert dict to YAML string (helper method)."""
        import yaml

        return yaml.dump(data, default_flow_style=False, sort_keys=False).rstrip(
            "\n"
        ) + "\n"


class TestSyncResult:
    """Test suite for SyncResult dataclass."""

    def test_sync_result_initialization(self):
        """Test SyncResult can be initialized."""
        result = SyncResult(
            consistent=[],
            updated=[],
            orphaned=[],
            untracked=[],
        )

        assert result.consistent == []
        assert result.updated == []
        assert result.orphaned == []
        assert result.untracked == []


class TestSyncAction:
    """Test suite for SyncAction enum."""

    def test_sync_action_values(self):
        """Test SyncAction enum has correct values."""
        assert SyncAction.BOARD_UPDATED.value == "board_updated"
        assert SyncAction.ORPHANED.value == "orphaned"
        assert SyncAction.UNTRACKED.value == "untracked"
        assert SyncAction.CONSISTENT.value == "consistent"
