from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass
class BridgeWorkflowError(Exception):
    code: str
    message: str


class BridgeWorkflow:
    def __init__(self) -> None:
        self._handoffs: dict[str, dict[str, str]] = {}

    def handoff(self, source_pack: str, target_pack: str, artifact_id: str) -> dict[str, str]:
        hid = f"handoff-{uuid4().hex[:8]}"
        record = {
            "id": hid,
            "source_pack": source_pack,
            "target_pack": target_pack,
            "artifact_id": artifact_id,
            "status": "accepted",
            "lineage_ref": f"lineage:{source_pack}->{target_pack}:{artifact_id}",
        }
        self._handoffs[hid] = record
        return dict(record)

    def rework(self, parent_handoff_id: str) -> dict[str, str]:
        parent = self._handoffs.get(parent_handoff_id)
        if parent is None:
            raise BridgeWorkflowError("parent_missing", "Rework parent handoff does not exist.")
        return {"status": "rework", "parent_handoff_id": parent_handoff_id}
