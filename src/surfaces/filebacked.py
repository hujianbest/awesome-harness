from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SurfaceRoutingError(Exception):
    code: str
    message: str


class FilebackedSurface:
    def __init__(self, root: str) -> None:
        self.root = root.replace("\\", "/")
        self._kind_paths = {
            "facts": "facts",
            "evidence": "evidence",
            "sessions": "sessions",
            "archive": "archive",
        }

    def route_artifact(self, workspace_id: str, artifact_kind: str, file_name: str) -> str:
        suffix = self._kind_paths.get(artifact_kind)
        if suffix is None:
            raise SurfaceRoutingError(
                "unknown_artifact_kind", f"Unknown artifact kind: {artifact_kind}"
            )
        return f"{self.root}/workspaces/{workspace_id}/{suffix}/{file_name}"
