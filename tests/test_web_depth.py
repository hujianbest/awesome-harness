from bootstrap.session_api import SessionApi
from bootstrap.web import WebControlPlane


def test_web_depth_exposes_review_panel_summary():
    api = SessionApi()
    web = WebControlPlane(api)
    created = web.create_session("garage", "default", "dev")
    panel = web.get_review_panel(created["session_id"])
    assert panel["session_id"] == created["session_id"]
    assert panel["review_count"] == 0


def test_web_depth_optional_orchestration_guardrail_disabled_by_default():
    api = SessionApi()
    web = WebControlPlane(api)
    decision = web.optional_orchestration_enabled()
    assert decision is False
