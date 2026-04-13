from bootstrap.session_api import SessionApi
from bootstrap.web import WebControlPlane


def test_web_create_and_resume_session():
    api = SessionApi()
    web = WebControlPlane(api)

    created = web.create_session(team_id="garage", workspace_id="default", profile="dev")
    resumed = web.resume_session(created["session_id"])

    assert resumed["session_id"] == created["session_id"]
    assert resumed["status"] == "active"


def test_web_returns_stale_facts_flag_when_facts_unavailable():
    api = SessionApi()
    web = WebControlPlane(api)
    created = web.create_session(team_id="garage", workspace_id="default", profile="dev")

    snapshot = web.get_workspace_facts(created["session_id"], force_unavailable=True)
    assert snapshot["facts_state"] == "stale"
    assert snapshot["stale"] is True
