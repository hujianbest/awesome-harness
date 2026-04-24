"""F009 T3: Manifest schema 1 → 2 migration + ManifestMigrationError 测试.

Covers:
- spec FR-905 (manifest schema migration 单向, 1 → 2)
- spec FR-905 验收 #4 + CON-904 (migration 失败时旧 manifest 不被覆盖, 安全语义硬门槛)
- design ADR-D9-8 (ManifestMigrationError + exit 1)
- design ADR-D9-3 (dst project-relative → absolute)
- design ADR-D9-1 (旧 entry 默认 scope='project')

Fixture isolation:
- 用 tmp_path 隔离, 不影响真实 .garage/
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

from garage_os.adapter.installer.manifest import (
    Manifest,
    ManifestFileEntry,
    ManifestMigrationError,
    migrate_v1_to_v2,
    read_manifest,
)


def _write_schema_v1_manifest(garage_dir: Path, files: list[dict]) -> Path:
    """Helper: 构造 F007/F008 schema 1 manifest 写入磁盘."""
    config_dir = garage_dir / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    target = config_dir / "host-installer.json"
    payload = {
        "schema_version": 1,
        "installed_hosts": ["claude"],
        "installed_packs": ["garage"],
        "installed_at": "2026-04-23T10:00:00",
        "files": files,
    }
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return target


class TestMigrateV1ToV2Function:
    """ADR-D9-1 + ADR-D9-3: migrate_v1_to_v2 函数行为."""

    def test_migrate_adds_scope_project_to_each_entry(self, tmp_path: Path) -> None:
        v1 = Manifest(
            schema_version=1,
            installed_hosts=["claude"],
            installed_packs=["garage"],
            installed_at="2026-04-23T10:00:00",
            files=[
                ManifestFileEntry(
                    src="packs/garage/skills/garage-hello/SKILL.md",
                    dst=".claude/skills/garage-hello/SKILL.md",  # schema 1 relative
                    host="claude",
                    pack_id="garage",
                    content_hash="abc",
                ),
            ],
        )
        v2 = migrate_v1_to_v2(v1, workspace_root=tmp_path)
        assert v2.schema_version == 2
        assert len(v2.files) == 1
        assert v2.files[0].scope == "project"

    def test_migrate_converts_dst_to_absolute(self, tmp_path: Path) -> None:
        v1 = Manifest(
            schema_version=1,
            installed_hosts=["claude"],
            installed_packs=["garage"],
            installed_at="2026-04-23T10:00:00",
            files=[
                ManifestFileEntry(
                    src="packs/garage/skills/garage-hello/SKILL.md",
                    dst=".claude/skills/garage-hello/SKILL.md",
                    host="claude",
                    pack_id="garage",
                    content_hash="abc",
                ),
            ],
        )
        v2 = migrate_v1_to_v2(v1, workspace_root=tmp_path)
        # dst 转 absolute (workspace_root + relative)
        expected = (tmp_path / ".claude/skills/garage-hello/SKILL.md").as_posix()
        assert v2.files[0].dst == expected

    def test_migrate_preserves_other_top_level_fields(self, tmp_path: Path) -> None:
        v1 = Manifest(
            schema_version=1,
            installed_hosts=["claude", "cursor"],
            installed_packs=["coding", "garage"],
            installed_at="2026-04-23T10:00:00",
            files=[],
        )
        v2 = migrate_v1_to_v2(v1, workspace_root=tmp_path)
        assert v2.installed_hosts == ["claude", "cursor"]
        assert v2.installed_packs == ["coding", "garage"]
        assert v2.installed_at == "2026-04-23T10:00:00"


class TestReadManifestAutoMigration:
    """FR-905: read_manifest 自动 detect schema_version=1 → 调 migrate."""

    def test_read_v1_on_disk_returns_v2_in_memory(self, tmp_path: Path) -> None:
        """F008 用户已落 schema 1 manifest, F009 read 后内存对象是 schema 2."""
        garage_dir = tmp_path / ".garage"
        _write_schema_v1_manifest(
            garage_dir,
            files=[
                {
                    "src": "packs/garage/skills/garage-hello/SKILL.md",
                    "dst": ".claude/skills/garage-hello/SKILL.md",
                    "host": "claude",
                    "pack_id": "garage",
                    "content_hash": "abc",
                }
            ],
        )

        result = read_manifest(garage_dir)
        assert result is not None
        # F009: 自动 migrate 到 schema 2
        assert result.schema_version == 2
        # 旧 entry 默认 scope='project'
        assert result.files[0].scope == "project"
        # dst 转 absolute
        expected_dst = (
            tmp_path / ".claude/skills/garage-hello/SKILL.md"
        ).as_posix()
        assert result.files[0].dst == expected_dst

    def test_read_v2_on_disk_no_migration(self, tmp_path: Path) -> None:
        garage_dir = tmp_path / ".garage"
        config_dir = garage_dir / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        target = config_dir / "host-installer.json"
        target.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "installed_hosts": ["claude"],
                    "installed_packs": ["garage"],
                    "installed_at": "2026-04-23T10:00:00",
                    "files": [
                        {
                            "src": "packs/garage/skills/garage-hello/SKILL.md",
                            "dst": "/workspace/.claude/skills/garage-hello/SKILL.md",
                            "host": "claude",
                            "pack_id": "garage",
                            "scope": "project",
                            "content_hash": "abc",
                        }
                    ],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        result = read_manifest(garage_dir)
        assert result is not None
        assert result.schema_version == 2
        assert result.files[0].scope == "project"


class TestSafetySemantics:
    """FR-905 验收 #4 + CON-904 安全语义硬门槛: migration 失败时旧 manifest 不被覆盖."""

    def test_corrupted_manifest_not_overwritten(self, tmp_path: Path) -> None:
        """JSON 损坏时抛 ManifestMigrationError + 旧文件字节级 + mtime 严格保留."""
        garage_dir = tmp_path / ".garage"
        config_dir = garage_dir / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        target = config_dir / "host-installer.json"
        # 写入故意损坏的 JSON (闭合括号缺失)
        original_content = '{"schema_version": 1, "files": [BROKEN'
        target.write_text(original_content, encoding="utf-8")
        original_sha = hashlib.sha256(target.read_bytes()).hexdigest()
        original_mtime = target.stat().st_mtime

        # read_manifest 应抛 ManifestMigrationError
        with pytest.raises(ManifestMigrationError) as exc_info:
            read_manifest(garage_dir)

        assert "Failed to parse manifest" in str(exc_info.value)
        # 安全语义硬门槛: 文件字节级未变
        assert target.read_bytes().decode("utf-8") == original_content
        assert hashlib.sha256(target.read_bytes()).hexdigest() == original_sha
        # mtime 也未变 (read_manifest 不应触发任何 write)
        assert target.stat().st_mtime == original_mtime

    def test_unsupported_schema_version_raises_no_overwrite(self, tmp_path: Path) -> None:
        """未来 schema 版本 (e.g. 3) 应抛 ManifestMigrationError + 文件不被覆盖."""
        garage_dir = tmp_path / ".garage"
        config_dir = garage_dir / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        target = config_dir / "host-installer.json"
        original_payload = {
            "schema_version": 99,  # 未来未支持的 schema
            "installed_hosts": [],
            "installed_packs": [],
            "installed_at": "2026-04-23T10:00:00",
            "files": [],
        }
        target.write_text(
            json.dumps(original_payload, indent=2), encoding="utf-8"
        )
        original_sha = hashlib.sha256(target.read_bytes()).hexdigest()

        with pytest.raises(ManifestMigrationError) as exc_info:
            read_manifest(garage_dir)
        assert "Unsupported manifest schema_version=99" in str(exc_info.value)
        # 文件未被覆盖
        assert hashlib.sha256(target.read_bytes()).hexdigest() == original_sha


class TestErrorTypes:
    """ADR-D9-8 + ADR-D9-10: ManifestMigrationError 与 UserHomeNotFoundError 类型."""

    def test_manifest_migration_error_is_value_error_subclass(self) -> None:
        """ADR-D9-8: ManifestMigrationError 是 ValueError 子类."""
        assert issubclass(ManifestMigrationError, ValueError)

    def test_user_home_not_found_error_is_runtime_error_subclass(self) -> None:
        """ADR-D9-10: UserHomeNotFoundError 是 RuntimeError 子类."""
        from garage_os.adapter.installer.manifest import UserHomeNotFoundError

        assert issubclass(UserHomeNotFoundError, RuntimeError)
