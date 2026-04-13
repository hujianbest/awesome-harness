from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass
class GrowthError(Exception):
    code: str
    message: str


class GrowthEngine:
    def __init__(self) -> None:
        self._proposals: dict[str, dict[str, str]] = {}

    def create_proposal(self, evidence_ref: str, summary: str) -> str:
        pid = f"gp-{uuid4().hex[:8]}"
        self._proposals[pid] = {"evidence_ref": evidence_ref, "summary": summary, "status": "pending"}
        return pid

    def decide(self, proposal_id: str, decision: str) -> dict[str, str]:
        proposal = self._proposals.get(proposal_id)
        if proposal is None:
            raise GrowthError("proposal_missing", f"Proposal '{proposal_id}' does not exist.")

        if decision == "accepted":
            proposal["status"] = "promoted"
            return {"proposal_id": proposal_id, "status": "promoted"}
        if decision == "rejected":
            proposal["status"] = "rejected"
            return {"proposal_id": proposal_id, "status": "rejected"}
        if decision == "deferred":
            proposal["status"] = "deferred"
            return {"proposal_id": proposal_id, "status": "deferred"}

        raise GrowthError("invalid_decision", f"Unsupported decision: {decision}")
