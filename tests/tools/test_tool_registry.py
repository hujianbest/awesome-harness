"""Tests for tool_registry module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from garage_os.tools.tool_registry import ToolRegistry


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a temporary project root with the expected .garage structure."""
    tools_dir = tmp_path / ".garage" / "config" / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture
def registry(tmp_project: Path) -> ToolRegistry:
    """Return a ToolRegistry backed by the temp project."""
    return ToolRegistry(project_root=tmp_project)


class TestToolRegistryRegister:
    """Register tool declarations and verify YAML contents."""

    def test_register_writes_yaml(self, registry: ToolRegistry, tmp_project: Path) -> None:
        """Registration should produce a valid YAML file with the declaration."""
        ok = registry.register_tool(
            "search_web",
            version="1.0.0",
            description="Search the web",
            capabilities=["search", "web"],
        )
        assert ok is True

        # Read YAML from disk directly
        yaml_path = tmp_project / ".garage" / "config" / "tools" / "registered-tools.yaml"
        assert yaml_path.exists()
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

        assert data["schema_version"] == 1
        assert len(data["tools"]) == 1
        tool = data["tools"][0]
        assert tool["name"] == "search_web"
        assert tool["version"] == "1.0.0"
        assert "search" in tool["capabilities"]

    def test_register_upsert(self, registry: ToolRegistry) -> None:
        """Registering the same tool twice should update, not duplicate."""
        registry.register_tool("my_tool", description="first")
        registry.register_tool("my_tool", description="second")

        all_tools = registry.list_all()
        assert len(all_tools) == 1
        assert all_tools[0]["description"] == "second"

    def test_register_multiple_tools(self, registry: ToolRegistry) -> None:
        """Multiple different tools can be registered."""
        registry.register_tool("tool_a", capabilities=["alpha"])
        registry.register_tool("tool_b", capabilities=["beta"])

        all_tools = registry.list_all()
        assert len(all_tools) == 2
        names = {t["name"] for t in all_tools}
        assert names == {"tool_a", "tool_b"}


class TestToolRegistryDiscover:
    """Discover tools by capability."""

    def test_discover_by_capability(self, registry: ToolRegistry) -> None:
        """discover_tools should return only tools with matching capability."""
        registry.register_tool("web_search", capabilities=["search", "web"])
        registry.register_tool("file_read", capabilities=["io", "file"])
        registry.register_tool("code_search", capabilities=["search", "code"])

        results = registry.discover_tools("search")
        names = {t["name"] for t in results}
        assert names == {"web_search", "code_search"}

    def test_discover_no_match(self, registry: ToolRegistry) -> None:
        """discover_tools returns empty list when nothing matches."""
        registry.register_tool("solo", capabilities=["lonely"])
        assert registry.discover_tools("nonexistent") == []

    def test_discover_returns_deep_copies(self, registry: ToolRegistry) -> None:
        """Mutating discover results must not affect stored data."""
        registry.register_tool("tool_x", capabilities=["cap_a"])
        results = registry.discover_tools("cap_a")
        results[0]["name"] = "mutated"
        assert registry.get_tool_info("tool_x") is not None


class TestToolRegistryListAll:
    """List all registered tools."""

    def test_list_all_empty(self, registry: ToolRegistry) -> None:
        """list_all on empty registry returns []."""
        assert registry.list_all() == []

    def test_list_all_returns_copies(self, registry: ToolRegistry) -> None:
        """list_all returns deep copies, not references."""
        registry.register_tool("t1", capabilities=["c1"])
        tools = registry.list_all()
        tools[0]["name"] = "hacked"
        assert registry.list_all()[0]["name"] == "t1"


class TestToolRegistryUnregister:
    """Unregister tool declarations."""

    def test_unregister_existing(self, registry: ToolRegistry) -> None:
        """Unregister an existing tool returns True."""
        registry.register_tool("temp_tool")
        assert registry.unregister_tool("temp_tool") is True
        assert registry.list_all() == []

    def test_unregister_nonexistent(self, registry: ToolRegistry) -> None:
        """Unregistering a tool that doesn't exist returns False."""
        assert registry.unregister_tool("ghost") is False


class TestToolRegistryGetToolInfo:
    """Get detailed info for a single tool."""

    def test_get_tool_info_found(self, registry: ToolRegistry) -> None:
        registry.register_tool("info_tool", description="details", version="2.0.0")
        info = registry.get_tool_info("info_tool")
        assert info is not None
        assert info["description"] == "details"
        assert info["version"] == "2.0.0"

    def test_get_tool_info_not_found(self, registry: ToolRegistry) -> None:
        assert registry.get_tool_info("nobody") is None


class TestConfigSchemaValidation:
    """Verify config_schema is persisted correctly."""

    def test_config_schema_stored(self, registry: ToolRegistry, tmp_project: Path) -> None:
        schema = {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        }
        registry.register_tool("schema_tool", config_schema=schema)

        info = registry.get_tool_info("schema_tool")
        assert info is not None
        assert info["config_schema"]["type"] == "object"
        assert "query" in info["config_schema"]["properties"]
