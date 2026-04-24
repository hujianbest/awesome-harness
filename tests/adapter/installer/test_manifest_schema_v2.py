"""F009 T3: Manifest schema 2 字段 + write/read 测试.

Covers:
- spec FR-905 (manifest schema 2 字段: dst absolute + scope)
- design ADR-D9-1 (字段命名 'project'/'user')
- design ADR-D9-3 (dst 绝对展开, 不带 ~/ 前缀)
- design CON-901 (write_manifest 始终写 schema_version=2)

Fixture isolation:
- 用 tmp_path 隔离, 不影响真实 .garage/
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from garage_os.adapter.installer.manifest import (
    MANIFEST_SCHEMA_VERSION,
    Manifest,
    ManifestFileEntry,
    read_manifest,
    write_manifest,
)


def _make_v2_entry(
    src: str = "packs/garage/skills/garage-hello/SKILL.md",
    dst: str = "/workspace/.claude/skills/garage-hello/SKILL.md",
    host: str = "claude",
    pack_id: str = "garage",
    scope: str = "project",
    content_hash: str = "abc",
) -> ManifestFileEntry:
    return ManifestFileEntry(
        src=src, dst=dst, host=host, pack_id=pack_id, scope=scope, content_hash=content_hash
    )


class TestSchemaV2Constant:
    """ADR-D9-1: MANIFEST_SCHEMA_VERSION 升到 2."""

    def test_constant_is_two(self) -> None:
        assert MANIFEST_SCHEMA_VERSION == 2


class TestManifestFileEntryFieldsExtended:
    """ADR-D9-1 + CON-901: 既有 ManifestFileEntry 类名保留 + 字段扩展同一类 (不引入 V2 新类)."""

    def test_entry_has_scope_field(self) -> None:
        entry = _make_v2_entry(scope="user")
        assert entry.scope == "user"

    def test_entry_scope_default_is_project(self) -> None:
        # 默认 scope='project' 兼容 schema 1 entry 在 migration 路径中的填充
        entry = ManifestFileEntry(
            src="a", dst="/abs/b", host="claude", pack_id="garage", content_hash="x"
        )
        assert entry.scope == "project"


class TestWriteManifestAlwaysSchemaTwo:
    """ADR-D9-3 + ADR-D9-1: write_manifest 始终写 schema_version=2."""

    def test_write_manifest_emits_schema_two_on_disk(self, tmp_path: Path) -> None:
        garage_dir = tmp_path / ".garage"
        (garage_dir / "config").mkdir(parents=True)

        manifest = Manifest(
            schema_version=2,  # F009 default
            installed_hosts=["claude"],
            installed_packs=["garage"],
            installed_at=datetime(2026, 4, 23).isoformat(),
            files=[_make_v2_entry()],
        )
        write_manifest(garage_dir, manifest)

        on_disk = json.loads(
            (garage_dir / "config" / "host-installer.json").read_text()
        )
        assert on_disk["schema_version"] == 2

    def test_write_manifest_overrides_input_schema_version(
        self, tmp_path: Path
    ) -> None:
        """即使调用方传 schema_version=1, write_manifest 也强制写 2 (fresh write 始终最新)."""
        garage_dir = tmp_path / ".garage"
        (garage_dir / "config").mkdir(parents=True)

        manifest = Manifest(
            schema_version=1,  # 调用方误传 1
            installed_hosts=["claude"],
            installed_packs=["garage"],
            installed_at=datetime(2026, 4, 23).isoformat(),
            files=[_make_v2_entry()],
        )
        write_manifest(garage_dir, manifest)

        on_disk = json.loads(
            (garage_dir / "config" / "host-installer.json").read_text()
        )
        # write_manifest 强制写 MANIFEST_SCHEMA_VERSION (=2), 不是调用方传入值
        assert on_disk["schema_version"] == 2

    def test_write_manifest_includes_scope_in_files(self, tmp_path: Path) -> None:
        """每个 files[] entry 都含 scope 字段."""
        garage_dir = tmp_path / ".garage"
        (garage_dir / "config").mkdir(parents=True)

        manifest = Manifest(
            schema_version=2,
            installed_hosts=["claude"],
            installed_packs=["garage"],
            installed_at=datetime(2026, 4, 23).isoformat(),
            files=[
                _make_v2_entry(scope="project"),
                _make_v2_entry(
                    dst="/home/alice/.claude/skills/garage-hello/SKILL.md",
                    scope="user",
                ),
            ],
        )
        write_manifest(garage_dir, manifest)

        on_disk = json.loads(
            (garage_dir / "config" / "host-installer.json").read_text()
        )
        scopes = {e["scope"] for e in on_disk["files"]}
        assert scopes == {"project", "user"}

    def test_write_manifest_dst_absolute_posix(self, tmp_path: Path) -> None:
        """ADR-D9-3: dst 绝对展开, POSIX 形式."""
        garage_dir = tmp_path / ".garage"
        (garage_dir / "config").mkdir(parents=True)

        manifest = Manifest(
            schema_version=2,
            installed_hosts=["claude"],
            installed_packs=["garage"],
            installed_at=datetime(2026, 4, 23).isoformat(),
            files=[
                _make_v2_entry(
                    dst="/home/alice/.claude/skills/garage-hello/SKILL.md"
                ),
            ],
        )
        write_manifest(garage_dir, manifest)

        on_disk = json.loads(
            (garage_dir / "config" / "host-installer.json").read_text()
        )
        # dst 是 absolute POSIX (forward slash, 含 home)
        assert on_disk["files"][0]["dst"].startswith("/home/alice/.claude/")
        assert "\\" not in on_disk["files"][0]["dst"]


class TestReadManifestSchemaV2:
    """read_manifest 对 schema_version=2 的文件直接读取, 无 migration."""

    def test_read_manifest_schema_v2_no_migration(self, tmp_path: Path) -> None:
        garage_dir = tmp_path / ".garage"
        (garage_dir / "config").mkdir(parents=True)

        # 写入 schema 2 manifest
        original = Manifest(
            schema_version=2,
            installed_hosts=["claude"],
            installed_packs=["garage"],
            installed_at=datetime(2026, 4, 23).isoformat(),
            files=[_make_v2_entry(scope="user")],
        )
        write_manifest(garage_dir, original)

        # 读回, 应直接是 schema 2 (无 migration)
        reloaded = read_manifest(garage_dir)
        assert reloaded is not None
        assert reloaded.schema_version == 2
        assert reloaded.files[0].scope == "user"
        # round-trip 保持
        assert reloaded == original


class TestRoundTripSchemaV2:
    """Schema 2 round-trip 完整性 (write → read 等价)."""

    def test_round_trip_mixed_scope(self, tmp_path: Path) -> None:
        garage_dir = tmp_path / ".garage"
        (garage_dir / "config").mkdir(parents=True)

        # 注意: write_manifest 会按 (src, dst, host, scope) 排序; reloaded files
        # 顺序由排序决定. 比较时按集合 / sorted 比较以避免顺序敏感.
        manifest = Manifest(
            schema_version=2,
            installed_hosts=["claude", "cursor"],
            installed_packs=["coding", "garage"],
            installed_at=datetime(2026, 4, 23, 12).isoformat(),
            files=[
                _make_v2_entry(
                    dst="/workspace/.claude/skills/hf-specify/SKILL.md",
                    scope="project",
                ),
                _make_v2_entry(
                    src="packs/coding/skills/hf-design/SKILL.md",
                    dst="/home/alice/.cursor/skills/hf-design/SKILL.md",
                    host="cursor",
                    pack_id="coding",
                    scope="user",
                    content_hash="def",
                ),
            ],
        )
        write_manifest(garage_dir, manifest)
        reloaded = read_manifest(garage_dir)

        # 顶层字段一致
        assert reloaded is not None
        assert reloaded.schema_version == 2
        assert reloaded.installed_hosts == manifest.installed_hosts
        assert reloaded.installed_packs == manifest.installed_packs
        assert reloaded.installed_at == manifest.installed_at
        # files 集合 (无视顺序) 一致
        assert sorted(reloaded.files, key=lambda e: (e.src, e.dst)) == sorted(
            manifest.files, key=lambda e: (e.src, e.dst)
        )
