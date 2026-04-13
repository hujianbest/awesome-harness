from bootstrap.runtime_ops import RuntimeOps


def test_runtime_ops_records_diagnostic_event():
    ops = RuntimeOps()
    event = ops.record("session-started", {"session_id": "sess-1"})
    assert event["name"] == "session-started"
    assert event["trace_ref"].startswith("trace:")


def test_runtime_ops_filters_events_by_name():
    ops = RuntimeOps()
    ops.record("session-started", {"session_id": "sess-1"})
    ops.record("session-ended", {"session_id": "sess-1"})
    events = ops.list_events("session-started")
    assert len(events) == 1
