"""Tool Registry — manages tool declarations in YAML format."""

from __future__ import annotations

import copy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


# Schema version for the registered-tools.yaml file
SCHEMA_VERSION = 1

# Path relative to project root where tool declarations live
DEFAULT_TOOLS_REL_PATH = ".garage/config/tools/registered-tools.yaml"


class ToolRegistry:
    """Register, discover, and list tool declarations.

    Tool declarations are persisted in a single YAML file whose schema is::

        schema_version: <int>
        tools:
          - name: <str>
            version: <str>
            description: <str>
            capabilities: <list[str]>
            config_schema: <dict | None>
            metadata: <dict>

    The YAML file is read from / written to *tools_path* (defaults to
    ``<project_root>/.garage/config/tools/registered-tools.yaml``).
    """

    def __init__(self, project_root: Path, tools_path: Optional[Path] = None) -> None:
        """Initialise the registry.

        Args:
            project_root: Absolute path to the Garage project root.
            tools_path:   Override path for the YAML declarations file.
                          If *None*, uses the default location under
                          ``project_root``.
        """
        self._project_root = project_root
        if tools_path is not None:
            self._tools_path = tools_path
        else:
            self._tools_path = project_root / DEFAULT_TOOLS_REL_PATH

        self._data: Optional[Dict[str, Any]] = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self) -> Dict[str, Any]:
        """Load YAML from disk (cached)."""
        if self._data is not None:
            return self._data

        if self._tools_path.exists():
            text = self._tools_path.read_text(encoding="utf-8")
            self._data = yaml.safe_load(text) or {}
        else:
            self._data = {"schema_version": SCHEMA_VERSION, "tools": []}

        # Ensure required keys
        self._data.setdefault("schema_version", SCHEMA_VERSION)
        self._data.setdefault("tools", [])
        return self._data

    def _flush(self) -> None:
        """Write current data to the YAML file."""
        self._tools_path.parent.mkdir(parents=True, exist_ok=True)
        text = yaml.dump(self._data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        self._tools_path.write_text(text, encoding="utf-8")

    def _find_tool_index(self, name: str) -> int:
        """Return the index of a tool by name, or -1."""
        data = self._load()
        for idx, tool in enumerate(data["tools"]):
            if tool.get("name") == name:
                return idx
        return -1

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register_tool(
        self,
        name: str,
        *,
        version: str = "1.0.0",
        description: str = "",
        capabilities: Optional[List[str]] = None,
        config_schema: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Register a tool declaration.

        If a tool with the same *name* already exists it will be **updated**
        (upsert semantics).

        Args:
            name:           Unique tool identifier.
            version:        Semantic version string.
            description:    Human-readable description.
            capabilities:   List of capability tags for discovery.
            config_schema:  Optional JSON-schema-style configuration spec.
            metadata:       Arbitrary key/value metadata.

        Returns:
            ``True`` on success.
        """
        data = self._load()

        entry: Dict[str, Any] = {
            "name": name,
            "version": version,
            "description": description,
            "capabilities": capabilities or [],
            "config_schema": config_schema,
            "metadata": metadata or {},
            "registered_at": datetime.now().isoformat(),
        }

        idx = self._find_tool_index(name)
        if idx >= 0:
            data["tools"][idx] = entry
        else:
            data["tools"].append(entry)

        self._flush()
        # Invalidate cache so next read hits disk (important for tests
        # that inspect the file directly).
        self._data = None
        return True

    def unregister_tool(self, name: str) -> bool:
        """Remove a tool declaration.

        Args:
            name: Tool identifier to remove.

        Returns:
            ``True`` if the tool existed and was removed, ``False`` otherwise.
        """
        data = self._load()
        idx = self._find_tool_index(name)
        if idx < 0:
            return False
        data["tools"].pop(idx)
        self._flush()
        self._data = None
        return True

    def discover_tools(self, capability: str) -> List[Dict[str, Any]]:
        """Find tools that declare a given capability.

        Args:
            capability: Capability tag to search for.

        Returns:
            List of matching tool declarations (deep copies).
        """
        data = self._load()
        results: List[Dict[str, Any]] = []
        for tool in data["tools"]:
            if capability in tool.get("capabilities", []):
                results.append(copy.deepcopy(tool))
        return results

    def list_all(self) -> List[Dict[str, Any]]:
        """Return a deep copy of every registered tool declaration."""
        data = self._load()
        return copy.deepcopy(data["tools"])

    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Return info for a single tool, or ``None`` if not found."""
        data = self._load()
        for tool in data["tools"]:
            if tool.get("name") == name:
                return copy.deepcopy(tool)
        return None
