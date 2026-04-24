"""F009 T1: host_id 命名约束 (不允许字面 ':' 字符) 守门测试.

Covers design ADR-D9-9 双层守门:
1. 运行时静态 assert (host_registry._build_registry import-time)
2. Protocol docstring 显式声明
3. 本测试守门 (this file)
"""

from __future__ import annotations

from garage_os.adapter.installer.host_registry import (
    HOST_REGISTRY,
    _build_registry,
)


class TestHostIdColonAssert:
    """ADR-D9-9: host_id 不允许字面 ':' (用作 --hosts <host>:<scope> 分隔符)."""

    def test_no_host_id_contains_colon_in_current_registry(self) -> None:
        """当前 first-class 三家 (claude/opencode/cursor) 天然符合."""
        for host_id in HOST_REGISTRY:
            assert ":" not in host_id, (
                f"ADR-D9-9 violation: host_id {host_id!r} contains ':' "
                "(used as --hosts <host>:<scope> override delimiter)"
            )

    def test_build_registry_returns_three_first_class_hosts(self) -> None:
        """同时验证 _build_registry 返回正确的注册表 (与 F007 行为一致)."""
        registry = _build_registry()
        assert set(registry.keys()) == {"claude", "opencode", "cursor"}

    def test_protocol_docstring_documents_constraint(self) -> None:
        """ADR-D9-9 双层守门: Protocol docstring 显式声明 host_id 不含 ':' 约束."""
        from garage_os.adapter.installer.host_registry import HostInstallAdapter

        # docstring 应含 ':' 字符约束 + ADR-D9-9 anchor + scope override 关键词
        doc = HostInstallAdapter.__doc__ or ""
        assert "ADR-D9-9" in doc, (
            "HostInstallAdapter docstring 未声明 ADR-D9-9 anchor (host_id ':' 约束)"
        )
        assert "scope override" in doc.lower() or "scope-override" in doc.lower(), (
            "HostInstallAdapter docstring 未声明 ':' 是 scope override 分隔符"
        )
