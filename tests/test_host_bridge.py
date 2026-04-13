from bootstrap.host_bridge import HostBridge, HostBridgeError
from bootstrap.session_api import SessionApi


def test_register_and_inject_context_success():
    api = SessionApi()
    session = api.create_session("garage", "default", "dev")
    bridge = HostBridge(api)

    token = bridge.register_host("cursor", {"context": True}, "v1")["host_binding_token"]
    result = bridge.inject_context(token, session["session_id"], {"branch": "main"}, scope="session")

    assert result["session_id"] == session["session_id"]
    assert result["applied_fields"] == ["branch"]


def test_request_action_rejects_authority_override():
    api = SessionApi()
    session = api.create_session("garage", "default", "dev")
    bridge = HostBridge(api)
    token = bridge.register_host("cursor", {"actions": True}, "v1")["host_binding_token"]

    try:
        bridge.request_action(
            token,
            session["session_id"],
            {"kind": "override_provider_authority"},
            {"safe": True},
        )
    except HostBridgeError as exc:
        assert exc.code == "authority_violation"
    else:
        raise AssertionError("expected authority_violation")
