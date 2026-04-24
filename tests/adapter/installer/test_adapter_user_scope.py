"""F009 T1: Adapter user scope path 测试.

Covers:
- spec FR-904 (三家 first-class adapter user scope path 解析)
- design ADR-D9-6 (HostInstallAdapter Protocol 新增 _user 后缀 method)
- spec § 2.3 调研锚点 (Anthropic Claude Code / OpenCode XDG / Cursor 官方文档)

Fixture isolation (INV-F9-8):
- 用 monkeypatch ``Path.home()`` → tmp_path 隔离, 不污染真实 ~/
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from garage_os.adapter.installer.hosts.claude import ClaudeInstallAdapter
from garage_os.adapter.installer.hosts.cursor import CursorInstallAdapter
from garage_os.adapter.installer.hosts.opencode import OpenCodeInstallAdapter


@pytest.fixture
def fake_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Monkeypatch Path.home() 到 tmp_path/fake-home, 隔离真实 ~/ (INV-F9-8)."""
    fake = tmp_path / "fake-home"
    fake.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake))
    return fake


class TestClaudeUserScope:
    """FR-904 + § 2.3: Anthropic Claude Code 官方 user scope path."""

    def test_target_skill_path_user_returns_absolute(self, fake_home: Path) -> None:
        adapter = ClaudeInstallAdapter()
        result = adapter.target_skill_path_user("hf-specify")
        assert result == fake_home / ".claude" / "skills" / "hf-specify" / "SKILL.md"
        assert result.is_absolute()

    def test_target_agent_path_user_returns_absolute(self, fake_home: Path) -> None:
        adapter = ClaudeInstallAdapter()
        result = adapter.target_agent_path_user("garage-sample-agent")
        assert (
            result
            == fake_home / ".claude" / "agents" / "garage-sample-agent.md"
        )
        assert result.is_absolute()


class TestOpenCodeUserScope:
    """FR-904 + § 2.3: OpenCode XDG default user scope path (PR #6174)."""

    def test_target_skill_path_user_xdg_default(self, fake_home: Path) -> None:
        adapter = OpenCodeInstallAdapter()
        result = adapter.target_skill_path_user("hf-specify")
        # XDG default: ~/.config/opencode/skills/<id>/SKILL.md
        assert (
            result
            == fake_home
            / ".config"
            / "opencode"
            / "skills"
            / "hf-specify"
            / "SKILL.md"
        )
        assert result.is_absolute()

    def test_target_agent_path_user_xdg_default(self, fake_home: Path) -> None:
        adapter = OpenCodeInstallAdapter()
        result = adapter.target_agent_path_user("garage-sample-agent")
        # OpenCode 历史 agent 单数
        assert (
            result
            == fake_home
            / ".config"
            / "opencode"
            / "agent"
            / "garage-sample-agent.md"
        )
        assert result.is_absolute()


class TestCursorUserScope:
    """FR-904 + § 2.3: Cursor 官方 user scope path (无 agent surface)."""

    def test_target_skill_path_user_returns_absolute(self, fake_home: Path) -> None:
        adapter = CursorInstallAdapter()
        result = adapter.target_skill_path_user("hf-specify")
        assert result == fake_home / ".cursor" / "skills" / "hf-specify" / "SKILL.md"
        assert result.is_absolute()

    def test_target_agent_path_user_returns_none(self, fake_home: Path) -> None:
        # Cursor 无 agent surface (与 project scope 一致)
        adapter = CursorInstallAdapter()
        assert adapter.target_agent_path_user("garage-sample-agent") is None


class TestF007MethodsUnchanged:
    """spec § 4.3 + CON-901: F007 既有 method 签名严格不变 (zero break)."""

    def test_claude_target_skill_path_unchanged(self) -> None:
        adapter = ClaudeInstallAdapter()
        sig = inspect.signature(adapter.target_skill_path)
        # F007 既有签名: (self, skill_id: str) -> Path
        assert list(sig.parameters.keys()) == ["skill_id"]

    def test_claude_target_agent_path_unchanged(self) -> None:
        adapter = ClaudeInstallAdapter()
        sig = inspect.signature(adapter.target_agent_path)
        assert list(sig.parameters.keys()) == ["agent_id"]

    def test_claude_target_skill_path_returns_relative(self) -> None:
        # F007 既有行为: project scope 返回相对路径
        adapter = ClaudeInstallAdapter()
        result = adapter.target_skill_path("hf-specify")
        assert not result.is_absolute()
        assert result == Path(".claude/skills/hf-specify/SKILL.md")

    def test_opencode_target_skill_path_unchanged(self) -> None:
        adapter = OpenCodeInstallAdapter()
        result = adapter.target_skill_path("hf-specify")
        assert not result.is_absolute()
        assert result == Path(".opencode/skills/hf-specify/SKILL.md")

    def test_cursor_target_skill_path_unchanged(self) -> None:
        adapter = CursorInstallAdapter()
        result = adapter.target_skill_path("hf-specify")
        assert not result.is_absolute()
        assert result == Path(".cursor/skills/hf-specify/SKILL.md")

    def test_render_method_unchanged(self) -> None:
        # F007 既有 render 默认 identity passthrough
        for adapter_cls in (
            ClaudeInstallAdapter,
            OpenCodeInstallAdapter,
            CursorInstallAdapter,
        ):
            adapter = adapter_cls()
            content = "---\nname: test\n---\nbody"
            assert adapter.render(content) == content


class TestPathHomeUsed:
    """spec § 4.2 + NFR-903: 用 Path.home() stdlib 标准, 不写死分隔符."""

    def test_claude_user_scope_uses_path_home(self, fake_home: Path) -> None:
        adapter = ClaudeInstallAdapter()
        result = adapter.target_skill_path_user("hf-specify")
        # 验证 fake_home 是结果的祖先 (Path.home() 被正确使用)
        assert fake_home in result.parents

    def test_opencode_user_scope_uses_path_home(self, fake_home: Path) -> None:
        adapter = OpenCodeInstallAdapter()
        result = adapter.target_skill_path_user("hf-specify")
        assert fake_home in result.parents

    def test_cursor_user_scope_uses_path_home(self, fake_home: Path) -> None:
        adapter = CursorInstallAdapter()
        result = adapter.target_skill_path_user("hf-specify")
        assert fake_home in result.parents
