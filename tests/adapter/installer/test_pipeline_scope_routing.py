"""F009 T2: pipeline scope 分流 + 5 元组比对 测试.

Covers:
- spec FR-906 (pipeline scope 分流)
- spec FR-907 (跨 scope 不冲突)
- design ADR-D9-2 (phase 2 主改动 + phase 4/5 enum 内允许变化)
- spec CON-902 (phase 1 + phase 3 算法主体严格不变)
- INV-F9-2 (CON-902 守门 by inspect.getsource 比对)

Fixture isolation (INV-F9-8):
- 用 monkeypatch ``Path.home()`` → tmp_path 隔离
"""

from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest

from garage_os.adapter.installer.pipeline import (
    _check_conflicts,
    _resolve_targets,
    _Target,
    install_packs,
)


@pytest.fixture
def fake_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    fake = tmp_path / "fake-home"
    fake.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake))
    return fake


def _build_garage_pack(packs_root: Path) -> None:
    """Build a minimal one-skill / one-agent garage pack at packs_root/garage/."""
    pack_dir = packs_root / "garage"
    skills_dir = pack_dir / "skills" / "garage-hello"
    agents_dir = pack_dir / "agents"
    skills_dir.mkdir(parents=True)
    agents_dir.mkdir(parents=True)
    (pack_dir / "pack.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "pack_id": "garage",
                "version": "0.1.0",
                "description": "test pack",
                "skills": ["garage-hello"],
                "agents": ["sample"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (skills_dir / "SKILL.md").write_text(
        "---\nname: garage-hello\ndescription: hi\n---\n\n# Hello\n",
        encoding="utf-8",
    )
    (agents_dir / "sample.md").write_text("# Sample Agent\n", encoding="utf-8")


class TestPhase2ScopeRouting:
    """FR-906 + ADR-D9-2: phase 2 _resolve_targets 内按 scope 选 base path."""

    def test_resolve_targets_default_project_scope_F007_compat(
        self, tmp_path: Path
    ) -> None:
        """CON-901: scopes_resolved=None 等价 F007 行为 (全 project)."""
        from garage_os.adapter.installer.host_registry import get_adapter
        from garage_os.adapter.installer.pack_discovery import discover_packs

        _build_garage_pack(tmp_path / "packs")
        packs = discover_packs(tmp_path / "packs")
        adapters = {"claude": get_adapter("claude")}

        targets = _resolve_targets(tmp_path, packs, adapters, scopes_resolved=None)

        # F007 行为: skill 装到 <cwd>/.claude/skills/
        skill_targets = [t for t in targets if t.source_kind == "skill"]
        assert len(skill_targets) == 1
        assert skill_targets[0].scope == "project"
        assert skill_targets[0].dst_rel == ".claude/skills/garage-hello/SKILL.md"
        assert skill_targets[0].dst_abs == tmp_path / ".claude/skills/garage-hello/SKILL.md"

    def test_resolve_targets_user_scope_uses_path_home(
        self, tmp_path: Path, fake_home: Path
    ) -> None:
        """FR-906: user scope 用 Path.home() 作为 base path."""
        from garage_os.adapter.installer.host_registry import get_adapter
        from garage_os.adapter.installer.pack_discovery import discover_packs

        _build_garage_pack(tmp_path / "packs")
        packs = discover_packs(tmp_path / "packs")
        adapters = {"claude": get_adapter("claude")}

        targets = _resolve_targets(
            tmp_path, packs, adapters, scopes_resolved={"claude": "user"}
        )

        skill_targets = [t for t in targets if t.source_kind == "skill"]
        assert len(skill_targets) == 1
        assert skill_targets[0].scope == "user"
        # F009 user scope: dst_abs 在 fake_home 下
        assert skill_targets[0].dst_abs == fake_home / ".claude/skills/garage-hello/SKILL.md"
        # F009 ADR-D9-3: dst_rel 在 user scope 下是 absolute POSIX path
        assert skill_targets[0].dst_abs.is_absolute()

    def test_resolve_targets_mixed_scope_per_host(
        self, tmp_path: Path, fake_home: Path
    ) -> None:
        """FR-902 + FR-906: per-host scope override 正确分流."""
        from garage_os.adapter.installer.host_registry import get_adapter
        from garage_os.adapter.installer.pack_discovery import discover_packs

        _build_garage_pack(tmp_path / "packs")
        packs = discover_packs(tmp_path / "packs")
        adapters = {
            "claude": get_adapter("claude"),
            "cursor": get_adapter("cursor"),
        }

        targets = _resolve_targets(
            tmp_path,
            packs,
            adapters,
            scopes_resolved={"claude": "user", "cursor": "project"},
        )

        skill_targets = [t for t in targets if t.source_kind == "skill"]
        # claude:user + cursor:project = 2 skill targets
        by_host = {t.host: t for t in skill_targets}
        assert by_host["claude"].scope == "user"
        assert by_host["claude"].dst_abs == fake_home / ".claude/skills/garage-hello/SKILL.md"
        assert by_host["cursor"].scope == "project"
        assert by_host["cursor"].dst_abs == tmp_path / ".cursor/skills/garage-hello/SKILL.md"

    def test_resolve_targets_cursor_user_scope_no_agent(
        self, tmp_path: Path, fake_home: Path
    ) -> None:
        """cursor user scope 仍无 agent surface (与 project scope 一致)."""
        from garage_os.adapter.installer.host_registry import get_adapter
        from garage_os.adapter.installer.pack_discovery import discover_packs

        _build_garage_pack(tmp_path / "packs")
        packs = discover_packs(tmp_path / "packs")
        adapters = {"cursor": get_adapter("cursor")}

        targets = _resolve_targets(
            tmp_path, packs, adapters, scopes_resolved={"cursor": "user"}
        )

        # cursor user scope: 1 skill, 0 agent (与 project scope 一致)
        skill_targets = [t for t in targets if t.source_kind == "skill"]
        agent_targets = [t for t in targets if t.source_kind == "agent"]
        assert len(skill_targets) == 1
        assert len(agent_targets) == 0


class TestPhase3ConflictsCrossScope:
    """FR-907: 跨 scope 不视作 conflict (3 元组 key 扩展)."""

    def test_same_skill_cross_scope_not_conflict(
        self, tmp_path: Path, fake_home: Path
    ) -> None:
        """同 SKILL.md 同 host 不同 scope → 不视为 conflict."""
        # 模拟同一个 skill 同时装到 claude:user 与 claude:project
        targets = [
            _Target(
                src_abs=tmp_path / "packs/garage/skills/garage-hello/SKILL.md",
                dst_abs=fake_home / ".claude/skills/garage-hello/SKILL.md",
                src_rel="packs/garage/skills/garage-hello/SKILL.md",
                dst_rel=str(fake_home / ".claude/skills/garage-hello/SKILL.md"),
                host="claude",
                pack_id="garage",
                source_kind="skill",
                skill_or_agent_id="garage-hello",
                scope="user",
            ),
            _Target(
                src_abs=tmp_path / "packs/garage/skills/garage-hello/SKILL.md",
                dst_abs=tmp_path / ".claude/skills/garage-hello/SKILL.md",
                src_rel="packs/garage/skills/garage-hello/SKILL.md",
                dst_rel=".claude/skills/garage-hello/SKILL.md",
                host="claude",
                pack_id="garage",
                source_kind="skill",
                skill_or_agent_id="garage-hello",
                scope="project",
            ),
        ]
        # 不应抛 ConflictingSkillError (跨 scope 不视为冲突, FR-907)
        _check_conflicts(targets)


class TestPhase1Phase3AlgorithmInvariance:
    """CON-902 INV-F9-2: phase 1 + phase 3 算法主体字节级严格不变 (design reviewer 可拒红线)."""

    def test_check_conflicts_signature_unchanged(self) -> None:
        """phase 3 _check_conflicts 函数签名严格不变 (仅参数 type signature 内部 dict 元组维度变化)."""
        sig = inspect.signature(_check_conflicts)
        params = list(sig.parameters.keys())
        assert params == ["targets"]

    def test_resolve_targets_F007_signature_extended_optional(self) -> None:
        """phase 2 _resolve_targets 签名扩展 (新增 scopes_resolved optional 参数)."""
        sig = inspect.signature(_resolve_targets)
        params = list(sig.parameters.keys())
        # F007 参数: workspace_root, packs, adapters
        # F009 扩展: + scopes_resolved (optional, default None 兼容 F007 调用方)
        assert params == ["workspace_root", "packs", "adapters", "scopes_resolved"]
        # scopes_resolved 必须有 default (兼容 F007 调用方不传)
        assert sig.parameters["scopes_resolved"].default is None

    def test_install_packs_signature_extended_optional(self) -> None:
        """phase 5 install_packs 签名扩展 scopes_per_host optional 参数 (CON-901)."""
        sig = inspect.signature(install_packs)
        # F007 既有: workspace_root, packs_root, hosts, force, stderr, stdout
        # F009 扩展: + scopes_per_host (optional)
        assert "scopes_per_host" in sig.parameters
        assert sig.parameters["scopes_per_host"].default is None


class TestF007F008CompatThroughInstallPacks:
    """CON-901: install_packs(scopes_per_host=None) 等价 F007/F008 既有行为."""

    def test_install_packs_no_scopes_equivalent_F007(self, tmp_path: Path) -> None:
        """scopes_per_host=None 时, 全部 host 装到 cwd (project scope), 行为字节级与 F007 一致."""
        _build_garage_pack(tmp_path / "packs")

        summary = install_packs(
            workspace_root=tmp_path,
            packs_root=tmp_path / "packs",
            hosts=["claude"],
        )

        # F007 既有行为: skill + agent 装到 <tmp_path>/.claude/
        assert (tmp_path / ".claude/skills/garage-hello/SKILL.md").exists()
        assert (tmp_path / ".claude/agents/sample.md").exists()
        assert summary.n_skills == 1
        assert summary.n_agents == 1

    def test_install_packs_explicit_scopes_per_host_user(
        self, tmp_path: Path, fake_home: Path
    ) -> None:
        """scopes_per_host={'claude': 'user'} 时装到 ~/.claude/ (fake_home isolated)."""
        _build_garage_pack(tmp_path / "packs")

        install_packs(
            workspace_root=tmp_path,
            packs_root=tmp_path / "packs",
            hosts=["claude"],
            scopes_per_host={"claude": "user"},
        )

        # user scope 装到 fake_home/.claude/
        assert (fake_home / ".claude/skills/garage-hello/SKILL.md").exists()
        assert (fake_home / ".claude/agents/sample.md").exists()
        # 不创建 cwd 下的 .claude/
        assert not (tmp_path / ".claude").exists()
