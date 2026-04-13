from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GovernanceError(Exception):
    code: str
    message: str


class GovernanceRuntime:
    def evaluate(self, action: str, payload: dict[str, object]) -> dict[str, str]:
        approved = bool(payload.get("approved"))
        session_id = str(payload.get("session_id", "unknown"))
        if not approved:
            raise GovernanceError(
                "governance_gate_failed", f"Action '{action}' is blocked by governance gate."
            )
        return {
            "decision": "pass",
            "action": action,
            "session_id": session_id,
            "evidence_ref": f"evidence:{session_id}:{action}",
        }
