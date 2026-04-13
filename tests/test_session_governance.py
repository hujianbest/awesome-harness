from governance.runtime import GovernanceRuntime, GovernanceError


def test_governance_runtime_allows_approved_action_and_emits_evidence():
    runtime = GovernanceRuntime()
    result = runtime.evaluate("submit_step", {"approved": True, "session_id": "sess-1"})
    assert result["decision"] == "pass"
    assert result["evidence_ref"].startswith("evidence:")


def test_governance_runtime_rejects_unapproved_action():
    runtime = GovernanceRuntime()
    try:
        runtime.evaluate("submit_step", {"approved": False, "session_id": "sess-1"})
    except GovernanceError as exc:
        assert exc.code == "governance_gate_failed"
    else:
        raise AssertionError("expected governance_gate_failed")
