from __future__ import annotations

from bootstrap.session_api import SessionApi


class WebControlPlane:
    """Minimal local-first Web entry adapter over shared SessionApi."""

    def __init__(self, api: SessionApi) -> None:
        self._api = api
        self._last_facts_snapshot: dict[str, object] | None = None

    def create_session(self, team_id: str, workspace_id: str, profile: str) -> dict[str, object]:
        session = self._api.create_session(team_id, workspace_id, profile)
        self._last_facts_snapshot = {
            "session_id": session["session_id"],
            "workspace_id": session["workspace_id"],
            "facts_state": "fresh",
            "stale": False,
        }
        return session

    def resume_session(self, session_id: str) -> dict[str, object]:
        return self._api.resume_session(session_id)

    def get_workspace_facts(
        self, session_id: str, force_unavailable: bool = False
    ) -> dict[str, object]:
        status = self._api.get_status(session_id)
        if force_unavailable:
            if self._last_facts_snapshot is None:
                return {
                    "session_id": session_id,
                    "workspace_id": status["workspace_id"],
                    "facts_state": "stale",
                    "stale": True,
                }
            stale_snapshot = dict(self._last_facts_snapshot)
            stale_snapshot["facts_state"] = "stale"
            stale_snapshot["stale"] = True
            return stale_snapshot

        self._last_facts_snapshot = {
            "session_id": session_id,
            "workspace_id": status["workspace_id"],
            "facts_state": "fresh",
            "stale": False,
        }
        return dict(self._last_facts_snapshot)

    def get_review_panel(self, session_id: str) -> dict[str, object]:
        status = self._api.get_status(session_id)
        return {
            "session_id": status["session_id"],
            "status": status["status"],
            "review_count": 0,
        }

    def optional_orchestration_enabled(self) -> bool:
        return False
