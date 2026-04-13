from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass
class SessionStateError(Exception):
    code: str
    message: str


class SessionRuntime:
    def __init__(self) -> None:
        self._states: dict[str, str] = {}

    def create(self, workspace_id: str) -> str:
        sid = f"sess-{uuid4().hex[:8]}"
        self._states[sid] = "active"
        return sid

    def transition(self, session_id: str, action: str) -> str:
        state = self._states.get(session_id)
        if state is None:
            raise SessionStateError("session_missing", f"Session '{session_id}' does not exist.")

        if action == "interrupt" and state == "active":
            self._states[session_id] = "interrupted"
            return "interrupted"
        if action == "resume" and state == "interrupted":
            self._states[session_id] = "active"
            return "active"

        raise SessionStateError(
            "invalid_transition", f"Cannot apply action '{action}' from state '{state}'."
        )

    def get_state(self, session_id: str) -> str:
        state = self._states.get(session_id)
        if state is None:
            raise SessionStateError("session_missing", f"Session '{session_id}' does not exist.")
        return state
