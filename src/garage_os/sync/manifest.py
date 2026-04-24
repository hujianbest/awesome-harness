"""F010 sync manifest: ``.garage/config/sync-manifest.json`` (schema_version=1).

Implements ADR-D10-6 + spec § 5.1 A4 schema.

Independent from ``host-installer.json`` (CON-1005): two separate files, separate
schemas, mutual non-reference.

ADR-D10-6: ``targets[].path`` is absolute POSIX path (per ``Path(...).resolve(strict=False).as_posix()``,
same rule as F009 schema 2 ``host-installer.json files[].dst``).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

# F010: sync-manifest.json schema version
SYNC_MANIFEST_SCHEMA_VERSION = 1
SYNC_MANIFEST_FILENAME = "sync-manifest.json"
CONFIG_SUBDIR = "config"


class SyncManifestMigrationError(ValueError):
    """Raised on JSON parse failure or unsupported schema_version. Read-only call
    does NOT overwrite existing file (F009 CON-904 同精神 sync-side mirror)."""


@dataclass
class SyncSources:
    knowledge_count: int
    experience_count: int
    knowledge_kinds: list[str] = field(default_factory=list)
    size_bytes: int = 0
    size_budget_bytes: int = 0


@dataclass
class SyncTargetEntry:
    host: str
    scope: str  # "project" | "user"
    path: str  # absolute POSIX
    content_hash: str  # SHA-256 of marker block content
    wrote_at: str  # ISO 8601 UTC
    action: str  # F007 WriteAction.value: write_new | update_from_source | skip_locally_modified | overwrite_forced


@dataclass
class SyncManifest:
    schema_version: int  # always 1 in F010
    synced_at: str  # ISO 8601 UTC
    sources: SyncSources
    targets: list[SyncTargetEntry] = field(default_factory=list)


def write_sync_manifest(garage_dir: Path, manifest: SyncManifest) -> Path:
    """Persist manifest to ``garage_dir/config/sync-manifest.json``.

    Always writes ``schema_version = SYNC_MANIFEST_SCHEMA_VERSION`` (overrides input).
    Sorts ``targets`` by (host, scope) for stable diffs (与 F009 ASCII-sorted精神).
    """
    config_dir = garage_dir / CONFIG_SUBDIR
    config_dir.mkdir(parents=True, exist_ok=True)
    target = config_dir / SYNC_MANIFEST_FILENAME

    targets_sorted = sorted(manifest.targets, key=lambda t: (t.host, t.scope))
    payload = {
        "schema_version": SYNC_MANIFEST_SCHEMA_VERSION,
        "synced_at": manifest.synced_at,
        "sources": asdict(manifest.sources),
        "targets": [asdict(t) for t in targets_sorted],
    }
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return target


def read_sync_manifest(garage_dir: Path) -> SyncManifest | None:
    """Load sync-manifest.json or None when the file does not exist.

    Raises:
        SyncManifestMigrationError: on JSON parse failure or unsupported schema.
            File is NOT overwritten on error (sync-side mirror of F009 CON-904).
    """
    target = garage_dir / CONFIG_SUBDIR / SYNC_MANIFEST_FILENAME
    if not target.is_file():
        return None
    try:
        raw = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SyncManifestMigrationError(
            f"Failed to parse sync-manifest at {target}: {exc}"
        ) from exc

    schema_version = int(raw.get("schema_version", SYNC_MANIFEST_SCHEMA_VERSION))
    if schema_version != 1:
        raise SyncManifestMigrationError(
            f"Unsupported sync-manifest schema_version={schema_version} in {target}; "
            f"supported: 1 (F010)"
        )

    try:
        sources_raw = raw.get("sources", {})
        sources = SyncSources(
            knowledge_count=int(sources_raw.get("knowledge_count", 0)),
            experience_count=int(sources_raw.get("experience_count", 0)),
            knowledge_kinds=list(sources_raw.get("knowledge_kinds", [])),
            size_bytes=int(sources_raw.get("size_bytes", 0)),
            size_budget_bytes=int(sources_raw.get("size_budget_bytes", 0)),
        )
        targets = [
            SyncTargetEntry(
                host=str(t["host"]),
                scope=str(t["scope"]),
                path=str(t["path"]),
                content_hash=str(t["content_hash"]),
                wrote_at=str(t["wrote_at"]),
                action=str(t["action"]),
            )
            for t in raw.get("targets", [])
        ]
        return SyncManifest(
            schema_version=1,
            synced_at=str(raw.get("synced_at", "")),
            sources=sources,
            targets=sorted(targets, key=lambda t: (t.host, t.scope)),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise SyncManifestMigrationError(
            f"Failed to parse sync-manifest at {target}: {exc}"
        ) from exc
