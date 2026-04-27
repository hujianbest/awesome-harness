"""F016 T4 sentinel: CON-1601 — F016 不修改 F003-F015 既有 pipeline 模块.

INV-F16-1 守门: F016 仅添加 src/garage_os/memory_activation/ 顶级包 + cli.py 加 subparser/handler/init prompt + _status 集成. 不动 F003 memory/ / F004 knowledge/{experience_index,knowledge_store}.py / F010 ingest/ / F011 KnowledgeType enum / F013-A skill_mining/ / F014 workflow_recall/ / F015 agent_compose/ 任何文件.

This sentinel detects accidental drift via AST-level static analysis: cli.py imports `memory_activation` only via deferred imports (function-local), so the public API of memory_activation (types + ingest functions) should not leak into other src modules.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _module_imports(file_path: Path) -> set[str]:
    """Return the set of imported module names parsed statically (no runtime imports)."""
    try:
        src = file_path.read_text(encoding="utf-8")
    except OSError:
        return set()
    try:
        tree = ast.parse(src, filename=str(file_path))
    except SyntaxError:
        return set()
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                out.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                out.add(node.module)
    return out


def test_existing_pipeline_modules_do_not_import_memory_activation() -> None:
    """F003-F015 既有 pipeline 模块 MUST NOT import memory_activation.

    F016 是 sibling layer; 不能反向耦合.
    """
    src_root = REPO_ROOT / "src" / "garage_os"
    forbidden = "memory_activation"
    # Modules that should NOT import memory_activation
    target_dirs = [
        "memory",
        "knowledge",
        "ingest",
        "skill_mining",
        "workflow_recall",
        "agent_compose",
        "runtime",
        "storage",
        "adapter",
        "sync",
        "tools",
        "platform",
        "types",
    ]
    for dir_name in target_dirs:
        target_dir = src_root / dir_name
        if not target_dir.is_dir():
            continue
        for py_file in target_dir.rglob("*.py"):
            imports = _module_imports(py_file)
            for imp in imports:
                assert forbidden not in imp, (
                    f"INV-F16-1 violated: {py_file.relative_to(REPO_ROOT)} "
                    f"imports '{imp}' which contains '{forbidden}'. "
                    "memory_activation is sibling layer; F003-F015 modules must remain "
                    "independent of F016 to maintain CON-1601."
                )


def test_memory_activation_module_exists() -> None:
    """F016 module structure sentinel: required files exist."""
    pkg_dir = REPO_ROOT / "src" / "garage_os" / "memory_activation"
    assert pkg_dir.is_dir(), "F016: src/garage_os/memory_activation/ missing"
    for module in ("__init__.py", "types.py", "templates.py", "ingest.py"):
        assert (pkg_dir / module).is_file(), f"F016: memory_activation/{module} missing"


def test_style_templates_packaged() -> None:
    """F016 packed STYLE template files exist + parseable (3 lang)."""
    templates_dir = REPO_ROOT / "packs" / "garage" / "templates" / "style-templates"
    assert templates_dir.is_dir(), "F016: packs/garage/templates/style-templates/ missing"
    for lang in ("python", "typescript", "markdown"):
        path = templates_dir / f"{lang}.md"
        assert path.is_file(), f"F016: {lang}.md template missing"
        # Sanity: file has at least one `- prefix:` line
        text = path.read_text(encoding="utf-8")
        assert "- " in text and ":" in text, f"F016: {lang}.md has no parseable entries"
