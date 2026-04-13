from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RuntimeHomeError(Exception):
    code: str
    message: str


class RuntimeHome:
    """Runtime home/workspace topology authority for bootstrap."""

    def __init__(self, root: str) -> None:
        self.root = root.replace("\\", "/")
        self._allowed_profiles = {"dev", "standard", "full", "lightweight"}

    def bind_workspace(self, workspace_id: str, profile: str) -> dict[str, str]:
        if profile not in self._allowed_profiles:
            raise RuntimeHomeError("profile_denied", f"Profile '{profile}' is not allowed.")
        return {
            "runtime_home": self.root,
            "workspace_id": workspace_id,
            "workspace_path": f"{self.root}/workspaces/{workspace_id}",
            "profile": profile,
        }
