from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from bootstrap.session_api import SessionApi, SessionError


@dataclass
class HostBridgeError(Exception):
    code: str
    message: str


class HostBridge:
    def __init__(self, api: SessionApi) -> None:
        self._api = api
        self._bindings: dict[str, dict[str, object]] = {}

    def register_host(
        self, host_id: str, host_capabilities: dict[str, bool], bridge_version: str
    ) -> dict[str, object]:
        if not bridge_version:
            raise HostBridgeError("version_mismatch", "Bridge version is required.")
        token = f"hb-{uuid4().hex[:8]}"
        self._bindings[token] = {
            "host_id": host_id,
            "host_capabilities": host_capabilities,
            "bridge_version": bridge_version,
        }
        return {
            "host_binding_token": token,
            "allowed_capabilities": sorted(host_capabilities.keys()),
        }

    def inject_context(
        self, host_binding_token: str, session_id: str, context_payload: dict[str, object], scope: str
    ) -> dict[str, object]:
        self._require_binding(host_binding_token)
        if scope != "session":
            raise HostBridgeError("scope_violation", "Only session scope is supported.")
        self._assert_session_exists(session_id)
        return {"session_id": session_id, "context_ref": f"ctx:{session_id}", "applied_fields": sorted(context_payload.keys())}

    def request_action(
        self,
        host_binding_token: str,
        session_id: str,
        action_hint: dict[str, object],
        constraints: dict[str, object],
    ) -> dict[str, object]:
        self._require_binding(host_binding_token)
        self._assert_session_exists(session_id)
        if action_hint.get("kind") == "override_provider_authority":
            raise HostBridgeError("authority_violation", "Host cannot override provider authority.")
        return {
            "session_id": session_id,
            "action_result": "accepted",
            "trace_ref": f"trace:{session_id}:bridge",
            "constraints": constraints,
        }

    def _require_binding(self, token: str) -> None:
        if token not in self._bindings:
            raise HostBridgeError("binding_missing", "Host binding token does not exist.")

    def _assert_session_exists(self, session_id: str) -> None:
        try:
            self._api.get_status(session_id)
        except SessionError as exc:
            raise HostBridgeError(exc.code, exc.message) from exc
