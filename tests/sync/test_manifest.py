"""F010 T3 prep: sync-manifest.py basic tests (round-trip + schema).

Note: manifest dataclass + read/write are introduced in T2 (compiler imports them
via __init__.py). T3 will add isolation tests + pipeline integration.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from garage_os.sync.manifest import (
    SYNC_MANIFEST_SCHEMA_VERSION,
    SyncManifest,
    SyncManifestMigrationError,
    SyncSources,
    SyncTargetEntry,
    read_sync_manifest,
    write_sync_manifest,
)


class TestSchemaVersion:
    def test_constant_is_one(self) -> None:
        assert SYNC_MANIFEST_SCHEMA_VERSION == 1


class TestRoundTrip:
    def test_write_then_read(self, tmp_path: Path) -> None:
        garage_dir = tmp_path / ".garage"
        manifest = SyncManifest(
            schema_version=1,
            synced_at="2026-04-24T18:30:00Z",
            sources=SyncSources(
                knowledge_count=5,
                experience_count=2,
                knowledge_kinds=["decision", "solution"],
                size_bytes=2048,
                size_budget_bytes=16384,
            ),
            targets=[
                SyncTargetEntry(
                    host="claude",
                    scope="project",
                    path="/abs/path/CLAUDE.md",
                    content_hash="abc123",
                    wrote_at="2026-04-24T18:30:00Z",
                    action="write_new",
                ),
            ],
        )
        write_sync_manifest(garage_dir, manifest)
        reloaded = read_sync_manifest(garage_dir)
        assert reloaded is not None
        assert reloaded.schema_version == 1
        assert reloaded.synced_at == manifest.synced_at
        assert reloaded.sources.knowledge_count == 5
        assert len(reloaded.targets) == 1
        assert reloaded.targets[0].action == "write_new"


class TestReadMissing:
    def test_returns_none_when_no_file(self, tmp_path: Path) -> None:
        assert read_sync_manifest(tmp_path / ".garage") is None


class TestSchemaMigrationError:
    def test_corrupted_json_raises(self, tmp_path: Path) -> None:
        config_dir = tmp_path / ".garage" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "sync-manifest.json").write_text("{BROKEN", encoding="utf-8")

        with pytest.raises(SyncManifestMigrationError) as exc_info:
            read_sync_manifest(tmp_path / ".garage")
        assert "Failed to parse" in str(exc_info.value)

    def test_unsupported_schema_raises(self, tmp_path: Path) -> None:
        config_dir = tmp_path / ".garage" / "config"
        config_dir.mkdir(parents=True)
        (config_dir / "sync-manifest.json").write_text(
            json.dumps({"schema_version": 99, "synced_at": "x", "sources": {}, "targets": []}),
            encoding="utf-8",
        )

        with pytest.raises(SyncManifestMigrationError) as exc_info:
            read_sync_manifest(tmp_path / ".garage")
        assert "Unsupported sync-manifest schema_version=99" in str(exc_info.value)


class TestStableOrdering:
    def test_targets_sorted_by_host_scope(self, tmp_path: Path) -> None:
        garage_dir = tmp_path / ".garage"
        manifest = SyncManifest(
            schema_version=1,
            synced_at="2026-04-24T18:30:00Z",
            sources=SyncSources(0, 0),
            targets=[
                SyncTargetEntry("opencode", "user", "/p3", "h3", "t3", "write_new"),
                SyncTargetEntry("claude", "user", "/p2", "h2", "t2", "write_new"),
                SyncTargetEntry("claude", "project", "/p1", "h1", "t1", "write_new"),
            ],
        )
        write_sync_manifest(garage_dir, manifest)

        on_disk = json.loads(
            (garage_dir / "config" / "sync-manifest.json").read_text()
        )
        # claude/project, claude/user, opencode/user ordering
        actual_order = [(t["host"], t["scope"]) for t in on_disk["targets"]]
        assert actual_order == [("claude", "project"), ("claude", "user"), ("opencode", "user")]
