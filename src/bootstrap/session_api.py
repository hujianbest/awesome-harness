from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class SessionError(Exception):
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"error": self.code, "message": self.message}


@dataclass
class Session:
    session_id: str
    team_id: str
    workspace_id: str
    profile: str
    status: str = "active"
    host_binding: str = "cli"
    steps: list[dict[str, Any]] = field(default_factory=list)

    def snapshot(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "team_id": self.team_id,
            "workspace_id": self.workspace_id,
            "profile": self.profile,
            "status": self.status,
            "host_binding": self.host_binding,
            "step_count": len(self.steps),
        }


class SessionApi:
    """Minimal shared SessionApi used by CLI entry."""

    def __init__(self) -> None:
        self._workspaces: set[str] = {"default"}
        self._sessions: dict[str, Session] = {}

    def create_session(self, team_id: str, workspace_id: str, profile: str) -> dict[str, Any]:
        self._assert_workspace(workspace_id)
        session_id = f"sess-{uuid4().hex[:8]}"
        session = Session(
            session_id=session_id,
            team_id=team_id,
            workspace_id=workspace_id,
            profile=profile,
        )
        self._sessions[session_id] = session
        return session.snapshot()

    def resume_session(self, session_id: str) -> dict[str, Any]:
        return self._get_session(session_id).snapshot()

    def attach_workspace(self, session_id: str, workspace_id: str) -> dict[str, Any]:
        self._assert_workspace(workspace_id)
        session = self._get_session(session_id)
        session.workspace_id = workspace_id
        return {
            "session_id": session.session_id,
            "workspace_binding": workspace_id,
            "status": session.status,
        }

    def submit_step(self, session_id: str, step_payload: str) -> dict[str, Any]:
        session = self._get_session(session_id)
        session.steps.append({"input": step_payload})
        return {
            "session_id": session.session_id,
            "status": session.status,
            "step_result": "accepted",
            "trace_ref": f"trace:{session.session_id}:{len(session.steps)}",
            "evidence_ref": f"evidence:{session.session_id}:{len(session.steps)}",
        }

    def get_status(self, session_id: str) -> dict[str, Any]:
        return self._get_session(session_id).snapshot()

    def _get_session(self, session_id: str) -> Session:
        session = self._sessions.get(session_id)
        if session is None:
            raise SessionError("session_missing", f"Session '{session_id}' does not exist.")
        return session

    def _assert_workspace(self, workspace_id: str) -> None:
        if workspace_id not in self._workspaces:
            raise SessionError(
                "workspace_not_found", f"Workspace '{workspace_id}' is not available."
            )
