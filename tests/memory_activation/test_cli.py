"""F016 T3 tests: CLI memory enable / disable / status / ingest + init prompt + status integration."""

from __future__ import annotations

import io
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from garage_os.cli import main


def _read_platform_config(workspace: Path) -> dict:
    return json.loads((workspace / ".garage" / "config" / "platform.json").read_text(encoding="utf-8"))


# T3.1 — `init --yes` does NOT enable memory (Cr-1 r2 sentinel)
class TestInitYesDoesNotEnableMemory:
    """Cr-1 r2 critical: --yes preserves F007 host semantics; does NOT touch memory.

    This is the core USER-INPUT decision; if F016 ever regresses this behavior,
    F007 CI / scripted-use scenarios break silently.
    """

    def test_init_yes_keeps_extraction_disabled(self, tmp_path: Path) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        rc = main(["init", "--path", str(ws), "--yes"])
        assert rc == 0
        config = _read_platform_config(ws)
        assert config["memory"]["extraction_enabled"] is False

    def test_init_no_memory_keeps_extraction_disabled(self, tmp_path: Path) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        rc = main(["init", "--path", str(ws), "--no-memory"])
        assert rc == 0
        config = _read_platform_config(ws)
        assert config["memory"]["extraction_enabled"] is False

    def test_init_yes_no_memory_keeps_disabled(self, tmp_path: Path) -> None:
        """Both flags together → still disabled."""
        ws = tmp_path / "ws"
        ws.mkdir()
        rc = main(["init", "--path", str(ws), "--yes", "--no-memory"])
        assert rc == 0
        config = _read_platform_config(ws)
        assert config["memory"]["extraction_enabled"] is False


