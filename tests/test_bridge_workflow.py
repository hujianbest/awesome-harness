from bridge.workflow import BridgeWorkflow, BridgeWorkflowError


def test_bridge_workflow_accepts_handoff_and_keeps_lineage():
    wf = BridgeWorkflow()
    result = wf.handoff("pack-a", "pack-b", "artifact-1")
    assert result["status"] == "accepted"
    assert result["lineage_ref"].startswith("lineage:")


def test_bridge_workflow_rejects_rework_without_parent():
    wf = BridgeWorkflow()
    try:
        wf.rework("missing-parent")
    except BridgeWorkflowError as exc:
        assert exc.code == "parent_missing"
    else:
        raise AssertionError("expected parent_missing")
