"""
Unit tests for extended type definitions.

These tests validate the additional data structures and enums for error handling,
state transitions, checkpoints, and synchronization.
"""

import pytest
from datetime import datetime
from pathlib import Path
from garage_os.types import (
    ErrorCategory,
    StateTransition,
    Checkpoint,
    SyncLogEntry,
    SessionState,
)


class TestErrorCategory:
    """Test ErrorCategory enum."""

    def test_error_category_values(self):
        """Verify all 4 error categories are defined."""
        expected_categories = {
            ErrorCategory.RETRYABLE: "retryable",
            ErrorCategory.USER_INTERVENTION: "user_intervention",
            ErrorCategory.FATAL: "fatal",
            ErrorCategory.IGNORABLE: "ignorable",
        }
        for category, value in expected_categories.items():
            assert category.value == value


class TestStateTransition:
    """Test StateTransition dataclass."""

    def test_state_transition_creation(self):
        """Test creating a state transition record."""
        transition = StateTransition(
            from_state=SessionState.IDLE,
            to_state=SessionState.RUNNING,
            timestamp=datetime.now(),
            reason="User started the workflow",
            metadata={"trigger": "manual", "user_id": "test-user"},
        )
        assert transition.from_state == SessionState.IDLE
        assert transition.to_state == SessionState.RUNNING
        assert transition.reason == "User started the workflow"
        assert len(transition.metadata) == 2
        assert transition.metadata["trigger"] == "manual"


class TestCheckpoint:
    """Test Checkpoint dataclass."""

    def test_checkpoint_creation(self):
        """Test creating a checkpoint with all fields."""
        checkpoint = Checkpoint(
            checkpoint_id="ckpt-001",
            node_id="node-specify",
            timestamp=datetime.now(),
            state_snapshot={"current_step": 2, "variables": {"count": 5}},
            checksum="abc123def456",
        )
        assert checkpoint.checkpoint_id == "ckpt-001"
        assert checkpoint.node_id == "node-specify"
        assert checkpoint.checksum == "abc123def456"
        assert checkpoint.state_snapshot["current_step"] == 2

    def test_checkpoint_without_checksum(self):
        """Test creating a checkpoint without optional checksum."""
        checkpoint = Checkpoint(
            checkpoint_id="ckpt-002",
            node_id="node-design",
            timestamp=datetime.now(),
            state_snapshot={"status": "in_progress"},
        )
        assert checkpoint.checkpoint_id == "ckpt-002"
        assert checkpoint.checksum is None
        assert len(checkpoint.state_snapshot) == 1


class TestSyncLogEntry:
    """Test SyncLogEntry dataclass."""

    def test_sync_log_entry_creation(self):
        """Test creating a sync log entry with all fields."""
        entry = SyncLogEntry(
            artifact_path=Path("docs/specs/test.md"),
            board_status="synced",
            file_exists=True,
            checksum_match=True,
            timestamp=datetime.now(),
            resolution=None,
        )
        assert entry.artifact_path == Path("docs/specs/test.md")
        assert entry.board_status == "synced"
        assert entry.file_exists is True
        assert entry.checksum_match is True
        assert entry.resolution is None

    def test_sync_log_entry_with_resolution(self):
        """Test creating a sync log entry with resolution."""
        entry = SyncLogEntry(
            artifact_path=Path("docs/designs/conflict.md"),
            board_status="conflict",
            file_exists=True,
            checksum_match=False,
            timestamp=datetime.now(),
            resolution="User selected local version",
        )
        assert entry.board_status == "conflict"
        assert entry.checksum_match is False
        assert entry.resolution == "User selected local version"

    def test_sync_log_entry_orphan(self):
        """Test creating a sync log entry for orphan artifact."""
        entry = SyncLogEntry(
            artifact_path=Path("docs/deleted.md"),
            board_status="orphan",
            file_exists=False,
            checksum_match=None,
            timestamp=datetime.now(),
        )
        assert entry.board_status == "orphan"
        assert entry.file_exists is False
        assert entry.checksum_match is None