# T3.2 — interactive prompt path
class TestInitInteractivePrompt:
    def test_prompt_y_enables(self, tmp_path: Path) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        with patch("garage_os.cli.sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = True
            with patch("builtins.input", return_value="y"):
                rc = main(["init", "--path", str(ws)])
        assert rc == 0
        config = _read_platform_config(ws)
        assert config["memory"]["extraction_enabled"] is True

    def test_prompt_empty_enables_default(self, tmp_path: Path) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        with patch("garage_os.cli.sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = True
            with patch("builtins.input", return_value=""):
                rc = main(["init", "--path", str(ws)])
        assert rc == 0
        config = _read_platform_config(ws)
        assert config["memory"]["extraction_enabled"] is True  # default Y on empty

    def test_prompt_n_disables(self, tmp_path: Path) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        with patch("garage_os.cli.sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = True
            with patch("builtins.input", return_value="n"):
                rc = main(["init", "--path", str(ws)])
        assert rc == 0
        config = _read_platform_config(ws)
        assert config["memory"]["extraction_enabled"] is False


# T3.3 — memory enable / disable
class TestMemoryEnableDisable:
    def test_enable_sets_true(self, tmp_path: Path, capsys) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        main(["init", "--path", str(ws), "--no-memory"])
        capsys.readouterr()

        rc = main(["memory", "enable", "--path", str(ws)])
        assert rc == 0
        config = _read_platform_config(ws)
        assert config["memory"]["extraction_enabled"] is True
        captured = capsys.readouterr()
        assert "Memory extraction enabled" in captured.out
        assert "garage memory ingest" in captured.out

    def test_disable_sets_false(self, tmp_path: Path, capsys) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        with patch("garage_os.cli.sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = True
            with patch("builtins.input", return_value="y"):
                main(["init", "--path", str(ws)])
        capsys.readouterr()

        rc = main(["memory", "disable", "--path", str(ws)])
        assert rc == 0
        config = _read_platform_config(ws)
        assert config["memory"]["extraction_enabled"] is False
        captured = capsys.readouterr()
        assert "Memory extraction disabled" in captured.out


# T3.4 — memory status
class TestMemoryStatus:
    def test_status_shows_disabled_state(self, tmp_path: Path, capsys) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        main(["init", "--path", str(ws), "--no-memory"])
        capsys.readouterr()

        rc = main(["memory", "status", "--path", str(ws)])
        assert rc == 0
        captured = capsys.readouterr()
        assert "Memory extraction: disabled" in captured.out
        assert "garage memory enable" in captured.out
        assert "KnowledgeEntry: 0" in captured.out
        assert "ExperienceRecord: 0" in captured.out
        assert "Last extraction: never" in captured.out


# T3.5 — memory ingest --style-template
class TestMemoryIngestStyleTemplate:
    def test_ingest_python_template(self, tmp_path: Path, capsys) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        # Need real packs/garage/templates to exist; symlink or copy from repo
        repo_root = Path(__file__).resolve().parent.parent.parent
        (ws / "packs").mkdir()
        # Symlink garage pack directory
        import os
        os.symlink(repo_root / "packs" / "garage", ws / "packs" / "garage")
        main(["init", "--path", str(ws), "--no-memory"])
        capsys.readouterr()

        rc = main([
            "memory", "ingest", "--path", str(ws),
            "--style-template", "python",
        ])
        assert rc == 0
        captured = capsys.readouterr()
        assert "Ingested" in captured.out
        # Verify by checking knowledge/style/ has files
        style_dir = ws / ".garage" / "knowledge" / "style"
        assert style_dir.is_dir()
        assert len(list(style_dir.glob("*.md"))) >= 5

    def test_ingest_dry_run(self, tmp_path: Path, capsys) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        repo_root = Path(__file__).resolve().parent.parent.parent
        (ws / "packs").mkdir()
        import os
        os.symlink(repo_root / "packs" / "garage", ws / "packs" / "garage")
        main(["init", "--path", str(ws), "--no-memory"])
        capsys.readouterr()

        rc = main([
            "memory", "ingest", "--path", str(ws),
            "--style-template", "python", "--dry-run",
        ])
        assert rc == 0
        captured = capsys.readouterr()
        assert "Would ingest" in captured.out
        # Verify nothing was written
        style_dir = ws / ".garage" / "knowledge" / "style"
        # Either dir doesn't exist, or it's empty
        if style_dir.is_dir():
            assert list(style_dir.glob("*.md")) == []


# T3.6 — garage status integration (FR-1605 + Im-1 r2)
class TestStatusMemoryLine:
    def test_status_includes_memory_line_when_no_data(self, tmp_path: Path, capsys) -> None:
        """Im-1 r2: Memory extraction line crosses No data early-return."""
        ws = tmp_path / "ws"
        ws.mkdir()
        main(["init", "--path", str(ws), "--no-memory"])
        capsys.readouterr()

        rc = main(["status", "--path", str(ws)])
        assert rc == 0
        captured = capsys.readouterr()
        # Both lines present even with No data
        assert "Memory extraction: disabled" in captured.out
        assert "No data" in captured.out

    def test_status_shows_memory_enabled(self, tmp_path: Path, capsys) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        with patch("garage_os.cli.sys.stdin") as mock_stdin:
            mock_stdin.isatty.return_value = True
            with patch("builtins.input", return_value="y"):
                main(["init", "--path", str(ws)])
        capsys.readouterr()

        rc = main(["status", "--path", str(ws)])
        assert rc == 0
        captured = capsys.readouterr()
        assert "Memory extraction: enabled" in captured.out


# T3.7 — memory ingest invalid combos
class TestMemoryIngestInvalid:
    def test_no_source_flag_argparse_error(self, tmp_path: Path) -> None:
        ws = tmp_path / "ws"
        ws.mkdir()
        main(["init", "--path", str(ws), "--no-memory"])
        # argparse mutex: --from-reviews / --from-git-log / --style-template required
        with pytest.raises(SystemExit) as exc_info:
            main(["memory", "ingest", "--path", str(ws)])
        assert exc_info.value.code != 0
