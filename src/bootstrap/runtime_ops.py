from __future__ import annotations

from typing import Any


class RuntimeOps:
    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []

    def record(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        event = {
            "name": name,
            "payload": dict(payload),
            "trace_ref": f"trace:{payload.get('session_id', 'unknown')}:{name}",
        }
        self._events.append(event)
        return dict(event)

    def list_events(self, name: str | None = None) -> list[dict[str, Any]]:
        if name is None:
            return [dict(e) for e in self._events]
        return [dict(e) for e in self._events if e["name"] == name]
