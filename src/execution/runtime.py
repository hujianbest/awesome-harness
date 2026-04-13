from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExecutionError(Exception):
    code: str
    message: str


class ExecutionRuntime:
    def execute(self, session_id: str, action: dict[str, str], authority: str) -> dict[str, str]:
        if authority != "runtime":
            raise ExecutionError("authority_violation", "Only runtime authority may execute actions.")
        tool = action.get("tool", "unknown")
        return {
            "session_id": session_id,
            "status": "accepted",
            "tool": tool,
            "trace_ref": f"trace:{session_id}:{tool}",
            "evidence_ref": f"evidence:{session_id}:{tool}",
        }
