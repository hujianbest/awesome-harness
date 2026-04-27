"""F016 T4 sentinel: Cr-1 r2 critical — `garage init --yes` MUST NOT enable memory.

The single most important regression guard for F016: the `garage init --yes`
flag has long-standing F007 semantics ("CI / scripted use; equivalent to
--hosts none if no --hosts given"). F016 must NOT overload `--yes` to also
enable memory extraction. Otherwise, every existing `garage init --yes` call
in CI / docs / shell scripts silently flips memory on without user consent.

This sentinel guards Cr-1 r2 USER-INPUT decision (option a). If anyone in
F017+ tries to "make --yes opt into memory", this test fails and forces a
deliberate user-pact discussion.
"""

from __future__ import annotations

import json
from pathlib import Path

from garage_os.cli import main


def test_init_yes_keeps_memory_disabled(tmp_path: Path) -> None:
    """garage init --yes → platform.json memory.extraction_enabled=false (Cr-1 r2).

    Companion test in tests/memory_activation/test_cli.py covers the full
    decision matrix (--yes / --no-memory / interactive prompt y/n/empty).
    This sentinel pins the canonical Cr-1 r2 contract in a clearly-named file
    so `git grep init_yes_does_not_enable_memory` finds it.
    """
    ws = tmp_path / "ws"
    ws.mkdir()
    rc = main(["init", "--path", str(ws), "--yes"])
    assert rc == 0

    config_path = ws / ".garage" / "config" / "platform.json"
    assert config_path.is_file()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert config["memory"]["extraction_enabled"] is False, (
        "Cr-1 r2 violated: `garage init --yes` enabled memory.extraction_enabled. "
        "F007 既有 --yes 语义 = CI/scripted use ONLY (skip host installer prompt); "
        "F016 MUST NOT overload it to also opt into memory. "
        "If you need --yes + memory enabled, use: garage init --yes && garage memory enable"
    )
